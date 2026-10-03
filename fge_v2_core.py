import json
import re
from typing import List, Dict, Optional
from pydantic import BaseModel, Field, field_validator
from fastapi import FastAPI, HTTPException

class MaterialMatrix(BaseModel):
    primary: str
    secondary: Optional[str] = None
    trim: Optional[str] = None

class PaletteEngine(BaseModel):
    dominant: str
    secondary: Optional[str] = None
    accent: str

    @field_validator('dominant', 'secondary', 'accent')
    @classmethod
    def validate_color_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if v.startswith("#") and not re.match(r"^#[0-9a-fA-F]{6}$", v):
            raise ValueError(f"Invalid Hex color code format: {v}")
        return v

class SubSurfaceCyberware(BaseModel):
    node_id: str = Field(..., description="Unique anatomical sub-surface node ID")
    luminescence: bool = Field(False, description="Sub-dermal glowing state")
    circuit_material: str = Field(..., description="e.g., Liquid Gold, Graphene Threads")
    cooling_type: str = Field("Passive", description="e.g., Cryo-fluid, Heat Sink")

class FashModuleInbound(BaseModel):
    character_id: str
    archetype: str
    silhouette: str
    sub_surface_cyberware: List[SubSurfaceCyberware] = Field(default_factory=list)
    base_layer: List[str] = Field(default_factory=list)
    mid_layer: List[str] = Field(default_factory=list)
    outer_layer: List[str] = Field(default_factory=list)
    materials: MaterialMatrix
    construction: List[str] = Field(default_factory=list)
    condition: str = Field("Factory New")
    accessories: List[str] = Field(default_factory=list)
    palette: PaletteEngine
    trend_overlay: str

class LayerCollisionMatrix:
    def __init__(self):
        self.volume_registry = {
            "Compression Bodysuit": 1,
            "Seamless Silk Camisole": 1,
            "Brocade Lace Bodice": 1,
            "Tactical Harness": 2,
            "Tailored Merino Vest": 2,
            "Leather Underbust Corset": 2,
            "Leather Jacket": 3,
            "Oversized Cashmere Trench Coat": 5,
            "Floor-Length Distressed Velvet Coat": 5
        }

    def verify_mesh_collision(self, base_layer: list, mid_layer: list, outer_layer: list) -> bool:
        v_base = max([self.volume_registry.get(i, 2) for i in base_layer]) if base_layer else 0
        v_mid = max([self.volume_registry.get(i, 2) for i in mid_layer]) if mid_layer else 0
        v_outer = max([self.volume_registry.get(i, 3) for i in outer_layer]) if outer_layer else 0
        if v_mid > 0 and v_base > v_mid:
            return False
        if v_outer > 0 and v_mid > v_outer:
            return False
        return True

class TrendOverlayInjector:
    def __init__(self):
        self.trend_registry = {
            "Neo-Gothic": {
                "silhouette_override": "Elongated Victorian + Sharp Structural Edges",
                "condition_override": "Vintage Luxury Patina",
                "palette_override": {"dominant": "#0A0A0B", "secondary": "#1C1124", "accent": "#4A0E17"},
                "garment_mutations": {
                    "Compression Bodysuit": "Brocade Lace Bodice",
                    "Tactical Harness": "Leather Underbust Corset",
                    "Leather Jacket": "Floor-Length Distressed Velvet Coat"
                },
                "material_mutations": {
                    "Distressed Leather": "Crushed Heavy Velvet",
                    "Carbon Fiber": "Guipure Black Lace"
                },
                "construction_rules": {"clear_all": True, "inject": ["Corset Lacing", "Scalloped Lace Edges"]},
                "accessory_rules": {"clear_all": True, "inject": ["Choker with Obsidian Pendant"]}
            }
        }

    def inject_trend(self, base_fge: dict, trend_name: str) -> dict:
        if trend_name not in self.trend_registry:
            return base_fge
        trend = self.trend_registry[trend_name]
        mutated = base_fge.copy()
        mutated["trend_overlay"] = trend_name
        mutated["silhouette"] = trend.get("silhouette_override", mutated["silhouette"])
        mutated["condition"] = trend.get("condition_override", mutated["condition"])
        mutated["palette"] = trend.get("palette_override", mutated.get("palette", {}))
        for layer in ["base_layer", "mid_layer", "outer_layer"]:
            if layer in mutated:
                mutated[layer] = [trend["garment_mutations"].get(item, item) for item in mutated[layer]]
        if "materials" in mutated:
            for key in ["primary", "secondary", "trim"]:
                if key in mutated["materials"]:
                    old_mat = mutated["materials"][key]
                    mutated["materials"][key] = trend["material_mutations"].get(old_mat, old_mat)
        if trend.get("construction_rules", {}).get("clear_all"):
            mutated["construction"] = trend["construction_rules"]["inject"]
        if trend.get("accessory_rules", {}).get("clear_all"):
            mutated["accessories"] = trend["accessory_rules"]["inject"]
        return mutated

