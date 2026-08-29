import copy
import json
from pathlib import Path
import unittest

from systems.modular_fashion_os.adapter.character_os_adapter import (
    authorize_binding,
    compile_wardrobe_binding_candidate,
)
from systems.modular_fashion_os.runtime.customization import hex_to_vector3
from systems.modular_fashion_os.runtime.fde import (
    FabricDescriptionIndex,
    compile_fde_output,
)
from systems.modular_fashion_os.runtime.llm_display import (
    compile_display_packet,
    propose_delta,
)
from systems.modular_fashion_os.validation import ContractValidationError


FIXTURES = Path(__file__).resolve().parents[1] / "examples"
FDE_RECORD = {
    "global_fabric_id": "fab_lthr_nappa_01",
    "localization_manifest": {
        "display_name_en": "Premium Heavy Nappa Leather",
        "tactile_description": "Dense structured leather.",
    },
    "display_ui_anchors": {
        "icon_thumbnail_uri": "s3://ui/nappa.png",
        "sound_profile_on_movement": "sfx_leather_low",
    },
    "viewport_rendering_overrides": {
        "use_raytracing_anisotropy": True,
    },
}


class ModularFashionOSRuntimeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.asset = json.loads(
            (FIXTURES / "EXAMPLE_NONCANON_fashion_asset.json").read_text()
        )
        cls.character = json.loads(
            (FIXTURES / "EXAMPLE_NONCANON_character_chip.json").read_text()
        )
        cls.fde = FabricDescriptionIndex([FDE_RECORD])

    def ready_asset(self):
        asset = copy.deepcopy(self.asset)
        asset["validation"]["state"] = "PASSED"
        asset["validation"]["unknowns"] = []
        adapter = asset["representations"]["adapters"][0]
        adapter["runtime_status"] = "LIVE"
        adapter["live_runtime"] = True
        return asset

    def test_display_is_ephemeral_and_fde_compiles(self):
        packet = compile_display_packet(
            self.asset,
            character_context=self.character,
            fabric_index=self.fde,
        )
        self.assertEqual(packet["authority"], "EPHEMERAL_DISPLAY_ONLY")
        self.assertEqual(packet["canon_effect"], "NONE")
        self.assertEqual(packet["fabric_description"]["status"], "COMPILED")
        self.assertIn(
            "display_ui_anchors", packet["fabric_description"]["ui"]
        )
        self.assertFalse(packet["governance"]["may_mutate_storage"])

    def test_display_packet_detaches_all_mutable_source_data(self):
        asset = copy.deepcopy(self.asset)
        character = copy.deepcopy(self.character)
        packet = compile_display_packet(
            asset,
            character_context=character,
            fabric_index=self.fde,
        )

        packet["fit"]["rig_compatibility"].append("MUTATED")
        packet["representations"]["adapters"][0]["target"] = "MUTATED"
        packet["validation"]["gates"]["RIGHTS"] = "MUTATED"
        packet["character_context"]["wardrobe_authority"]["status"] = "MUTATED"
        packet["fabric_description"]["ui"]["display_ui_anchors"][
            "icon_thumbnail_uri"
        ] = "MUTATED"

        self.assertNotIn("MUTATED", asset["garment"]["fit"]["rig_compatibility"])
        self.assertEqual(
            asset["representations"]["adapters"][0]["target"],
            "UNREAL_ENGINE_5",
        )
        self.assertEqual(asset["validation"]["gates"]["RIGHTS"], "PASSED")
        self.assertEqual(character["wardrobe_authority"]["status"], "AUTHORIZED")
        self.assertEqual(
            self.fde.lookup("fab_lthr_nappa_01")["display_ui_anchors"][
                "icon_thumbnail_uri"
            ],
            "s3://ui/nappa.png",
        )

    def test_delta_stays_proposed(self):
        packet = compile_display_packet(self.asset)
        propose_delta(packet, "garment.material.optical_intent.test", 1, "test")
        delta = packet["proposed_deltas"][0]
        self.assertEqual(delta["status"], "PROPOSED")
        self.assertEqual(delta["canon_effect"], "NONE")

    def test_fde_unknown_fabric_is_preserved(self):
        asset = copy.deepcopy(self.asset)
        asset["garment"]["material"]["fabric_id"] = "missing"
        output = compile_fde_output(asset, self.fde)
        self.assertEqual(output["status"], "UNKNOWN_FABRIC")

    def test_hex_to_vector3(self):
        self.assertEqual(hex_to_vector3("#FF8000"), [1.0, 0.501961, 0.0])

    def test_rgba_pattern_and_uv_compile_under_rights(self):
        asset = copy.deepcopy(self.asset)
        customization = asset["garment"]["customization"]
        customization["enabled"] = True
        customization["rgba_control_texture_uri"] = "s3://maps/nappa-control.png"
        customization["color_tints"] = [
            {
                "channel": "R",
                "semantic": "PRIMARY_TEXTILE",
                "default_hex": "#1A1A1A",
                "runtime_override_allowed": True,
            }
        ]
        customization["pattern_overlays"] = [
            {
                "pattern_id": "pattern_monogram_gold_04",
                "tiling_frequency": [4.0, 4.0],
                "uv_channel_index": 1,
                "offset_speed": [0.0, 0.0],
                "blend_mode": "LERP_SUBSTRATE_SLAB_ROUGHNESS",
            }
        ]
        output = compile_fde_output(asset, self.fde)
        runtime = output["runtime_customization"]
        self.assertEqual(runtime["status"], "COMPILED")
        self.assertEqual(runtime["vector_tints"][0]["vector3"], [0.101961] * 3)
        self.assertEqual(runtime["pattern_overlays"][0]["uv_channel_index"], 1)

    def test_customization_rights_denial_blocks_display_output(self):
        asset = copy.deepcopy(self.asset)
        customization = asset["garment"]["customization"]
        customization["enabled"] = True
        customization["color_tints"] = [
            {
                "channel": "R",
                "semantic": "PRIMARY_TEXTILE",
                "default_hex": "#000000",
                "runtime_override_allowed": True,
            }
        ]
        asset["rights"]["modification_operations"]["color_tint"] = False
        output = compile_fde_output(asset, self.fde)
        self.assertEqual(output["status"], "BLOCKED")
        self.assertIn(
            "RIGHTS_DENY_COLOR_TINT:R",
            output["runtime_customization"]["violations"],
        )

    def test_live_adapter_is_required(self):
        candidate = compile_wardrobe_binding_candidate(
            self.character,
            self.asset,
            target_runtime="UNREAL_ENGINE_5",
            require_live_adapter=True,
        )
        self.assertEqual(candidate["status"], "BLOCKED")
        self.assertIn(
            "PLATFORM_ADAPTER_NOT_LIVE", candidate["compatibility"]["blockers"]
        )

    def test_unsupported_runtime_blocks_when_live_adapter_required(self):
        asset = self.ready_asset()
        asset["rights"]["platform_authorizations"].append(
            {
                "target": "WEBXR",
                "status": "AUTHORIZED",
                "license_id": "FGE-LICENSE-TEST-ONLY-001",
                "expires_at": None,
            }
        )
        candidate = compile_wardrobe_binding_candidate(
            self.character,
            asset,
            target_runtime="WEBXR",
            require_live_adapter=True,
        )
        self.assertEqual(candidate["status"], "BLOCKED")
        self.assertIn(
            "NO_EXACT_PLATFORM_ADAPTER", candidate["compatibility"]["blockers"]
        )

    def test_target_adapter_must_match_character_rig(self):
        asset = self.ready_asset()
        asset["representations"]["adapters"][0]["rig_profile"] = "OTHER_RIG"
        candidate = compile_wardrobe_binding_candidate(
            self.character,
            asset,
            target_runtime="UNREAL_ENGINE_5",
            require_live_adapter=True,
        )
        self.assertEqual(candidate["status"], "BLOCKED")
        self.assertIsNone(candidate["selected_adapter"])
        self.assertIn(
            "NO_RIG_COMPATIBLE_PLATFORM_ADAPTER",
            candidate["compatibility"]["blockers"],
        )

    def test_live_compatible_adapter_wins_over_earlier_wrong_rig(self):
        asset = self.ready_asset()
        compatible = copy.deepcopy(asset["representations"]["adapters"][0])
        compatible["adapter_id"] = "ADAPTER-COMPATIBLE-LIVE"
        asset["representations"]["adapters"][0]["rig_profile"] = "OTHER_RIG"
        asset["representations"]["adapters"].append(compatible)
        candidate = compile_wardrobe_binding_candidate(
            self.character,
            asset,
            target_runtime="UNREAL_ENGINE_5",
            require_live_adapter=True,
        )
        self.assertEqual(candidate["status"], "READY_CANDIDATE")
        self.assertEqual(
            candidate["selected_adapter"]["adapter_id"],
            "ADAPTER-COMPATIBLE-LIVE",
        )

    def test_ready_binding_uses_reference_and_compiles_execution_plan(self):
        candidate = compile_wardrobe_binding_candidate(
            self.character,
            self.ready_asset(),
            target_runtime="UNREAL_ENGINE_5",
        )
        self.assertEqual(candidate["status"], "READY_CANDIDATE")
        self.assertEqual(candidate["binding"]["mode"], "REFERENCE_NOT_COPY")
        self.assertEqual(
            candidate["binding"]["wardrobe_asset_ref"],
            "FGE-FASH-EXAMPLE-COAT-001@0.1.0",
        )
        payload = candidate["executable_adapter_payload"]
        self.assertEqual(payload["status"], "EXECUTION_PLAN_CANDIDATE")
        self.assertEqual(
            payload["clipping_occlusion_engine"]["alpha_mask_registry"][
                "lower_assets_to_mask"
            ],
            ["FGE-FASH-EXAMPLE-BASE-001@0.1.0"],
        )

    def test_rights_gate_blocks_ready_candidate(self):
        asset = self.ready_asset()
        asset["validation"]["gates"]["RIGHTS"] = "UNKNOWN"
        candidate = compile_wardrobe_binding_candidate(
            self.character, asset, target_runtime="UNREAL_ENGINE_5"
        )
        self.assertEqual(candidate["status"], "BLOCKED")
        self.assertIn("RIGHTS_GATE_NOT_PASSED", candidate["compatibility"]["blockers"])

    def test_body_profile_mismatch_is_compared(self):
        asset = self.ready_asset()
        asset["garment"]["fit"]["source_body_profile"] = "OTHER_BODY"
        asset["garment"]["fit"]["morph_strategy"] = None
        candidate = compile_wardrobe_binding_candidate(
            self.character, asset, target_runtime="UNREAL_ENGINE_5"
        )
        self.assertIn("BODY_PROFILE_INCOMPATIBLE", candidate["compatibility"]["blockers"])

    def test_active_layer_collision_blocks(self):
        character = copy.deepcopy(self.character)
        character["active_wardrobe"][0]["layer_priority"] = 60
        candidate = compile_wardrobe_binding_candidate(
            character, self.ready_asset(), target_runtime="UNREAL_ENGINE_5"
        )
        self.assertTrue(
            any(
                item.startswith("LAYER_PRIORITY_COLLISION:")
                for item in candidate["compatibility"]["blockers"]
            )
        )

    def test_legacy_character_shape_is_rejected(self):
        with self.assertRaises(ContractValidationError):
            compile_wardrobe_binding_candidate(
                {"character_id": "legacy"},
                self.asset,
                target_runtime="UNREAL_ENGINE_5",
            )

    def test_adapter_cannot_authorize(self):
        with self.assertRaises(PermissionError):
            authorize_binding({})


if __name__ == "__main__":
    unittest.main()
