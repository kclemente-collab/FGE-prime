# FGE Modular Fashion OS — Layered Fashion Module

**Object:** `FGE-SYS-MODULAR-FASHION-OS-001`  
**Spec:** `FGE-SPEC-LAYERED-FASHION-DB-001`  
**Version:** `0.2.0`  
**Status:** `IMPLEMENTED_BRANCH / SPEC_CANDIDATE / NOT_CANON_PROMOTED`  
**Owner:** Keith Clemente / Feral Gloss Empire  
**Created:** 2026-08-28  
**Canon effect:** `NONE`  
**Parent:** Character OS modular wardrobe substrate  
**Branch:** `fge/modular-fashion-os-v0.1`  
**Primary contract:** [`contracts/fashion_asset_envelope.schema.json`](contracts/fashion_asset_envelope.schema.json)

Interoperable premium digital-fashion schema for FGE Character OS. The module separates **what a garment is** from **how it is shown** and **how a target engine wears it**, so Character OS can stack undergarments, streetwear, outerwear, and attachments without clipping, without rewriting character gospel, and without letting engine-specific fields redefine garment identity.

This README is the developer repository manifest. Companion files:

| File | Role |
|------|------|
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Executive / brand-partner architecture brief |
| [`schema/layered_fashion_module.sql`](schema/layered_fashion_module.sql) | PostgreSQL DDL with cascade integrity |
| [`schema/payloads/`](schema/payloads/) | Storage, Display, Adapter, FDE, occlusion JSON models |
| [`contracts/fashion_asset_envelope.schema.json`](contracts/fashion_asset_envelope.schema.json) | Canonical transport object |
| [`manifest.json`](manifest.json) | Package authority + module IDs |

---

## 1. Vision

FGE does not treat clothes as texture swaps. A garment is a versioned asset with provenance, rights, fit, material intent, physics intent, and platform adapters. Character identity stays in Character OS. Garment truth stays in Storage. Display is ephemeral. Adapter evaluates compatibility and emits a binding candidate. Authorization is never implicit.

```text
PHYSICAL / MATERIAL INTENT
        -> adapter profile
        -> UE5 / WebXR / future runtime parameters
```

No Unreal, WebGPU, glTF, USD, or solver-specific field is allowed to redefine the garment's core identity.

---

## 2. Governing Laws

1. **UNKNOWN over invented.** Missing fields stay `UNKNOWN`. Display and Adapter never fabricate gospel, rights, URIs, or physics constants.
2. **Generated output is not canon.** LLM packets and adapter bindings are candidates until an explicit authority promotes them.
3. **Storage / Display / Adapter authority separation.** Storage owns persisted records. Display owns runtime interpretation. Character OS owns identity and wardrobe authorization.
4. **Garment reference over character-data duplication.** Bindings store `asset_id@version`, not copied physics or material maps.
5. **Engine-specific parameters are downstream of garment intent.**
6. **Conflicts are preserved until resolved.** Clipping, rig mismatch, and rights collisions stay visible.

```text
ROLE=READ_ONLY_INTERPRETER
LAW=UNKNOWN>INVENT|CONFLICT>PRESERVE|GENERATED!=CANON
MAY=DESCRIBE|COMPARE|RECOMMEND|PROPOSE_DELTA|SELECT_COMPATIBLE_REPRESENTATION
MUST_NOT=AUTHORIZE|LOCK|MUTATE_STORAGE|MUTATE_CHARACTER_IDENTITY
```

---

## 3. System Architecture Map

See package tree under `systems/modular_fashion_os/` for Storage, Display, Adapter, schema SQL, and payload models.

### Three-module runtime

```text
STORAGE (immutable source + provenance)
   -> DISPLAY (LOD / shaders / occlusion)
   -> ADAPTER (rig + physics + platform bridge)
   <- governed write-back / proposed deltas
```

