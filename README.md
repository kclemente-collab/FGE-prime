# Epoch 0.1 — Machine-Checkable Governance Pack (MCP)

**Status:** PROPOSED  
**Owner:** Keith Clemente / Feral Gloss Empire  
**Created:** 2026-06-26  
**Purpose:** Executable constitution layer for CharacterOS. All downstream modules, seeds, and contracts must pass these schemas and rules or be rejected.

This pack replaces prose governance with machine-enforceable structure.

## Contents

- `dependency_graph.json` — Canonical authority DAG (who depends on what)
- `schemas/` — JSON Schemas for core objects (VOCAB-001, REG-001, REG-002, CON-001, SPEC-001)
- `validators/` — Enforcement engines (CLI validator v0.1 starts here)
- Cross-artifact governance rules (see below)

## How to Use (Machine Layer)

1. Every new artifact MUST declare version, owner, and dependencies (LAW-001).
2. No term may appear in any schema or module unless defined in VOCAB-001 (LAW-002).
3. All classifications/enums MUST come from a REG-00X registry (LAW-003).
4. Inter-module communication MUST use CON-001 structures only (LAW-004).
5. Semantic changes MUST create new version or append CDR entry (CDR-001).
6. Missing dependency → BLOCK with unresolved_dependency_error (Gate 0.5).

## Validation Command (once validator is complete)

```bash
python validators/epoch0.1_validator.py --artifact path/to/my_spec.json --type SPEC-001
```

## Next Layer

Epoch 0.1 Validator Engine (chosen form: pure JSON-schema + CLI first, then thin FastAPI wrapper).

This is the point where CharacterOS becomes executable governance.

## Ratification Gate

This pack passes Machine Translation Gate and Cold-Reader Gate by design. It is ready for Canon-Lock Authority review and promotion to RATIFIED once the minimal validator confirms basic structural enforcement.