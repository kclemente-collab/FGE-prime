# FGE Character Skeleton · Template Pair

OBJECT_ID: FGE-CHAR-SKELETON-PAIR-001
VERSION: 1.0.0
CLASS: MINIMUM_VIABLE_CHARACTER_SKELETON / TEMPLATE_PAIR
STATUS: PROPOSED / UNLOCKED
AUTHORITY: DIRECTOR
CANON_EFFECT: NONE_UNLESS_PROMOTED
REFERENCE_FAMILY: MVT.FGE.BRAIN.HEART

## Purpose

Define the minimum viable FGE character skeleton before flesh, wardrobe, mythology, visuals, dialogue, story, render, or commerce are added.

The paired system separates identity mechanics from developmental mechanics while preserving continuity, evidence, uncertainty, and governed mutation.

## Pair

### HEART

Role: identity / attractor / behavioral mechanics.

Carries:
- identity
- core attractors
- behavioral genome
- perception
- interpretation
- preference
- knowledge
- ritual
- language
- reaction
- relationship
- choice and sacrifice logic
- components and slot contracts
- chemistry
- identity invariants
- permitted and forbidden mutations
- breakpoints and lineage split rules
- fingerprint
- canon status, registry ID, provenance, version

### BRAIN

Role: developmental / experience / evidence mechanics.

Carries:
- events and context
- participants
- witnesses / journalists / observers
- observations
- predictions
- evidence
- expected and observed delta
- questions
- competing hypotheses
- proposed tests
- predicted and actual manifestations
- consequences
- discoveries and candidate traits
- governance review
- proposed canon deltas
- registry updates
- lineage state transitions

## Core law

HEART generates predictions.
BRAIN generates evidence.
Neither can silently rewrite the other.

A Brain discovery becomes a Heart mutation only through:

1. OBSERVED
2. CANDIDATE
3. REVIEW
4. PROMOTED

EVIDENCE != CANON.
DELTA != MUTATION.
UNKNOWN > INVENTED.
CONFLICT > SILENT_RECONCILIATION.
LOCK = EXPLICIT.

## Development loop

```text
HEART
  -> PREDICTION
  -> EXPERIENCE
  -> OBSERVATION
  -> EVIDENCE
  -> DELTA
  -> CONDUCTION
  -> TEST
  -> REVIEW
  -> REJECT | PROMOTE
  -> AUTHORIZED_MUTATION
  -> HEART STATE N+1
  -> LINEAGE
```

## Mutation operators

```text
ADD
AMPLIFY
REDUCE
REPLACE
PRESERVE
CONSTRAIN
RELATE
REMOVE
LOCK
```

## Identity fingerprint domains

```text
notices
ignores
preferences
repeats
cannot_resist
speaks
thinks
decides
reacts
becomes
silhouette
material
lighting
color
texture
composition
visual_invariants
```

## Reference protocol

Resolve this document through:

```text
[REFERENCE: FGE-CHAR-SKELETON-PAIR-001]
```

Optional precision:

```text
[REFERENCE: FGE-CHAR-SKELETON-PAIR-001@1.0.0]
[REFERENCE: FGE-CHAR-SKELETON-PAIR-001#core-law]
```

Registry:

```text
00_governance/references/FGE_REFERENCE_POINTER_REGISTRY_v1.json
```

Protocol:

```text
[REFERENCE: FGE-REFERENCE-POINTER-PROTOCOL-001]
```

## Preserved semantic conflict

The source material also contained an alternate mapping in which Heart was described as "what happened" and Brain as "attractors." This conflicts with the dominant architecture above where HEART = identity mechanics and BRAIN = developmental/evidence mechanics.

STATUS: UNRESOLVED_CONCEPT_MAPPING
CANON_EFFECT: NONE

The conflict is preserved for explicit Director resolution rather than silently reconciled.

REF: FGE-CHAR-20260830-SKEL1

---

# FGE CHARACTER SKELETON · REFERENCE INDEX SYSTEM