| Layer | Owns | Must not |
|-------|------|----------|
| Storage | Raw source, provenance, rights, fabric constants | Care how an engine renders |
| Display | LODs, shading profiles, z-depth, skin-hide groups | Persist as canon |
| Adapter | Rig retarget, Chaos / AmmoJS bridges, morph drivers | Rewrite character DNA / Heart / Brain / identity locks |

---

## 4. Product Registry, Layer-Fit, Material-Shader

### 4.1 Product Registry (`digital_assets_registry`)

| Field | Type | Notes |
|-------|------|-------|
| `asset_id` | UUID PK | Maps to envelope `identity.asset_id` |
| `sku_identifier` | VARCHAR(64) UNIQUE | Global ledger / retail SKU |
| `brand_name` | VARCHAR(100) | Haus / drop owner |
| `rarity_tier` | CHECK enum | `Haute_Couture`, `Premium`, `Street_Drop` |
| `interoperability_tokens` | TEXT[] | Engine verification keys (UE5, Unity, WebGPU, Roblox) |
| `digital_rights_framework` | JSONB | Commercial / rental / modification locks |
| `created_at` | TIMESTAMPTZ | Ledger timestamp |

### 4.2 Layer and Fit Engine

| `z_layer_index` | Class | Examples |
|-----------------|-------|----------|
| 10-19 | Base skin / underwear | Compression, undergarments |
| 20-39 | Inner wear | T-shirts, button-downs, leggings |
| 40-59 | Outer wear | Sweaters, hoodies, jeans |
| 60-79 | Over wear | Coats, trench, armor |
| 70+ | Attachments | Belts, tactical, floating tech |

### 4.3 Material and Shader Hub

Physics constants live in Storage. Optical intent compiles into Display Substrate slabs. Adapter maps constants into Chaos or AmmoJS. Colorways use RGBA tint channels, not unique albedo files.

---

## 5. Fabric Data Pipeline

Hybrid execution: pre-bake structural meshes and bone weights; runtime mesh deformation, clipping, and shader overrides.

```text
STORAGE                         DISPLAY                         ADAPTER
raw physical constants   ->     UE5 Substrate graph        ->   Chaos clothing config
USD / 8K EXR source      ->     LOD0/1/2 runtime meshes    ->   rig + solver bridge
```

See `schema/payloads/storage_module.json`, `schema/payloads/display_module.json`, and `schema/payloads/adapter_module.json`.

---

## 6. Multi-Layer Occlusion and Clipping

Three coordinated systems:

- Rigid Z-index. Higher `z_layer_index` occludes lower.
- Pre-baked alpha clipping masks. Equipping a Layer 60 trench deactivates torso / upper-arm patches on Layer 10 and Layer 20. The performance claim remains suppressed until the governed UE5 benchmark records measured evidence.
- Dynamic runtime collision buffer. Collar / cuff / hem borders use a 2.5 mm push-out along normals.

See `schema/payloads/clipping_occlusion_engine.json`.

---

## 7. Fabric Description Engine (FDE)

FDE translates physics numbers into UI copy, swatches, movement SFX, and viewport overrides. Lookup key: `global_fabric_id` (example `fab_lthr_nappa_01`).

**Representation decision:** `display_ui_anchors` is an extensible JSON object in the payload contract and PostgreSQL `JSONB` in the FDE registry. It is the single persisted source for UI anchor keys such as `icon_thumbnail_uri` and `sound_profile_on_movement`; those keys are not duplicated as independently writable SQL columns. This keeps optional and future anchors sparse while the JSON Schema governs their known types.

See `schema/payloads/fabric_description_index.json`.

---

## 8. Dynamic Customization

Do not mint 50 albedo files for 50 colorways. Use one RGBA control map plus runtime vectors. Customization never mutates Storage physical constants.

See `schema/payloads/runtime_customization_parameters.json`.

---

## 9. Database Setup

Prerequisites: Python 3.10+, dependencies in `requirements.txt`, PostgreSQL 15+, optional Docker, S3 or Cloudflare R2 for source/runtime files.

