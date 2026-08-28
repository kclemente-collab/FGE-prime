import json
from pathlib import Path
import unittest

from systems.modular_fashion_os.adapter.character_os_adapter import compile_wardrobe_binding_candidate
from systems.modular_fashion_os.runtime.llm_display import compile_display_packet, propose_delta


FIXTURES = Path(__file__).resolve().parents[1] / "examples"


class ModularFashionOSSmokeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.asset = json.loads((FIXTURES / "EXAMPLE_NONCANON_fashion_asset.json").read_text())
        cls.character = json.loads((FIXTURES / "EXAMPLE_NONCANON_character_chip.json").read_text())

    def test_display_is_ephemeral(self):
        packet = compile_display_packet(self.asset, character_context=self.character)
        self.assertEqual(packet["authority"], "EPHEMERAL_DISPLAY_ONLY")
        self.assertEqual(packet["canon_effect"], "NONE")
        self.assertFalse(packet["governance"]["may_mutate_storage"])
        self.assertFalse(packet["governance"]["may_mutate_character_identity"])

    def test_delta_stays_proposed(self):
        packet = compile_display_packet(self.asset)
        propose_delta(packet, "garment.material.optical_intent.test", 1, "smoke test")
        delta = packet["proposed_deltas"][0]
        self.assertEqual(delta["status"], "PROPOSED")
        self.assertEqual(delta["canon_effect"], "NONE")

    def test_character_binding_uses_reference(self):
        candidate = compile_wardrobe_binding_candidate(
            self.character,
            self.asset,
            target_runtime="UNREAL_ENGINE_5",
        )
        self.assertIn(candidate["status"], {"READY_CANDIDATE", "NEEDS_VALIDATION"})
        self.assertEqual(candidate["binding"]["mode"], "REFERENCE_NOT_COPY")
        self.assertEqual(
            candidate["binding"]["wardrobe_asset_ref"],
            "FGE-FASH-EXAMPLE-COAT-001@0.1.0",
        )
        self.assertEqual(candidate["mutations_applied"], [])


if __name__ == "__main__":
    unittest.main()
