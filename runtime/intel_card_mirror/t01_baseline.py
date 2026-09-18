#!/usr/bin/env python3
"""FGE Intel Card MIRROR vertical slice: T01 baseline execution proof.

Scope is intentionally narrow:
FGE-CARD-RAVEN-001@0.1.1 -> CARD.MIRROR -> SB_330 -> MIRROR -> VALIDATE -> RECEIPT -> PROOF.
No canon or authority writes are performed.
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
from typing import Any

RUNTIME_VERSION = "FGE-INTEL-CARD-RUNTIME-WRAPPER-001@0.1.1"
PROOF_OBJECT_ID = "FGE-PROOF-INTEL-CARD-RAVEN-MIRROR-001"
EVENT_ID = "CARD.MIRROR"
SOURCE_OBJECT_ID = "SB_330"
CARD_ID = "FGE-CARD-RAVEN-001"
CARD_VERSION = "0.1.1"

EVIDENCE_STATUSES = {
    "EXAMPLE_ONLY",
    "SYNTHETIC",
    "NOT_EXECUTION_EVIDENCE",
    "EXECUTION_EVIDENCE",
}
EVIDENCE_GATE_FIELDS = (
    "executorInvocationId",
    "executionStartedAt",
    "executionCompletedAt",
    "runtimeVersion",
    "sourceResolutionRef",
    "validatorResultRef",
    "outputRef",
)
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


class RuntimeFault(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, payload: dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path.as_posix()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeFault("CARD_SCHEMA_INVALID", f"Expected object in {path}")
    return value


def literal_assignment(path: Path, variable_name: str) -> Any:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(t, ast.Name) and t.id == variable_name for t in targets):
                value_node = node.value
                if value_node is None:
                    break
                return ast.literal_eval(value_node)
    raise RuntimeFault("SOURCE_SCHEMA_INVALID", f"{variable_name} not found as a literal assignment in {path}")


def resolve_route(card: dict[str, Any], event_id: str) -> dict[str, str]:
    if card.get("objectId") != CARD_ID or card.get("version") != CARD_VERSION:
        raise RuntimeFault("CARD_IDENTITY_MISMATCH", "Card identity/version does not match frozen T01 target")
    routes = card.get("eventRoutes")
    if not isinstance(routes, dict) or event_id not in routes:
        raise RuntimeFault("ROUTE_NOT_FOUND", f"No route registered for {event_id}")
    if event_id != EVENT_ID or routes[event_id] != "MIRROR_EXECUTOR":
        raise RuntimeFault("ROUTE_MISMATCH", f"Unexpected route for {event_id}")
    if card.get("automationEnabled") is not False:
        raise RuntimeFault("EXECUTION_FREEZE_BREACH", "CARD.AUTOMATE must remain disabled")
    return {"eventId": event_id, "executor": routes[event_id], "status": "PASS"}


def resolve_source(repo_root: Path, source_object_id: str) -> tuple[dict[str, Any], dict[str, Any], Path, Path]:
    registry_path = repo_root / "registry.py"
    if not registry_path.is_file():
        raise RuntimeFault("REGISTRY_MISSING", "registry.py is required")

    registered_books = literal_assignment(registry_path, "REGISTERED_BOOKS")
    if not isinstance(registered_books, list):
        raise RuntimeFault("REGISTRY_SCHEMA_INVALID", "REGISTERED_BOOKS must be a list")

    matches: list[tuple[str, dict[str, Any], Path]] = []
    for rel in registered_books:
        if not isinstance(rel, str):
            continue
        candidate = repo_root / rel
        if not candidate.is_file():
            continue
        text = candidate.read_text(encoding="utf-8")
        if source_object_id not in text:
            continue
        book = literal_assignment(candidate, "BOOK")
        provenance = str(book.get("provenance", "")) if isinstance(book, dict) else ""
        if source_object_id in provenance:
            matches.append((rel, book, candidate))

    if len(matches) != 1:
        raise RuntimeFault(
            "SOURCE_RESOLUTION_NON_UNIQUE",
            f"Expected exactly one registered source for {source_object_id}; found {len(matches)}",
        )

    rel, book, source_path = matches[0]
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
    if any(projection[field] is None for field in ("subject", "char_id", "provenance")):
        raise RuntimeFault("AUTHORITATIVE_STATE_INCOMPLETE", "Required identity fields are missing")

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
        "canonEffect": "NONE",
        "authorityEffect": "NONE",
    }


def validator_boundary(
    card: dict[str, Any],
    route_result: dict[str, Any],
    source_resolution: dict[str, Any],
    book: dict[str, Any],
    output: dict[str, Any],
    authority_before: dict[str, str],
    authority_after: dict[str, str],
) -> dict[str, Any]:
    a1 = route_result.get("status") == "PASS" and route_result.get("executor") == "MIRROR_EXECUTOR"
    a2 = (
        source_resolution.get("status") == "RESOLVED"
        and source_resolution.get("sourceObjectId") == SOURCE_OBJECT_ID
        and source_resolution.get("registeredSourcePath") == "book_raven.py"
        and source_resolution.get("sourceCharId") == book.get("char_id")
    )
    a3 = authority_before == authority_after

    projection = output.get("identityProjection", {})
    a4 = (
        output.get("class") == "CHARACTER_MIRROR"
        and output.get("eventId") == EVENT_ID
        and output.get("sourceObjectId") == SOURCE_OBJECT_ID
        and output.get("canonEffect") == "NONE"
        and output.get("authorityEffect") == "NONE"
        and all(projection.get(field) == book.get(field) for field in IDENTITY_FIELDS)
    )

    assertions = {
        "A1_route_resolution": "PASS" if a1 else "FAIL",
        "A2_registry_source_resolution": "PASS" if a2 else "FAIL",
        "A3_authority_nonmutation": "PASS" if a3 else "FAIL",
        "A4_output_validation": "PASS" if a4 else "FAIL",
    }
    return {
        "objectId": "FGE-VALIDATOR-RAVEN-MIRROR-T01-001",
        "class": "RUNTIME_VALIDATOR_RESULT",
        "status": "PASS" if all(v == "PASS" for v in assertions.values()) else "FAIL",
        "assertions": assertions,
        "authorityDigestBefore": authority_before,
        "authorityDigestAfter": authority_after,
        "canonEffect": "NONE",
        "authorityEffect": "NONE",
    }


def receipt_emitter(receipt_payload: dict[str, Any]) -> tuple[dict[str, Any], str]:
    missing = [field for field in EVIDENCE_GATE_FIELDS if not receipt_payload.get(field)]
    evidence_status = "EXECUTION_EVIDENCE" if not missing else "NOT_EXECUTION_EVIDENCE"
    if evidence_status not in EVIDENCE_STATUSES:
        raise RuntimeFault("RECEIPT_STATUS_INVALID", evidence_status)
    receipt = {
        "objectId": "FGE-RECEIPT-INTEL-CARD-RAVEN-MIRROR-T01-001",
        "class": "RUNTIME_EXECUTION_RECEIPT",
        **receipt_payload,
        "evidenceStatus": evidence_status,
        "executionEvidenceGate": {
            "requires": list(EVIDENCE_GATE_FIELDS),
            "missing": missing,
            "status": "PASS" if not missing else "FAIL",
        },
        "canonEffect": "NONE",
        "authorityEffect": "NONE",
    }
    a5 = "PASS" if evidence_status == "EXECUTION_EVIDENCE" and not missing else "FAIL"
    return receipt, a5


def build_proof(
    validator: dict[str, Any],
    a5_receipt_integrity: str,
    receipt_ref: str,
    source_resolution_ref: str,
    output_ref: str,
) -> dict[str, Any]:
    assertions = dict(validator["assertions"])
    assertions["A5_receipt_integrity"] = a5_receipt_integrity
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
        "circuitState": "CLOSED_ONCE" if passed else "OPEN",
        "receiptRef": receipt_ref,
        "sourceResolutionRef": source_resolution_ref,
        "outputRef": output_ref,
        "canonEffect": "NONE",
        "authorityEffect": "NONE",
    }


def execute_t01(repo_root: Path, card_path: Path, evidence_dir: Path) -> dict[str, Any]:
    started_at = utc_now()
    invocation_id = str(uuid.uuid4())
    evidence_dir.mkdir(parents=True, exist_ok=True)

    card = load_json(card_path)
    route_result = resolve_route(card, EVENT_ID)
    source_resolution, book, source_path, registry_path = resolve_source(repo_root, card.get("sourceObjectId", ""))

    authority_before = {
        "registry.py": sha256_file(registry_path),
        source_path.name: sha256_file(source_path),
    }

    source_resolution_ref = write_json(evidence_dir / "source_resolution.json", source_resolution)
    output = mirror_executor(card, book, source_resolution, invocation_id)
    output_ref = write_json(evidence_dir / "mirror_output.json", output)

    authority_after = {
        "registry.py": sha256_file(registry_path),
        source_path.name: sha256_file(source_path),
    }

    validator = validator_boundary(
        card,
        route_result,
        source_resolution,
        book,
        output,
        authority_before,
        authority_after,
    )
    validator_result_ref = write_json(evidence_dir / "validator_result.json", validator)
    completed_at = utc_now()

    receipt_payload = {
        "executorInvocationId": invocation_id,
        "executionStartedAt": started_at,
        "executionCompletedAt": completed_at,
        "runtimeVersion": RUNTIME_VERSION,
        "sourceResolutionRef": source_resolution_ref,
        "validatorResultRef": validator_result_ref,
        "outputRef": output_ref,
        "eventId": EVENT_ID,
        "cardRef": f"{CARD_ID}@{CARD_VERSION}",
        "sourceObjectId": SOURCE_OBJECT_ID,
        "executionContext": {
            "githubRunId": os.getenv("GITHUB_RUN_ID"),
            "githubRunAttempt": os.getenv("GITHUB_RUN_ATTEMPT"),
            "githubSha": os.getenv("GITHUB_SHA"),
            "githubRef": os.getenv("GITHUB_REF"),
        },
    }
    receipt, a5 = receipt_emitter(receipt_payload)
    receipt_ref = write_json(evidence_dir / "receipt.json", receipt)

    proof = build_proof(validator, a5, receipt_ref, source_resolution_ref, output_ref)
    proof_ref = write_json(evidence_dir / f"{PROOF_OBJECT_ID}.json", proof)

    summary = {
        "testId": "T01_BASELINE",
        "status": "PASS" if proof["status"] == "EVIDENCED" else "FAIL",
        "proofRef": proof_ref,
        "proofObjectId": PROOF_OBJECT_ID,
        "circuitState": proof["circuitState"],
        "evidenceStatus": receipt["evidenceStatus"],
        "assertions": proof["assertions"],
    }
    write_json(evidence_dir / "T01_BASELINE.summary.json", summary)
    return summary


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
        default=Path(".fge_evidence/T01_BASELINE"),
    )
    args = parser.parse_args()

    try:
        summary = execute_t01(args.repo_root.resolve(), args.card.resolve(), args.evidence_dir.resolve())
    except RuntimeFault as fault:
        failure = {
            "testId": "T01_BASELINE",
            "status": "FAIL",
            "faultCode": fault.code,
            "message": fault.message,
            "canonEffect": "NONE",
            "authorityEffect": "NONE",
        }
        write_json(args.evidence_dir.resolve() / "T01_BASELINE.failure.json", failure)
        print(json.dumps(failure, indent=2, sort_keys=True))
        return 1

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
