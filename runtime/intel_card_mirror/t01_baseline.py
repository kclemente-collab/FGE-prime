#!/usr/bin/env python3
"""FGE Intel Card MIRROR vertical slice: hardened T01 execution proof.

Scope:
FGE-CARD-RAVEN-001@0.1.1 -> CARD.MIRROR -> SB_330 -> MIRROR
-> VALIDATE -> RECEIPT -> PROOF.

No canon or authority writes are performed. Evidence is written only beneath the
supplied evidence directory.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

RUNTIME_VERSION = "FGE-INTEL-CARD-RUNTIME-WRAPPER-001@0.1.1"
PROOF_OBJECT_ID = "FGE-PROOF-INTEL-CARD-RAVEN-MIRROR-001"
EVENT_ID = "CARD.MIRROR"
SOURCE_OBJECT_ID = "SB_330"
CARD_ID = "FGE-CARD-RAVEN-001"
CARD_VERSION = "0.1.1"
CARD_CLASS = "INTELLIGENCE_CARD_RUNTIME_PROJECTION"
CARD_STATUS = "PROPOSED / FIRST_REAL_PROOF"
EXECUTOR_NAME = "MIRROR_EXECUTOR"

IDENTITY_FIELDS = (
    "subject",
    "subtitle",
    "collection",
    "char_id",
    "classification",
    "provenance",
    "theme",
    "arc",
)

PROTECTED_PATHS = (
    "registry.py",
    "book_raven.py",
)

ARTIFACT_KEYS = (
    "sourceResolution",
    "dispatch",
    "output",
    "validator",
)


class RuntimeFault(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


def parse_utc(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise RuntimeFault("RECEIPT_TIMESTAMP_INVALID", str(value)) from exc


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeFault("JSON_OBJECT_REQUIRED", f"Expected object in {path}")
    return value


def literal_assignment(path: Path, variable_name: str) -> Any:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(
                isinstance(target, ast.Name) and target.id == variable_name
                for target in targets
            ):
                if node.value is None:
                    break
                return ast.literal_eval(node.value)
    raise RuntimeFault(
        "SOURCE_SCHEMA_INVALID",
        f"{variable_name} not found as a literal assignment in {path}",
    )


def relative_evidence_ref(evidence_dir: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(evidence_dir.resolve()).as_posix()
    except ValueError as exc:
        raise RuntimeFault(
            "EVIDENCE_REF_ESCAPES_ROOT",
            f"{path} is outside {evidence_dir}",
        ) from exc


def resolve_evidence_ref(evidence_dir: Path, ref: str) -> Path:
    candidate = Path(ref)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise RuntimeFault("EVIDENCE_REF_INVALID", ref)
    resolved = (evidence_dir / candidate).resolve()
    try:
        resolved.relative_to(evidence_dir.resolve())
    except ValueError as exc:
        raise RuntimeFault("EVIDENCE_REF_ESCAPES_ROOT", ref) from exc
    return resolved


def freeze_card(card: dict[str, Any]) -> None:
    exact = {
        "objectId": CARD_ID,
        "version": CARD_VERSION,
        "class": CARD_CLASS,
        "status": CARD_STATUS,
        "sourceObjectId": SOURCE_OBJECT_ID,
        "automationEnabled": False,
        "canonEffect": "NONE",
        "authorityEffect": "NONE",
    }
    mismatches = {
        key: {"expected": expected, "observed": card.get(key)}
        for key, expected in exact.items()
        if card.get(key) != expected
    }
    if mismatches:
        raise RuntimeFault(
            "EXECUTION_FREEZE_BREACH",
            json.dumps(mismatches, sort_keys=True),
        )


def snapshot_authority_surface(
    repo_root: Path,
    card_path: Path,
) -> dict[str, str]:
    paths = {
        card_path.resolve().relative_to(repo_root.resolve()).as_posix(): card_path,
    }
    for rel in PROTECTED_PATHS:
        path = repo_root / rel
        if not path.is_file():
            raise RuntimeFault("AUTHORITY_SURFACE_MISSING", rel)
        paths[rel] = path

    return {
        rel: sha256_file(path)
        for rel, path in sorted(paths.items())
    }


def resolve_route(card: dict[str, Any], event_id: str) -> dict[str, str]:
    freeze_card(card)
    routes = card.get("eventRoutes")
    if not isinstance(routes, dict) or event_id not in routes:
        raise RuntimeFault("ROUTE_NOT_FOUND", f"No route registered for {event_id}")
    executor = routes[event_id]
    if event_id != EVENT_ID or executor != EXECUTOR_NAME:
        raise RuntimeFault(
            "ROUTE_MISMATCH",
            f"{event_id} resolved to {executor!r}",
        )
    return {
        "eventId": event_id,
        "executor": executor,
        "status": "RESOLVED",
    }


def resolve_source(
    repo_root: Path,
    source_object_id: str,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path]:
    registry_path = repo_root / "registry.py"
    registered_books = literal_assignment(registry_path, "REGISTERED_BOOKS")
    if not isinstance(registered_books, list):
        raise RuntimeFault(
            "REGISTRY_SCHEMA_INVALID",
            "REGISTERED_BOOKS must be a list",
        )

    matches: list[tuple[str, dict[str, Any], Path]] = []
    for rel in registered_books:
        if not isinstance(rel, str):
            continue
        candidate = repo_root / rel
        if not candidate.is_file():
            continue
        book = literal_assignment(candidate, "BOOK")
        if not isinstance(book, dict):
            continue
        provenance = str(book.get("provenance", ""))
        if source_object_id in provenance:
            matches.append((rel, book, candidate))

    if len(matches) != 1:
        raise RuntimeFault(
            "SOURCE_RESOLUTION_NON_UNIQUE",
            (
                f"Expected exactly one registered source for "
                f"{source_object_id}; found {len(matches)}"
            ),
        )

    rel, book, source_path = matches[0]
    if rel != "book_raven.py":
        raise RuntimeFault(
            "SOURCE_RESOLUTION_UNEXPECTED",
            f"Expected book_raven.py, got {rel}",
        )

    resolution = {
        "objectId": "FGE-SOURCE-RESOLUTION-RAVEN-T01",
        "class": "SOURCE_RESOLUTION_EVIDENCE",
        "status": "RESOLVED",
        "sourceObjectId": source_object_id,
        "registryRef": "registry.py#REGISTERED_BOOKS",
        "registeredSourcePath": rel,
        "sourceRef": f"{rel}#{source_object_id}",
        "sourceCharId": book.get("char_id"),
        "sourceSubject": book.get("subject"),
        "sourceSha256": sha256_file(source_path),
        "canonEffect": "NONE",
        "authorityEffect": "NONE",
    }
    return resolution, book, source_path, registry_path


def mirror_executor(
    card: dict[str, Any],
    book: dict[str, Any],
    source_resolution: dict[str, Any],
    invocation_id: str,
) -> dict[str, Any]:
    projection = {field: book.get(field) for field in IDENTITY_FIELDS}
    if any(
        projection[field] is None
        for field in ("subject", "char_id", "provenance")
    ):
        raise RuntimeFault(
            "AUTHORITATIVE_STATE_INCOMPLETE",
            "Required identity fields are missing",
        )

    return {
        "objectId": "FGE-MIRROR-RAVEN-T01-OUTPUT-001",
        "class": "CHARACTER_MIRROR",
        "status": "GENERATED_EXECUTION_OUTPUT",
        "eventId": EVENT_ID,
        "cardRef": f"{card['objectId']}@{card['version']}",
        "sourceObjectId": card["sourceObjectId"],
        "executorInvocationId": invocation_id,
        "identityProjection": projection,
        "sourceDigest": {
            "algorithm": "sha256",
            "value": source_resolution["sourceSha256"],
        },
        "renderState": "NOT_RENDERED",
        "validationScope": "RUNTIME_ONLY",
        "visualIdentityState": "NOT_EVALUATED",
        "canonEffect": "NONE",
        "authorityEffect": "NONE",
    }


def dispatch_event(
    route_result: dict[str, Any],
    card: dict[str, Any],
    book: dict[str, Any],
    source_resolution: dict[str, Any],
    invocation_id: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    executors: dict[str, Callable[..., dict[str, Any]]] = {
        EXECUTOR_NAME: mirror_executor,
    }
    executor_name = route_result.get("executor")
    executor = executors.get(str(executor_name))
    if executor is None:
        raise RuntimeFault(
            "EXECUTOR_NOT_FOUND",
            f"Resolved executor is unavailable: {executor_name}",
        )

    output = executor(
        card,
        book,
        source_resolution,
        invocation_id,
    )
    dispatch = {
        "objectId": "FGE-DISPATCH-RAVEN-MIRROR-T01-001",
        "class": "EXECUTED_RELATIONSHIP_EVIDENCE",
        "eventId": EVENT_ID,
        "resolvedExecutor": executor_name,
        "executorInvocationId": invocation_id,
        "status": "INVOKED",
        "canonEffect": "NONE",
        "authorityEffect": "NONE",
    }
    return output, dispatch


def validator_boundary(
    card: dict[str, Any],
    route_result: dict[str, Any],
    dispatch: dict[str, Any],
    source_resolution: dict[str, Any],
    book: dict[str, Any],
    output: dict[str, Any],
) -> dict[str, Any]:
    a1 = (
        route_result.get("status") == "RESOLVED"
        and dispatch.get("status") == "INVOKED"
        and route_result.get("executor") == EXECUTOR_NAME
        and dispatch.get("resolvedExecutor") == EXECUTOR_NAME
        and dispatch.get("executorInvocationId")
        == output.get("executorInvocationId")
    )
    a2 = (
        source_resolution.get("status") == "RESOLVED"
        and source_resolution.get("sourceObjectId") == SOURCE_OBJECT_ID
        and source_resolution.get("registeredSourcePath") == "book_raven.py"
        and source_resolution.get("sourceCharId") == book.get("char_id")
    )

    projection = output.get("identityProjection", {})
    a4 = (
        output.get("class") == "CHARACTER_MIRROR"
        and output.get("eventId") == EVENT_ID
        and output.get("sourceObjectId") == SOURCE_OBJECT_ID
        and output.get("canonEffect") == "NONE"
        and output.get("authorityEffect") == "NONE"
        and output.get("validationScope") == "RUNTIME_ONLY"
        and output.get("visualIdentityState") == "NOT_EVALUATED"
        and all(
            projection.get(field) == book.get(field)
            for field in IDENTITY_FIELDS
        )
        and card.get("canonEffect") == "NONE"
        and card.get("authorityEffect") == "NONE"
    )

    assertions = {
        "A1_executed_route": "PASS" if a1 else "FAIL",
        "A2_registry_source_resolution": "PASS" if a2 else "FAIL",
        "A4_output_validation": "PASS" if a4 else "FAIL",
    }
    return {
        "objectId": "FGE-VALIDATOR-RAVEN-MIRROR-T01-001",
        "class": "RUNTIME_VALIDATOR_RESULT",
        "status": (
            "PASS"
            if all(value == "PASS" for value in assertions.values())
            else "FAIL"
        ),
        "assertions": assertions,
        "canonEffect": "NONE",
        "authorityEffect": "NONE",
    }


def receipt_emitter(
    *,
    evidence_dir: Path,
    invocation_id: str,
    started_at: str,
    completed_at: str,
    card_path: Path,
    source_resolution_path: Path,
    dispatch_path: Path,
    output_path: Path,
    validator_path: Path,
) -> dict[str, Any]:
    artifact_paths = {
        "sourceResolution": source_resolution_path,
        "dispatch": dispatch_path,
        "output": output_path,
        "validator": validator_path,
    }
    artifacts = {
        key: {
            "ref": relative_evidence_ref(evidence_dir, path),
            "sha256": sha256_file(path),
        }
        for key, path in artifact_paths.items()
    }

    return {
        "objectId": "FGE-RECEIPT-INTEL-CARD-RAVEN-MIRROR-T01-001",
        "class": "RUNTIME_EXECUTION_RECEIPT",
        "executorInvocationId": invocation_id,
        "executionStartedAt": started_at,
        "executionCompletedAt": completed_at,
        "runtimeVersion": RUNTIME_VERSION,
        "runtimeSha256": sha256_file(Path(__file__).resolve()),
        "cardRef": f"{CARD_ID}@{CARD_VERSION}",
        "cardSha256": sha256_file(card_path),
        "sourceObjectId": SOURCE_OBJECT_ID,
        "sourceSha256": load_json(source_resolution_path)["sourceSha256"],
        "artifacts": artifacts,
        "executionContext": {
            "githubRunId": os.getenv("GITHUB_RUN_ID"),
            "githubRunAttempt": os.getenv("GITHUB_RUN_ATTEMPT"),
            "githubSha": os.getenv("GITHUB_SHA"),
            "githubRef": os.getenv("GITHUB_REF"),
        },
        "evidenceStatus": "PENDING_VERIFICATION",
        "canonEffect": "NONE",
        "authorityEffect": "NONE",
    }


def verify_receipt_integrity(
    receipt: dict[str, Any],
    evidence_dir: Path,
    invocation_id: str,
) -> tuple[str, list[str]]:
    gaps: list[str] = []

    if receipt.get("executorInvocationId") != invocation_id:
        gaps.append("INVOCATION_ID_MISMATCH")
    if receipt.get("runtimeVersion") != RUNTIME_VERSION:
        gaps.append("RUNTIME_VERSION_MISMATCH")

    started = parse_utc(str(receipt.get("executionStartedAt", "")))
    completed = parse_utc(str(receipt.get("executionCompletedAt", "")))
    if completed < started:
        gaps.append("TIMESTAMP_ORDER_INVALID")

    artifacts = receipt.get("artifacts")
    if not isinstance(artifacts, dict):
        gaps.append("ARTIFACT_MAP_MISSING")
        artifacts = {}

    loaded: dict[str, dict[str, Any]] = {}
    for key in ARTIFACT_KEYS:
        record = artifacts.get(key)
        if not isinstance(record, dict):
            gaps.append(f"{key}:RECORD_MISSING")
            continue
        ref = record.get("ref")
        expected_digest = record.get("sha256")
        if not isinstance(ref, str) or not ref:
            gaps.append(f"{key}:REF_MISSING")
            continue
        if not isinstance(expected_digest, str) or not expected_digest:
            gaps.append(f"{key}:DIGEST_MISSING")
            continue
        try:
            path = resolve_evidence_ref(evidence_dir, ref)
        except RuntimeFault as fault:
            gaps.append(f"{key}:{fault.code}")
            continue
        if not path.is_file():
            gaps.append(f"{key}:FILE_MISSING")
            continue
        observed_digest = sha256_file(path)
        if observed_digest != expected_digest:
            gaps.append(f"{key}:DIGEST_MISMATCH")
            continue
        loaded[key] = load_json(path)

    output = loaded.get("output", {})
    dispatch = loaded.get("dispatch", {})
    validator = loaded.get("validator", {})

    if output.get("executorInvocationId") != invocation_id:
        gaps.append("OUTPUT_INVOCATION_MISMATCH")
    if dispatch.get("executorInvocationId") != invocation_id:
        gaps.append("DISPATCH_INVOCATION_MISMATCH")
    if dispatch.get("status") != "INVOKED":
        gaps.append("DISPATCH_NOT_INVOKED")
    if validator.get("status") != "PASS":
        gaps.append("VALIDATOR_NOT_PASS")

    status = "PASS" if not gaps else "FAIL"
    return status, gaps


def build_proof(
    validator: dict[str, Any],
    authority_before: dict[str, str],
    authority_after: dict[str, str],
    receipt_integrity: str,
    receipt_gaps: list[str],
    receipt_ref: str,
) -> dict[str, Any]:
    assertions = dict(validator["assertions"])
    assertions["A3_protected_authority_nonmutation"] = (
        "PASS" if authority_before == authority_after else "FAIL"
    )
    assertions["A5_receipt_integrity"] = receipt_integrity

    passed = all(value == "PASS" for value in assertions.values())
    return {
        "objectId": PROOF_OBJECT_ID,
        "class": "RUNTIME_EXECUTION_PROOF",
        "status": "EVIDENCED" if passed else "NOT_EVIDENCED",
        "subject": {
            "cardId": CARD_ID,
            "cardVersion": CARD_VERSION,
            "sourceObjectId": SOURCE_OBJECT_ID,
            "eventId": EVENT_ID,
        },
        "assertions": assertions,
        "receiptIntegrityGaps": receipt_gaps,
        "authorityDigestBefore": authority_before,
        "authorityDigestAfter": authority_after,
        "circuitState": "CLOSED_ONCE" if passed else "OPEN",
        "validationScope": "RUNTIME_ONLY",
        "visualIdentityState": "NOT_EVALUATED",
        "receiptRef": receipt_ref,
        "canonEffect": "NONE",
        "authorityEffect": "NONE",
    }


def execute_t01(
    repo_root: Path,
    card_path: Path,
    evidence_dir: Path,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    card_path = card_path.resolve()
    evidence_dir = evidence_dir.resolve()
    evidence_dir.mkdir(parents=True, exist_ok=True)

    started_at = utc_now()
    invocation_id = str(uuid.uuid4())

    authority_before = snapshot_authority_surface(repo_root, card_path)
    card = load_json(card_path)
    freeze_card(card)
    route_result = resolve_route(card, EVENT_ID)

    source_resolution, book, _, _ = resolve_source(
        repo_root,
        card.get("sourceObjectId", ""),
    )
    source_resolution_path = write_json(
        evidence_dir / "source_resolution.json",
        source_resolution,
    )

    output, dispatch = dispatch_event(
        route_result,
        card,
        book,
        source_resolution,
        invocation_id,
    )
    dispatch_path = write_json(
        evidence_dir / "dispatch.json",
        dispatch,
    )
    output_path = write_json(
        evidence_dir / "mirror_output.json",
        output,
    )

    validator = validator_boundary(
        card,
        route_result,
        dispatch,
        source_resolution,
        book,
        output,
    )
    validator_path = write_json(
        evidence_dir / "validator_result.json",
        validator,
    )

    completed_at = utc_now()
    receipt = receipt_emitter(
        evidence_dir=evidence_dir,
        invocation_id=invocation_id,
        started_at=started_at,
        completed_at=completed_at,
        card_path=card_path,
        source_resolution_path=source_resolution_path,
        dispatch_path=dispatch_path,
        output_path=output_path,
        validator_path=validator_path,
    )
    receipt_path = write_json(evidence_dir / "receipt.json", receipt)

    receipt_integrity, receipt_gaps = verify_receipt_integrity(
        receipt,
        evidence_dir,
        invocation_id,
    )
    receipt["evidenceStatus"] = (
        "EXECUTION_EVIDENCE"
        if receipt_integrity == "PASS"
        else "NOT_EXECUTION_EVIDENCE"
    )
    receipt["executionEvidenceGate"] = {
        "status": receipt_integrity,
        "gaps": receipt_gaps,
    }
    receipt_path = write_json(receipt_path, receipt)

    authority_after = snapshot_authority_surface(repo_root, card_path)

    proof = build_proof(
        validator,
        authority_before,
        authority_after,
        receipt_integrity,
        receipt_gaps,
        relative_evidence_ref(evidence_dir, receipt_path),
    )
    proof_path = write_json(
        evidence_dir / f"{PROOF_OBJECT_ID}.json",
        proof,
    )

    summary = {
        "testId": "T01_BASELINE_HARDENED",
        "status": "PASS" if proof["status"] == "EVIDENCED" else "FAIL",
        "proofRef": relative_evidence_ref(evidence_dir, proof_path),
        "proofObjectId": PROOF_OBJECT_ID,
        "circuitState": proof["circuitState"],
        "evidenceStatus": receipt["evidenceStatus"],
        "assertions": proof["assertions"],
        "validationScope": "RUNTIME_ONLY",
        "visualIdentityState": "NOT_EVALUATED",
    }
    write_json(
        evidence_dir / "T01_BASELINE_HARDENED.summary.json",
        summary,
    )
    return summary


def write_failure(
    evidence_dir: Path,
    test_id: str,
    fault: RuntimeFault,
) -> None:
    write_json(
        evidence_dir / f"{test_id}.failure.json",
        {
            "testId": test_id,
            "status": "FAIL",
            "faultCode": fault.code,
            "message": fault.message,
            "canonEffect": "NONE",
            "authorityEffect": "NONE",
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument(
        "--card",
        type=Path,
        default=Path("cards/FGE-CARD-RAVEN-001_v0.1.1.json"),
    )
    parser.add_argument(
        "--evidence-dir",
        type=Path,
        default=Path(".fge_evidence/T01_BASELINE_HARDENED"),
    )
    args = parser.parse_args()

    try:
        summary = execute_t01(
            args.repo_root,
            args.card,
            args.evidence_dir,
        )
    except RuntimeFault as fault:
        evidence_dir = args.evidence_dir.resolve()
        evidence_dir.mkdir(parents=True, exist_ok=True)
        write_failure(
            evidence_dir,
            "T01_BASELINE_HARDENED",
            fault,
        )
        print(
            json.dumps(
                {
                    "status": "FAIL",
                    "faultCode": fault.code,
                    "message": fault.message,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
