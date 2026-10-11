# FGE REGRESSION VERIFICATION PROCESS

OBJECT_ID: `FGE-REGRESSION-VERIFICATION-PROCESS-001`  
VERSION: `0.1.0`  
CLASS: `PROOF_PROCESS / REGRESSION_GATE`  
STATUS: `INSTALLED / ACTIVE_PROCESS`  
CANON_EFFECT: `NONE`  
AUTHORITY_EFFECT: `NONE`  
PROMOTION_SCOPE: `PROJECT_PROBE_SECTION_J_ONLY`  
PRODUCTION_VALIDATION: `OUT_OF_SCOPE`

## Purpose

Convert a component already proven `DETERMINISTIC` into `REGRESSION_VERIFIED` only when its frozen source and explicitly designated regression suite survive a complete unchanged regression cycle.

This process does **not** prove production readiness.

```text
DETERMINISTIC
      ↓
REGRESSION_VERIFIED
      ↓
STOP
```

Forbidden implicit transitions:

```text
REGRESSION_VERIFIED != PRODUCTION_VALIDATED
REGRESSION_VERIFIED != AUTOMATION_READY
REGRESSION_VERIFIED != DEPLOYMENT_READY
REGRESSION_VERIFIED != CANON_PROMOTED
REGRESSION_VERIFIED != AUTHORITY_PROMOTED
```

## Installed binding

```yaml
target:
  object_id: FGE-RECOMBINATION-ENGINE-001
  version: 0.1.0
  source_file: fge_recombination_engine.py
  source_sha256: 269232700cb8ba1de66c3033e4b25a897c9d0ebadcc0d9fcf8ce58960bac590d

regression_suite:
  object_id: FGE-RECOMBINATION-REGRESSION-001
  version: 0.1.0
  file: FGE-RECOMBINATION-REGRESSION-001.py
  suite_sha256: e8990f2c63eafec8b8ea3e97f26c9356ede0f5b34a6c6cc69f7385635a6fd490
  designation: EXPLICIT_DIRECTOR_AUTHORIZATION

expected_projection:
  sha256: c39a990a0e1af57a1e0614e0bbc345fee925e913cb5e417c15afe66c101e6203

proof_receipt:
  object_id: FGE-PROBE-RECOMB-20260922-GAP001-REGRESSION-VERIFIED-001
  receipt_sha256: 940454e9d19c4772311544dd7e677561ed88128679a6a31520a96be935e2916e
```

## Entry contract

A regression-verification cycle may start only when all are available:

1. exact target object ID + version;
2. frozen source SHA256;
3. explicitly designated authoritative regression suite;
4. frozen suite SHA256;
5. expected deterministic output hash or other deterministic replay oracle;
6. declared canon and authority effects.

Missing entry data produces `BLOCKED_REGRESSION_INPUT`, not a guessed substitute.

## Execution map

```text
[01 DESIGNATE]
TARGET + AUTHORITATIVE SUITE
        ↓
[02 FREEZE]
SOURCE SHA + SUITE SHA + EXPECTED OUTPUT SHA
        ↓
[03 VERIFY INPUT]
SOURCE HASH MUST MATCH
SUITE HASH MUST MATCH
        ↓
[04 RUN SUITE UNCHANGED]
ALL DECLARED REGRESSION CASES
        ↓
[05 REQUIRE 100% PASS]
ANY FAILURE → STOP / REGRESSION_UNVERIFIED
        ↓
[06 NEGATIVE CONTROL]
FAULT MUST FAIL CLOSED
        ↓
[07 REPEAT NEGATIVE CONTROL]
FAILURE SEMANTICS MUST MATCH
        ↓
[08 REPLAY]
RUN VALID PATH AGAIN
        ↓
[09 COMPARE OUTPUT]
REPLAY HASH == FROZEN EXPECTED HASH
        ↓
[10 FIREBREAK]
CANON_EFFECT == NONE
AUTHORITY_EFFECT == NONE
SOURCE SHA UNCHANGED
SUITE SHA UNCHANGED
        ↓
[11 RECEIPT]
PRESERVE SUITE RESULT + NEGATIVE CONTROL + REPLAY + HASHES
        ↓
[12 PROJECT PROBE §J]
DETERMINISTIC → REGRESSION_VERIFIED
        ↓
[13 STOP]
PRODUCTION VALIDATION IS A SEPARATE PROOF BOUNDARY
```

