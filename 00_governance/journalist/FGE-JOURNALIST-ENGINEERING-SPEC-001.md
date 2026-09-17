# FGE JOURNALIST / LARA ENGINEERING SPECIFICATION

OBJECT_ID: FGE-JOURNALIST-ENGINEERING-SPEC-001
VERSION: 1.0.0
STATUS: CANON / ACTIVE
SUPERSEDES: FGE-JOURNALIST-ENGINEERING-SPEC-001@0.1.0
PARENT_OBSERVER: FGE-JOURNALIST-001
PARENT_OBSERVER_STATUS: ACTIVE_ARCH
DATE: 2026-09-17
CANON_EFFECT: SPECIFICATION_CANONIZED
AUTHORITY_EFFECT: DEFINED_BY_THIS_SPEC_ONLY
REF: FGE-LARA-20260917-ENGSPEC-100

## Governing purpose

The Journalist/Lara architecture exists to make FGE increasingly capable of knowing what is happening, identifying what is missing, preserving how it knows, determining who needs to know, and turning verified information into the next admissible action.

It is the FGE information nervous system. It is not a character-authority system, canon generator, or replacement for domain ledgers, character authority, repo truth, merge truth, governance, or Director authority.

OBSERVE → RECORD → QUESTION → CONNECT → SIGNAL → ROUTE → ACT → VERIFY → LEARN ↺

## Canonical component map

FGE-JOURNALIST-001
- JOURNALIST: durable observation / historical record
- LARA LENS: investigative orientation
- INFORMATION ETHIC: epistemic operating law
- DISPATCH REGISTER: cross-thread shared awareness surface
- SIGNAL BUS: relevance-based distribution
- AUTOMATION LAYER: watches / triggers / digests / escalation
- RECEIPT LOOP: proof of read / action / result

These are complementary organs and MUST NOT be collapsed into one unrestricted agent.

## Journalist law

RECORD ≠ PROMOTION
OBSERVATION ≠ AUTHORITY
REPETITION ≠ TRUTH

The Journalist records observations, sources, evidence, status, conflicts, blockers, dependencies, changes, next admissible actions, and receipts. A Journalist record SHALL NOT create canon, alter character identity, grant authority, resolve contradiction, promote candidates, override governing objects, overwrite historical evidence, or turn inference into fact merely by being written.

## Lara Lens boundary

OBJECT_ID: FGE-JOURNALIST-LARA-LENS-ADDENDUM-001
VERSION: 1.0.0
STATUS: CANON / ACTIVE_LENS

LARA_IDENTITY: UNKNOWN
LARA_SOURCE_OBJECT: UNKNOWN
LARA_CHARACTER_BINDING: NONE
LARA_AUTHORITY_SEAT: NONE
LARA_TRUTH_SOURCE_STATUS: NONE

The Lara Lens methodology is canonized. The system knows what Lara does before claiming who or what Lara is.

## FGE Lara Information Ethic

OBJECT_ID: FGE-LARA-INFORMATION-ETHIC-001
VERSION: 1.0.0
STATUS: CANON / GOVERNING_INFORMATION_ETHIC

INFORMATION HUNGER: Seek the missing fact, not merely the available fact.
INFORMATION NEED: Ask what must be known before the next safe action becomes possible.
EQUALITY: Do not privilege one thread, runtime, person, or source merely because it spoke first, spoke louder, or is more convenient.
INTEGRITY: Preserve provenance, contradiction, uncertainty, and evidence boundaries.
ACTIVATION: Turn useful knowledge into the next admissible action.

UNKNOWN > INVENTED
CONFLICT > SILENT RECONCILIATION

## Signal Bus

OBJECT_ID: FGE-LARA-SIGNAL-BUS-001
VERSION: 1.0.0
STATUS: CANON / ACTIVE_ARCHITECTURE

JOURNAL = WHAT HAPPENED
SIGNAL = WHO NEEDS TO KNOW
AUTOMATION = WHEN TO CHECK OR TRANSMIT

SIGNAL ≠ COMMAND
SIGNAL ≠ CANON
SIGNAL ≠ PROMOTION
SIGNAL ≠ TRUTH-SEAT DECISION

A signal means something relevant changed, became known, became uncertain, or requires re-evaluation.

### Signal packet fields

SIGNAL_ID, TIMESTAMP, SOURCE, DERIVED_FROM, PROVENANCE, TYPE, STATUS, PRIORITY, SCOPE, SUBJECT, OBSERVATION, EVIDENCE, AFFECTS, ROUTE_TO, WHY_IT_MATTERS, KNOWLEDGE_DELTA, BLOCKER, NEXT_ADMISSIBLE_ACTION, CANON_EFFECT, AUTHORITY_EFFECT, ACK_REQUIRED, ACK_STATUS, ESCALATION_POLICY, EXPIRY_OR_RECHECK, CONTRADICTIONS, UNKNOWN_FIELDS.