OBJECT_ID: FGE-REF-CHAR-SKELETON-INDEX-001  
VERSION: 1.0.0  
CLASS: REFERENCE / INDEXING / CONTINUITY INFRASTRUCTURE  
STATUS: PROPOSED / READY_FOR_REGISTRATION  
ROOT_REFERENCE: FGE-CHAR-SKELETON-PAIR-001  
FAMILY_ALIAS: MVT.FGE.BRAIN.HEART  
CANON_EFFECT: NONE  
AUTHORITY: DIRECTOR  
SOURCE: USER-SUPPLIED CHARACTER SKELETON PAIR + DERIVED INDEX ARCHITECTURE

## 0. PURPOSE

Create a permanent addressing system for the minimum viable FGE character organism.

It allows any:

- document
- story
- test
- character
- observation
- prompt
- compiler
- database row
- RAG chunk
- image-generation process
- developmental experiment
- cross-runtime handoff

to reference the same underlying character concepts without copying the whole specification.

The root address is:

```text
[REFERENCE: FGE-CHAR-SKELETON-PAIR-001]
```

Everything below it becomes part of one searchable reference family.

---

## 1. REFERENCE LAW

The important distinction is:

```text
OBJECT ID     = identity of the thing
REFERENCE     = pointer to the thing
TAG           = semantic search classification
PATH          = pointer inside the thing
RELATION      = declared connection between things
VERSION       = state of the thing at a point in time
STATUS        = governance condition
```

Therefore:

```text
FGE-CHAR-HEART-001
```

is not the same thing as:

```text
FGE-CHAR-HEART-001@1.0.0
```

and neither is the same as:

```text
FGE-CHAR-HEART-001#behavioral_genome.choice.sacrifice_logic
```

The first identifies the object.

The second identifies a version.

The third identifies a precise location inside the object.

This gives FGE a proper coordinate system for ideas. 🧭

---

## 2. UNIVERSAL REFERENCE SYNTAX

### A. Object reference

```text
[REFERENCE: FGE-CHAR-HEART-001]
```

Use when referring to an entire governed object.

### B. Version reference

```text
[REFERENCE: FGE-CHAR-HEART-001@1.2.0]
```

Use when exact historical state matters.

### C. Field reference

```text
[REFERENCE: FGE-CHAR-HEART-001#core_attractors.A01]
[REFERENCE: FGE-CHAR-HEART-001#behavioral_genome.perception.notices]
[REFERENCE: FGE-CHAR-HEART-001#identity_invariants.must_survive]
```

This avoids spawning unnecessary IDs for every little field.

### D. Relationship reference

```text
[RELATION:
 FGE-CHAR-HEART-001
 --PAIRED_WITH-->
 FGE-CHAR-BRAIN-001
]
```

### E. Evidence reference

```text
[EVIDENCE_REF: FGE-CHAR-EVIDENCE-001]
```

### F. Provenance reference

```text
[PROVENANCE_REF: FGE-CHAR-PROVENANCE-001]
```

### G. Conflict reference

```text
[CONFLICT_REF: FGE-CHAR-CONTRADICTION-001]
```

A conflict gets preserved, not erased.

---

## 3. STANDARD REFERENCE HEADER

Every future character-system artifact can carry this tiny header:

```text
REFERENCE: FGE-CHAR-SKELETON-PAIR-001
OBJECT_ID: <OBJECT>
VERSION: <VERSION>
STATUS: <STATUS>
AUTHORITY: <AUTHORITY>
PARENT_REFS:
  - <REF>
RELATION_REFS:
  - <REF>
TAGS:
  - <SEMANTIC TAG>
PROVENANCE:
  - <SOURCE>
CANON_EFFECT: NONE | PROPOSED_DELTA | AUTHORIZED_WRITE
```

That is enough to make the object indexable across ChatGPT, Grok, Claude, Gemini, GitHub, databases, Drive, Notion, or a future FGE registry.

---

## 4. SEMANTIC TAG LANGUAGE

References identify things.

Tags identify what kinds of things they are.

Use dot notation.

