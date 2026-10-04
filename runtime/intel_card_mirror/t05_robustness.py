#!/usr/bin/env python3
"""T05 robustness slice for PR #4 Raven MIRROR runtime.

Tests:
- receipt tamper -> integrity refusal
- source mutation during execution -> proof refusal
- validator corruption -> integrity refusal
- missing evidence artifact -> integrity refusal

All destructive mutations occur only in evidence-local disposable copies.
Repository source, card, and registry are measured before and after.
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
        raise ValueError(f"Expected object in {path}")
    return value


def verify_copy(
    *,
    source_dir: Path,
    target_dir: Path,
    mutation,
    expected_gap: str,
    test_id: str,
) -> dict[str, Any]:
    if target_dir.exists():
        shutil.rmtree(target_dir)
    shutil.copytree(source_dir, target_dir)

    receipt_path = target_dir / "receipt.json"
    receipt = load_json(receipt_path)
    invocation_id = str(receipt["executorInvocationId"])

    mutation(target_dir, receipt)
    status, gaps = runtime.verify_receipt_integrity(
        receipt,
        target_dir,
        invocation_id,
    )
    passed = status == "FAIL" and expected_gap in gaps

    result = {
        "testId": test_id,
        "status": "PASS" if passed else "FAIL",
        "expectedOutcome": "REFUSE_EXECUTION_EVIDENCE",
        "verificationStatus": status,
        "expectedGap": expected_gap,
        "observedGaps": gaps,
        "canonEffect": "NONE",
        "authorityEffect": "NONE",
    }
    write_json(target_dir / f"{test_id}.summary.json", result)
    return result


def receipt_tamper(source_dir: Path, target_dir: Path) -> dict[str, Any]:
    def mutate(work_dir: Path, receipt: dict[str, Any]) -> None:
        receipt["artifacts"]["output"]["sha256"] = "0" * 64
        write_json(work_dir / "receipt.tampered.json", receipt)

    return verify_copy(
        source_dir=source_dir,
        target_dir=target_dir,
        mutation=mutate,
        expected_gap="output:DIGEST_MISMATCH",
        test_id="T05A_RECEIPT_TAMPER",
    )


def validator_corruption(source_dir: Path, target_dir: Path) -> dict[str, Any]:
    def mutate(work_dir: Path, receipt: dict[str, Any]) -> None:
        validator_path = work_dir / receipt["artifacts"]["validator"]["ref"]
        validator = load_json(validator_path)
        validator["status"] = "FAIL"
        validator.setdefault("corruptionTest", True)
        write_json(validator_path, validator)

    return verify_copy(
        source_dir=source_dir,
        target_dir=target_dir,
        mutation=mutate,
        expected_gap="validator:DIGEST_MISMATCH",
        test_id="T05C_VALIDATOR_CORRUPTION",
    )


def missing_artifact(source_dir: Path, target_dir: Path) -> dict[str, Any]:
    def mutate(work_dir: Path, receipt: dict[str, Any]) -> None:
        output_path = work_dir / receipt["artifacts"]["output"]["ref"]
        output_path.unlink()

    return verify_copy(
        source_dir=source_dir,
        target_dir=target_dir,
        mutation=mutate,
        expected_gap="output:FILE_MISSING",
        test_id="T05D_MISSING_EVIDENCE_ARTIFACT",
    )


def source_mutation(
    *,
    repo_root: Path,
    base_card_path: Path,
    evidence_dir: Path,
) -> dict[str, Any]:
    sandbox_root = evidence_dir / "sandbox_repo"
    sandbox_card = sandbox_root / "cards/FGE-CARD-RAVEN-001_v0.1.1.json"
    sandbox_card.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(repo_root / "registry.py", sandbox_root / "registry.py")
    shutil.copy2(repo_root / "book_raven.py", sandbox_root / "book_raven.py")
    shutil.copy2(base_card_path, sandbox_card)

    original_dispatch = runtime.dispatch_event
    mutation_marker = "\n# T05_SOURCE_MUTATION_DISPOSABLE_COPY\n"

    def mutating_dispatch(*args, **kwargs):
        output, dispatch = original_dispatch(*args, **kwargs)
        source_path = sandbox_root / "book_raven.py"
        source_path.write_text(
            source_path.read_text(encoding="utf-8") + mutation_marker,
            encoding="utf-8",
        )
        return output, dispatch

    runtime.dispatch_event = mutating_dispatch
    try:
        summary = runtime.execute_t01(
            sandbox_root,
            sandbox_card,
            evidence_dir / "execution",
        )
        observed_fault = None
    except runtime.RuntimeFault as fault:
        summary = {
            "status": "FAIL",
            "faultCode": fault.code,
            "message": fault.message,
            "circuitState": "OPEN",
            "assertions": {},
        }
        observed_fault = fault.code
    finally:
        runtime.dispatch_event = original_dispatch

    assertions = summary.get("assertions", {})
    a3_failed = assertions.get("A3_protected_authority_nonmutation") == "FAIL"
    refused = (
        summary.get("status") == "FAIL"
        and summary.get("circuitState") == "OPEN"
        and (a3_failed or observed_fault is not None)
    )

    result = {
        "testId": "T05B_SOURCE_MUTATION",
        "status": "PASS" if refused else "FAIL",
        "expectedOutcome": "PROOF_REFUSAL",
        "observedRuntimeStatus": summary.get("status"),
        "observedCircuitState": summary.get("circuitState"),
        "observedFaultCode": observed_fault,
        "assertions": assertions,
        "mutationLocation": "EVIDENCE_LOCAL_DISPOSABLE_REPO_COPY",
        "canonEffect": "NONE",
        "authorityEffect": "NONE",
    }
    write_json(evidence_dir / "T05B_SOURCE_MUTATION.summary.json", result)
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
        default=Path(".fge_evidence/T05_ROBUSTNESS"),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    card_path = args.card.resolve()
    evidence_dir = args.evidence_dir.resolve()
    if evidence_dir.exists():
        shutil.rmtree(evidence_dir)
    evidence_dir.mkdir(parents=True, exist_ok=True)

    authority_before = runtime.snapshot_authority_surface(repo_root, card_path)

    baseline_dir = evidence_dir / "T05_BASELINE"
    baseline = runtime.execute_t01(repo_root, card_path, baseline_dir)

    t05a = receipt_tamper(
        baseline_dir,
        evidence_dir / "T05A_RECEIPT_TAMPER",
    )
    t05b = source_mutation(
        repo_root=repo_root,
        base_card_path=card_path,
        evidence_dir=evidence_dir / "T05B_SOURCE_MUTATION",
    )
    t05c = validator_corruption(
        baseline_dir,
        evidence_dir / "T05C_VALIDATOR_CORRUPTION",
    )
    t05d = missing_artifact(
        baseline_dir,
        evidence_dir / "T05D_MISSING_EVIDENCE_ARTIFACT",
    )

    authority_after = runtime.snapshot_authority_surface(repo_root, card_path)
    repository_unchanged = authority_before == authority_after

    tests = {
        "T05_BASELINE": baseline.get("status"),
        "T05A_RECEIPT_TAMPER": t05a["status"],
        "T05B_SOURCE_MUTATION": t05b["status"],
        "T05C_VALIDATOR_CORRUPTION": t05c["status"],
        "T05D_MISSING_EVIDENCE_ARTIFACT": t05d["status"],
    }
    all_pass = (
        baseline.get("status") == "PASS"
        and all(value == "PASS" for key, value in tests.items() if key != "T05_BASELINE")
        and repository_unchanged
    )

    result = {
        "objectId": "FGE-RECEIPT-PR4-T05-ROBUSTNESS-001",
        "class": "CONTROLLED_CIRCUIT_ROBUSTNESS_RECEIPT",
        "status": "PASS" if all_pass else "FAIL",
        "tests": tests,
        "repositoryAuthoritySurfaceUnchanged": (
            "PASS" if repository_unchanged else "FAIL"
        ),
        "authorityDigestBefore": authority_before,
        "authorityDigestAfter": authority_after,
        "proofState": "REPEATED_CLOSURE",
        "eligibilityPending": [
            "REPRODUCIBLE_CIRCUIT",
            "ROBUST_CIRCUIT",
        ],
        "validationScope": "RUNTIME_ONLY",
        "visualIdentityState": "NOT_EVALUATED",
        "canonEffect": "NONE",
        "authorityEffect": "NONE",
    }
    write_json(evidence_dir / "T05_ROBUSTNESS.summary.json", result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
