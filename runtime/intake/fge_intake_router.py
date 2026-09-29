#!/usr/bin/env python3
"""FGE GitHub Intake Router.

Fail-closed candidate router for files committed under intake/inbox/.
Preserves source identity, never overwrites destinations, emits receipts,
and never promotes canon or authority.

Default mode is DRY_RUN. Use --apply to move eligible files and append indexes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import re
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Tuple

ROUTER_OBJECT_ID = "FGE-GITHUB-INTAKE-ROUTER-001"
ROUTER_VERSION = "0.1.1"
MEDIA_CLASSES = {"IMAGE", "VIDEO"}
MEDIA_ORIGINS = {"RAW_SOURCE", "EDITED_DERIVATIVE", "GENERATED_OUTPUT", "COMPOSITE"}


@dataclass
class Decision:
    drop_id: str
    source_path: str
    sha256: str
    mime_type: str
    physical_class: str
    object_class: str
    confidence: float
    route_state: str
    destination: Optional[str]
    hold_reason: Optional[str]
    decision_basis: list[str]
    sidecar_path: Optional[str]
    decision_fingerprint: str
    attention_required: bool
    canon_effect: str = "NONE"
    authority_effect: str = "NONE"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def parse_simple_yaml(path: Path) -> Dict[str, Any]:
    """Parse simple top-level YAML sidecars without external dependencies.

    Complex YAML is deliberately rejected. .fge.json is canonical.
    """
    out: Dict[str, Any] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith(("-", "{", "[")) or ": " not in line:
            raise ValueError("Complex YAML unsupported; use .fge.json")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if value.lower() in {"true", "false"}:
            parsed: Any = value.lower() == "true"
        elif value.lower() in {"null", "none"}:
            parsed = None
        else:
            parsed = value
        out[key] = parsed
    return out


def find_sidecar(path: Path) -> Tuple[Optional[Path], Dict[str, Any]]:
    candidates = [
        path.with_name(path.name + ".fge.json"),
        path.with_name(path.stem + ".fge.json"),
        path.with_name(path.name + ".fge.yaml"),
        path.with_name(path.stem + ".fge.yaml"),
        path.with_name(path.name + ".fge.yml"),
        path.with_name(path.stem + ".fge.yml"),
    ]
    for candidate in candidates:
        if candidate.exists():
            if candidate.name.lower().endswith(".fge.json"):
                return candidate, load_json(candidate)
            return candidate, parse_simple_yaml(candidate)
    return None, {}


def is_sidecar(path: Path) -> bool:
    name = path.name.lower()
    return name.endswith(".fge.json") or name.endswith(".fge.yaml") or name.endswith(".fge.yml")


def read_text_prefix(path: Path, limit: int = 65536) -> str:
    try:
        return path.read_bytes()[:limit].decode("utf-8")
    except (UnicodeDecodeError, OSError):
        return ""


def embedded_fge_class(text: str) -> Optional[str]:
    if not text:
        return None
    class_match = re.search(r"(?im)^\s*(?:CLASS|OBJECT_CLASS)\s*:\s*([^\n]+)", text)
    object_match = re.search(r"(?im)^\s*OBJECT_ID\s*:\s*([^\n]+)", text)
    haystack = " ".join(m.group(1) for m in (class_match, object_match) if m).upper()
    if "INFOGRAPHIC" in haystack:
        return "INFOGRAPHIC_MANIFEST"
    if "PAYLOAD" in haystack:
        return "PAYLOAD"
    if "RECEIPT" in haystack or "RCPT" in haystack:
        return "RECEIPT"
    if "SPEC" in haystack or "ENGINEERING" in haystack:
        return "SPEC"
    return None


def schema_class(path: Path) -> Optional[str]:
    if path.suffix.lower() != ".json":
        return None
    try:
        payload = load_json(path)
    except (json.JSONDecodeError, UnicodeDecodeError, OSError):
        return None
    if not isinstance(payload, dict):
        return "STRUCTURED_DATA"
    if "payload_id" in payload or "payload_type" in payload:
        return "PAYLOAD"
    if "receipt_id" in payload:
        return "RECEIPT"
    combined = f"{payload.get('object_id', '')} {payload.get('class', '')} {payload.get('object_class', '')}".upper()
    if "INFOGRAPHIC" in combined:
        return "INFOGRAPHIC_MANIFEST"
    return "STRUCTURED_DATA"


def normalize_declared_class(value: Any) -> Optional[str]:
    if not value:
        return None
    v = str(value).upper().strip()
    aliases = {
        "INFOGRAPHIC": "INFOGRAPHIC_MANIFEST",
        "INFOGRAPHIC_SYSTEM": "INFOGRAPHIC_MANIFEST",
        "CHARACTER_INFOGRAPHIC": "INFOGRAPHIC_MANIFEST",
        "JSON": "STRUCTURED_DATA",
        "YAML": "STRUCTURED_DATA",
        "MARKDOWN": "SPEC",
        "ENGINEERING_SPEC": "SPEC",
        "RAW_IMAGE": "IMAGE",
        "EDITED_IMAGE": "IMAGE",
        "GENERATED_IMAGE": "IMAGE",
        "ARTIFACT_RENDER": "IMAGE",
    }
    return aliases.get(v, v)


def extension_class(path: Path, config: Dict[str, Any]) -> Optional[str]:
    ext = path.suffix.lower()
    for cls, extensions in config.get("extensions", {}).items():
        if ext in {str(x).lower() for x in extensions}:
            return cls
    return None


def classify(path: Path, config: Dict[str, Any], sidecar: Dict[str, Any]) -> Tuple[str, float, list[str]]:
    declared = normalize_declared_class(sidecar.get("route_class") or sidecar.get("object_class"))
    if declared:
        return declared, 1.0, ["SIDECAR_DECLARATION"]

    embedded = embedded_fge_class(read_text_prefix(path))
    if embedded:
        return embedded, 0.98, ["EMBEDDED_FGE_HEADER"]

    schema = schema_class(path)
    if schema:
        score = 0.96 if schema in {"PAYLOAD", "RECEIPT", "INFOGRAPHIC_MANIFEST"} else 0.90
        return schema, score, ["SCHEMA_MATCH"]

    ext_class = extension_class(path, config)
    if ext_class:
        score = 0.95 if ext_class == "CODE" else 0.85
        return ext_class, score, ["MIME_EXTENSION"]

    return "UNKNOWN", 0.0, ["NO_SUPPORTED_CLASSIFICATION"]


def public_repo_guard(physical_class: str, sidecar: Dict[str, Any], config: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    guard = config.get("public_repo_guard", {})
    if not guard.get("enabled", True):
        return True, None

    binary_classes = {str(x).upper() for x in guard.get("binary_classes", [])}
    if physical_class not in binary_classes:
        return True, None

    if guard.get("binary_requires_sidecar", True) and not sidecar:
        return False, "BINARY_PUBLICATION_UNVERIFIED"
    if guard.get("binary_requires_public_ok", True) and sidecar.get("public_ok") is not True:
        return False, "BINARY_PUBLICATION_UNVERIFIED"

    if physical_class in MEDIA_CLASSES:
        sensitivity = str(sidecar.get("sensitivity", "UNKNOWN")).upper()
        blocked = {str(x).upper() for x in guard.get("blocked_sensitivity_values", [])}
        if sensitivity in blocked:
            return False, "SENSITIVE_OR_PRIVATE_MEDIA"
        required_sensitivity = str(guard.get("media_requires_sensitivity", "STANDARD")).upper()
        if sensitivity != required_sensitivity:
            return False, "BINARY_PUBLICATION_UNVERIFIED"
        origin = str(sidecar.get("origin_class", "")).upper()
        if guard.get("media_requires_origin_class", True) and origin not in MEDIA_ORIGINS:
            return False, "BINARY_PUBLICATION_UNVERIFIED"
    return True, None


def governance_guard(sidecar: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    entity_state = str(sidecar.get("entity_state", "")).upper()
    if sidecar.get("collision_hold") is True or entity_state in {"AMBIGUOUS", "COLLISION_HOLD"}:
        return False, "COLLISION_HOLD" if sidecar.get("collision_hold") else "ENTITY_AMBIGUOUS"

    sensitivity = str(sidecar.get("sensitivity", "")).upper()
    age_state = str(sidecar.get("age_state", "")).upper()
    if sensitivity in {"NUDITY_NONSEXUAL", "NUDITY_SEXUALIZED", "EXPLICIT_SEXUAL", "INTIMATE_PRIVATE"} and age_state not in {"VERIFIED_ADULT", "NOT_APPLICABLE"}:
        return False, "AGE_OR_CONSENT_UNCERTAIN"

    primary = sidecar.get("primary_character_id")
    pointer = sidecar.get("enterprise_asset_pointer")
    if primary and pointer and str(primary) == str(pointer):
        return False, "POINTER_IDENTITY_SUBSTITUTION"
    return True, None


def load_seen_fingerprints(index_path: Path) -> set[str]:
    seen: set[str] = set()
    if not index_path.exists():
        return seen
    for line in index_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        fp = row.get("decision_fingerprint")
        if fp:
            seen.add(str(fp))
    return seen


def decision_fingerprint(file_sha: str, sidecar: Dict[str, Any]) -> str:
    canonical = json.dumps(sidecar, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(f"{file_sha}|{canonical}".encode("utf-8")).hexdigest()


def choose_destination(path: Path, object_class: str, config: Dict[str, Any], sidecar: Dict[str, Any]) -> Optional[str]:
    route_class = "PUBLIC_MEDIA" if object_class in MEDIA_CLASSES else object_class
    base = config.get("destinations", {}).get(route_class)
    if not base:
        return None
    domain = str(sidecar.get("domain", "unclassified")).strip().lower().replace(" ", "_") or "unclassified"
    safe_domain = re.sub(r"[^a-z0-9_.-]+", "_", domain)
    return str(Path(base) / safe_domain / path.name)


def plan_decision(path: Path, root: Path, config: Dict[str, Any]) -> Decision:
    file_sha = sha256_file(path)
    mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    sidecar_path, sidecar = find_sidecar(path)
    physical_class = extension_class(path, config) or "UNKNOWN"
    object_class, confidence, basis = classify(path, config, sidecar)
    basis = list(basis) + [f"PHYSICAL_CLASS:{physical_class}"]
    fp = decision_fingerprint(file_sha, sidecar)
    drop_id = f"FGE-DROP-{file_sha[:16].upper()}"

    ok, reason = governance_guard(sidecar)
    if ok:
        ok, reason = public_repo_guard(physical_class, sidecar, config)

    thresholds = config.get("thresholds", {})
    auto_route = float(thresholds.get("auto_route", 0.90))
    review_route = float(thresholds.get("route_and_review", 0.70))
    destination: Optional[str] = None
    attention = False

    if not ok:
        state = "HOLD"
        attention = True
    elif object_class == "UNKNOWN" or confidence < review_route:
        state = "HOLD"
        reason = reason or "UNKNOWN_ROUTE"
        attention = True
    else:
        destination = choose_destination(path, object_class, config, sidecar)
        if not destination:
            state = "HOLD"
            reason = "UNKNOWN_ROUTE"
            attention = True
        elif confidence >= auto_route:
            state = "ROUTE"
        else:
            state = "ROUTE_AND_REVIEW"
            attention = True

    return Decision(
        drop_id=drop_id,
        source_path=str(path.relative_to(root)),
        sha256=file_sha,
        mime_type=mime_type,
        physical_class=physical_class,
        object_class=object_class,
        confidence=round(confidence, 3),
        route_state=state,
        destination=destination,
        hold_reason=reason,
        decision_basis=basis,
        sidecar_path=str(sidecar_path.relative_to(root)) if sidecar_path else None,
        decision_fingerprint=fp,
        attention_required=attention,
    )


def unique_destination(root: Path, rel: str, file_sha: str) -> Path:
    target = root / rel
    if not target.exists():
        return target
    stem, suffix = target.stem, target.suffix
    for n in range(1, 10000):
        candidate = target.with_name(f"{stem}__{file_sha[:8]}_{n}{suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError("Unable to allocate non-overwriting destination")


def append_jsonl(path: Path, row: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def sidecar_target_name(target: Path, sidecar_path: Path) -> Path:
    lower = sidecar_path.name.lower()
    if lower.endswith(".fge.json"):
        ext = ".fge.json"
    elif lower.endswith(".fge.yaml"):
        ext = ".fge.yaml"
    else:
        ext = ".fge.yml"
    candidate = target.with_name(target.name + ext)
    if not candidate.exists():
        return candidate
    for n in range(1, 10000):
        alt = target.with_name(f"{target.name}__sidecar_{n}{ext}")
        if not alt.exists():
            return alt
    raise RuntimeError("Unable to allocate sidecar destination")


def write_receipt(root: Path, config: Dict[str, Any], decision: Decision, final_destination: Optional[str]) -> Path:
    receipt_dir = root / config["route_receipts"]
    receipt_dir.mkdir(parents=True, exist_ok=True)
    short = decision.drop_id.removeprefix("FGE-DROP-")
    receipt_id = f"FGE-RCPT-ROUTE-{short}-{decision.decision_fingerprint[:8].upper()}"
    receipt = {
        "receipt_id": receipt_id,
        "router_object_id": ROUTER_OBJECT_ID,
        "router_version": ROUTER_VERSION,
        "timestamp": utc_now(),
        "decision": asdict(decision),
        "final_destination": final_destination,
        "source_preserved_by_git_history": True,
        "canon_effect": "NONE",
        "authority_effect": "NONE",
        "storage_promotion": False,
    }
    out = receipt_dir / f"{receipt_id}.json"
    if out.exists():
        raise RuntimeError(f"Receipt already exists: {out}")
    out.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def route_file(path: Path, root: Path, config: Dict[str, Any], decision: Decision, apply: bool) -> Dict[str, Any]:
    final_destination = decision.destination
    if decision.route_state in {"ROUTE", "ROUTE_AND_REVIEW"} and decision.destination:
        target = unique_destination(root, decision.destination, decision.sha256)
        final_destination = str(target.relative_to(root))
        if apply:
            target.parent.mkdir(parents=True, exist_ok=True)
            sidecar_path, _ = find_sidecar(path)
            shutil.move(str(path), str(target))
            if sidecar_path and sidecar_path.exists():
                shutil.move(str(sidecar_path), str(sidecar_target_name(target, sidecar_path)))

    event = {
        "timestamp": utc_now(),
        "router_object_id": ROUTER_OBJECT_ID,
        **asdict(decision),
        "final_destination": final_destination,
    }
    if apply:
        append_jsonl(root / config["index"], event)
        if decision.attention_required:
            short = decision.drop_id.removeprefix("FGE-DROP-")
            append_jsonl(
                root / config["attention_queue"],
                {
                    "event_id": f"FGE-ATTN-{short}-{decision.decision_fingerprint[:8].upper()}",
                    "object_ref": decision.drop_id,
                    "object_type": decision.object_class,
                    "reason": [decision.hold_reason or "ROUTE_REVIEW_REQUIRED"],
                    "priority": "P1" if decision.route_state == "HOLD" else "P2",
                    "state": "OPEN",
                    "created_at": utc_now(),
                    "next_action": "REVIEW_ROUTING_DECISION",
                    "canon_effect": "NONE",
                    "authority_effect": "NONE",
                },
            )
        write_receipt(root, config, decision, final_destination)
    return event


def iter_inbox_files(inbox: Path) -> Iterable[Path]:
    if not inbox.exists():
        return []
    return (
        p
        for p in sorted(inbox.rglob("*"))
        if p.is_file() and p.name not in {"README.md", ".gitkeep"} and not is_sidecar(p)
    )


def error_decision(path: Path, root: Path, exc: Exception) -> Decision:
    file_sha = sha256_file(path) if path.exists() else "UNKNOWN"
    fp = hashlib.sha256(f"{file_sha}|ERROR|{type(exc).__name__}".encode()).hexdigest()
    return Decision(
        drop_id=f"FGE-DROP-{file_sha[:16].upper()}",
        source_path=str(path.relative_to(root)),
        sha256=file_sha,
        mime_type=mimetypes.guess_type(path.name)[0] or "application/octet-stream",
        physical_class="UNKNOWN",
        object_class="UNKNOWN",
        confidence=0.0,
        route_state="HOLD",
        destination=None,
        hold_reason="CORRUPT_OR_UNREADABLE",
        decision_basis=[f"ERROR:{type(exc).__name__}"],
        sidecar_path=None,
        decision_fingerprint=fp,
        attention_required=True,
    )


def run(root: Path, config_path: Path, apply: bool) -> list[Dict[str, Any]]:
    config = load_json(config_path)
    inbox = root / config["inbox"]
    seen = load_seen_fingerprints(root / config["index"])
    events: list[Dict[str, Any]] = []
    for path in iter_inbox_files(inbox):
        try:
            decision = plan_decision(path, root, config)
        except Exception as exc:  # Fail closed and keep the source untouched.
            decision = error_decision(path, root, exc)
        if decision.decision_fingerprint in seen:
            continue
        events.append(route_file(path, root, config, decision, apply=apply))
        if apply:
            seen.add(decision.decision_fingerprint)
    return events


def main() -> int:
    parser = argparse.ArgumentParser(description="FGE fail-closed GitHub intake router")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--config", default="storage_makeover/config/routing-rules.json")
    parser.add_argument("--apply", action="store_true", help="Apply routes; default is dry-run")
    parser.add_argument("--json", action="store_true", help="Print machine-readable result")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    events = run(root, (root / args.config).resolve(), apply=args.apply)
    summary = {
        "router_object_id": ROUTER_OBJECT_ID,
        "version": ROUTER_VERSION,
        "mode": "APPLY" if args.apply else "DRY_RUN",
        "processed": len(events),
        "routed": sum(1 for e in events if e["route_state"] == "ROUTE"),
        "routed_with_review": sum(1 for e in events if e["route_state"] == "ROUTE_AND_REVIEW"),
        "held": sum(1 for e in events if e["route_state"] == "HOLD"),
        "events": events,
    }
    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print(
            f"FGE intake router {summary['mode']}: processed={summary['processed']} "
            f"routed={summary['routed']} review={summary['routed_with_review']} held={summary['held']}"
        )
        for event in events:
            print(f"- {event['source_path']} -> {event['route_state']} {event.get('final_destination') or event.get('hold_reason')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
