import copy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator

from systems.modular_fashion_os.runtime.benchmark import evaluate_ue5_benchmark
from systems.modular_fashion_os.validation import validate_envelope


ROOT = Path(__file__).resolve().parents[1]


class ContractAndBenchmarkTest(unittest.TestCase):
    def test_all_six_payload_schemas_are_valid(self):
        names = {
            "storage_module.json",
            "display_module.json",
            "adapter_module.json",
            "clipping_occlusion_engine.json",
            "fabric_description_index.json",
            "runtime_customization_parameters.json",
        }
        payload_dir = ROOT / "schema" / "payloads"
        self.assertEqual({path.name for path in payload_dir.glob("*.json")}, names)
        for name in names:
            schema = json.loads((payload_dir / name).read_text())
            Draft202012Validator.check_schema(schema)

    def test_fixture_matches_envelope_contract(self):
        asset = json.loads(
            (ROOT / "examples" / "EXAMPLE_NONCANON_fashion_asset.json").read_text()
        )
        validate_envelope(asset)

    def test_unmeasured_performance_claim_is_suppressed(self):
        evidence = json.loads(
            (ROOT / "benchmarks" / "ue5_occlusion_benchmark.json").read_text()
        )
        result = evaluate_ue5_benchmark(evidence)
        self.assertFalse(result["claim_publishable"])
        self.assertEqual(result["status"], "SUPPRESSED_PENDING_MEASUREMENT")

    def test_verified_measurement_computes_observed_reduction(self):
        evidence = {
            "evidence_status": "VERIFIED_UE5_RUN",
            "run_id": "UE5-RUN-001",
            "ue5_version": "5.x",
            "hardware_profile": "TEST-RIG",
            "sample_count": 600,
            "baseline_gpu_frame_ms": 10.0,
            "occlusion_gpu_frame_ms": 7.5,
        }
        result = evaluate_ue5_benchmark(evidence)
        self.assertTrue(result["claim_publishable"])
        self.assertEqual(result["measured_reduction_percent"], 25.0)


if __name__ == "__main__":
    unittest.main()
