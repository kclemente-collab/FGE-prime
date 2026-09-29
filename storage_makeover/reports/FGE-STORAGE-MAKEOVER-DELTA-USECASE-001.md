# FGE Storage Makeover · Delta + Use Case Analysis

OBJECT_ID: FGE-STORAGE-MAKEOVER-DELTA-USECASE-001
VERSION: 0.1.0
STATUS: ACTIVE_CANDIDATE / MIRROR_REPORT
CANON_EFFECT: NONE
AUTHORITY_EFFECT: NONE

## Delta report

### Before
- Files could exist without durable object addresses.
- Infographics and payloads did not have dedicated first-class indexes.
- Search depended too heavily on filenames, repository browsing, or source-specific memory.
- New resources could appear without an explicit attention event or promotion receipt.
- Heavy media, generated imagery, edited imagery and source imagery could be discoverable without a common lineage/index contract.
- Niche infographics were strong visually but weakly addressable as reusable machine-readable intelligence surfaces.

### After
- `FGE-STORAGE-MAKEOVER-001` becomes the candidate parent for the storage migration plane.
- `FGE-INFOGRAPHIC-PAYLOAD-HUB-001` defines addressable homes for infographic and payload objects.
- `FGE-UNIFIED-OBJECT-INDEX-001` establishes a search-first structural layer.
- `FGE-ATTENTION-QUEUE-001` gives unresolved/high-value objects an explicit action path.
- `FGE-STORAGE-PROMOTION-BUS-001` separates storage promotion from canon promotion and makes reusable resources announceable.
- Eight current niche infographics are hydrated into the infographic index.
- Two artifact renders are preserved as related visual assets rather than being flattened into infographic semantics.
- Six reusable payload classes are indexed, including character compiler, signal, mastery primitive, scene governance, presentation and storage-promotion packets.
- A Grok entry point exposes deterministic read order and governance laws.

## Use case analysis

### UC-01 · Grok bootstrap
Query: "What FGE storage resources should I read first?"
Route: `GROK_ENTRYPOINT.md` → manifest → indexes → queues → source pointer.
Value: reduces blind repository search and keeps authority boundaries visible.

### UC-02 · Find an infographic by function
Query: "Which infographic handles scene parameter governance?"
Route: infographic index → `FGE-INFO-000007` → declared domains and payload refs.
Value: function-based lookup instead of filename archaeology.

### UC-03 · Preserve niche infographic value
Query: "Can the signal engine learn from SIREN without replacing SIREN?"
Route: infographic index → signal compatibility class → permitted depth/lenses.
Value: interoperability without flattening specialist systems.

### UC-04 · Payload routing
Query: "Which packet should leave the character compiler?"
Route: payload index → `CHARACTER_COMPILER_PACKET` → destinations + constraints.
Value: cross-app consistency across Grok, iOS, factory and Notion.

### UC-05 · Attention discovery
Query: "What needs review now?"
Route: attention queue ordered by priority.
Value: no silent orphaning of new resources.

### UC-06 · Storage promotion
Query: "What is indexed but not yet an active reusable resource?"
Route: promotion queue → gate → receipt.
Value: promotion becomes observable and reversible without implying canon.

### UC-07 · Image derivation and signal intelligence
Query: "Which visual surfaces can feed emotional-signal reproduction?"
Route: infographic index → CLASS_A/B/C compatibility → signal payloads.
Value: source-bound emotional/contextual intelligence while preserving source identity.

### UC-08 · Artifact preservation
Query: "What can be learned from the heart pendant or Siren Seal render?"
Route: related visual assets → form/material/brand lenses only by default.
Value: meaning extraction without unsupported character-emotion inference.

### UC-09 · Generated/edit lineage
Query: "Is this image raw, edited, generated or composite?"
Route: source normalizer / future visual lineage registry → source-native pointer.
Value: prevents generated output from laundering itself into source evidence.

### UC-10 · Sensitive/adult visual routing
Query: "Can a restricted adult visual contribute useful information?"
Route: sensitivity gate → safe derivative packet → index pointer.
Value: preserves operational value while limiting binary exposure and preventing automatic publication/canon effects.

### UC-11 · Cross-system discovery
Query: "Which systems can consume this signal packet?"
Route: payload index → destination targets → dependent system pointers.
Value: turns the storage plane into a capability map rather than a folder tree.

### UC-12 · iPhone-first dump workflow
Action: user drops material into an inbox.
Route: inbox → separator → normalizer → M21/M22/M23 → address → index → queue.
Value: the user can capture first and organize later without losing traceability.

## Primary risks
- indexing generated claims as source truth
- binary duplication without lineage
- overinterpreting niche graphics through a universal emotional lens
- storage promotion being mistaken for canon promotion
- source pointers becoming stale or unverified
- private/sensitive binaries entering a public mirror

## Controls
- source-native routing
- explicit provenance and object class
- CLASS_A / CLASS_B / CLASS_C derivation compatibility
- attention and promotion gates
- no silent mutation / no silent promotion
- GitHub mirrors metadata and text intelligence; sensitive/heavy binaries remain in declared vaults unless explicitly mirrored

## Acceptance state
The architecture is useful immediately as a searchable mirror, but individual infographic rows remain CANDIDATE until source binaries/pointers and declared relationships are verified.

REF: FGE-STORAGE-20260928-DELTA-USECASE
