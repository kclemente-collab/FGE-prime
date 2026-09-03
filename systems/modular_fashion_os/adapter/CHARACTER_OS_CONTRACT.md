# FGE Character OS Fashion Adapter Contract

**Object:** `FGE-FASHION-CHARACTER-OS-ADAPTER-001`  
**Version:** `0.2.0`  
**Status:** `IMPLEMENTED_EXACT_PROJECTION_AND_EXECUTION_PLAN`  
**Canon effect:** `NONE`

## Purpose

Attach a fashion asset to a character through references and compatibility checks without duplicating garment truth into character canon or allowing a garment to rewrite character identity.

## Character-facing input contract

The adapter requires the exact `FGE-CHARACTER-CHIP-FASHION-PROJECTION-001@1.0.0` contract. It is a read-only projection from the Character Chip, not a replacement for the full Character Chip:

```json
{
  "object_id": "FGE-CHARACTER-CHIP-FASHION-PROJECTION-001",
  "schema_version": "1.0.0",
  "character_ref": {
    "object_id": "FGE-CHAR-...",
    "version": "1.0.0",
    "authority": "LOCKED"
  },
  "embodiment": {
    "rig_profile_id": "FGE_RIG_PROFILE_ID",
    "body_profile_id": "FGE_BODY_PROFILE_ID"
  },
  "wardrobe_authority": {
    "status": "AUTHORIZED",
    "allowed_asset_classes": ["GARMENT", "ACCESSORY"],
    "forbidden_asset_ids": [],
    "max_layer_priority": 100
  },
  "active_wardrobe": []
}
```

Missing or malformed fields fail schema validation. They are never fabricated.

## Fashion-facing input

A complete `Fashion Asset Envelope`.

## Output

The adapter emits a `CHARACTER_WARDROBE_BINDING_CANDIDATE` with one of three statuses:

- `READY_CANDIDATE`
- `NEEDS_VALIDATION`
- `BLOCKED`

The binding stores a reference such as:

```text
FGE-FASH-EXAMPLE-COAT-001@0.1.0
```

rather than copying garment physics/material data into the character object.

It also emits `FGE_FASHION_EXECUTABLE_ADAPTER_PAYLOAD`, containing rig binding, solver-neutral physics, clipping/occlusion, vertex push and rights receipts. This is an execution plan; a live UE5 or other platform adapter remains separately required.

## Authority boundary

```text
CHARACTER OS
  owns identity + wardrobe authorization

FASHION STORAGE
  owns garment records + version provenance

ADAPTER
  owns compatibility evaluation only
```

Calling `authorize_binding()` inside the adapter intentionally raises `PermissionError`. Authorization must occur in Character OS governance.

## Fail-closed gates

- Character wardrobe authority must be active.
- Rights validation must be `PASSED`.
- Target platform rights must be `AUTHORIZED`.
- Rig, body profile and active layer stack must be compatible.
- When a live runtime is required, an exact adapter must report `runtime_status=LIVE`, `live_runtime=true`, and all mandatory capabilities.
