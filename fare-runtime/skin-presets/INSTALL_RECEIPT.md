# FGE-ADP-SKIN-PRESET-001 — Skin Preset Install Receipt

## Registry State

- **Object ID:** `FGE-ADP-SKIN-PRESET-001`
- **Family ID:** `FGE-SKN-FAM-CARMEL-001`
- **Parent preset:** `SKN-PST-CARMEL-001@0.1.0`
- **Version:** `0.1.0`
- **Type:** Material Adapter / Skin Preset Summon / FARE Gate
- **Status:** INSTALLED_RUNTIME
- **Lock:** NOT LOCKED
- **Canon effect:** NONE

## Authority Binding

- Parent law: `KIC-ENG-002` v1.1 (Notion 327d6954-40cb-43c9-b81a-eafecb4ec119)
- Playbook: `RENDER-002` `FGE_SkinLightPlaybook.md`
- Spec candidate: `FGE-SKIN-RENDER-ENGINEERING-SPEC-001@0.1.0` PROPOSED
- Parent FARE runtime: `FGE-FARE-001`
- Sibling: `FGE-ADP-LEATHER-FARE-001`
- Process binds: `FGE-PROC-MIRROR-001`, `FGE-PROC-ARTIFACT-001`
- Gate: `FARE-VAL-SKIN-001`

## Adapter Law

`TOKEN → SKIN_GENOME → MIRROR → FARE_A/R/E → PASS|FAIL → SUMMON_PACKET`

The adapter never writes character canon. FAIL halts with NOSILENT_DRIFT.
Tone class is not a character lock.

## Locked Invariants (runtime, not canon)

- SSS foundation mandatory (KIC-ENG-002)
- Finish layers additive only
- Tone class `CARMEL` / alias `CARAMEL`
- Sheen class `DRY_SATIN` on parent
- Porosity class `ASYM`
- Light class `NATURAL` on parent
- Anisotropy installed: `0.2` (playbook). Spec `0.50-0.65` stored, not applied
- Heart rewrite: false

## Installed Planes

- Grok skill: `fge-skin-preset-summon`
- GitHub: `kclemente-collab/FGE-prime/fare-runtime/skin-presets/`
- Notion receipt: under FGE MASTER REPOSITORY PRIME
- Summon priority: BEFORE Grok default skin language

## Validation

Parent FARE design score 96/100. Gate VALIDATED_PASS.
Measured Arnold vertical slice: PENDING.
Commerce OFF. Canon effect NONE.

## Promotion Boundary

INSTALLED_RUNTIME. Not LOCKED. Director retains veto.
No character or complexion gospel promotion.
