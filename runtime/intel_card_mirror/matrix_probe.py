#!/usr/bin/env python3
"""Run one fresh environment probe for the Raven MIRROR runtime."""

from __future__ import annotations

import argparse
import json
import platform
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument(
        "--card",
        type=Path,
        default=Path("cards/FGE-CARD-RAVEN-001_v0.1.1.json"),
    )
    parser.add_argument("--environment-id", required=True)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    card_path = args.card.resolve()
    evidence_dir = args.evidence_dir.resolve()
    if evidence_dir.exists():
        shutil.rmtree(evidence_dir)
    evidence_dir.mkdir(parents=True, exist_ok=True)

    try:
        summary = runtime.execute_t01(repo_root, card_path, evidence_dir)
        receipt = load_json(evidence_dir / "receipt.json")
        output = load_json(evidence_dir / "mirror_output.json")
        proof = load_json(evidence_dir / f"{runtime.PROOF_OBJECT_ID}.json")
        status = "PASS" if summary.get("status") == "PASS" else "FAIL"
        signature = {
            "environmentId": args.environment_id,
            "status": status,
            "pythonVersion": platform.python_version(),
            "pythonImplementation": platform.python_implementation(),
            "platformSystem": platform.system(),
            "platformMachine": platform.machine(),
            "invariants": {
                "cardSha256": receipt["cardSha256"],
                "sourceSha256": receipt["sourceSha256"],
                "runtimeSha256": receipt["runtimeSha256"],
                "identityProjection": output["identityProjection"],
                "assertions": proof["assertions"],
                "validationScope": proof["validationScope"],
                "visualIdentityState": proof["visualIdentityState"],
            },
            "execution": {
                "invocationId": receipt["executorInvocationId"],
                "circuitState": proof["circuitState"],
                "evidenceStatus": receipt["evidenceStatus"],
            },
            "canonEffect": "NONE",
            "authorityEffect": "NONE",
        }
    except Exception as exc:
        signature = {
            "environmentId": args.environment_id,
            "status": "FAIL",
            "pythonVersion": platform.python_version(),
            "pythonImplementation": platform.python_implementation(),
            "platformSystem": platform.system(),
            "platformMachine": platform.machine(),
            "errorType": type(exc).__name__,
            "error": str(exc),
            "canonEffect": "NONE",
            "authorityEffect": "NONE",
        }

    write_json(evidence_dir / "matrix_signature.json", signature)
    print(json.dumps(signature, indent=2, sort_keys=True))
    return 0 if signature["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