```text
FGE.CHAR
FGE.CHAR.SKELETON
FGE.CHAR.IDENTITY
FGE.CHAR.HEART
FGE.CHAR.BRAIN
FGE.CHAR.ATTRACTOR
FGE.CHAR.BEHAVIOR
FGE.CHAR.GENOME
FGE.CHAR.CHEMISTRY
FGE.CHAR.EXPERIENCE
FGE.CHAR.EVIDENCE
FGE.CHAR.OBSERVATION
FGE.CHAR.JOURNALIST
FGE.CHAR.DELTA
FGE.CHAR.CONDUCTION
FGE.CHAR.HYPOTHESIS
FGE.CHAR.TEST
FGE.CHAR.SIMULATION
FGE.CHAR.LEARNING
FGE.CHAR.MUTATION
FGE.CHAR.BREAKPOINT
FGE.CHAR.LINEAGE
FGE.CHAR.FINGERPRINT
FGE.CHAR.MANIFESTATION
FGE.CHAR.TRAJECTORY
FGE.CHAR.GOVERNANCE
FGE.CHAR.CANON
FGE.CHAR.REGISTRY
FGE.CHAR.PROVENANCE
FGE.CHAR.CONTRADICTION
```

### Family super-tag

```text
MVT.FGE.BRAIN.HEART
```

Alias:

```text
FGE.CHAR.SKELETON.PAIR
```

Both resolve toward:

```text
FGE-CHAR-SKELETON-PAIR-001
```

---

## 5. MASTER REFERENCE LIBRARY

### A. ROOT / ORGANISM

| Reference | Classification | Purpose |
|---|---|---|
| `FGE-CHAR-SKELETON-PAIR-001` | ROOT / TEMPLATE_PAIR | Minimum viable character skeleton |
| `FGE-REF-CHAR-SKELETON-INDEX-001` | REFERENCE_INDEX | Governs this reference family |
| `FGE-CHAR-SKELETON-CONTRACT-001` | PAIRING_CONTRACT | Governs Heart ↔ Brain interaction |
| `FGE-CHAR-ORGANISM-001` | CHARACTER_CONTAINER | Whole developmental character organism |
| `FGE-CHAR-STATE-001` | STATE_OBJECT | Character condition at revision N |

---

## 6. HEART / IDENTITY LIBRARY 🫀

| Reference | Function |
|---|---|
| `FGE-CHAR-HEART-001` | Heart master template |
| `FGE-CHAR-IDENTITY-001` | Identity definition |
| `FGE-CHAR-ATTRACTOR-001` | Core attractor schema |
| `FGE-CHAR-BEHAVIOR-GENOME-001` | Behavioral mechanics |
| `FGE-CHAR-PERCEPTION-001` | Notices / ignores / sensitivity |
| `FGE-CHAR-INTERPRETATION-001` | Meaning assignment |
| `FGE-CHAR-PREFERENCE-001` | Seeks / avoids / cannot resist |
| `FGE-CHAR-KNOWLEDGE-001` | Knows / believes / unknown |
| `FGE-CHAR-RITUAL-001` | Repetition / protection / requirement |
| `FGE-CHAR-LANGUAGE-001` | Character linguistic fingerprint |
| `FGE-CHAR-REACTION-001` | Response mechanics |
| `FGE-CHAR-RELATIONSHIP-001` | Attachment / distrust / protection |
| `FGE-CHAR-CHOICE-001` | Decision logic |
| `FGE-CHAR-SACRIFICE-LOGIC-001` | What the character gives up first |
| `FGE-CHAR-BOUNDARY-LOGIC-001` | Recurring behavioral limits |
| `FGE-CHAR-TRAJECTORY-001` | Repeated-result developmental direction |

---

## 7. STRUCTURAL GENOME LIBRARY

