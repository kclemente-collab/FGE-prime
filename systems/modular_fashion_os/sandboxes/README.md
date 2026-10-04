# FGE FARE v0.6 — Persistent Evidence Engine Sandbox

**Object:** `FGE-FARE-SERIALIZATION-LEDGER-001`  
**File:** [`FGE-FARE-v0.6-serialization-ledger.html`](FGE-FARE-v0.6-serialization-ledger.html)  
**Version:** `0.6.1`  
**Status:** `REVIEWED_CANDIDATE_ARCHITECTURE`  
**Canon effect:** `NONE`  
**Execution authority:** `CANDIDATE`  
**Parent:** `FGE-SYS-MODULAR-FASHION-OS-001` / `FGE-SPEC-LAYERED-FASHION-DB-001`  
**Source:** Google-constructed single-file sandbox, reconstructed into repo form.

Single-file runtime harness for fashion-asset evidence. It does **not** mutate Character OS gospel. It evaluates a three-garment stack against fit, rights, platform, and stability gates, then emits a v0.6 serialization packet.

## What it proves

| Scenario | Intent | Disposition |
|----------|--------|-------------|
| V1 Denied color tint | Corset `allow_tint: false` | Recoverable — restore authorized default |
| V2 Unauthorized platform | `UnauthorizedWebClient` | Terminal — terminate asset |
| V3 Fit morph budget | Waist `0.82` vs corset `[0.35, 0.52]` + 6 mm cap | Terminal — reject garment |
| V4 Envelope oscillation | Stability budget 3/3 | Quarantine — no LKG commit |
| V5 Corrupted rights | Licensor signature invalid | Fail closed |
| V6 Post-crash revocation | Start corrupted, restart against LKG hash | Reverify + append recovery/provenance |

## Ledger tables (emulated)

`fare_asset_identity` · `fare_mutation_attempt` · `fare_validation_event` · `fare_recovery_event` · `fare_validated_checkpoint` · `fare_provenance_event`

These are evidence tables, not the product registry. DDL lives in [`../schema/layered_fashion_module.sql`](../schema/layered_fashion_module.sql) (section 8). Product truth stays in Storage. FARE only records what the runtime *did*. Soft-link via `sku_identifier` / `garment_runtime_id`. No cascade into `digital_assets_registry`. `fare_runtime_frame` is a serialization packet, not a table.

## Authority split

```text
STORAGE        garment identity + rights source
FARE SANDBOX   validation / recovery / LKG evidence
DISPLAY        viewport stack + skin-zone map (ephemeral)
CHARACTER OS   authorization (this sandbox cannot lock)
```

Open the HTML locally or via GitHub raw preview. No build step. Tailwind + JetBrains Mono load from CDN.