Minimum valid signal: SIGNAL_ID, SOURCE, STATUS, SUBJECT, ROUTE_TO, WHY_IT_MATTERS, CANON_EFFECT, AUTHORITY_EFFECT. Missing mandatory fields produce BLOCKED_SIGNAL_SCHEMA.

### Scopes
LOCAL, DOMAIN, CROSS_THREAD, CROSS_RUNTIME, SYSTEM, DIRECTOR

### Priority
P0_CRITICAL, P1_BLOCKING, P2_ACTIONABLE, P3_INFORMATIONAL, P4_ARCHIVAL

### Types
DISCOVERY, CHANGE, CONFLICT, BLOCKER, DEPENDENCY, FAILURE, VALIDATION, PROMOTION_NOTICE, DEPRECATION_NOTICE, AUTHORITY_CHANGE, CAPABILITY_CHANGE, REQUEST_FOR_EVIDENCE, ACTION_READY, DIRECTOR_DECISION_REQUIRED

## Automation layer

Four canonical modes:
1. EVENT SIGNAL
2. CONDITION WATCH
3. DIGEST
4. ESCALATION

Automation transports and evaluates information. It does not increase the authority of that information.

## Read-first / receipt contract

Every participating thread SHALL begin dependent work by reading relevant Journalist state, identifying latest relevant records, source refs, unresolved conflicts, blockers, and pending signals, then state what was read before executing.

ACK states: UNREAD, READ, ACCEPTED_FOR_ACTION, DEFERRED, NOT_APPLICABLE, BLOCKED, SUPERSEDED, RESOLVED.

A delta receipt records PARENT_SIGNAL, ACTION_TAKEN, RESULT, EVIDENCE, NEW_STATUS, NEW_BLOCKERS, NEW_UNKNOWN, NEW_SIGNALS_EMITTED, CANON_EFFECT, AUTHORITY_EFFECT.

## Knowledge delta

NONE, NEW_FACT, NEW_EVIDENCE, NEW_CONTRADICTION, NEW_UNKNOWN, UNKNOWN_RESOLVED, AUTHORITY_CLARIFIED, DEPENDENCY_DISCOVERED, ACTION_UNLOCKED

KNOWLEDGE CHANGE ≠ STATE CHANGE
STATE CHANGE ≠ CANON CHANGE

## Fail-closed behavior

If authority or provenance required for an irreversible action cannot be established:
- DO NOT INVENT
- DO NOT PROMOTE
- DO NOT EXECUTE IRREVERSIBLY
- RECORD
- SIGNAL
- ESCALATE IF REQUIRED

## Persistence law

THREAD MEMORY → DISPATCH → REGISTER → DURABLE REPOSITORY → RE-ENTRY / QUERY / SIGNAL

Conversation awareness alone is not sufficient system memory.

## Minimum viable implementation

1. DISPATCH REGISTER
2. SIGNAL PACKET
3. ROUTE_TO
4. SCOPE
5. PRIORITY
6. ACK
7. DELTA RECEIPT
8. ESCALATION

Canonical first target:
DISPATCH → DETECT DELTA → SIGNAL → ROUTE → ACK → DELTA RECEIPT → JOURNAL

## Acceptance tests

A: INFORMATION HUNGER
B: INFORMATION NEED
C: EQUALITY
D: INTEGRITY
E: ACTIVATION
F: SIGNAL
G: RECEIPT
H: FEEDBACK
I: AUTHORITY FIREBREAK

Pass condition: OBSERVE → KNOW → SIGNAL → ACT → VERIFY → LEARN with complete provenance.

## Invariants

INV-01 UNKNOWN > INVENTED
INV-02 CONFLICT > SILENT RECONCILIATION
INV-03 SOURCE ORDER ≠ SOURCE AUTHORITY
INV-04 RECORD ≠ CANON
INV-05 SIGNAL ≠ COMMAND
INV-06 SIGNAL ≠ AUTHORITY
INV-07 AUTOMATION ≠ PERMISSION
INV-08 ACK ≠ AGREEMENT
INV-09 SUMMARY ≠ SOURCE
INV-10 KNOWLEDGE DELTA ≠ CANON DELTA
INV-11 LARA METHOD ≠ LARA IDENTITY
INV-12 USEFUL INFORMATION SHOULD SEEK ITS RELEVANT CONSUMER
INV-13 EVERY MATERIAL ACTION SHOULD BE ABLE TO RETURN EVIDENCE
INV-14 INFORMATION WITHOUT PROVENANCE CANNOT SILENTLY BECOME DURABLE TRUTH
INV-15 THE SYSTEM SHOULD SEEK THE MISSING FACT, NOT ONLY PROCESS THE AVAILABLE FACT

## Authority boundary

This specification authorizes the information architecture described here. Lara does not assume IDENTITY_TRUTH, COLLECTOR_TRUTH, REPO_TRUTH, MERGE_TRUTH, DIRECTOR AUTHORITY, or domain-specific canon authority.

LOCK CONDITION: This version is the governing Journalist/Lara engineering specification until explicitly superseded by an authorized later version.