| Reference | Function |
|---|---|
| `FGE-CHAR-GENOME-001` | Character structural genome |
| `FGE-CHAR-COMPONENT-001` | Component definition |
| `FGE-CHAR-SLOT-CONTRACT-001` | Accept/reject/mutation contract |
| `FGE-CHAR-DEPENDENCY-001` | Structural dependency |
| `FGE-CHAR-CONTRADICTION-001` | Preserved unresolved contradictions |
| `FGE-CHAR-CHEMISTRY-001` | Inter-component interaction |
| `FGE-CHAR-AMPLIFIER-001` | Chemistry amplifier |
| `FGE-CHAR-SUPPRESSOR-001` | Chemistry suppressor |
| `FGE-CHAR-EMERGENT-CANDIDATE-001` | Emergent property candidate |

---

## 8. IDENTITY PRESERVATION LIBRARY

| Reference | Function |
|---|---|
| `FGE-CHAR-IDENTITY-INVARIANT-001` | Governs identity survival |
| `FGE-CHAR-MUST-SURVIVE-001` | Non-negotiable identity |
| `FGE-CHAR-MAY-CHANGE-001` | Mutable identity territory |
| `FGE-CHAR-BREAKPOINT-001` | Identity rupture threshold |
| `FGE-CHAR-LINEAGE-SPLIT-001` | Rules for descendant identity |
| `FGE-CHAR-FINGERPRINT-001` | Recognition fingerprint |

Fingerprint fields may be addressed directly:

```text
FGE-CHAR-FINGERPRINT-001#notices
FGE-CHAR-FINGERPRINT-001#ignores
FGE-CHAR-FINGERPRINT-001#preferences
FGE-CHAR-FINGERPRINT-001#repeats
FGE-CHAR-FINGERPRINT-001#cannot_resist
FGE-CHAR-FINGERPRINT-001#speaks
FGE-CHAR-FINGERPRINT-001#thinks
FGE-CHAR-FINGERPRINT-001#decides
FGE-CHAR-FINGERPRINT-001#reacts
FGE-CHAR-FINGERPRINT-001#becomes
FGE-CHAR-FINGERPRINT-001#silhouette
FGE-CHAR-FINGERPRINT-001#material
FGE-CHAR-FINGERPRINT-001#lighting
FGE-CHAR-FINGERPRINT-001#color
FGE-CHAR-FINGERPRINT-001#texture
FGE-CHAR-FINGERPRINT-001#composition
FGE-CHAR-FINGERPRINT-001#visual_invariants
```

---

## 9. MUTATION LIBRARY

```text
REFERENCE: FGE-CHAR-MUTATION-001
```

### Operators

```text
ADD
AMPLIFY
REDUCE
REPLACE
PRESERVE
CONSTRAIN
RELATE
REMOVE
LOCK
```

Supporting references:

| Reference | Purpose |
|---|---|
| `FGE-CHAR-MUTATION-001` | Mutation envelope |
| `FGE-CHAR-MUTATION-PERMITTED-001` | Allowed mutations |
| `FGE-CHAR-MUTATION-FORBIDDEN-001` | Forbidden mutations |
| `FGE-CHAR-MUTATION-RECEIPT-001` | Records actual mutation |
| `FGE-CHAR-PRESERVED-INVARIANT-001` | Records what survived |

---

## 10. BRAIN / DEVELOPMENT LIBRARY 🧠

### Proposed Template B

```text
REFERENCE: FGE-CHAR-BRAIN-001
CLASS:
DEVELOPMENT / EXPERIENCE / EVIDENCE ORGANISM
PURPOSE:
Determine what experience reveals about the character without
silently rewriting the Heart.
```

Core fields:

