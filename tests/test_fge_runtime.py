"""FGE public runtime contract tests: read-only, fail-closed."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runtime" / "motherboard"))
from preflight import validate  # noqa: E402


class RuntimeTests(unittest.TestCase):
    def test_contract_structure(self):
        r = validate()
        self.assertEqual(r["structural_result"], "PASS")
        self.assertEqual(r["passed"], r["total"])

    def test_release_stays_on_hold(self):
        r = validate()
        self.assertEqual(r["release_gate"], "HOLD")
        self.assertEqual(r["runtime_attestation"], "NOT_PROVEN")

    def test_no_side_effects(self):
        r = validate()
        self.assertFalse(r["canon_write"])
        self.assertEqual(r["external_dispatches"], 0)

    def test_source_proof_not_inferred(self):
        r = validate()
        self.assertEqual(r["nrcpt"], "SOURCE_BYTES_AND_LIVE_EXECUTION_NOT_ATTESTED")


if __name__ == "__main__":
    unittest.main()