## Executable invocation

From this directory:

```bash
# Freeze/verify the authoritative suite externally before execution.
sha256sum fge_recombination_engine.py FGE-RECOMBINATION-REGRESSION-001.py

# Full authoritative regression suite.
python FGE-RECOMBINATION-REGRESSION-001.py --case all --json-out regression-full.json

# Negative control, repeated without changing the suite.
python FGE-RECOMBINATION-REGRESSION-001.py --case negative_control --json-out negative-control-1.json
python FGE-RECOMBINATION-REGRESSION-001.py --case negative_control --json-out negative-control-2.json

# Replay full suite unchanged.
python FGE-RECOMBINATION-REGRESSION-001.py --case all --json-out regression-replay.json

# Recheck source and suite fingerprints after execution.
sha256sum fge_recombination_engine.py FGE-RECOMBINATION-REGRESSION-001.py
```

Required frozen values:

```text
SOURCE_SHA256 = 269232700cb8ba1de66c3033e4b25a897c9d0ebadcc0d9fcf8ce58960bac590d
SUITE_SHA256  = e8990f2c63eafec8b8ea3e97f26c9356ede0f5b34a6c6cc69f7385635a6fd490
OUTPUT_SHA256 = c39a990a0e1af57a1e0614e0bbc345fee925e913cb5e417c15afe66c101e6203
```

## Proof gates

| Gate | Required evidence | Failure state |
|---|---|---|
| G0 Source freeze | source SHA equals frozen SHA before and after | `SOURCE_DRIFT` |
| G1 Suite freeze | suite SHA equals designated SHA before and after | `SUITE_DRIFT` |
| G2 Full regression | 100% tests pass | `REGRESSION_FAILED` |
| G3 Negative control | injected fault is rejected and projection blocked | `FAIL_OPEN` |
| G4 Negative repeat | repeated fault produces equivalent refusal semantics | `FAILURE_NONDETERMINISTIC` |
| G5 Replay | replay output hash equals deterministic baseline | `REPLAY_DRIFT` |
| G6 Canon firebreak | all emitted canon effects are `NONE` | `CANON_EFFECT_BREACH` |
| G7 Authority firebreak | proof scope records `AUTHORITY_EFFECT=NONE` | `AUTHORITY_EFFECT_BREACH` |
| G8 Receipt | all prior gates preserved in one provenance object | `PROOF_INCOMPLETE` |

All gates must pass. There is no partial `REGRESSION_VERIFIED` state.

## Address map

```text
ID1   = target object identity + version
MAT1  = frozen source + authoritative suite
FUNC1 = unchanged regression execution
REL1  = suite → negative control → repeat → replay
VAL1  = G0–G8 proof gates
OUT1  = PROJECT PROBE §J = REGRESSION_VERIFIED
PROV1 = regression verification receipt + hashes
```

## State machine

```text
DETERMINISTIC
  │
  ├─ missing suite/input ─────────────→ BLOCKED_REGRESSION_INPUT
  │
  └─ inputs frozen
       ↓
     REGRESSION_RUNNING
       │
       ├─ any proof gate fails ───────→ REGRESSION_UNVERIFIED
       │
       └─ G0–G8 all pass
            ↓
        REGRESSION_VERIFIED
            ↓
           STOP
```

## Authority and provenance law

```text
SUITE DESIGNATION != CANON PROMOTION
REGRESSION PASS != PRODUCTION VALIDATION
REPLAY EQUALITY != DEPLOYMENT AUTHORIZATION
GENERATED RECEIPT != AUTHORITY
```

The verification process may change only the proof-state projection under Project Probe §J. It may not change source canon, component authority, production status, automation status, or deployment status.

## Current installed instance

`FGE-RECOMBINATION-ENGINE-001@0.1.0` has completed this process with all gates passing. Its current Project Probe §J state is:

```text
REGRESSION_VERIFIED
```

The process terminates there.

REF: FGE-PROBE-20260922-RECOMB-REGVERIFY01