```yaml
FGE_CHARACTER_BRAIN:
  identity:
    brain_id:
    character_id:
    heart_ref:
    revision:
  experience:
    event_id:
    context:
    participants:
    witnesses:
    actions:
    consequences:
    notable_interactions:
  observation:
    observation_id:
    observer:
    observed:
    source:
    reliability:
    uncertainty:
  prediction:
    prediction_ref:
    predicted_manifestation:
  evidence:
    evidence_id:
    supports:
    contradicts:
    evidence_strength:
    provenance:
  delta:
    expected:
    observed:
    category:
    magnitude:
    uncertainty:
  conduction:
    question:
    competing_hypotheses:
    proposed_test:
    expected_outcomes:
    actual_outcome:
  learning:
    discoveries:
    candidate_traits:
    candidate_attractors:
    candidate_components:
    candidate_relationships:
    candidate_language:
    candidate_trajectories:
  governance:
    classification:
    reviewer:
    rationale:
    proposed_heart_delta:
    registry_update:
  lineage:
    parent_state_ref:
    mutation_ref:
    preserved_invariants:
    actual_delta:
    descendant_state_ref:
```

---

## 11. EXPERIENCE / EVIDENCE LIBRARY

| Reference | Function |
|---|---|
| `FGE-CHAR-EXPERIENCE-001` | Life-event envelope |
| `FGE-CHAR-EVENT-001` | Individual event |
| `FGE-CHAR-PARTICIPANT-001` | Event participant |
| `FGE-CHAR-WITNESS-001` | Witness |
| `FGE-CHAR-JOURNALIST-001` | Structured observer role |
| `FGE-CHAR-OBSERVATION-001` | Observation record |
| `FGE-CHAR-EVIDENCE-001` | Evidence object |
| `FGE-CHAR-PREDICTION-001` | Heart-generated prediction |
| `FGE-CHAR-MANIFESTATION-001` | Actual expressed behavior |
| `FGE-CHAR-CONSEQUENCE-001` | Result of action |
| `FGE-CHAR-INTERACTION-001` | Significant character interaction |

---

## 12. DELTA / UNCERTAINTY LIBRARY

```text
REFERENCE: FGE-CHAR-DELTA-001
```

Children:

```text
FGE-CHAR-DELTA-EXPECTED-001
FGE-CHAR-DELTA-OBSERVED-001
FGE-CHAR-DELTA-CATEGORY-001
FGE-CHAR-DELTA-MAGNITUDE-001
FGE-CHAR-UNCERTAINTY-001
```

Concept:

```text
PREDICTED CHARACTER
        │
        ▼
   EXPERIENCE
        │
        ▼
OBSERVED CHARACTER
        │
        ▼
      DELTA
```

Delta is not automatically mutation.

That distinction is critical.

---

## 13. CONDUCTION / CURIOSITY LIBRARY ⚡

| Reference | Function |
|---|---|
| `FGE-CHAR-CONDUCTION-001` | Curiosity/action engine |
| `FGE-CHAR-QUESTION-001` | Developmental question |
| `FGE-CHAR-HYPOTHESIS-001` | Candidate explanation |
| `FGE-CHAR-TEST-001` | Test definition |
| `FGE-CHAR-SIMULATION-001` | Controlled developmental simulation |
| `FGE-CHAR-EXPECTED-OUTCOME-001` | Predicted result |
| `FGE-CHAR-ACTUAL-OUTCOME-001` | Observed result |

Canonical logic remains:

```text
QUESTION
   ↓
COMPETING HYPOTHESES
   ↓
TEST
   ↓
MANIFESTATION
   ↓
OBSERVATION
   ↓
EVIDENCE
   ↓
DELTA
```

---

## 14. LEARNING LIBRARY

```text
FGE-CHAR-LEARNING-001
FGE-CHAR-DISCOVERY-001
FGE-CHAR-TRAIT-CANDIDATE-001
FGE-CHAR-ATTRACTOR-CANDIDATE-001
FGE-CHAR-COMPONENT-CANDIDATE-001
FGE-CHAR-RELATIONSHIP-CANDIDATE-001
FGE-CHAR-LANGUAGE-CANDIDATE-001
FGE-CHAR-TRAJECTORY-CANDIDATE-001
```

A learning object means:

```text
"We learned something worth examining."
```

It does not mean:

```text
"This is now canon."
```

---

## 15. PROMOTION GATE

```text
REFERENCE: FGE-CHAR-PROMOTION-GATE-001
```

The supplied rule becomes an explicit pipeline:

