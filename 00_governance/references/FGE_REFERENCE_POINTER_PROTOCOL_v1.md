# FGE Reference Pointer Protocol v1.1

OBJECT_ID: FGE-REFERENCE-POINTER-PROTOCOL-001
VERSION: 1.1.0
CLASS: REFERENCE / RESOLUTION / CIRCUIT_BREAKER INFRASTRUCTURE
STATUS: ACTIVE_SPEC / UNLOCKED
AUTHORITY: FGE GOVERNANCE
CANON_EFFECT: NONE

## 1. Purpose

Provide one stable FGE reference address that resolves to a governed GitHub document without requiring callers to know repository paths, while preventing unresolved pointers from falling back to model memory or semantic guessing.

Core law:

```text
REFERENCE > MEMORY
RESOLVE > INTERPRET
SOURCE > SEMANTIC GUESS
UNKNOWN > INVENTED
```

## 2. Human syntax

```text
[REFERENCE: FGE-CHAR-SKELETON-PAIR-001]
[REFERENCE: FGE-CHAR-SKELETON-PAIR-001@1.0.0]
[REFERENCE: FGE-CHAR-SKELETON-PAIR-001#core-law]
[REFERENCE: FGE-CHAR-SKELETON-PAIR-001@1.0.0#core-law]
```

`@VERSION` pins the governed version. `#ANCHOR` targets an internal document section/field.

## 3. Resolution order

1. Extract exact FGE reference ID.
2. Look up `reference_id` in `FGE_REFERENCE_POINTER_REGISTRY_v1.json`.
3. Verify registry schema before accepting the record.
4. Verify repository and repository-relative path.
5. Resolve live or frozen Git target.
6. Verify explicit `@VERSION` when present.
7. Verify bound Git blob when `blob_sha` is present.
8. Verify requested or registered anchor when present.
9. Preserve record authority, lifecycle state, lock state, and provenance.
10. Classify unresolved conflicts.
11. Only then permit downstream execution.

No step may silently substitute internal model memory for a failed source resolution.

## 4. Pointer modes

### LIVE

`pointer_mode: LIVE`

- `git_ref` is the current source branch/tag.
- `commit_sha` and `blob_sha` may be present as provenance snapshots.
- A changed document does not change reference identity unless the governed object identity changes.

### FROZEN

`pointer_mode: FROZEN`

- `commit_sha` is required.
- `blob_sha` is required.
- Resolution must verify immutable Git evidence.
- Use for locked specifications, releases, audits, evidence, and historical provenance.

## 5. Pointer authority law

A pointer transports access, not authority.

```text
REFERENCE != DOCUMENT
REFERENCE != CANON
REFERENCE != AUTHORIZATION
REFERENCE != MUTATION PERMISSION
PATH != IDENTITY
```

The resolved object retains its own:

```text
STATUS
AUTHORITY
VERSION
PROVENANCE
CANON_EFFECT
LOCKS
CONFLICTS
```

## 6. Registry contract

Registry:

```text
00_governance/references/FGE_REFERENCE_POINTER_REGISTRY_v1.json
```

Typed schema:

```text
00_governance/references/FGE_REFERENCE_POINTER_REGISTRY.schema.json
```

Validator/resolver:

```text
00_governance/references/validate_reference_registry.py
```

The v1.1 registry uses authoritative `records` while preserving legacy `pointers` as a compatibility mirror. The validator must reject intake if the two views diverge.

Typed governance is represented by:

```text
lifecycle_status
lock_state
authority
pointer_mode
```

Legacy display `status` may remain for compatibility but is not the typed execution authority.

## 7. Failure and circuit breaker law

Fault specification:

```text
[REFERENCE: FGE-REFERENCE-RESOLUTION-FAULT-SPEC-001]
```

Failure classes include:

```text
FGE-FAULT-REFERENCE-UNREGISTERED
FGE-FAULT-RESOLUTION-404
FGE-FAULT-RESOLUTION-403
FGE-FAULT-RESOLUTION-TIMEOUT
FGE-FAULT-RESOLUTION-5XX
FGE-FAULT-VERSION-MISMATCH
FGE-FAULT-BLOB-MISMATCH
FGE-FAULT-ANCHOR-MISSING
FGE-FAULT-SCHEMA-INVALID
FGE-FAULT-REGISTRY-COMPAT-DIVERGENCE
```

Distinction:

```text
UNREGISTERED != 404
TIMEOUT != 404
404 = REGISTERED PHYSICAL TARGET ABSENT
```

Execution:

```text
DETERMINISTIC FAILURE
→ HARD LOCK
→ FAULT RECORD
→ NO GENERATION

TRANSIENT FAILURE
→ RETRY
→ IF EXHAUSTED: LOCK
→ FAULT RECORD
→ NO GENERATION
```

Default retryable classes:

```text
TIMEOUT
HTTP 5XX
```

404, 403, version mismatch, blob mismatch, anchor missing, unregistered IDs, and invalid registry schema are non-retryable by default.

## 8. Visual fault boundary

A diagnostic fault surface is a deterministic host-runtime/UI artifact.

```text
RESOLUTION FAILURE
→ DO NOT CALL GROK IMAGINE / IMAGE MODEL
→ RENDER DETERMINISTIC FAULT SURFACE
```

Exact fault IDs, reference strings, and governance labels must not depend on generative image text rendering.

## 9. HEART / BRAIN conflict law

Do not implement `HEART ALWAYS WINS` as an unconditional historical override.

Use:

```text
HEART INVARIANT > UNPROMOTED BRAIN DELTA
```

If developmental evidence produces a possible identity breakpoint:

```text
HEART_N
→ BRAIN EVIDENCE
→ DELTA / CONFLICT
→ BREAKPOINT REVIEW
   ├─ REJECT → HEART_N preserved
   └─ PROMOTE → HEART_N+1 → LINEAGE
```

Laws:

- Unpromoted BRAIN evidence cannot override HEART invariants.
- Promoted breakpoint evidence may authorize a new HEART state.
- Previous HEART states remain preserved in lineage.
- Neither object silently rewrites the other.

## 10. Candidate contradiction presentation

An intentionally rendered unresolved contradiction must be classified as:

```text
FGE-CHAR-STATE-UNCONFIRMED-CONTRADICTION
```

Governance uncertainty belongs in a telemetry wrapper, badge, frame, or metadata layer. It must not automatically mutate scene lighting, color, contrast, character body, or world aesthetics.

```text
FAULT_TELEMETRY != CHARACTER_EXPRESSION
GOVERNANCE_UNCERTAINTY != WORLD_AESTHETIC
```

## 11. Reference ID grammar

Canonical object-ID parser:

```regex
^FGE-(?:[A-Z0-9]+-)+[0-9]{3,}$
```

This replaces the defective `[A-Z0-T]` range and permits the complete A-Z namespace plus numeric segments.

## 12. Runtime gate

Generation or downstream execution is permitted only after required references are:

```text
REGISTERED
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

## 13. Governance laws

- MOVING A FILE MUST UPDATE THE REGISTRY.
- CHANGING A DOCUMENT DOES NOT REQUIRE A NEW REFERENCE ID unless identity changes.
- VERSION CHANGES MUST BE EXPLICIT.
- FROZEN references require immutable Git evidence.
- UNKNOWN > INVENTED.
- CONFLICT > SILENT RECONCILIATION.
- EVIDENCE != CANON.
- DELTA != MUTATION.
- MUTATION REQUIRES PROMOTION.
- LOCK = EXPLICIT.

REF: FGE-GITHUB-REF-20260830-PTR2
