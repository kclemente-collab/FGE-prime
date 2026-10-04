#!/usr/bin/env python3
"""Aggregate T05 robustness + environment matrix into eligibility evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


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


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--download-root", type=Path, required=True)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    parser.add_argument("--expected-count", type=int, default=9)
    args = parser.parse_args()

    root = args.download_root.resolve()
    evidence_dir = args.evidence_dir.resolve()
    evidence_dir.mkdir(parents=True, exist_ok=True)

    signature_paths = sorted(root.glob("**/matrix_signature.json"))
    signatures = [load_json(path) for path in signature_paths]

    robustness_paths = sorted(root.glob("**/T05_ROBUSTNESS.summary.json"))
    robustness = (
        load_json(robustness_paths[0])
        if len(robustness_paths) == 1
        else None
    )

    environment_ids = {str(item.get("environmentId")) for item in signatures}
    python_versions = {str(item.get("pythonVersion")) for item in signatures}
    platforms = {str(item.get("platformSystem")) for item in signatures}

    invariant_fields = (
        "cardSha256",
        "sourceSha256",
        "runtimeSha256",
        "identityProjection",
        "assertions",
        "validationScope",
        "visualIdentityState",
    )
    invariant_checks: dict[str, bool] = {}
    for field in invariant_fields:
        values = {
            canonical(item.get("invariants", {}).get(field))
            for item in signatures
            if item.get("status") == "PASS"
        }
        invariant_checks[field] = len(values) == 1 and len(signatures) > 0

    matrix_checks = {
        "expected_environment_count": len(signatures) == args.expected_count,
        "unique_environment_ids": len(environment_ids) == args.expected_count,
        "all_environment_runs_pass": all(
            item.get("status") == "PASS" for item in signatures
        ),
        "three_or_more_python_versions": len(python_versions) >= 3,
        "three_or_more_platforms": len(platforms) >= 3,
        **{
            f"invariant_{field}": passed
            for field, passed in invariant_checks.items()
        },
    }
    matrix_pass = all(matrix_checks.values())
    robustness_pass = (
        robustness is not None
        and robustness.get("status") == "PASS"
        and robustness.get("repositoryAuthoritySurfaceUnchanged") == "PASS"
    )

    reproducible_eligible = matrix_pass
    robust_eligible = matrix_pass and robustness_pass
    all_pass = reproducible_eligible and robust_eligible

    comparison = {
        "objectId": "FGE-RECEIPT-PR4-T05-MATRIX-001",
        "class": "RUNTIME_ENVIRONMENT_MATRIX_RECEIPT",
        "status": "PASS" if matrix_pass else "FAIL",
        "expectedEnvironmentCount": args.expected_count,
        "observedEnvironmentCount": len(signatures),
        "pythonVersions": sorted(python_versions),
        "platforms": sorted(platforms),
        "environmentIds": sorted(environment_ids),
        "checks": {
            key: "PASS" if value else "FAIL"
            for key, value in matrix_checks.items()
        },
        "signatures": signatures,
        "canonEffect": "NONE",
        "authorityEffect": "NONE",
    }
    write_json(
        evidence_dir / "T05_MATRIX_COMPARISON.summary.json",
        comparison,
    )

    final = {
        "objectId": "FGE-RECEIPT-PR4-T05-PROOF-001",
        "class": "CONTROLLED_CIRCUIT_T05_PROOF_RECEIPT",
        "status": "PASS" if all_pass else "FAIL",
        "proofState": "REPEATED_CLOSURE",
        "eligibility": {
            "REPRODUCIBLE_CIRCUIT": (
                "PASS" if reproducible_eligible else "FAIL"
            ),
            "ROBUST_CIRCUIT": (
                "PASS" if robust_eligible else "FAIL"
            ),
        },
        "promotionEffect": "NONE",
        "robustnessReceiptFound": robustness is not None,
        "robustnessStatus": (
            robustness.get("status") if robustness is not None else "MISSING"
        ),
        "matrixStatus": comparison["status"],
        "validationScope": "RUNTIME_ONLY",
        "visualIdentityState": "NOT_EVALUATED",
        "explicitNonClaims": [
            "AUTOMATION_CANDIDATE",
            "VISUAL_IDENTITY_VALIDATED",
            "CANON_PROMOTION",
            "AUTHORITY_PROMOTION",
            "EXHAUSTIVE_SYSTEM_ROBUSTNESS",
            "REPOSITORY_WIDE_CI_HEALTH",
        ],
        "canonEffect": "NONE",
        "authorityEffect": "NONE",
    }
    write_json(evidence_dir / "T05_PROOF_RECEIPT.json", final)
    print(json.dumps(final, indent=2, sort_keys=True))
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
