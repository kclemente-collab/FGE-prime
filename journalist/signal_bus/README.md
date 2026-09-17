# FGE Lara Signal Bus

OBJECT_ID: FGE-LARA-SIGNAL-BUS-IMPLEMENTATION-001
VERSION: 1.0.0
STATUS: INSTALLED / ACTIVE_IMPLEMENTATION
PARENT_SPEC: FGE-JOURNALIST-ENGINEERING-SPEC-001@1.0.0
CANON_EFFECT: NONE
AUTHORITY_EFFECT: NONE

## Vertical slice

DISPATCH → DETECT DELTA → SIGNAL → ROUTE → ACK → DELTA RECEIPT → JOURNAL

## Durable paths

- `journalist/dispatches/dispatch_register.jsonl` — machine-readable dispatch ingress
- `journalist/signal_bus/signals.jsonl` — emitted signal ledger
- `journalist/signal_bus/acks.jsonl` — acknowledgement ledger
- `journalist/signal_bus/receipts.jsonl` — delta receipt ledger
- `journalist/signal_bus/state.json` — cursor and deduplication state
- `journalist/signal_bus/bus.py` — runtime
- `.github/workflows/lara-signal-bus.yml` — hourly/manual automation

## Contract

The bus does not grant canon, authority, or permission. It routes information only.

Every emitted signal forces:

- `CANON_EFFECT: NONE`
- `AUTHORITY_EFFECT: NONE`

unless the source dispatch explicitly reports an already-authorized external authority change. Even then, the signal only reports that change; it does not cause it.

## Dispatch input

Each JSONL dispatch should contain at minimum:

```json
{"dispatch_id":"FGE-DISPATCH-...","timestamp":"...","source":"...","status":"VERIFIED","subject":"...","observation":"...","affects":["CHARACTER"],"route_to":["CHARACTER"],"why_it_matters":"...","knowledge_delta":"NEW_EVIDENCE","next_admissible_action":"...","canon_effect":"NONE","authority_effect":"NONE"}
```

Unknown fields are preserved.

## Run

```bash
python journalist/signal_bus/bus.py run
python journalist/signal_bus/bus.py validate
python journalist/signal_bus/bus.py ack FGE-SIGNAL-... READ CHATGPT THREAD_ID
python journalist/signal_bus/bus.py receipt FGE-SIGNAL-... RESOLVED "action" "result"
```

## Fail-closed behavior

Malformed dispatches are not promoted into signals. They are recorded as `BLOCKED_SIGNAL_SCHEMA` signals only when enough source identity exists to preserve provenance. Irreversible work is never executed by this runtime.

## Acceptance target

The implementation is considered VERIFIED only after the integration tests prove:

1. missing-fact detection
2. blocking-vs-nonblocking information need
3. source-order neutrality
4. provenance retention
5. correct route selection
6. ACK persistence
7. delta receipt persistence
8. feedback journal entry
9. authority firebreak

REF: FGE-LARA-20260917-BUS-INSTALL-001
