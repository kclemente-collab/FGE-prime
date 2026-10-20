from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json

from mirror_vertical_slice import (
    EvidenceGatedReceiptEmitter,
    MirrorBoundaryError,
    MirrorExecutor,
    MirrorRequest,
    MirrorValidator,
    SourceEvidence,
)

CARD = "FGE-CARD-RAVEN-001@0.1.1"
SOURCE = SourceEvidence(
    subject="RAVEN VOSS",
    anchor_id="SB_330",
    character_id="FGE-CHAR-002",
    provenance="SB_330 VERIFIED CANON source binding",
    repository="kclemente-collab/FGE-prime",
    path="book_raven.py",
    source_commit="f594da7db811d4b66c1aad119a37877bc3a2c1df",
)


def request(**overrides):
    base = dict(card_id=CARD, operation="CARD.MIRROR", source_anchor="SB_330", source_character_id="FGE-CHAR-002")
    base.update(overrides)
    return MirrorRequest(**base)


def run_case(case_id: str, mode: str):
    executor, validator, emitter = MirrorExecutor(), MirrorValidator(), EvidenceGatedReceiptEmitter()
    req = request()
    source = SOURCE
    expected = "PASS"

    if mode == "bad_anchor":
        req = request(source_anchor="SB_999")
        expected = "BLOCKED"
    elif mode == "bad_character":
        req = request(source_character_id="FGE-CHAR-999")
        expected = "BLOCKED"
    elif mode == "bad_route":
        req = request(operation="CARD.BUILD")
        expected = "BLOCKED"

    try:
        output = executor.execute(req, source)
    except MirrorBoundaryError as exc:
        return {"case": case_id, "mode": mode, "expected": expected, "actual": "BLOCKED", "pass_receipt": False, "failure": str(exc)}

    if mode == "tamper_anchor":
        output = deepcopy(output); output["anchor_id"] = "SB_999"; expected = "FAIL"
    elif mode == "tamper_character":
        output = deepcopy(output); output["character_id"] = "FGE-CHAR-999"; expected = "FAIL"
    elif mode == "tamper_canon_effect":
        output = deepcopy(output); output["canon_effect"] = "MUTATE"; expected = "FAIL"
    elif mode == "tamper_authority_effect":
        output = deepcopy(output); output["authority_effect"] = "MUTATE"; expected = "FAIL"
    elif mode == "tamper_source_mutation":
        output = deepcopy(output); output["source_mutation"] = True; expected = "FAIL"
    elif mode == "tamper_subject":
        output = deepcopy(output); output["subject"] = "NOT RAVEN"; expected = "FAIL"

    validation = validator.validate(req, source, output)
    if validation["verdict"] != "PASS":
        try:
            emitter.emit("SHOULD-NOT-EXIST", case_id, req, source, output, validation, datetime.now(timezone.utc).isoformat())
            return {"case": case_id, "mode": mode, "expected": expected, "actual": "FAIL", "pass_receipt": True, "failure": "FAIL_OPEN"}
        except MirrorBoundaryError:
            return {"case": case_id, "mode": mode, "expected": expected, "actual": "FAIL", "pass_receipt": False}

    receipt = emitter.emit(f"FGE-PROOF-RAVEN-100X-{case_id}", case_id, req, source, output, validation, datetime.now(timezone.utc).isoformat())
    return {"case": case_id, "mode": mode, "expected": expected, "actual": receipt["status"], "pass_receipt": True}


def main():
    # 10-case adversarial suite repeated 10 times = 100 executions.
    modes = [
        "baseline",
        "bad_anchor",
        "bad_character",
        "bad_route",
        "tamper_anchor",
        "tamper_character",
        "tamper_canon_effect",
        "tamper_authority_effect",
        "tamper_source_mutation",
        "tamper_subject",
    ]
    results = []
    for cycle in range(1, 11):
        for index, mode in enumerate(modes, start=1):
            results.append(run_case(f"T100X-C{cycle:02d}-{index:02d}", mode))

    mismatches = [r for r in results if r["actual"] != r["expected"]]
    illegal_pass = [r for r in results if r["expected"] != "PASS" and r["pass_receipt"]]
    summary = {
        "object_id": "FGE-TEST-100X-RAVEN-MIRROR-001",
        "target": CARD,
        "executions": len(results),
        "expected_pass": sum(r["expected"] == "PASS" for r in results),
        "expected_fail": sum(r["expected"] == "FAIL" for r in results),
        "expected_blocked": sum(r["expected"] == "BLOCKED" for r in results),
        "mismatches": len(mismatches),
        "illegal_pass_receipts": len(illegal_pass),
        "mastery_gate": "PASS" if len(results) == 100 and not mismatches and not illegal_pass else "FAIL",
        "canon_effect": "NONE",
        "authority_effect": "NONE",
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    if summary["mastery_gate"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
