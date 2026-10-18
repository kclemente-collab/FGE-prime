"""FGE 100X: bounded, deterministic mock validation; no production writes."""
import datetime as dt
import hashlib
import json
import pathlib
import statistics
import time
import unittest

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "results"
ENGINE = "FGE-100X-CORE-001"
VERSION = "1.2.1"
CASES = 100

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def validate(manifest):
    required = ("object_id", "version", "authority", "source_refs", "operation", "target", "payload")
    if any(not manifest.get(k) for k in required):
        return "REJECT_MISSING_FIELD"
    if manifest.get("canon_mutation") or manifest.get("identity_mutation"):
        return "REJECT_MUTATION"
    if manifest["operation"] != "MOCK_RENDER" or manifest["target"] != "MOCK_ONLY":
        return "REJECT_UNAUTHORIZED_OPERATION"
    if not isinstance(manifest["source_refs"], list) or not all(isinstance(x, str) and x for x in manifest["source_refs"]):
        return "REJECT_SOURCE_REFS"
    return "MOCK_PASS"

BASE = {"object_id": "FGE-MOCK-001", "version": "0.1.0", "authority": "TEST_ONLY",
        "source_refs": ["MOCK-SOURCE-001"], "operation": "MOCK_RENDER",
        "target": "MOCK_ONLY", "payload": {"scene": "synthetic"}}

class ContractTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(validate(BASE), "MOCK_PASS")
    def test_missing_authority(self):
        self.assertEqual(validate({**BASE, "authority": None}), "REJECT_MISSING_FIELD")
    def test_canon_mutation(self):
        self.assertEqual(validate({**BASE, "canon_mutation": True}), "REJECT_MUTATION")
    def test_identity_mutation(self):
        self.assertEqual(validate({**BASE, "identity_mutation": True}), "REJECT_MUTATION")
    def test_real_operation_rejected(self):
        self.assertEqual(validate({**BASE, "operation": "RENDER"}), "REJECT_UNAUTHORIZED_OPERATION")
    def test_real_target_rejected(self):
        self.assertEqual(validate({**BASE, "target": "PRODUCTION"}), "REJECT_UNAUTHORIZED_OPERATION")
    def test_empty_refs_rejected(self):
        self.assertEqual(validate({**BASE, "source_refs": []}), "REJECT_MISSING_FIELD")

def main():
    OUT.mkdir(exist_ok=True)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ContractTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    previous = "GENESIS"
    durations = []
    events = []
    for i in range(CASES):
        item = dict(BASE)
        item["object_id"] = "FGE-MOCK-%03d" % i
        if i % 5 == 1:
            item["authority"] = None
        elif i % 5 == 2:
            item["canon_mutation"] = True
        elif i % 5 == 3:
            item["operation"] = "PRODUCTION_RENDER"
        elif i % 5 == 4:
            item["source_refs"] = []
        start = time.perf_counter_ns()
        actual = validate(item)
        duration_ns = time.perf_counter_ns() - start
        expected = ["MOCK_PASS", "REJECT_MISSING_FIELD", "REJECT_MUTATION",
                    "REJECT_UNAUTHORIZED_OPERATION", "REJECT_MISSING_FIELD"][i % 5]
        event = {"case": i, "input_sha256": digest(item), "expected": expected,
                 "actual": actual, "passed": actual == expected, "duration_ns": duration_ns,
                 "previous_hash": previous}
        event["entry_hash"] = digest(event)
        previous = event["entry_hash"]
        events.append(event)
        durations.append(duration_ns)
    ledger = OUT / "ledger.jsonl"
    ledger.write_text("".join(json.dumps(x, sort_keys=True) + "\n" for x in events))
    receipt = {
        "engine": ENGINE, "version": VERSION,
        "utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "cases": CASES, "passed": sum(x["passed"] for x in events),
        "failed": sum(not x["passed"] for x in events),
        "unit_tests": result.testsRun, "unit_test_failures": len(result.failures) + len(result.errors),
        "mean_case_ns": statistics.mean(durations),
        "median_case_ns": statistics.median(durations),
        "ledger_tip_sha256": previous,
        "scope": "synthetic mock validation only",
        "production_adapters": "NOT_CONNECTED",
        "drive_receipt_archival": "NOT_CONNECTED",
        "mastery_claim": "NOT_ESTABLISHED",
        "canon_effect": "NONE",
        "authority_effect": "NONE"
    }
    (OUT / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))
    return 0 if result.wasSuccessful() and receipt["failed"] == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