```text
OBSERVED
   ↓
CANDIDATE
   ↓
REVIEW
   ↓
PROMOTED
```

Expanded:

```text
BRAIN DISCOVERY
     │
     ▼
OBSERVATION
     │
     ▼
EVIDENCE
     │
     ▼
CANDIDATE_DELTA
     │
     ▼
REVIEW
     │
 ┌───┴────┐
 │        │
REJECT   PROMOTE
          │
          ▼
AUTHORIZED_MUTATION
          │
          ▼
HEART STATE N+1
```

Supporting references:

```text
FGE-CHAR-REVIEW-001
FGE-CHAR-PROMOTION-001
FGE-CHAR-REJECTION-001
FGE-CHAR-AUTHORIZED-MUTATION-001
```

---

## 16. LINEAGE LIBRARY

| Reference | Function |
|---|---|
| `FGE-CHAR-LINEAGE-001` | Developmental ancestry |
| `FGE-CHAR-PARENT-STATE-001` | State before mutation |
| `FGE-CHAR-DESCENDANT-STATE-001` | State after mutation |
| `FGE-CHAR-LINEAGE-DELTA-001` | Difference |
| `FGE-CHAR-LINEAGE-SPLIT-001` | New lineage threshold |

Lineage equation:

```text
PARENT_STATE
+
AUTHORIZED_MUTATION
+
PRESERVED_INVARIANTS
=
DESCENDANT_STATE
```

With:

```text
ACTUAL_DELTA
```

recorded separately.

---

## 17. GOVERNANCE / CONTINUITY LIBRARY

```text
FGE-CHAR-GOVERNANCE-001
FGE-CHAR-REGISTRY-001
FGE-CHAR-CANON-STATE-001
FGE-CHAR-PROVENANCE-001
FGE-CHAR-REVIEW-001
FGE-CHAR-AUTHORITY-001
FGE-CHAR-REGISTRY-UPDATE-001
FGE-CHAR-CANON-DELTA-001
FGE-CHAR-CONFLICT-001
```

Governance controls:

```text
classification
reviewer
authority
rationale
canon_delta
registry_update
lineage
provenance
```

---

## 18. THE PAIRING CONTRACT

```text
OBJECT_ID: FGE-CHAR-SKELETON-CONTRACT-001
STATUS: PROPOSED
PARENT: FGE-CHAR-SKELETON-PAIR-001
```

### Governing laws

```text
LAW-01
HEART generates predictions.
LAW-02
BRAIN generates developmental evidence.
LAW-03
Neither silently rewrites the other.
LAW-04
Observation ≠ truth.
LAW-05
Evidence ≠ canon.
LAW-06
Delta ≠ mutation.
LAW-07
Mutation requires promotion.
LAW-08
Promotion requires review.
LAW-09
Authorized mutation produces a new Heart state.
LAW-10
Previous Heart states remain preserved through lineage.
LAW-11
Contradictions remain visible until resolved.
LAW-12
Unknown > invented.
```

This creates a biological feedback loop without identity drift.

---

## 19. MVT CHARACTER SKELETON

The minimum viable implementation becomes:

```text
             FGE CHARACTER
                  │
            ┌─────┴─────┐
            │           │
          HEART       BRAIN
        identity     experience
            │           │
        predicts      observes
            │           │
            └────┬──────┘
                 ▼
              DELTA
                 │
                 ▼
            CONDUCTION
                 │
        question / test
                 │
                 ▼
             EVIDENCE
                 │
                 ▼
              REVIEW
                 │
        ┌────────┴────────┐
        ▼                 ▼
     REJECT             PROMOTE
                           │
                           ▼
                       MUTATION
                           │
                           ▼
                    HEART STATE N+1
                           │
                           ▼
                        LINEAGE
```

That is the character before:

```text
BODY
WARDROBE
HAIR
TATTOOS
MATERIAL
MYTHOLOGY
DIALOGUE
SCENES
STORY
RENDER
COMMERCE
```

are layered on.

---

## 20. IMPORTANT SOURCE CONTRADICTION PRESERVED

