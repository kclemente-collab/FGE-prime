# FGE Reference Resolution Fault & Circuit Breaker Specification

OBJECT_ID: FGE-REFERENCE-RESOLUTION-FAULT-SPEC-001
VERSION: 1.1.0
CLASS: FAILURE / CIRCUIT_BREAKER / GOVERNANCE_UI
STATUS: PROPOSED / READY_FOR_TEST
AUTHORITY: DIRECTOR
CANON_EFFECT: NONE
PARENT_PROTOCOL: FGE-REFERENCE-POINTER-PROTOCOL-001

## 1. Purpose

Prevent unresolved references, registered-but-uninstalled sources, broken GitHub targets, transient transport faults, version mismatches, blob mismatches, and missing anchors from being silently replaced with model memory or semantic guessing.

Core law:

```text
REFERENCE > MEMORY
RESOLVE > INTERPRET
UNKNOWN > INVENTED
DETERMINISTIC_FAILURE > GENERATION
TRANSIENT_FAILURE > RETRY > LOCK_IF_EXHAUSTED
```

No resolution fault grants creative license.

## 2. Resolution state machine

```text
REFERENCE
   ↓
REGISTRY LOOKUP
   ↓
RESOLUTION_STATE
   ├── SOURCE_MISSING → HARD LOCK
   ├── DEPRECATED_TARGET → HARD LOCK
   └── RESOLVABLE
            ↓
      TARGET RESOLUTION
            ↓
┌───────────────────────┬─────────────────────┐
│ deterministic failure │ transient failure   │
│                       │                     │
│ 404 / 403 / mismatch  │ timeout / 5xx       │
│        ↓              │        ↓            │
│    HARD LOCK          │      RETRY          │
│        ↓              │        ↓            │
│   FAULT RECORD        │ exhausted?          │
│                       │        ↓            │
│                       │      LOCK           │
└───────────────────────┴─────────────────────┘
                         ↓
                  GENERATION FORBIDDEN
```

## 3. Fault taxonomy

### FGE-FAULT-REFERENCE-UNREGISTERED

The FGE OBJECT_ID does not exist in the pointer registry.

This is not HTTP 404 because no physical target was resolved.

Action: hard lock.

### FGE-FAULT-REFERENCE-SOURCE-MISSING

The reference ID is registered as a valid schema/catalog identity, but no physical source document has been installed yet.

This preserves `UNKNOWN > INVENTED` while allowing future objects to be reserved without fake Git paths.

Action: hard lock dependent execution. Do not guess or synthesize the missing source.

### FGE-FAULT-REFERENCE-DEPRECATED-TARGET

The reference is known, but its registered physical target is deprecated for new execution.

Action: hard lock unless an explicit governed replacement is resolved.

### FGE-FAULT-RESOLUTION-404

A registered physical GitHub target was requested and GitHub definitively reports that it does not exist.

Action: hard lock immediately. Do not retry deterministic 404 failures.

### FGE-FAULT-RESOLUTION-403

The target could not be accessed under current authority.

Action: hard lock. Preserve access/authority distinction.

### FGE-FAULT-RESOLUTION-TIMEOUT

Transport failed before resolution could be determined.

Action: retry according to runtime policy. If exhausted, lock.

### FGE-FAULT-RESOLUTION-5XX

GitHub/server returned a transient server-side failure.

Action: retry according to runtime policy. If exhausted, lock.

### FGE-FAULT-VERSION-MISMATCH

Caller requested an explicit @VERSION that differs from the registered version.

Action: hard lock.

### FGE-FAULT-BLOB-MISMATCH

Retrieved content does not produce the registered Git blob SHA.

Action: hard lock. Treat as provenance/integrity failure.

### FGE-FAULT-ANCHOR-MISSING

The document exists but the requested Markdown section/field target does not.

Action: hard lock for requests dependent on that anchor.

### FGE-FAULT-SCHEMA-INVALID

The registry itself does not satisfy the typed registry contract.

Action: reject registry intake and lock dependent execution.

### FGE-FAULT-REGISTRY-COMPAT-DIVERGENCE

Legacy `pointers` compatibility view differs from authoritative `records` view.

Action: reject registry intake.

## 4. Retry policy

Default:

