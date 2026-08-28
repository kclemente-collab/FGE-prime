"""FGE Character OS adapter for Fashion Asset Envelopes.

The adapter never mutates either input. It emits a wardrobe binding candidate
that Character OS may explicitly authorize, reject or promote.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple


UNKNOWN = "UNKNOWN"


def _list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


def _choose_target_adapter(adapters: List[Dict[str, Any]], target_runtime: str) -> Optional[Dict[str, Any]]:
    target_norm = target_runtime.strip().lower()
    for adapter in adapters:
        if str(adapter.get("target", "")).strip().lower() == target_norm:
            return deepcopy(adapter)
    return None


def _policy_check(character: Dict[str, Any], fashion: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """Return blockers, warnings from generic wardrobe policy fields."""
    blockers: List[str] = []
    warnings: List[str] = []

    policy = character.get("wardrobe_policy") or {}
    identity = fashion.get("identity") or {}
    garment = fashion.get("garment") or {}
    asset_id = identity.get("asset_id")
    asset_class = identity.get("asset_class")
    layer_priority = (garment.get("layering") or {}).get("layer_priority")

    forbidden_ids = _list(policy.get("forbidden_asset_ids"))
    if asset_id in forbidden_ids:
        blockers.append("WARDROBE_POLICY_FORBIDS_ASSET_ID")

    allowed_classes = _list(policy.get("allowed_asset_classes"))
    if allowed_classes and asset_class not in allowed_classes:
        blockers.append("WARDROBE_POLICY_ASSET_CLASS_NOT_ALLOWED")

    max_priority = policy.get("max_layer_priority")
    if isinstance(max_priority, int) and isinstance(layer_priority, int) and layer_priority > max_priority:
        blockers.append("WARDROBE_POLICY_LAYER_PRIORITY_EXCEEDED")

    if not policy:
        warnings.append("WARDROBE_POLICY_UNKNOWN")

    return blockers, warnings


def _fit_check(character: Dict[str, Any], fashion: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    blockers: List[str] = []
    warnings: List[str] = []

    fit = ((fashion.get("garment") or {}).get("fit") or {})
    garment_rigs = [str(x) for x in _list(fit.get("rig_compatibility"))]
    character_rig = character.get("rig_profile")

    if character_rig and garment_rigs:
        if str(character_rig) not in garment_rigs:
            blockers.append("RIG_PROFILE_INCOMPATIBLE")
    elif not character_rig:
        warnings.append("CHARACTER_RIG_PROFILE_UNKNOWN")
    elif not garment_rigs:
        warnings.append("GARMENT_RIG_COMPATIBILITY_UNKNOWN")

    if not character.get("body_profile"):
        warnings.append("CHARACTER_BODY_PROFILE_UNKNOWN")
    if not fit.get("source_body_profile"):
        warnings.append("GARMENT_SOURCE_BODY_PROFILE_UNKNOWN")

    return blockers, warnings


def compile_wardrobe_binding_candidate(
    character_chip: Dict[str, Any],
    fashion_asset: Dict[str, Any],
    *,
    target_runtime: str = "LLM_GENERIC",
) -> Dict[str, Any]:
    """Evaluate compatibility and emit an authority-safe wardrobe binding candidate."""
    identity = fashion_asset.get("identity") or {}
    validation = fashion_asset.get("validation") or {}
    representations = fashion_asset.get("representations") or {}

    blockers: List[str] = []
    warnings: List[str] = []

    if validation.get("state") == "FAILED":
        blockers.append("FASHION_ASSET_VALIDATION_FAILED")
    elif validation.get("state") != "PASSED":
        warnings.append("FASHION_ASSET_NOT_FULLY_VALIDATED")

    blockers_a, warnings_a = _policy_check(character_chip, fashion_asset)
    blockers_b, warnings_b = _fit_check(character_chip, fashion_asset)
    blockers.extend(blockers_a + blockers_b)
    warnings.extend(warnings_a + warnings_b)

    adapters = [x for x in _list(representations.get("adapters")) if isinstance(x, dict)]
    selected_adapter = _choose_target_adapter(adapters, target_runtime)
    if selected_adapter is None and target_runtime != "LLM_GENERIC":
        warnings.append("NO_EXACT_PLATFORM_ADAPTER")

    explicit_unknowns = [str(x) for x in _list(validation.get("unknowns"))]
    conflicts = [str(x) for x in _list(validation.get("conflicts"))]
    if conflicts:
        warnings.append("SOURCE_CONFLICTS_PRESERVED")

    if blockers:
        compatibility = "BLOCKED"
    elif warnings or explicit_unknowns:
        compatibility = "NEEDS_VALIDATION"
    else:
        compatibility = "READY_CANDIDATE"

    return {
        "object_type": "CHARACTER_WARDROBE_BINDING_CANDIDATE",
        "adapter_object_id": "FGE-FASHION-CHARACTER-OS-ADAPTER-001",
        "adapter_version": "0.1.0",
        "status": compatibility,
        "canon_effect": "NONE",
        "authority": "CANDIDATE_ONLY",
        "character_ref": {
            "character_id": character_chip.get("character_id", UNKNOWN),
            "version": character_chip.get("version", UNKNOWN),
            "authority": character_chip.get("authority", UNKNOWN),
        },
        "fashion_ref": {
            "object_id": fashion_asset.get("object_id", UNKNOWN),
            "asset_id": identity.get("asset_id", UNKNOWN),
            "version": fashion_asset.get("version", UNKNOWN),
            "source_status": fashion_asset.get("status", UNKNOWN),
            "source_canon_effect": fashion_asset.get("canon_effect", "NONE"),
        },
        "target_runtime": target_runtime,
        "selected_adapter": selected_adapter,
        "compatibility": {
            "blockers": sorted(set(blockers)),
            "warnings": sorted(set(warnings)),
            "unknowns": explicit_unknowns,
            "conflicts": conflicts,
        },
        "binding": {
            "mode": "REFERENCE_NOT_COPY",
            "wardrobe_asset_ref": f"{identity.get('asset_id', UNKNOWN)}@{fashion_asset.get('version', UNKNOWN)}",
            "fit_strategy": ((fashion_asset.get("garment") or {}).get("fit") or {}).get("morph_strategy", UNKNOWN),
            "layering": ((fashion_asset.get("garment") or {}).get("layering") or {}),
            "coverage": ((fashion_asset.get("garment") or {}).get("coverage") or {}),
        },
        "required_authorization": "CHARACTER_OS_WARDROBE_PROMOTION",
        "mutations_applied": [],
    }


def authorize_binding(candidate: Dict[str, Any]) -> None:
    """Intentionally unavailable here.

    Authorization belongs to Character OS governance, not this adapter.
    """
    raise PermissionError(
        "Fashion adapter cannot authorize wardrobe bindings; route candidate to Character OS authority"
    )
