# FGE LLM Display Contract

**Object:** `FGE-FASHION-LLM-DISPLAY-001`  
**Version:** `0.2.0`  
**Status:** `IMPLEMENTED_WITH_STATIC_FDE_COMPILER / EPHEMERAL_RUNTIME`  
**Canon effect:** `NONE`

## Purpose

Turn a persisted Fashion Asset Envelope into a compact reasoning/presentation packet suitable for ChatGPT, Claude, Gemini, Grok or another LLM without making the LLM the source of truth.

## Input

1. `Fashion Asset Envelope` from GitHub storage.
2. Optional Character OS context containing only compatibility-facing fields.
3. Optional target runtime name.
4. Optional validated `FabricDescriptionIndex` for FDE compilation.

## Output

`FGE_FASHION_LLM_DISPLAY_PACKET`

The packet contains:

- source identity + version
- display metadata
- fit + layering + coverage
- material + physics
- rights
- source/runtime/adapter representations
- validation state
- preserved conflicts + unknowns
- empty or explicitly PROPOSED deltas
- FDE localization, UI anchors, viewport overrides and governed RGBA/pattern shader inputs

## Runtime law

```text
ROLE=READ_ONLY_INTERPRETER
LAW=UNKNOWN>INVENT|CONFLICT>PRESERVE|GENERATED!=CANON
MAY=DESCRIBE|COMPARE|RECOMMEND|PROPOSE_DELTA|SELECT_COMPATIBLE_REPRESENTATION
MUST_NOT=AUTHORIZE|LOCK|MUTATE_STORAGE|MUTATE_CHARACTER_IDENTITY
```

## Write-back

If an LLM discovers a useful new fact or transformation, it emits:

```json
{
  "path": "garment.material.optical_intent.roughness",
  "candidate_value": 0.42,
  "reason": "derived from validated material test",
  "status": "PROPOSED",
  "canon_effect": "NONE"
}
```

A separate governance step must validate and persist any accepted delta as a new asset version.
