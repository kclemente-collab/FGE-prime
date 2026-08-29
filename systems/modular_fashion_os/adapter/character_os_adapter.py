"""Governed Character OS projection and executable fashion adapter compiler."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple

from systems.modular_fashion_os.validation import (
    PACKAGE_ROOT,
    validate_character_projection,
    validate_envelope,
    validate_json_contract,
)


UNKNOWN = "UNKNOWN"
REQUIRED_LIVE_CAPABILITIES = {
    "RIG_BIND",
    "MATERIAL_TRANSLATION",
    "PHYSICS_TRANSLATION",
    "CLIPPING_OCCLUSION",
}


def _list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


def _choose_target_adapter(
    adapters: List[Dict[str, Any]], target_runtime: str
) -> Optional[Dict[str, Any]]:
    target_norm = target_runtime.strip().lower()
    for adapter in adapters:
        if str(adapter.get("target", "")).strip().lower() == target_norm:
            return deepcopy(adapter)
    return None


def _policy_check(
    character: Dict[str, Any], fashion: Dict[str, Any]
) -> Tuple[List[str], List[str]]:
    blockers: List[str] = []
    warnings: List[str] = []
    policy = character["wardrobe_authority"]
    identity = fashion["identity"]
    layering = fashion["garment"]["layering"]
    if policy["status"] not in ("AUTHORIZED", "LOCKED"):
        blockers.append("CHARACTER_WARDROBE_AUTHORITY_NOT_ACTIVE")
    if identity["asset_id"] in policy["forbidden_asset_ids"]:
        blockers.append("WARDROBE_POLICY_FORBIDS_ASSET_ID")
    if identity["asset_class"] not in policy["allowed_asset_classes"]:
        blockers.append("WARDROBE_POLICY_ASSET_CLASS_NOT_ALLOWED")
    if layering["layer_priority"] > policy["max_layer_priority"]:
        blockers.append("WARDROBE_POLICY_LAYER_PRIORITY_EXCEEDED")
    return blockers, warnings


def _fit_check(
    character: Dict[str, Any], fashion: Dict[str, Any]
) -> Tuple[List[str], List[str]]:
    blockers: List[str] = []
    warnings: List[str] = []
    embodiment = character["embodiment"]
    fit = fashion["garment"]["fit"]
    garment_rigs = [str(value) for value in _list(fit.get("rig_compatibility"))]
    if embodiment["rig_profile_id"] not in garment_rigs:
        blockers.append("RIG_PROFILE_INCOMPATIBLE")
    source_body = fit.get("source_body_profile")
    if source_body != embodiment["body_profile_id"]:
        if fit.get("morph_strategy") and fit.get("fit_tolerance_mm") is not None:
            warnings.append("BODY_PROFILE_MORPH_VALIDATION_REQUIRED")
        else:
            blockers.append("BODY_PROFILE_INCOMPATIBLE")
    return blockers, warnings


def _rights_check(
    fashion: Dict[str, Any], target_runtime: str
) -> Tuple[List[str], List[str], Dict[str, Any]]:
    blockers: List[str] = []
    warnings: List[str] = []
    validation = fashion["validation"]
    rights = fashion["rights"]
    rights_gate = (validation.get("gates") or {}).get("RIGHTS", "UNKNOWN")
    if rights_gate != "PASSED":
        blockers.append("RIGHTS_GATE_NOT_PASSED")
    authorization = next(
        (
            item
            for item in rights["platform_authorizations"]
            if str(item["target"]).lower() == target_runtime.lower()
        ),
        None,
    )
    platform_authorized = bool(
        authorization and authorization.get("status") == "AUTHORIZED"
    )
    if target_runtime != "LLM_GENERIC" and not platform_authorized:
        blockers.append("PLATFORM_RIGHTS_NOT_AUTHORIZED")
    return blockers, warnings, {
        "gate": rights_gate,
        "platform_authorized": platform_authorized,
        "authorization": deepcopy(authorization),
        "license_id": rights["license_id"],
    }


def _covered_zones(coverage: Dict[str, str]) -> set[str]:
    return {
        zone
        for zone, state in coverage.items()
        if state in ("COVER", "PARTIAL")
    }


def _layer_stack_check(
    character: Dict[str, Any], fashion: Dict[str, Any]
) -> Tuple[List[str], List[str], List[str]]:
    blockers: List[str] = []
    warnings: List[str] = []
    lower_assets_to_mask: List[str] = []
    candidate = fashion["garment"]["layering"]
    candidate_zones = _covered_zones(fashion["garment"]["coverage"])
    for active in character["active_wardrobe"]:
        overlap = candidate_zones & _covered_zones(active["coverage"])
        if not overlap:
            continue
        active_priority = active["layer_priority"]
        if active_priority == candidate["layer_priority"]:
            blockers.append(f"LAYER_PRIORITY_COLLISION:{active['asset_ref']}")
        elif active_priority < candidate["layer_priority"]:
            if active["layer_class"] not in candidate["compatible_under_layers"]:
                blockers.append(f"UNDER_LAYER_NOT_COMPATIBLE:{active['asset_ref']}")
            else:
                lower_assets_to_mask.append(active["asset_ref"])
        elif active["layer_class"] not in candidate["compatible_over_layers"]:
            blockers.append(f"OVER_LAYER_NOT_COMPATIBLE:{active['asset_ref']}")
    return blockers, warnings, sorted(set(lower_assets_to_mask))


def _runtime_check(
    selected_adapter: Optional[Dict[str, Any]], require_live_adapter: bool
) -> Tuple[List[str], List[str]]:
    blockers: List[str] = []
    warnings: List[str] = []
    if selected_adapter is None:
        if require_live_adapter:
            blockers.append("NO_EXACT_PLATFORM_ADAPTER")
        else:
            warnings.append("NO_EXACT_PLATFORM_ADAPTER")
        return blockers, warnings
    if require_live_adapter and (
        not selected_adapter.get("live_runtime")
        or selected_adapter.get("runtime_status") != "LIVE"
    ):
        blockers.append("PLATFORM_ADAPTER_NOT_LIVE")
    capabilities = set(_list(selected_adapter.get("capabilities")))
    missing = REQUIRED_LIVE_CAPABILITIES - capabilities
    if require_live_adapter and missing:
        blockers.extend(f"ADAPTER_CAPABILITY_MISSING:{item}" for item in sorted(missing))
    return blockers, warnings


def _compile_clipping_plan(
    fashion: Dict[str, Any], lower_assets_to_mask: List[str]
) -> Dict[str, Any]:
    layering = fashion["garment"]["layering"]
    occlusion = layering["occlusion"]
    payload = {
        "layer_stacking_priority": layering["layer_priority"],
        "alpha_mask_registry": {
            "skin_zones_to_hide": sorted(set(occlusion["deactivation_zones_skin"])),
            "lower_assets_to_mask": lower_assets_to_mask,
        },
        "runtime_vertex_push_matrix": {
            "enabled": occlusion["push_out_distance_mm"] > 0,
            "collision_channel": occlusion["collision_channel"],
            "push_out_distance_mm": occlusion["push_out_distance_mm"],
            "normal_offset_falloff_power": occlusion["normal_offset_falloff_power"],
        },
    }
    return payload


def compile_executable_adapter_payload(
    fashion: Dict[str, Any],
    selected_adapter: Optional[Dict[str, Any]],
    target_runtime: str,
    clipping_plan: Dict[str, Any],
    rights_receipt: Dict[str, Any],
    blockers: List[str],
) -> Dict[str, Any]:
    """Compile a deterministic execution plan; execution remains platform-owned."""
    fit = fashion["garment"]["fit"]
    physics = fashion["garment"]["physics"]
    payload = {
        "payload_type": "FGE_FASHION_EXECUTABLE_ADAPTER_PAYLOAD",
        "status": "BLOCKED" if blockers else "EXECUTION_PLAN_CANDIDATE",
        "target_runtime": target_runtime,
        "adapter_id": None if selected_adapter is None else selected_adapter["adapter_id"],
        "rig_binding": {
            "compatible_rigs": fit.get("rig_compatibility", []),
            "anchor_points": fit.get("anchor_points", []),
            "morph_strategy": fit.get("morph_strategy"),
            "fit_tolerance_mm": fit.get("fit_tolerance_mm"),
        },
        "physics_solver": {
            "solver": None if selected_adapter is None else selected_adapter.get("physics_solver"),
            "profile_id": physics.get("profile_id"),
            "solver_neutral": physics.get("solver_neutral", {}),
            "fallback_behavior": physics.get("fallback_behavior"),
        },
        "clipping_occlusion_engine": clipping_plan,
        "rights_receipt": rights_receipt,
    }
    validate_json_contract(
        clipping_plan,
        PACKAGE_ROOT / "schema" / "payloads" / "clipping_occlusion_engine.json",
    )
    validate_json_contract(
        payload,
        PACKAGE_ROOT / "schema" / "payloads" / "adapter_module.json",
    )
    return payload


def compile_wardrobe_binding_candidate(
    character_projection: Dict[str, Any],
    fashion_asset: Dict[str, Any],
    *,
    target_runtime: str = "LLM_GENERIC",
    require_live_adapter: bool = True,
) -> Dict[str, Any]:
    """Validate exact inputs and emit a governed wardrobe binding candidate."""
    validate_character_projection(character_projection)
    validate_envelope(fashion_asset)
    identity = fashion_asset["identity"]
    validation = fashion_asset["validation"]
    representations = fashion_asset["representations"]
    blockers: List[str] = []
    warnings: List[str] = []
    if validation["state"] == "FAILED":
        blockers.append("FASHION_ASSET_VALIDATION_FAILED")
    elif validation["state"] != "PASSED":
        warnings.append("FASHION_ASSET_NOT_FULLY_VALIDATED")
    for check in (_policy_check, _fit_check):
        check_blockers, check_warnings = check(character_projection, fashion_asset)
        blockers.extend(check_blockers)
        warnings.extend(check_warnings)
    rights_blockers, rights_warnings, rights_receipt = _rights_check(
        fashion_asset, target_runtime
    )
    blockers.extend(rights_blockers)
    warnings.extend(rights_warnings)
    layer_blockers, layer_warnings, lower_assets = _layer_stack_check(
        character_projection, fashion_asset
    )
    blockers.extend(layer_blockers)
    warnings.extend(layer_warnings)
    adapters = [
        value
        for value in _list(representations.get("adapters"))
        if isinstance(value, dict)
    ]
    selected_adapter = _choose_target_adapter(adapters, target_runtime)
    runtime_blockers, runtime_warnings = _runtime_check(
        selected_adapter, require_live_adapter
    )
    blockers.extend(runtime_blockers)
    warnings.extend(runtime_warnings)
    conflicts = [str(value) for value in _list(validation.get("conflicts"))]
    unknowns = [str(value) for value in _list(validation.get("unknowns"))]
    if conflicts:
        warnings.append("SOURCE_CONFLICTS_PRESERVED")
    blockers = sorted(set(blockers))
    warnings = sorted(set(warnings))
    status = "BLOCKED" if blockers else (
        "NEEDS_VALIDATION" if warnings or unknowns else "READY_CANDIDATE"
    )
    clipping_plan = _compile_clipping_plan(fashion_asset, lower_assets)
    execution_payload = compile_executable_adapter_payload(
        fashion_asset,
        selected_adapter,
        target_runtime,
        clipping_plan,
        rights_receipt,
        blockers,
    )
    character_ref = character_projection["character_ref"]
    return {
        "object_type": "CHARACTER_WARDROBE_BINDING_CANDIDATE",
        "adapter_object_id": "FGE-FASHION-CHARACTER-OS-ADAPTER-001",
        "adapter_version": "0.2.0",
        "status": status,
        "canon_effect": "NONE",
        "authority": "CANDIDATE_ONLY",
        "character_ref": deepcopy(character_ref),
        "fashion_ref": {
            "object_id": fashion_asset["object_id"],
            "asset_id": identity["asset_id"],
            "version": fashion_asset["version"],
            "source_status": fashion_asset["status"],
            "source_canon_effect": fashion_asset["canon_effect"],
        },
        "target_runtime": target_runtime,
        "selected_adapter": selected_adapter,
        "compatibility": {
            "blockers": blockers,
            "warnings": warnings,
            "unknowns": unknowns,
            "conflicts": conflicts,
        },
        "binding": {
            "mode": "REFERENCE_NOT_COPY",
            "wardrobe_asset_ref": f"{identity['asset_id']}@{fashion_asset['version']}",
            "fit_strategy": fashion_asset["garment"]["fit"].get("morph_strategy", UNKNOWN),
            "layering": deepcopy(fashion_asset["garment"]["layering"]),
            "coverage": deepcopy(fashion_asset["garment"]["coverage"]),
        },
        "executable_adapter_payload": execution_payload,
        "required_authorization": "CHARACTER_OS_WARDROBE_PROMOTION",
        "mutations_applied": [],
    }


def authorize_binding(candidate: Dict[str, Any]) -> None:
    """Authorization belongs to Character OS governance, not this adapter."""
    raise PermissionError(
        "Fashion adapter cannot authorize wardrobe bindings; route candidate to Character OS authority"
    )