```text
MAX_ATTEMPTS: 3
RETRYABLE:
  - TIMEOUT
  - HTTP_5XX
NON_RETRYABLE:
  - UNREGISTERED
  - SOURCE_MISSING
  - DEPRECATED_TARGET
  - 404
  - 403
  - VERSION_MISMATCH
  - BLOB_MISMATCH
  - ANCHOR_MISSING
  - SCHEMA_INVALID
```

Backoff may increase between attempts, but retry behavior must not alter reference authority or target identity.

## 5. Fault record

```json
{
  "fault_id": "FGE-FAULT-2026-0830-001",
  "fault_class": "FGE-FAULT-RESOLUTION-404",
  "timestamp": "2026-08-30T15:01:00Z",
  "failed_reference": "FGE-CHAR-SKELETON-PAIR-001@1.0.0",
  "target_url": "https://github.com/kclemente-collab/FGE-prime/blob/main/example.md",
  "http_status": 404,
  "retryable": false,
  "action_taken": "GENERATION_LOCKED_HEURISTIC_PREVENTED"
}
```

Fault IDs for individual executions should be unique. Fault classes remain stable.

## 6. Visual Fault Surface

The Visual Fault Surface is a deterministic governance/UI artifact.

It MUST NOT be delegated to Grok Imagine or another generative image model when exact diagnostic text matters.

```text
RESOLUTION FAIL
     ↓
DO NOT CALL IMAGE GENERATOR
     ↓
FAULT SURFACE RENDERER
```

### Canvas

- Dimensions: requested output aspect/dimensions.
- Base fill: `#12131C`.
- Optional 32 px grid: `#1C1E2A`.
- No character/world render behind the fault surface.

### Primary frame

- 48 px interior horizontal margin where dimensions permit.
- 3 px solid border.
- Border: `#E03C3C`.
- Square corners.

### Text

- Monospace UI font supplied by host runtime.
- Header: `[FGE RESOLUTION FAULT CRITICAL]`.
- Header color: `#E03C3C`.
- Metadata color: `#A0A5C0`.
- Must display exact fault class and failed reference.
- Footer: `PIPELINE_LOCKED_PRESERVE_CANON`.

The host renderer chooses available fonts. Font identity is presentation-only and must not affect fault semantics.

## 7. Heart / Brain conflict rule

Do not implement the phrase `HEART ALWAYS WINS` literally.

Use:

```text
HEART INVARIANT
    > UNPROMOTED BRAIN DELTA
```

A validated developmental event may create a legitimate identity breakpoint, but only through promotion:

```text
HEART_N
   ↓
BRAIN EVIDENCE
   ↓
CONFLICT / DELTA
   ↓
BREAKPOINT REVIEW
   ├── REJECT → HEART_N preserved
   └── PROMOTE
           ↓
      HEART_N+1
           ↓
        LINEAGE
```

Laws:

- Unpromoted BRAIN evidence cannot override HEART invariants.
- Promoted breakpoint evidence may authorize a new HEART state.
- Previous HEART states remain preserved in lineage.
- No consumer silently rewrites either object.

## 8. Candidate contradiction rendering

If a requested render intentionally explores an unresolved developmental contradiction, classify the resulting asset:

```text
FGE-CHAR-STATE-UNCONFIRMED-CONTRADICTION
```

The character image itself should not be desaturated, distorted, or otherwise aesthetically mutated merely to signal governance uncertainty.

Use a separate telemetry wrapper:

```text
IMAGE_CONTENT
+
GOVERNANCE_TELEMETRY
```

Telemetry may contain a border, badge, metadata strip, or external wrapper identifying the candidate state.

Law:

```text
FAULT_TELEMETRY != CHARACTER_EXPRESSION
GOVERNANCE_UNCERTAINTY != WORLD_AESTHETIC
```

## 9. Generation gate

Generation is permitted only when all required references satisfy:

```text
REGISTERED
AND RESOLUTION_STATE == RESOLVABLE
AND TARGET_RESOLVED
AND VERSION_VALID
AND BLOB_VALID_IF_BOUND
AND ANCHOR_VALID_IF_REQUIRED
AND AUTHORITY_RESOLVED
AND REQUIRED_CONFLICTS_CLASSIFIED
```

Otherwise:

```text
NO VALID REFERENCE
→ NO GENERATION
```

REF: FGE-REF-20260830-FAULT2
