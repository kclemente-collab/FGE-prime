# FGE Intake Inbox

OBJECT_ID: FGE-GITHUB-INTAKE-INBOX-001
STATUS: ACTIVE_CANDIDATE
CANON_EFFECT: NONE
AUTHORITY_EFFECT: NONE

Drop candidate files here only when they are appropriate for this repository.

## Critical public-repository warning

`kclemente-collab/FGE-prime` is public. **Do not upload private, restricted, intimate, nude, age-uncertain, confidential, credential-bearing, or otherwise sensitive binaries into this inbox.** Once committed to a public Git repository, a later move or delete does not guarantee removal from Git history.

Use a private vault/repository for restricted media. The router intentionally fails closed for unverified binary publication.

## What happens after a drop

1. Hash and fingerprint the file.
2. Read optional FGE sidecar metadata.
3. Classify using declared metadata, embedded FGE headers, schema shape, then file type.
4. Apply collision, identity-pointer, age/consent, and public-binary guards.
5. Route eligible files into `storage_makeover/routed/` candidate staging.
6. Append `storage_makeover/registry/drop-index.jsonl`.
7. Emit a route receipt under `storage_makeover/receipts/routes/`.
8. Send uncertain or review-required objects to `storage_makeover/queues/attention-queue.jsonl`.

Routing never writes canon, never mints identity, and never promotes an object to `ACTIVE_RESOURCE`.

## Canonical sidecar

For important files, add `<filename>.fge.json` beside the file.

Example for a standard public infographic image:

```json
{
  "object_class": "INFOGRAPHIC",
  "domain": "signals",
  "sensitivity": "STANDARD",
  "public_ok": true,
  "origin_class": "GENERATED_OUTPUT",
  "subject_refs": ["SB_330"],
  "entity_state": "RESOLVED"
}
```

For raw / edited / generated image lineage, use one of:

- `RAW_SOURCE`
- `EDITED_DERIVATIVE`
- `GENERATED_OUTPUT`
- `COMPOSITE`

A sidecar is a routing declaration, not authority or canon proof.

## Fail-closed conditions

The router holds instead of guessing when it encounters ambiguity, collision state, unsupported routing, pointer/identity substitution, unreadable content, restricted media, or unverified binary publication.

REF: FGE-STORAGE-20260929-GITHUB-INBOX
