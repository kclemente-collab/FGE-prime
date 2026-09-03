"""Compile governed RGBA and procedural customization into shader parameters."""

from __future__ import annotations

from typing import Any, Dict, List

from systems.modular_fashion_os.validation import PACKAGE_ROOT, validate_json_contract


CHANNEL_SEMANTICS = {
    "R": "PRIMARY_TEXTILE",
    "G": "SECONDARY_ACCENT",
    "B": "RIGID_HARDWARE",
    "A": "ROUGHNESS_WEAR",
}


def hex_to_vector3(value: str) -> List[float]:
    """Translate #RRGGBB into a normalized shader Vector3."""
    if not isinstance(value, str) or len(value) != 7 or not value.startswith("#"):
        raise ValueError("Hex colors must use #RRGGBB")
    try:
        channels = [int(value[index:index + 2], 16) for index in (1, 3, 5)]
    except ValueError as exc:
        raise ValueError("Hex colors must use #RRGGBB") from exc
    return [round(channel / 255.0, 6) for channel in channels]


def compile_runtime_customization(
    customization: Dict[str, Any], rights: Dict[str, Any]
) -> Dict[str, Any]:
    """Return enforceable shader inputs without mutating the source envelope."""
    contract_input = {
        "rgba_control_texture_uri": customization.get("rgba_control_texture_uri"),
        "max_pattern_tiling_scale": customization.get("max_pattern_tiling_scale"),
        "color_tints": customization.get("color_tints") or [],
        "pattern_overlays": customization.get("pattern_overlays") or [],
    }
    validate_json_contract(
        contract_input,
        PACKAGE_ROOT / "schema" / "payloads" / "runtime_customization_parameters.json",
    )
    if not customization.get("enabled"):
        return {
            "status": "DISABLED",
            "rgba_control_texture_uri": customization.get("rgba_control_texture_uri"),
            "vector_tints": [],
            "pattern_overlays": [],
            "violations": [],
        }

    operations = rights.get("modification_operations") or {}
    violations: List[str] = []
    vector_tints = []
    seen_channels = set()
    for channel in customization.get("color_tints") or []:
        channel_id = channel["channel"]
        if channel_id in seen_channels:
            violations.append(f"DUPLICATE_RGBA_CHANNEL:{channel_id}")
        seen_channels.add(channel_id)
        if channel["semantic"] != CHANNEL_SEMANTICS[channel_id]:
            violations.append(f"RGBA_SEMANTIC_MISMATCH:{channel_id}")
        if channel["runtime_override_allowed"] and operations.get("color_tint") is not True:
            violations.append(f"RIGHTS_DENY_COLOR_TINT:{channel_id}")
        vector_tints.append(
            {
                **channel,
                "vector3": hex_to_vector3(channel["default_hex"]),
            }
        )

    max_scale = float(customization.get("max_pattern_tiling_scale", 1.0))
    patterns = []
    for pattern in customization.get("pattern_overlays") or []:
        if operations.get("pattern_overlay") is not True:
            violations.append(f"RIGHTS_DENY_PATTERN_OVERLAY:{pattern['pattern_id']}")
        if any(float(value) > max_scale for value in pattern["tiling_frequency"]):
            violations.append(f"PATTERN_TILING_EXCEEDS_MAX:{pattern['pattern_id']}")
        patterns.append(dict(pattern))

    return {
        "status": "BLOCKED" if violations else "COMPILED",
        "rgba_control_texture_uri": customization.get("rgba_control_texture_uri"),
        "vector_tints": vector_tints,
        "pattern_overlays": patterns,
        "violations": sorted(set(violations)),
    }