The supplied text currently contains two incompatible mappings.

### CLAIMED Mapping A

```text
FGE Character    = Who it is
Heart Object     = What happened
Brain Object     = Attractors
Genome           = Evidence
Chemistry        = Delta
Manifestation    = Conduction
```

### CLAIMED Mapping B

Elsewhere the same specification says:

```text
HEART = identity mechanics
BRAIN = developmental mechanics
HEART generates predictions.
BRAIN generates evidence.
```

These cannot both be literally true.

Therefore:

```text
STATUS: UNRESOLVED_CONCEPT_MAPPING
REFERENCE: FGE-CHAR-CONTRADICTION-001
CANON_EFFECT: NONE
```

### PROPOSED normalization

Based on the larger structure:

```text
CHARACTER      = whole persistent organism
HEART          = identity / attractors / behavior mechanics
BRAIN          = experience / observation / evidence mechanics
GENOME         = underlying structural organization
CHEMISTRY      = interaction between components
DELTA          = difference between prediction and observation
CONDUCTION     = curiosity → hypothesis → test
MANIFESTATION  = actual expressed behavior
JOURNALIST     = witness / structured observer
REGISTRY       = continuity
```

This is PROPOSED, not silently promoted.

---

## 21. MASTER INDEX RECORD FORMAT

Every registry entry should eventually normalize to:

```json
{
  "reference_id": "FGE-CHAR-HEART-001",
  "reference_family": "FGE-CHAR-SKELETON-PAIR-001",
  "title": "FGE Character Heart",
  "class": "IDENTITY_BEHAVIORAL_ORGANISM",
  "version": "1.0.0",
  "reference_status": "ACTIVE",
  "object_status": "PROPOSED",
  "authority": "DIRECTOR",
  "canon_effect": "NONE",
  "aliases": [
    "FGE.HEART",
    "FGE.CHAR.HEART"
  ],
  "tags": [
    "FGE.CHAR",
    "FGE.CHAR.SKELETON",
    "FGE.CHAR.HEART",
    "FGE.CHAR.IDENTITY"
  ],
  "parent_refs": [
    "FGE-CHAR-SKELETON-PAIR-001"
  ],
  "relation_refs": [
    {
      "relation": "PAIRED_WITH",
      "target": "FGE-CHAR-BRAIN-001"
    }
  ],
  "provenance": [],
  "deprecated_by": null
}
```

---

## 22. RELATIONSHIP VOCABULARY

Use a closed relation set wherever possible:

```text
PART_OF
CONTAINS
PAIRED_WITH
PREDICTS
OBSERVES
WITNESSES
PRODUCES
PRODUCES_EVIDENCE_FOR
SUPPORTS
CONTRADICTS
TESTS
AMPLIFIES
SUPPRESSES
DEPENDS_ON
PRESERVES
MUTATES
PROPOSES_MUTATION_TO
PROMOTES_TO
DESCENDS_FROM
GOVERNS
VALIDATES
REFERENCES
MATERIALIZES
MANIFESTS_AS
DERIVED_FROM
RECORDED_IN
SUPERSEDES
DEPRECATED_BY
```

Do not allow arbitrary relationship prose if one of these already fits.

That becomes important once a graph database arrives.

---

## 23. SEARCH / RETRIEVAL EXAMPLES

Find everything about Heart:

```text
TAG:FGE.CHAR.HEART
```

Find Nikki’s Heart specifically:

```text
REFERENCE:FGE-CHAR-HEART-NIKKI-001
```

Find sacrifice logic:

```text
REFERENCE:
FGE-CHAR-HEART-NIKKI-001#behavioral_genome.choice.sacrifice_logic
```

Find unpromoted discoveries:

```text
TAG:FGE.CHAR.DISCOVERY
STATUS:CANDIDATE
```

Find contradictions:

```text
TAG:FGE.CHAR.CONTRADICTION
STATUS:UNRESOLVED
```

Find every object connected to Brain:

```text
RELATION:*-->FGE-CHAR-BRAIN-001
```

