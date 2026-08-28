# FGE Modular Fashion OS

**Object:** `FGE-SYS-MODULAR-FASHION-OS-001`  
**Version:** `0.1.0`  
**Status:** `IMPLEMENTED_BRANCH / NOT_CANON_PROMOTED`  
**Canon effect:** `NONE`  

A three-module garment infrastructure built for FGE Character OS.

```text
GITHUB STORAGE                     LLM DISPLAY                    CHARACTER OS ADAPTER
(source + provenance)             (runtime interpretation)       (identity-safe attachment)
       |                                  |                                  |
       +---- immutable asset envelope --->+---- display packet ------------->+
       ^                                  |                                  |
       +---- governed write-back <--------+---- proposed deltas -------------+
```

## Governing boundary

1. **Storage is authoritative for persisted garment records.** The LLM may read, summarize, compare and propose changes, but it does not silently mutate authority.
2. **Display is ephemeral.** It compiles a stored asset into a compact LLM-facing packet and can emit proposed deltas. Display output is not canon.
3. **Character OS is authoritative for character identity and wardrobe attachment.** The adapter may reference garment assets, fit profiles and render adapters but cannot rewrite character DNA, Heart, Brain or identity locks.

## Modules

### 1. Storage

`storage/github_store.py`

Persists versioned garment envelopes in GitHub under:

```text
storage/assets/<asset_id>/<version>.json
```

and maintains a lightweight registry at:

```text
storage/index.json
```

### 2. LLM Display

`runtime/llm_display.py`

Loads a Fashion Asset Envelope and compiles a deterministic `LLM_DISPLAY_PACKET` containing identity, fit, material, physics, rights, representations, validation and unresolved fields. It does not invent missing values.

### 3. Character OS Adapter

`adapter/character_os_adapter.py`

Takes:

- Character Chip / character envelope
- Fashion Asset Envelope
- target runtime capability profile

and emits a `CHARACTER_WARDROBE_BINDING_CANDIDATE`.

The binding references the garment by ID and version. It does not copy garment truth into character canon.

## Core contract

The system uses one canonical transport object:

`contracts/fashion_asset_envelope.schema.json`

The envelope separates:

- identity / provenance / rights
- geometry / fit / layering / coverage
- material / physics / customization
- source / runtime / platform representations
- validation state

## Write path

```text
DESIGN OR INGEST
   -> validate envelope
   -> persist version to GitHub
   -> register index entry
   -> compile LLM display packet
   -> Character OS adapter evaluates compatibility
   -> emit binding candidate
   -> explicit authority promotes or rejects
```

## Reverse-engineering rule

Engine-specific data is always downstream of universal garment intent.

```text
physical/material intent
        -> adapter profile
        -> UE / Web / future runtime parameters
```

No Unreal, WebGPU, glTF, USD or solver-specific field is allowed to redefine the garment's core identity.

## Current implementation status

- GitHub persistence contract: `IMPLEMENTED`
- LLM display compiler: `IMPLEMENTED`
- Character OS adapter: `IMPLEMENTED`
- Example asset: `NON_CANON_TEST_FIXTURE`
- Live engine-specific adapters: `CANDIDATE / NOT_IMPLEMENTED`
- Character OS schema handshake beyond generic Character Chip fields: `PROPOSED`
