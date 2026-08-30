#!/usr/bin/env python3
"""FGE reference pointer registry validator/resolver v1.1.

Execution law:
REFERENCE > MEMORY
RESOLVE > INTERPRET
UNKNOWN > INVENTED
TRANSIENT_FAILURE -> RETRY
DETERMINISTIC_FAILURE -> LOCK

The resolver never substitutes semantic guessing or model memory for a failed
reference. Registry records may intentionally exist before a physical source
is installed; those records are classified SOURCE_MISSING and hard-lock any
execution that depends on them.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


REF_PATTERN = re.compile(
    r"\[REFERENCE:\s*"
    r"(?P<id>FGE-(?:[A-Z0-9]+-)+\d{3,})"
    r"(?:@(?P<ver>\d+\.\d+\.\d+|CURRENT))?"
    r"(?:#(?P<anchor>[A-Za-z0-9._/-]+))?"
    r"\s*\]"
)
FGE_ID_PATTERN = re.compile(r"^FGE-(?:[A-Z0-9]+-)+\d{3,}$")
SHA1_PATTERN = re.compile(r"^[0-9a-f]{40}$")
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")

FAULT_UNREGISTERED = "FGE-FAULT-REFERENCE-UNREGISTERED"
FAULT_SOURCE_MISSING = "FGE-FAULT-REFERENCE-SOURCE-MISSING"
FAULT_DEPRECATED_TARGET = "FGE-FAULT-REFERENCE-DEPRECATED-TARGET"
FAULT_404 = "FGE-FAULT-RESOLUTION-404"
FAULT_403 = "FGE-FAULT-RESOLUTION-403"
FAULT_TIMEOUT = "FGE-FAULT-RESOLUTION-TIMEOUT"
FAULT_5XX = "FGE-FAULT-RESOLUTION-5XX"
FAULT_VERSION = "FGE-FAULT-VERSION-MISMATCH"
FAULT_BLOB = "FGE-FAULT-BLOB-MISMATCH"
FAULT_ANCHOR = "FGE-FAULT-ANCHOR-MISSING"
FAULT_SCHEMA = "FGE-FAULT-SCHEMA-INVALID"
FAULT_REGISTRY_DIVERGENCE = "FGE-FAULT-REGISTRY-COMPAT-DIVERGENCE"

DEFAULT_RETRIES = 3
DEFAULT_TIMEOUT_SECONDS = 8.0


@dataclass
class Fault:
    fault_id: str
    failed_reference: Optional[str]
    reason: str
    severity: str = "HIGH"
    action_taken: str = "GENERATION_LOCKED_HEURISTIC_PREVENTED"
    http_status: Optional[int] = None
    target_url: Optional[str] = None
    retryable: bool = False


@dataclass
class ReferenceToken:
    raw: str
    reference_id: str
    version_constraint: Optional[str]
    anchor: Optional[str]


class RegistryValidationError(ValueError):
    pass


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def git_blob_sha(content: bytes) -> str:
    header = f"blob {len(content)}\0".encode("utf-8")
    return hashlib.sha1(header + content).hexdigest()


def github_heading_anchor(heading: str) -> str:
    value = heading.strip().lower()
    value = re.sub(r"[^\w\- ]", "", value, flags=re.UNICODE)
    return value.replace(" ", "-")


def markdown_anchors(text: str) -> set[str]:
    anchors: set[str] = set()
    duplicate_count: Dict[str, int] = {}
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if not match:
            continue
        base = github_heading_anchor(match.group(1))
        count = duplicate_count.get(base, 0)
        duplicate_count[base] = count + 1
        anchors.add(base if count == 0 else f"{base}-{count}")
    return anchors


def extract_references(text: str) -> List[ReferenceToken]:
    return [
        ReferenceToken(
            raw=match.group(0),
            reference_id=match.group("id"),
            version_constraint=match.group("ver"),
            anchor=match.group("anchor"),
        )
        for match in REF_PATTERN.finditer(text)
    ]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RegistryValidationError(message)


def validate_record(record: Dict[str, Any], index: int) -> None:
    required = {
        "reference_id", "title", "repository", "path", "git_ref",
        "pointer_mode", "resolution_state", "version", "lifecycle_status",
        "lock_state", "authority", "provenance", "aliases", "tags",
    }
    missing = sorted(required - record.keys())
    _require(not missing, f"records[{index}] missing required fields: {missing}")

    ref_id = record["reference_id"]
    _require(isinstance(ref_id, str) and FGE_ID_PATTERN.fullmatch(ref_id) is not None,
             f"records[{index}].reference_id invalid: {ref_id!r}")

    repository = record["repository"]
    _require(isinstance(repository, str) and repository.count("/") == 1,
             f"records[{index}].repository must be owner/repo")

    pointer_mode = record["pointer_mode"]
    _require(pointer_mode in {"LIVE", "FROZEN"},
             f"records[{index}].pointer_mode invalid: {pointer_mode!r}")

    resolution_state = record["resolution_state"]
    _require(resolution_state in {"RESOLVABLE", "SOURCE_MISSING", "DEPRECATED_TARGET"},
             f"records[{index}].resolution_state invalid: {resolution_state!r}")

    path = record["path"]
    if resolution_state == "RESOLVABLE":
        _require(isinstance(path, str) and path and not path.startswith("/") and "../" not in path,
                 f"records[{index}].path must be repository-relative when RESOLVABLE")
    elif resolution_state == "SOURCE_MISSING":
        _require(path is None, f"records[{index}].path must be null when SOURCE_MISSING")
        _require(record.get("commit_sha") is None and record.get("blob_sha") is None,
                 f"records[{index}] SOURCE_MISSING cannot claim Git evidence")

    version = record["version"]
    _require(version == "CURRENT" or (isinstance(version, str) and SEMVER_PATTERN.fullmatch(version)),
             f"records[{index}].version invalid: {version!r}")

    _require(record["lifecycle_status"] in {"PROPOSED", "REVIEW", "ACTIVE", "PROMOTED", "DEPRECATED"},
             f"records[{index}].lifecycle_status invalid")
    _require(record["lock_state"] in {"LOCKED", "UNLOCKED", "NONE"},
             f"records[{index}].lock_state invalid")
    _require(record["authority"] in {"DIRECTOR", "CORE_RUNTIME", "SYSTEM_DEFAULT", "FGE_GOVERNANCE", "REPOSITORY"},
             f"records[{index}].authority invalid")

    for sha_field in ("commit_sha", "blob_sha"):
        value = record.get(sha_field)
        _require(value is None or (isinstance(value, str) and SHA1_PATTERN.fullmatch(value)),
                 f"records[{index}].{sha_field} invalid")

    if pointer_mode == "FROZEN":
        _require(resolution_state == "RESOLVABLE",
                 f"records[{index}] FROZEN pointer must be RESOLVABLE")
        _require(bool(record.get("commit_sha")) and bool(record.get("blob_sha")),
                 f"records[{index}] FROZEN pointer requires commit_sha and blob_sha")

    _require(isinstance(record["aliases"], list), f"records[{index}].aliases must be array")
    _require(isinstance(record["tags"], list), f"records[{index}].tags must be array")


def canonical_record(record: Dict[str, Any]) -> Dict[str, Any]:
    return json.loads(json.dumps(record, sort_keys=True))


def validate_registry(registry: Dict[str, Any], schema: Optional[Dict[str, Any]] = None) -> None:
    required = {"registry_id", "version", "records"}
    missing = sorted(required - registry.keys())
    _require(not missing, f"registry missing required fields: {missing}")

    registry_id = registry["registry_id"]
    _require(registry_id == "FGE-REFERENCE-POINTER-REGISTRY-001",
             f"unexpected registry_id: {registry_id!r}")
    if "object_id" in registry:
        _require(registry["object_id"] == registry_id,
                 "object_id compatibility alias diverges from registry_id")

    _require(isinstance(registry["version"], str) and SEMVER_PATTERN.fullmatch(registry["version"]),
             "registry version must be semver")
    _require(isinstance(registry["records"], list), "records must be an array")

    seen: set[str] = set()
    for index, record in enumerate(registry["records"]):
        _require(isinstance(record, dict), f"records[{index}] must be object")
        validate_record(record, index)
        ref_id = record["reference_id"]
        _require(ref_id not in seen, f"duplicate reference_id: {ref_id}")
        seen.add(ref_id)

    if "pointers" in registry:
        _require(isinstance(registry["pointers"], list), "pointers must be an array")
        records_map = {r["reference_id"]: canonical_record(r) for r in registry["records"]}
        pointers_map = {r["reference_id"]: canonical_record(r) for r in registry["pointers"]}
        if records_map != pointers_map:
            raise RegistryValidationError(
                f"{FAULT_REGISTRY_DIVERGENCE}: pointers compatibility mirror diverges from records"
            )

    if schema is not None:
        try:
            import jsonschema  # type: ignore
        except ImportError:
            return
        jsonschema.Draft202012Validator(schema).validate(registry)


class FGEReferenceResolver:
    def __init__(self, registry_data: Dict[str, Any]):
        validate_registry(registry_data)
        self.registry = registry_data
        self.records_map = {record["reference_id"]: record for record in registry_data["records"]}

    def resolve_token(self, token: ReferenceToken) -> Tuple[Optional[Dict[str, Any]], Optional[Fault]]:
        record = self.records_map.get(token.reference_id)
        if record is None:
            return None, Fault(
                fault_id=FAULT_UNREGISTERED,
                failed_reference=token.raw,
                reason="Identifier is absent from the pointer registry.",
            )

        if token.version_constraint and token.version_constraint != record["version"]:
            return None, Fault(
                fault_id=FAULT_VERSION,
                failed_reference=token.raw,
                reason=f"Required version {token.version_constraint}; registry holds {record['version']}.",
            )

        resolution_state = record["resolution_state"]
        if resolution_state == "SOURCE_MISSING":
            return None, Fault(
                fault_id=FAULT_SOURCE_MISSING,
                failed_reference=token.raw,
                reason="Reference is registered as a schema/catalog object but no physical source is installed.",
            )
        if resolution_state == "DEPRECATED_TARGET":
            return None, Fault(
                fault_id=FAULT_DEPRECATED_TARGET,
                failed_reference=token.raw,
                reason="Reference target is deprecated and cannot be used for new execution.",
            )

        path = record["path"]
        assert isinstance(path, str)
        effective_anchor = token.anchor or record.get("anchor")
        encoded_path = urllib.parse.quote(path, safe="/")
        encoded_ref = urllib.parse.quote(record["git_ref"], safe="")
        browser_url = f"https://github.com/{record['repository']}/blob/{encoded_ref}/{encoded_path}"
        if effective_anchor:
            browser_url += f"#{effective_anchor}"

        fetch_ref = record.get("commit_sha") if record["pointer_mode"] == "FROZEN" else record["git_ref"]
        raw_url = (
            f"https://raw.githubusercontent.com/{record['repository']}"
            f"/{urllib.parse.quote(fetch_ref, safe='')}/{encoded_path}"
        )

        return {
            "reference_id": token.reference_id,
            "version": record["version"],
            "anchor": effective_anchor,
            "repository": record["repository"],
            "path": path,
            "git_ref": record["git_ref"],
            "pointer_mode": record["pointer_mode"],
            "resolution_state": resolution_state,
            "commit_sha": record.get("commit_sha"),
            "blob_sha": record.get("blob_sha"),
            "browser_url": browser_url,
            "raw_url": raw_url,
            "lifecycle_status": record["lifecycle_status"],
            "lock_state": record["lock_state"],
            "authority": record["authority"],
            "provenance": record["provenance"],
        }, None

    def resolve_text(self, raw_text: str) -> Dict[str, Any]:
        tokens = extract_references(raw_text)
        resolved: List[Dict[str, Any]] = []
        faults: List[Dict[str, Any]] = []
        for token in tokens:
            result, fault = self.resolve_token(token)
            if fault:
                faults.append(asdict(fault))
            elif result:
                resolved.append(result)
        return {
            "valid": not faults,
            "generation_locked": bool(faults),
            "references_found": len(tokens),
            "resolved": resolved,
            "faults": faults,
        }


def fetch_with_retry(url: str, retries: int = DEFAULT_RETRIES, timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS) -> Tuple[Optional[bytes], Optional[Fault]]:
    last_fault: Optional[Fault] = None
    attempts = max(1, retries)

    for attempt in range(1, attempts + 1):
        request = urllib.request.Request(url, headers={"User-Agent": "FGEReferenceResolver/1.1"})
        try:
            with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
                return response.read(), None
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None, Fault(FAULT_404, None, "Registered physical target does not exist.", http_status=404, target_url=url)
            if exc.code == 403:
                return None, Fault(FAULT_403, None, "Registered target exists but access was denied.", http_status=403, target_url=url)
            if 500 <= exc.code <= 599:
                last_fault = Fault(FAULT_5XX, None, f"GitHub/server returned HTTP {exc.code}.", http_status=exc.code, target_url=url, retryable=True)
            else:
                return None, Fault(f"FGE-FAULT-RESOLUTION-{exc.code}", None, f"Unexpected HTTP {exc.code}.", http_status=exc.code, target_url=url)
        except (TimeoutError, urllib.error.URLError) as exc:
            last_fault = Fault(FAULT_TIMEOUT, None, f"Transient transport failure: {exc}", target_url=url, retryable=True)

        if attempt < attempts:
            time.sleep(min(2 ** (attempt - 1), 4))

    if last_fault:
        last_fault.action_taken = "RETRIES_EXHAUSTED_GENERATION_LOCKED"
    return None, last_fault


def verify_resolved_target(resolved: Dict[str, Any], content: bytes) -> Optional[Fault]:
    expected_blob = resolved.get("blob_sha")
    if expected_blob:
        actual_blob = git_blob_sha(content)
        if actual_blob != expected_blob:
            return Fault(
                FAULT_BLOB,
                resolved["reference_id"],
                f"Expected blob {expected_blob}; fetched {actual_blob}.",
                target_url=resolved["raw_url"],
            )

    anchor = resolved.get("anchor")
    if anchor:
        text = content.decode("utf-8", errors="replace")
        if anchor not in markdown_anchors(text):
            return Fault(
                FAULT_ANCHOR,
                resolved["reference_id"],
                f"Markdown anchor #{anchor} was not found in the resolved document.",
                target_url=resolved["browser_url"],
            )
    return None


def verify_remote_resolution(resolution: Dict[str, Any], retries: int, timeout_seconds: float) -> Optional[Fault]:
    content, fault = fetch_with_retry(resolution["raw_url"], retries=retries, timeout_seconds=timeout_seconds)
    if fault:
        fault.failed_reference = resolution["reference_id"]
        return fault
    assert content is not None
    return verify_resolved_target(resolution, content)


def scan_text_files(paths: Iterable[Path]) -> str:
    chunks: List[str] = []
    for path in paths:
        if path.is_file():
            chunks.append(path.read_text(encoding="utf-8"))
    return "\n".join(chunks)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and resolve FGE reference pointers.")
    parser.add_argument("--registry", default="00_governance/references/FGE_REFERENCE_POINTER_REGISTRY_v1.json")
    parser.add_argument("--schema", default="00_governance/references/FGE_REFERENCE_POINTER_REGISTRY.schema.json")
    parser.add_argument("--scan", action="append", default=[], help="Text/Markdown file containing [REFERENCE: ...] tokens. Repeatable.")
    parser.add_argument("--check-remote", action="store_true")
    parser.add_argument("--retries", type=int, default=DEFAULT_RETRIES)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    args = parser.parse_args()

    try:
        registry = load_json(Path(args.registry))
        schema_path = Path(args.schema)
        schema = load_json(schema_path) if schema_path.exists() else None
        validate_registry(registry, schema)
    except Exception as exc:
        fault = Fault(
            fault_id=FAULT_SCHEMA,
            failed_reference=None,
            reason=str(exc),
            action_taken="REGISTRY_REJECTED_GENERATION_LOCKED",
        )
        print(json.dumps({"valid": False, "generation_locked": True, "faults": [asdict(fault)]}, indent=2))
        return 2

    resolver = FGEReferenceResolver(registry)
    output: Dict[str, Any] = {
        "valid": True,
        "generation_locked": False,
        "registry_id": registry["registry_id"],
        "registry_version": registry["version"],
        "record_count": len(registry["records"]),
        "resolved": [],
        "faults": [],
    }

    if args.scan:
        text = scan_text_files(Path(item) for item in args.scan)
        result = resolver.resolve_text(text)
        output["resolved"].extend(result["resolved"])
        output["faults"].extend(result["faults"])

    if args.check_remote:
        if args.scan:
            targets = output["resolved"]
        else:
            targets = []
            for record in registry["records"]:
                result, fault = resolver.resolve_token(
                    ReferenceToken(
                        raw=f"[REFERENCE: {record['reference_id']}]",
                        reference_id=record["reference_id"],
                        version_constraint=None,
                        anchor=None,
                    )
                )
                if fault:
                    output["faults"].append(asdict(fault))
                elif result:
                    targets.append(result)

        for target in targets:
            fault = verify_remote_resolution(target, args.retries, args.timeout)
            if fault:
                output["faults"].append(asdict(fault))

    if output["faults"]:
        output["valid"] = False
        output["generation_locked"] = True

    print(json.dumps(output, indent=2))
    return 0 if output["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