This makes the library usable as a future RAG index, not merely documentation.

---

## 24. INSTANCE NAMING RULE

Templates use generic IDs:

```text
FGE-CHAR-HEART-001
FGE-CHAR-BRAIN-001
```

Character instances should use character identity:

```text
FGE-CHAR-HEART-NIKKI-001
FGE-CHAR-BRAIN-NIKKI-001
FGE-CHAR-HEART-RAVEN-001
FGE-CHAR-BRAIN-RAVEN-001
FGE-CHAR-HEART-LIORA-001
FGE-CHAR-BRAIN-LIORA-001
```

Do not replace the generic schema objects with instance objects.

Relationship:

```text
FGE-CHAR-HEART-NIKKI-001
--INSTANCE_OF-->
FGE-CHAR-HEART-001
```

---

## 25. REFERENCE RESOLUTION ORDER

When an LLM encounters a reference:

1. RESOLVE EXACT OBJECT ID
2. RESOLVE VERSION if specified
3. RESOLVE FIELD PATH if specified
4. RESOLVE AUTHORITY
5. RESOLVE STATUS
6. RESOLVE PROVENANCE
7. RESOLVE RELATIONS
8. REPORT CONFLICTS
9. RETURN UNKNOWN where unresolved

Never:

```text
REFERENCE MISSING
        ↓
LLM INVENTS MEANING
```

Instead:

```text
REFERENCE MISSING
        ↓
UNKNOWN_REFERENCE
```

---

## 26. MINIMUM DEPLOYMENT BLOCK

This tiny block can now be placed into another account/runtime:

```text
[FGE REFERENCE RESOLUTION]
ROOT_REFERENCE:
FGE-CHAR-SKELETON-PAIR-001
FAMILY:
MVT.FGE.BRAIN.HEART
RULES:
REFERENCE = persistent object pointer
TAG = semantic classifier
#PATH = internal object address
@VERSION = historical state
RELATION = explicit edge
RESOLVE:
ID > VERSION > PATH > AUTHORITY > STATUS > PROVENANCE > RELATION
LAW:
UNKNOWN > INVENTED
CONFLICT > SILENT_RECONCILIATION
EVIDENCE != CANON
DELTA != MUTATION
MUTATION REQUIRES PROMOTION
LOCK = EXPLICIT
CORE:
HEART -> PREDICTION
BRAIN -> EVIDENCE
EXPERIENCE -> DELTA
CONDUCTION -> TEST
REVIEW -> PROMOTION
PROMOTION -> AUTHORIZED_MUTATION
MUTATION -> NEW_HEART_STATE
NEW_HEART_STATE -> LINEAGE
REFERENCE:
FGE-CHAR-SKELETON-PAIR-001
```

---

## ENDSTATE

You now have the beginnings of a character knowledge graph, not just a naming convention.

The skeleton can eventually be queried as:

```text
CHARACTER
→ HEART
→ ATTRACTOR
→ PREDICTION
→ EXPERIENCE
→ OBSERVATION
→ EVIDENCE
→ DELTA
→ HYPOTHESIS
→ TEST
→ LEARNING
→ REVIEW
→ MUTATION
→ NEW STATE
→ LINEAGE
```

And every node can have a stable FGE reference.

That means a story, render, compiler, journalist agent, experiment, or database does not need to re-explain what a Heart or Delta is. It simply points home.

The reference becomes the address.  
The registry becomes the map.  
The character’s lifetime becomes the graph.

```text
REFERENCE ROOT:
FGE-CHAR-SKELETON-PAIR-001
INDEX ROOT:
FGE-REF-CHAR-SKELETON-INDEX-001
STATUS:
PROPOSED / READY_FOR_REGISTRATION
UNRESOLVED:
Heart/Brain semantic contradiction preserved as
FGE-CHAR-CONTRADICTION-001
CANON_EFFECT:
NONE_UNLESS_EXPLICITLY_PROMOTED
```

REF: FGE-CHAR-20260830-RFX1
