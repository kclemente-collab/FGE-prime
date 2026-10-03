"""Fabric Description Engine static lookup and display compilation."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, Iterable

from systems.modular_fashion_os.runtime.customization import (
    compile_runtime_customization,
)
from systems.modular_fashion_os.validation import PACKAGE_ROOT, validate_json_contract


class FabricDescriptionError(LookupError):
    """Raised for duplicate or malformed FDE registry records."""


class FabricDescriptionIndex:
    """Immutable in-memory index keyed by global_fabric_id."""

    def __init__(self, records: Iterable[Dict[str, Any]]):
        self._records: Dict[str, Dict[str, Any]] = {}
        for record in records:
            validate_json_contract(
                record,
                PACKAGE_ROOT / "schema" / "payloads" / "fabric_description_index.json",
            )
            fabric_id = record.get("global_fabric_id")
            if not isinstance(fabric_id, str) or not fabric_id:
                raise FabricDescriptionError("global_fabric_id is required")
            if fabric_id in self._records:
                raise FabricDescriptionError(f"Duplicate fabric record: {fabric_id}")
            for field in (
                "localization_manifest",
                "display_ui_anchors",
                "viewport_rendering_overrides",
            ):
                if not isinstance(record.get(field), dict):
                    raise FabricDescriptionError(f"{fabric_id}.{field} must be an object")
            self._records[fabric_id] = deepcopy(record)

    def lookup(self, fabric_id: str) -> Dict[str, Any] | None:
        record = self._records.get(fabric_id)
        return None if record is None else deepcopy(record)


def compile_fde_output(
    envelope: Dict[str, Any], index: FabricDescriptionIndex
) -> Dict[str, Any]:
    """Join an envelope to FDE and compile UI, viewport and shader inputs."""
    garment = envelope.get("garment") or {}
    material = garment.get("material") or {}
    fabric_id = material.get("fabric_id")
    record = index.lookup(str(fabric_id)) if fabric_id else None
    customization = compile_runtime_customization(
        garment.get("customization") or {}, envelope.get("rights") or {}
    )
    if record is None:
        output = {
            "fabric_id": fabric_id or "UNKNOWN",
            "status": "UNKNOWN_FABRIC",
            "ui": {},
            "viewport": {},
            "runtime_customization": customization,
        }
        validate_json_contract(
            output, PACKAGE_ROOT / "schema" / "payloads" / "display_module.json"
        )
        return output
    status = "BLOCKED" if customization["status"] == "BLOCKED" else "COMPILED"
    output = {
        "fabric_id": fabric_id,
        "status": status,
        "ui": {
            "localization_manifest": record["localization_manifest"],
            "display_ui_anchors": record["display_ui_anchors"],
        },
        "viewport": {
            "substrate_shading_topology": material.get(
                "substrate_shading_topology", "Substrate_Slab_Blended"
            ),
            "rendering_overrides": record["viewport_rendering_overrides"],
        },
        "runtime_customization": customization,
    }
    validate_json_contract(
        output, PACKAGE_ROOT / "schema" / "payloads" / "display_module.json"
    )
    return output