```bash
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 \
  -f systems/modular_fashion_os/schema/layered_fashion_module.sql
```

Equip join query is documented in this file on GitHub after schema push. Full SQL lives in `schema/layered_fashion_module.sql`.

---

## 10. Write Path (Character OS handoff)

```text
DESIGN OR INGEST
   -> deep-copy and validate the exact Fashion Asset Envelope snapshot
   -> persist version to GitHub Storage
   -> register storage/index.json entry
   -> compile LLM Display packet
   -> Character OS Adapter evaluates compatibility
   -> emit CHARACTER_WARDROBE_BINDING_CANDIDATE
        READY_CANDIDATE | NEEDS_VALIDATION | BLOCKED
   -> explicit authority promotes or rejects
```

GitHub Storage retries concurrent index compare-and-swap conflicts, preserves the highest semantic version as `latest_version`, and raises `StorageRecoveryRequired` when an immutable asset write succeeds but registration cannot be completed. Replaying the same save or calling `reconcile_asset_index()` revalidates the stored envelope before completing registration. Asset IDs use reversible path-segment encoding, so distinct IDs cannot collapse onto one repository path.

Adapter stores a reference such as `FGE-FASH-EXAMPLE-COAT-001@0.1.0`. `authorize_binding()` raises `PermissionError` on purpose.

---

## 11. Current Implementation Status

| Component | Object ID | Status |
|-----------|-----------|--------|
| Package | `FGE-SYS-MODULAR-FASHION-OS-001` | `IMPLEMENTED_BRANCH / NOT_CANON_PROMOTED` |
| Layered DB spec | `FGE-SPEC-LAYERED-FASHION-DB-001` | `SPEC_CANDIDATE` |
| GitHub persistence | `FGE-FASHION-STORAGE-GITHUB-001` | `IMPLEMENTED_SCHEMA_VALIDATED_RECOVERABLE` |
| LLM display compiler | `FGE-FASHION-LLM-DISPLAY-001` | `IMPLEMENTED_WITH_STATIC_FDE_COMPILER` |
| Character OS adapter | `FGE-FASHION-CHARACTER-OS-ADAPTER-001` | `IMPLEMENTED_EXACT_PROJECTION_AND_EXECUTION_PLAN` |
| PostgreSQL DDL | `schema/layered_fashion_module.sql` | `SPEC_CANDIDATE / INTEGRATION_TESTED` |
| UE5 Substrate / Chaos live adapters | — | `CANDIDATE / NOT_IMPLEMENTED` |
| UE5 performance claim | `FGE-BENCH-UE5-OCCLUSION-001` | `SUPPRESSED_PENDING_MEASUREMENT` |
| Example asset | `FGE-FASH-EXAMPLE-COAT-001` | `NON_CANON_TEST_FIXTURE` |

---

## 12. Contribution and Versioning

- New fabric types land in `fabric_description_index` first, then `fabric_master_profiles`.
- Semantic changes create a new spec version or a CDR entry.
- Engine-specific fields stay in Adapter payloads, never in Storage identity.
- Example fixtures stay labeled `NON_CANON_TEST_FIXTURE` with `canon_effect: NONE`.
- Do not set `LOCKED` or promote to canon from this module. Operator-only.

```text
FGE-FASH-<SLUG>-<NNN>           garment asset
FGE-FAB-<SLUG>-<NNN>            fabric id
FGE-MAT-<SLUG>-<NNN>            material chip
FGE-PHYS-<SLUG>-<NNN>           physics profile
FGE-SPEC-LAYERED-FASHION-DB-00X spec revisions
```

---

## 13. Validation

```bash
python -m pytest systems/modular_fashion_os/tests
```

*FGE-SPEC-LAYERED-FASHION-DB-001 v0.2.0 — candidate schema for Character OS wardrobe infrastructure. Not canon until operator promotion.*
