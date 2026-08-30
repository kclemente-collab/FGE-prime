# FGE Reference Pointer Protocol v1.0

OBJECT_ID: FGE-REFERENCE-POINTER-PROTOCOL-001
VERSION: 1.0.0
CLASS: REFERENCE / RESOLUTION INFRASTRUCTURE
STATUS: ACTIVE_SPEC / UNLOCKED
AUTHORITY: FGE GOVERNANCE
CANON_EFFECT: NONE

## Purpose

Provide one stable FGE reference tag that can resolve to a document stored in GitHub without requiring the caller to know the repository path.

## Human syntax

```text
[REFERENCE: FGE-CHAR-SKELETON-PAIR-001]
```

Optional precision:

```text
[REFERENCE: FGE-CHAR-SKELETON-PAIR-001@1.0.0]
[REFERENCE: FGE-CHAR-SKELETON-PAIR-001#section-or-field]
```

## Resolution law

A reference ID is an FGE identity pointer, not a filename.

Resolution order:

1. Find `reference_id` in `FGE_REFERENCE_POINTER_REGISTRY_v1.json`.
2. Verify `repository`.
3. Resolve `path`.
4. Use `git_ref` for the live/current document view.
5. If `commit_sha` or `blob_sha` is present, use it when an immutable historical source is required.
6. Apply `anchor` or the caller's `#path` when supplied.
7. Return `UNKNOWN_REFERENCE` if no registered pointer exists.
8. Never infer or invent a missing target.

## Pointer record

```json
{
  "reference_id": "FGE-EXAMPLE-001",
  "title": "Example document",
  "repository": "kclemente-collab/FGE-prime",
  "path": "path/to/document.md",
  "git_ref": "main",
  "commit_sha": null,
  "blob_sha": null,
  "anchor": null,
  "version": "1.0.0",
  "status": "ACTIVE",
  "authority": "FGE GOVERNANCE",
  "provenance": "REGISTERED",
  "aliases": [],
  "tags": []
}
```

## Live vs frozen pointers

### LIVE

`git_ref: main` resolves the current governed file at its registered path.

Use for operational documents expected to evolve.

### FROZEN

`commit_sha` and/or `blob_sha` binds the reference to exact Git content.

Use for evidence, locked specifications, releases, audits, tests, and historical provenance.

A live pointer may also carry a frozen revision so current state and historical evidence remain distinguishable.

## Governance laws

- REFERENCE != DOCUMENT.
- REFERENCE != CANON.
- PATH != IDENTITY.
- MOVING A FILE MUST UPDATE THE REGISTRY.
- CHANGING A DOCUMENT DOES NOT REQUIRE CHANGING ITS REFERENCE ID unless its identity changes.
- VERSION CHANGES MUST BE EXPLICIT.
- LOCKED/FROZEN references SHOULD carry immutable Git evidence.
- UNKNOWN > INVENTED.
- CONFLICT > SILENT RECONCILIATION.

## Registry

Canonical registry file for this protocol:

```text
00_governance/references/FGE_REFERENCE_POINTER_REGISTRY_v1.json
```

## Runtime behavior

When an FGE runtime sees:

```text
REFERENCE: <FGE-ID>
```

it should treat `<FGE-ID>` as a lookup key into the reference registry, retrieve the GitHub target, and preserve the target's own authority/status/provenance rather than promoting it merely because it was referenced.

REF: FGE-GITHUB-REF-20260830-PTR1
