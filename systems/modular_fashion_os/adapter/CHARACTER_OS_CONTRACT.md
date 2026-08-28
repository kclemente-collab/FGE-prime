# FGE Character OS Fashion Adapter Contract

**Object:** `FGE-FASHION-CHARACTER-OS-ADAPTER-001`  
**Status:** `IMPLEMENTED_GENERIC_HANDSHAKE`  
**Canon effect:** `NONE`

## Purpose

Attach a fashion asset to a character through references and compatibility checks without duplicating garment truth into character canon or allowing a garment to rewrite character identity.

## Character-facing input contract

The generic adapter reads only these compatibility-facing fields when present:

```json
{
  "character_id": "FGE-CHAR-...",
  "version": "1.0.0",
  "authority": "LOCKED",
  "rig_profile": "FGE_RIG_PROFILE_ID",
  "body_profile": "FGE_BODY_PROFILE_ID",
  "wardrobe_policy": {
    "allowed_asset_classes": ["GARMENT", "ACCESSORY"],
    "forbidden_asset_ids": [],
    "max_layer_priority": 100
  }
}
```

Missing fields are preserved as UNKNOWN and lower compatibility confidence. They are never fabricated.

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

## Future exact handshake

The current implementation accepts a generic Character Chip projection. When the authoritative Character Chip schema is available in-repository, add a projection layer that maps its exact locked field names into this narrow interface. Do not mutate the Character Chip schema to fit this adapter.
