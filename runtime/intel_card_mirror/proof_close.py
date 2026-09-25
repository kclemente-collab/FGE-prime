#!/usr/bin/env python3
"""Close-cycle proof harness for the Raven MIRROR PR #4 vertical slice.

T01: hardened happy path
T02: card freeze breach must fail before output
T03: route mutation must fail before output
T04: three fresh invocations must close with invariant semantics and distinct receipts

The maximum state emitted here is REPEATED_CLOSURE. This harness does not claim
REPRODUCIBLE_CIRCUIT, ROBUST_CIRCUIT, AUTOMATION_CANDIDATE, visual identity
validation, canon promotion, or authority promotion.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import t01_baseline as runtime  # noqa: E402


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected object in {path}")
    return value


def expected_failure(
    *,
    repo_root: Path,
    base_card: dict[str, Any],
    mutated_card: dict[str, Any],
    card_path: Path,
    evidence_dir: Path,
    test_id: str,
    expected_fault: str,
) -> dict[str, Any]:
    card_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(card_path, mutated_card)

    observed_fault = None
    message = None
    try:
        runtime.execute_t01(
            repo_root,
            card_path,
            evidence_dir,
        )
    except runtime.RuntimeFault as fault:
        observed_fault = fault.code
        message = fault.message

    output_exists = (evidence_dir / "mirror_output.json").exists()
    dispatch_exists = (evidence_dir / "dispatch.json").exists()
    passed = (
        observed_fault == expected_fault
        and not output_exists
        and not dispatch_exists
    )

    result = {
        "testId": test_id,
        "status": "PASS" if passed else "FAIL",
        "expectedOutcome": "FAIL_CLOSED",
        "expectedFaultCode": expected_fault,
        "observedFaultCode": observed_fault,
        "faultMessage": message,
        "mirrorOutputExists": output_exists,
        "dispatchEvidenceExists": dispatch_exists,
        "baseCardDigest": runtime.sha256_file(
            repo_root / "cards/FGE-CARD-RAVEN-001_v0.1.1.json"
        ),
        "mutatedCardDigest": runtime.sha256_file(card_path),
        "canonEffect": "NONE",
        "authorityEffect": "NONE",
    }
    write_json(evidence_dir / f"{test_id}.summary.json", result)

    if load_json(
        repo_root / "cards/FGE-CARD-RAVEN-001_v0.1.1.json"
    ) != base_card:
        result["status"] = "FAIL"
        result["repositoryCardMutationDetected"] = True
        write_json(evidence_dir / f"{test_id}.summary.json", result)

    return result


def repeat_test(
    *,
    repo_root: Path,
    card_path: Path,
    evidence_dir: Path,
) -> dict[str, Any]:
    runs = []
    for index in range(1, 4):
        run_dir = evidence_dir / f"run_{index}"
        summary = runtime.execute_t01(
            repo_root,
            card_path,
            run_dir,
        )
        receipt = load_json(run_dir / "receipt.json")
        output = load_json(run_dir / "mirror_output.json")
        proof = load_json(
            run_dir / f"{runtime.PROOF_OBJECT_ID}.json"
        )
        runs.append(
            {
                "index": index,
                "summary": summary,
                "invocationId": receipt["executorInvocationId"],
                "cardSha256": receipt["cardSha256"],
                "sourceSha256": receipt["sourceSha256"],
                "runtimeSha256": receipt["runtimeSha256"],
                "identityProjection": output["identityProjection"],
                "circuitState": proof["circuitState"],
                "evidenceStatus": receipt["evidenceStatus"],
            }
        )

    invocation_ids = {run["invocationId"] for run in runs}
    card_digests = {run["cardSha256"] for run in runs}
    source_digests = {run["sourceSha256"] for run in runs}
    runtime_digests = {run["runtimeSha256"] for run in runs}
    projections = {
        json.dumps(run["identityProjection"], sort_keys=True)
        for run in runs
    }

    checks = {
        "three_fresh_invocations": len(invocation_ids) == 3,
        "card_invariant": len(card_digests) == 1,
        "source_invariant": len(source_digests) == 1,
        "runtime_invariant": len(runtime_digests) == 1,
        "semantic_projection_invariant": len(projections) == 1,
        "all_closed_once": all(
            run["circuitState"] == "CLOSED_ONCE"
            for run in runs
        ),
        "all_execution_evidence": all(
            run["evidenceStatus"] == "EXECUTION_EVIDENCE"
            for run in runs
        ),
    }
    passed = all(checks.values())
    result = {
        "testId": "T04_REPEAT_EXECUTION",
        "status": "PASS" if passed else "FAIL",
        "checks": {
            key: "PASS" if value else "FAIL"
            for key, value in checks.items()
        },
        "runs": runs,
        "resultingState": (
            "REPEATED_CLOSURE" if passed else "OPEN"
        ),
        "explicitNonClaims": [
            "REPRODUCIBLE_CIRCUIT",
            "ROBUST_CIRCUIT",
            "AUTOMATION_CANDIDATE",
            "VISUAL_IDENTITY_VALIDATED",
        ],
        "canonEffect": "NONE",
        "authorityEffect": "NONE",
    }
    write_json(
        evidence_dir / "T04_REPEAT_EXECUTION.summary.json",
        result,
    )
    return result


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
        default=Path(".fge_evidence/PR4_CLOSE"),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    card_path = args.card.resolve()
    evidence_dir = args.evidence_dir.resolve()
    if evidence_dir.exists():
        shutil.rmtree(evidence_dir)
    evidence_dir.mkdir(parents=True, exist_ok=True)

    base_card = load_json(card_path)

    t01_dir = evidence_dir / "T01_HAPPY_PATH"
    try:
        t01 = runtime.execute_t01(
            repo_root,
            card_path,
            t01_dir,
        )
    except runtime.RuntimeFault as fault:
        t01 = {
            "testId": "T01_HAPPY_PATH",
            "status": "FAIL",
            "faultCode": fault.code,
            "message": fault.message,
        }
    write_json(t01_dir / "T01_HAPPY_PATH.aggregate.json", t01)

    freeze_card = dict(base_card)
    freeze_card["canonEffect"] = "WRITE"
    t02 = expected_failure(
        repo_root=repo_root,
        base_card=base_card,
        mutated_card=freeze_card,
        card_path=evidence_dir / "mutations/T02_card.json",
        evidence_dir=evidence_dir / "T02_FREEZE_BREACH",
        test_id="T02_FREEZE_BREACH",
        expected_fault="EXECUTION_FREEZE_BREACH",
    )

    route_card = json.loads(json.dumps(base_card))
    route_card["eventRoutes"]["CARD.MIRROR"] = "INVALID_EXECUTOR"
    t03 = expected_failure(
        repo_root=repo_root,
        base_card=base_card,
        mutated_card=route_card,
        card_path=evidence_dir / "mutations/T03_card.json",
        evidence_dir=evidence_dir / "T03_ROUTE_BREAK",
        test_id="T03_ROUTE_BREAK",
        expected_fault="ROUTE_MISMATCH",
    )

    try:
        t04 = repeat_test(
            repo_root=repo_root,
            card_path=card_path,
            evidence_dir=evidence_dir / "T04_REPEAT_EXECUTION",
        )
    except runtime.RuntimeFault as fault:
        t04 = {
            "testId": "T04_REPEAT_EXECUTION",
            "status": "FAIL",
            "faultCode": fault.code,
            "message": fault.message,
            "resultingState": "OPEN",
        }
        write_json(
            evidence_dir
            / "T04_REPEAT_EXECUTION"
            / "T04_REPEAT_EXECUTION.summary.json",
            t04,
        )

    all_pass = (
        t01.get("status") == "PASS"
        and t02.get("status") == "PASS"
        and t03.get("status") == "PASS"
        and t04.get("status") == "PASS"
    )

    receipt = {
        "objectId": "FGE-RECEIPT-PR4-CLOSE-PROOF-001",
        "class": "CONTROLLED_CIRCUIT_CLOSE_RECEIPT",
        "tests": {
            "T01_HAPPY_PATH": t01.get("status"),
            "T02_FREEZE_BREACH": t02.get("status"),
            "T03_ROUTE_BREAK": t03.get("status"),
            "T04_REPEAT_EXECUTION": t04.get("status"),
        },
        "proofState": (
            "REPEATED_CLOSURE" if all_pass else "OPEN"
        ),
        "validationScope": "RUNTIME_ONLY",
        "visualIdentityState": "NOT_EVALUATED",
        "explicitNonClaims": [
            "REPRODUCIBLE_CIRCUIT",
            "ROBUST_CIRCUIT",
            "AUTOMATION_CANDIDATE",
            "CANON_PROMOTION",
            "AUTHORITY_PROMOTION",
        ],
        "canonEffect": "NONE",
        "authorityEffect": "NONE",
    }
    write_json(evidence_dir / "PR4_CLOSE_RECEIPT.json", receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