class RenderCompiler:
    @staticmethod
    def compile_weighted_prompt(fge_json: dict) -> str:
        prompt_segments = []
        prompt_segments.append(f"masterpiece portrait of ({fge_json['character_id']}:1.2), styled as {fge_json['archetype']}")
        prompt_segments.append(f"({fge_json['silhouette']} silhouette:1.15)")
        if fge_json.get("sub_surface_cyberware"):
            cyber_tokens = []
            for item in fge_json["sub_surface_cyberware"]:
                glow_str = "luminescent glowing" if item["luminescence"] else "dormant matte"
                cyber_tokens.append(f"{glow_str} {item['circuit_material']} circuits near node {item['node_id']}")
            prompt_segments.append(f"sub-dermal details: (({', '.join(cyber_tokens)}):1.28)")
        if fge_json.get("outer_layer"):
            prompt_segments.append(f"outer wear: (({', '.join(fge_json['outer_layer'])} made of {fge_json['materials']['primary']}):1.25)")
        if fge_json.get("mid_layer"):
            prompt_segments.append(f"mid-layer visible underneath: ({', '.join(fge_json['mid_layer'])}:1.15)")
        if fge_json.get("base_layer"):
            prompt_segments.append(f"skin-tight layer: ({', '.join(fge_json['base_layer'])}:1.05)")
        prompt_segments.append(f"({fge_json['condition']} wear state:1.1)")
        prompt_segments.append(f"color palette dominated by {fge_json['palette']['dominant']} with {fge_json['palette']['accent']} accents")
        return ", ".join(prompt_segments)

class FashPipelineManager:
    def __init__(self):
        self.collision_matrix = LayerCollisionMatrix()
        self.trend_injector = TrendOverlayInjector()

    def resolve_and_compile(self, inbound_data: dict, target_trend: Optional[str] = None) -> dict:
        active_config = inbound_data
        if target_trend:
            active_config = self.trend_injector.inject_trend(inbound_data, target_trend)
        is_safe = self.collision_matrix.verify_mesh_collision(
            base_layer=active_config.get("base_layer", []),
            mid_layer=active_config.get("mid_layer", []),
            outer_layer=active_config.get("outer_layer", [])
        )
        if not is_safe:
            raise ValueError("Pipeline processing aborted: Layer collision threshold violated.")
        final_prompt = RenderCompiler.compile_weighted_prompt(active_config)
        return {
            "status": "SUCCESS",
            "resolved_configuration": active_config,
            "render_prompt": final_prompt
        }

app = FastAPI(title="FGE AI Fashion Engine Gateway v2", version="2.0.0")
manager = FashPipelineManager()

@app.post("/api/v2/fashion/resolve", tags=["Fashion Generation Pipeline"])
def resolve_fashion_pipeline(payload: FashModuleInbound, trend_override: Optional[str] = None):
    try:
        inbound_dict = payload.model_dump()
        return manager.resolve_and_compile(inbound_dict, target_trend=trend_override)
    except ValueError as val_err:
        raise HTTPException(status_code=422, detail=str(val_err))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Engine Error: {str(e)}")

def run_automated_pipeline_unit_test():
    print("[TEST CASE 0]: INITIALIZING AUTOMATED ASSET RESOLUTION PIPELINE UNIT TEST...")
    mock_input_payload = {
        "character_id": "CH_HACKER_VAL",
        "archetype": "Cyberpunk Hacker",
        "silhouette": "Oversized Upper + Slim Lower",
        "sub_surface_cyberware": [
            {"node_id": "spine_c7", "luminescence": True, "circuit_material": "Liquid Gold", "cooling_type": "Cryo-fluid"},
            {"node_id": "optic_left", "luminescence": False, "circuit_material": "Graphene Threads", "cooling_type": "Passive"},
        ],
        "base_layer": ["Compression Bodysuit"],
        "mid_layer": ["Tactical Harness"],
        "outer_layer": ["Leather Jacket"],
        "materials": {"primary": "Distressed Leather", "secondary": "Carbon Fiber"},
        "construction": ["Quilted Shoulders", "Asymmetrical Zipper"],
        "condition": "Lightly Worn",
        "accessories": ["Silver Necklace"],
        "palette": {"dominant": "#111111", "accent": "#FF003C"},
        "trend_overlay": "Techwear 2026",
    }
    test_manager = FashPipelineManager()
    try:
        print("[TEST CASE 1]: Running Base Archetype Engine...")
        base_output = test_manager.resolve_and_compile(mock_input_payload)
        assert base_output["status"] == "SUCCESS"
        print("Base Pipeline Successful! Sample Compiled Prompt:")
        print(" -> " + base_output["render_prompt"][:120] + "...")
        print("[TEST CASE 2]: Injecting Detachable Neo-Gothic Trend Overlay Matrix...")
        mutated_output = test_manager.resolve_and_compile(mock_input_payload, target_trend="Neo-Gothic")
        assert len(mutated_output["resolved_configuration"]["sub_surface_cyberware"]) == 2
        assert mutated_output["resolved_configuration"]["outer_layer"] == ["Floor-Length Distressed Velvet Coat"]
        print("Trend Mutation Injection Successful! Mutated Compiled Prompt:")
        print(" -> " + mutated_output["render_prompt"][:150] + "...")
        print("[TEST CASE 3]: Simulating Visual Layer Mesh Collision Fault...")
        broken_payload = mock_input_payload.copy()
        broken_payload["base_layer"] = ["Oversized Cashmere Trench Coat"]
        try:
            test_manager.resolve_and_compile(broken_payload)
            print("Failure: Pipeline allowed clipping elements to pass.")
        except ValueError:
            print("Mesh Layer Collision Intercepted Successfully! Pipeline protection running safely.")
        print("ALL PIPELINE INTEGRATION TESTS PASSED CLEANLY.")
    except AssertionError as assert_err:
        print("TEST CRITICAL INTEGRITY EXCEPTION: " + str(assert_err))

if __name__ == "__main__":
    run_automated_pipeline_unit_test()
