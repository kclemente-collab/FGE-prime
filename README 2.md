# Epoch 0.2 — Machine-Checkable Governance Pack (MCP) — Aligned to Master v0.2.0-DRAFT + CDR-ROOT

**Status:** PROPOSED  
**Owner:** Keith Clemente / Feral Gloss Empire  
**Created:** 2026-06-26  
**Last Updated:** 2026-06-26 (Aligned to CDR-ROOT consolidation rulings)  
**Purpose:** Executable constitution layer for CharacterOS. All downstream modules, seeds, and contracts must pass these schemas and rules or be rejected.

This pack is now synchronized with the official Epoch 0 Master Specification v0.2.0-DRAFT and the three canonical rulings in CDR-ROOT. The previous circular dependency (REG-002 ↔ VOCAB-001) has been resolved per CDR-ROOT-003.

## Contents

- `dependency_graph.json` — Canonical authority DAG (acyclic per CDR-ROOT-003)
- `schemas/` — JSON Schemas for core objects (VOCAB-001, REG-001, REG-002, CON-001, SPEC-001)
- `validators/` — Enforcement engines (CLI validator v0.1 starts here)
- Cross-artifact governance rules (see below)

## Key Consolidation Rulings Incorporated (CDR-ROOT)

1. **REG-002 Taxonomy (CDR-ROOT-001):** Event-first hybrid, two-axis (primary: event pattern enum; secondary: domain_tags array). State transition layer deferred to REG-002 v2.0 pending SVR-001 (Epoch I).
2. **VOCAB-001 Binding Model (CDR-ROOT-002):** Tiered system — Kernel Terms (immutable, referential only) + Working Terms (bounded interpretive, must reference Kernel/Registry). No redefinition of REG-002 fields.
3. **Dependency Direction (CDR-ROOT-003):** REG-002 Depends On = FGE-ARCH-LAWS-001 only. No vocabulary-to-registry dependency. Acyclic chain restored: LAW-001 → REG-002 → VOCAB-001 → SPEC-001.

## How to Use (Machine Layer)

1. Every new artifact MUST declare version, owner, and dependencies (LAW-001).
2. No term may appear in any schema or module unless defined in VOCAB-001 (LAW-002). Kernel Terms are referential only.
3. All classifications/enums MUST come from a REG-00X registry (LAW-003). REG-002 is event-first hybrid.
4. Inter-module communication MUST use CON-001 structures only (LAW-004).
5. Semantic changes MUST create new version or append CDR entry (CDR-001). CDR-ROOT rulings are now authoritative.
6. Missing dependency → BLOCK with unresolved_dependency_error (Gate 0.5).

## Validation Command (once validator is complete)

```bash
python validators/epoch0.1_validator.py --artifact path/to/my_spec.json --type SPEC-001
```

## Next Layer

Epoch 0.2 Validator Engine (CLI first, FastAPI wrapper next). Full support for tiered VOCAB and hybrid REG-002 in v0.2.

This is the point where CharacterOS becomes executable governance.

## Ratification Gate

This pack now aligns with the official master v0.2.0-DRAFT. It passes Machine Translation Gate and Cold-Reader Gate. Ready for Canon-Lock Authority review and promotion to RATIFIED once the validator confirms enforcement of the three CDR-ROOT rulings. Epoch 0 ratification checklist can now be completed.