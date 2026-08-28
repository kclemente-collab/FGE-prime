# FARE Runtime Execution & Telemetry Sandbox (v0.6)

## Component Configuration

- **Object ID:** `FGE-FARE-001`
- **Runtime Reference:** `FGE-FARE-VALIDATION-RECOVERY-001`
- **Ledger Reference:** `FGE-FARE-SERIALIZATION-LEDGER-001`
- **Deployment Status:** `IMPLEMENTED_BRANCH` (Isolated Feature Branch)
- **Canon Effect:** `NONE`
- **Source Authority:** `GOOGLE_SANDBOX_SOURCE_CLAIMED`
- **Source Verification:** `PENDING_EXTERNAL_AUDIT`

## Architectural Boundary Notice

This subdirectory contains the FARE v0.6 browser-based execution and telemetry simulator recovered from the Google Canvas source stream. It is explicitly isolated from the Modular Fashion OS branch and does not promote garment or character data into canon.

`archive/fare_sandbox_v0.6.original.html` preserves the recovered source without corrective edits. `index.html` is the executable entrypoint and contains one documented source-repair patch.

## Verification Lifecycle

The entrypoint exercises the sequence:

1. **MUTATE** — captures transient tint, material and waist-morph parameter changes.
2. **VALIDATE** — evaluates garment fit envelopes and rights/platform policies.
3. **RECOVER** — routes recoverable tint/material violations and stability-budget scenarios.
4. **COMMIT / ROLLBACK** — updates the browser simulation state and emits a JSON telemetry packet.

## Source Audit Findings

The recovered source supports the following classifications:

- Fit gate logic: **IMPLEMENTED IN BROWSER JAVASCRIPT**
- Rights/platform gate logic: **IMPLEMENTED IN BROWSER JAVASCRIPT**
- Skeletal-zone visualization: **IMPLEMENTED IN BROWSER JAVASCRIPT**
- V1–V6 preset controls: **IMPLEMENTED**, with V6 currently sharing the corrupted-licensor trigger used by V5
- Relational ledger rows: **EMULATED IN MEMORY**, not a live SQL database
- Append-only persistence: **SIMULATED**, not externally persistent
- Hash chain: **MOCK DETERMINISTIC HASH**, not cryptographic SHA-256
- True crash/restart/restore persistence: **NOT IMPLEMENTED IN THIS SOURCE**

## Applied Patch

### `FARE-PATCH-001_ROW_IDENTITY_DOM_BINDING`

The recovered source calls:

```js
document.getElementById("row-identity").textContent = `${dbRows.identity} rows`;
```

but the original HTML omitted the matching `row-identity` element. The executable `index.html` repairs that DOM binding by replacing the malformed identity row with:

```html
<span class="text-slate-500">fare_asset_identity:</span>
<span id="row-identity" class="text-slate-300 font-bold">3 rows</span>
```

The archived source remains unchanged.

## Directory Manifest

- `index.html` — repaired executable sandbox entrypoint
- `manifest.json` — governed deployment metadata
- `README.md` — architecture, provenance and audit notes
- `archive/fare_sandbox_v0.6.original.html` — preserved recovered source

## Promotion Boundary

Merging this branch promotes code into the repository only. It does not promote any garment, character, runtime observation or generated telemetry into FGE canon.
