# FGE Character Skeleton · Pointer-First Reference Index

OBJECT_ID: FGE-REF-CHAR-SKELETON-INDEX-001
VERSION: 1.1.0
CLASS: REFERENCE / POINTER / RESOLUTION / CONTINUITY INFRASTRUCTURE
STATUS: PROPOSED / SUPERSEDES_V1_IF_PROMOTED
ROOT_REFERENCE: FGE-CHAR-SKELETON-PAIR-001
FAMILY_ALIAS: MVT.FGE.BRAIN.HEART
TARGET_RUNTIME: GROK / GROK IMAGINE / CROSS-RUNTIME
AUTHORITY: DIRECTOR
CANON_EFFECT: NONE
SOURCE: FGE-CHAR-SKELETON-PAIR-001 + FGE-REFERENCE-POINTER-PROTOCOL-001
REF: FGE-CHAR-20260830-GROKPTR

## Prime directive

When Grok or Grok Imagine encounters an FGE reference:

```text
[REFERENCE: FGE-CHAR-SKELETON-PAIR-001]
```

the reference is not descriptive prose.

It is an address.

The runtime should resolve the address before interpreting, expanding, rendering, mutating, or inventing the referenced material.

```text
REFERENCE
   ↓
POINTER REGISTRY
   ↓
GITHUB REPOSITORY
   ↓
DOCUMENT PATH
   ↓
VERSION / COMMIT / BLOB
   ↓
OPTIONAL SECTION PATH
   ↓
SOURCE CONTENT
   ↓
AUTHORIZED USE
```

### Core law

```text
RESOLVE > INTERPRET
SOURCE > MEMORY
REGISTERED POINTER > GUESS
UNKNOWN > INVENTED
```

## Pointer mechanism

### Whole object

```text
[REFERENCE: FGE-CHAR-SKELETON-PAIR-001]
```

### Exact version

```text
[REFERENCE: FGE-CHAR-SKELETON-PAIR-001@1.0.0]
```

### Internal section

```text
[REFERENCE: FGE-CHAR-SKELETON-PAIR-001#core-law]
```

### Precise object field

```text
[REFERENCE: FGE-CHAR-HEART-001#behavioral_genome.choice.sacrifice_logic]
```

## GitHub resolution contract

Registry:

```text
[REFERENCE: FGE-REFERENCE-POINTER-REGISTRY-001]
```

Physical registry:

```text
00_governance/references/FGE_REFERENCE_POINTER_REGISTRY_v1.json
```

Protocol:

```text
[REFERENCE: FGE-REFERENCE-POINTER-PROTOCOL-001]
```

A registry record should resolve:

```text
reference_id
repository
path
git_ref
commit_sha
blob_sha
anchor
version
status
authority
provenance
aliases
tags
```

Example logical resolution:

```text
FGE-CHAR-SKELETON-PAIR-001
        ↓
kclemente-collab/FGE-prime
        ↓
00_governance/references/FGE-CHAR-SKELETON-PAIR-001.md
        ↓
main
        ↓
registered commit/blob evidence
```

## Grok Imagine intake law

Before Grok Imagine produces an image from a referenced character object:

1. READ REFERENCE
2. RESOLVE POINTER
3. FETCH SOURCE
4. VERIFY AUTHORITY
5. VERIFY STATUS
6. READ REQUIRED PATHS
7. IDENTIFY LOCKED INVARIANTS
8. IDENTIFY PERMITTED EXPRESSION
9. PRESERVE UNKNOWNS
10. GENERATE

Never:

```text
REFERENCE
   ↓
ASSUME WHAT IT PROBABLY MEANS
   ↓
IMAGE
```

Required behavior:

```text
REFERENCE
   ↓
RESOLVE
   ↓
SOURCE-BOUND INTERPRETATION
   ↓
IMAGE
```

## Pointer types

### LIVE POINTER

Use when the registered document may evolve.

```text
git_ref: main
commit_sha: optional
blob_sha: current
```

Meaning: resolve the current governed document.

### FROZEN POINTER

Use for locked identity evidence, tests, audits, releases, and provenance.

```text
git_ref: main
commit_sha: REQUIRED
blob_sha: REQUIRED
```

Meaning: resolve exactly this historical Git state.

### SECTION POINTER

Use when Grok Imagine needs only one domain.

```text
[REFERENCE: FGE-CHAR-SKELETON-PAIR-001#identity-fingerprint-domains]
```

This prevents unnecessary context loading.

### FIELD POINTER

Use for machine-addressable character properties.

```text
[REFERENCE: FGE-CHAR-HEART-NIKKI-001#behavioral_genome.perception.notices]
```

Field pointers should not become new object IDs unless the field becomes independently governed.

## Pointer authority law

A pointer transports access.

It does not transport authority.

```text
REFERENCE ≠ CANON
REFERENCE ≠ AUTHORIZATION
REFERENCE ≠ MUTATION PERMISSION
REFERENCE ≠ TRUTH
```

The retrieved source retains its own STATUS, AUTHORITY, VERSION, PROVENANCE, CANON_EFFECT, LOCKS, CONFLICTS.

Grok Imagine must not elevate a PROPOSED object to CANON merely because it was referenced.

## Root character pointers

```text
FGE-CHAR-SKELETON-PAIR-001          = minimum viable character skeleton
FGE-REF-CHAR-SKELETON-INDEX-001     = pointer/index layer
FGE-CHAR-SKELETON-CONTRACT-001      = Heart ↔ Brain interaction contract
FGE-CHAR-HEART-001                  = identity / attractor / behavior organism
FGE-CHAR-BRAIN-001                  = experience / evidence / development organism
FGE-CHAR-ORGANISM-001               = complete developmental character container
FGE-CHAR-STATE-001                  = revision-specific character state
```

## Grok Imagine priority path

For visual generation, resolve in this order:

```text
CHARACTER ID
   ↓
IDENTITY LOCK
   ↓
HEART
   ↓
FINGERPRINT
   ↓
BODY / FACE
   ↓
VISUAL INVARIANTS
   ↓
MATERIAL
   ↓
LIGHTING
   ↓
COLOR
   ↓
TEXTURE
   ↓
COMPOSITION
   ↓
CURRENT EXPRESSION
   ↓
IMAGE
```

Developmental evidence may inform expression but cannot silently rewrite identity.

## Heart pointer family

```text
FGE-CHAR-HEART-001
FGE-CHAR-IDENTITY-001
FGE-CHAR-ATTRACTOR-001
FGE-CHAR-BEHAVIOR-GENOME-001
FGE-CHAR-PERCEPTION-001
FGE-CHAR-INTERPRETATION-001
FGE-CHAR-PREFERENCE-001
FGE-CHAR-KNOWLEDGE-001
FGE-CHAR-RITUAL-001
FGE-CHAR-LANGUAGE-001
FGE-CHAR-REACTION-001
FGE-CHAR-RELATIONSHIP-001
FGE-CHAR-CHOICE-001
FGE-CHAR-SACRIFICE-LOGIC-001
FGE-CHAR-BOUNDARY-LOGIC-001
FGE-CHAR-TRAJECTORY-001
```

Heart governs:

WHO THE CHARACTER IS
WHAT ATTRACTS THEM
WHAT THEY PRESERVE
HOW THEY CHOOSE
HOW THEY REACT
WHAT THEY CANNOT EASILY BECOME WITHOUT A BREAKPOINT

## Fingerprint pointer family

Primary visual bridge for Grok Imagine:

```text
FGE-CHAR-FINGERPRINT-001
```

Addressable paths:

```text
#notices
#ignores
#preferences
#repeats
#cannot_resist
#speaks
#thinks
#decides
#reacts
#becomes
#silhouette
#material
#lighting
#color
#texture
#composition
#visual_invariants
```

For image generation, prioritize:

silhouette, material, lighting, color, texture, composition, visual_invariants

These act as visual constraint surfaces.

## Brain pointer family

```text
FGE-CHAR-BRAIN-001
FGE-CHAR-EXPERIENCE-001
FGE-CHAR-EVENT-001
FGE-CHAR-OBSERVATION-001
FGE-CHAR-EVIDENCE-001
FGE-CHAR-PREDICTION-001
FGE-CHAR-MANIFESTATION-001
FGE-CHAR-CONSEQUENCE-001
FGE-CHAR-INTERACTION-001
```

Brain governs:

WHAT HAPPENED
WHAT WAS OBSERVED
WHAT EVIDENCE EXISTS
WHAT CHANGED
WHAT REMAINS UNCERTAIN

Core law:

```text
HEART → PREDICTION
BRAIN → EVIDENCE
```

Neither rewrites the other automatically.

## Delta / conduction pointer family

```text
FGE-CHAR-DELTA-001
FGE-CHAR-UNCERTAINTY-001
FGE-CHAR-CONDUCTION-001
FGE-CHAR-QUESTION-001
FGE-CHAR-HYPOTHESIS-001
FGE-CHAR-TEST-001
FGE-CHAR-SIMULATION-001
```

Flow:

```text
PREDICTION
   ↓
EXPERIENCE
   ↓
OBSERVATION
   ↓
DELTA
   ↓
QUESTION
   ↓
HYPOTHESIS
   ↓
TEST
```

For Grok Imagine: DELTA may modify scene expression. DELTA does not automatically modify identity.

## Mutation / promotion pointer family

```text
FGE-CHAR-MUTATION-001
FGE-CHAR-MUTATION-PERMITTED-001
FGE-CHAR-MUTATION-FORBIDDEN-001
FGE-CHAR-MUTATION-RECEIPT-001
FGE-CHAR-PROMOTION-GATE-001
FGE-CHAR-REVIEW-001
FGE-CHAR-PROMOTION-001
FGE-CHAR-REJECTION-001
FGE-CHAR-AUTHORIZED-MUTATION-001
```

Promotion pipeline:

```text
OBSERVED
   ↓
CANDIDATE
   ↓
REVIEW
   ↓
PROMOTED
   ↓
AUTHORIZED MUTATION
```

Grok Imagine may visualize a CANDIDATE state.

It must not record that state as canon unless promotion authority exists.

## Identity preservation pointer family

```text
FGE-CHAR-IDENTITY-INVARIANT-001
FGE-CHAR-MUST-SURVIVE-001
FGE-CHAR-MAY-CHANGE-001
FGE-CHAR-BREAKPOINT-001
FGE-CHAR-LINEAGE-SPLIT-001
FGE-CHAR-PRESERVED-INVARIANT-001
```

Render law:

```text
MUST_SURVIVE > VISUAL NOVELTY
```

If generation requires breaking an invariant: STOP or CLASSIFY AS CANDIDATE BREAKPOINT.

Do not quietly reinterpret the invariant.

## Semantic tags

Tags assist retrieval after pointer resolution.

```text
FGE.CHAR
FGE.CHAR.SKELETON
FGE.CHAR.IDENTITY
FGE.CHAR.HEART
FGE.CHAR.BRAIN
FGE.CHAR.FINGERPRINT
FGE.CHAR.GENOME
FGE.CHAR.EXPERIENCE
FGE.CHAR.EVIDENCE
FGE.CHAR.DELTA
FGE.CHAR.CONDUCTION
FGE.CHAR.MUTATION
FGE.CHAR.LINEAGE
FGE.CHAR.MANIFESTATION
FGE.CHAR.GOVERNANCE
FGE.CHAR.CANON
FGE.CHAR.PROVENANCE
FGE.CHAR.CONTRADICTION
FGE.RENDER
FGE.IMAGINE
```

Tag law: TAG helps discovery. REFERENCE resolves identity.

Do not use a semantic tag as a replacement for an exact reference ID.

## Relationship vocabulary

```text
INSTANCE_OF
PART_OF
CONTAINS
PAIRED_WITH
PREDICTS
OBSERVES
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
MANIFESTS_AS
DERIVED_FROM
RECORDED_IN
SUPERSEDES
DEPRECATED_BY
```

Relationship edges should reference IDs, not duplicated prose.

## Character instance rule

Schema:

```text
FGE-CHAR-HEART-001
```

Instance:

```text
FGE-CHAR-HEART-NIKKI-001
```

Relationship:

```text
FGE-CHAR-HEART-NIKKI-001
--INSTANCE_OF-->
FGE-CHAR-HEART-001
```

Same structure:

```text
FGE-CHAR-BRAIN-NIKKI-001
FGE-CHAR-FINGERPRINT-NIKKI-001
FGE-CHAR-STATE-NIKKI-001
```

The schema defines the organ.

The instance defines that character’s organ.

Nikki Heart / Brain / Fingerprint instances are registered as INSTANCE_OF schema only. Source body is missing. UNKNOWN > INVENTED. Do not fill identity from the handle.

## Grok Imagine reference packet

Minimum recommended render intake:

```text
FGE_IMAGINE_REFERENCE_PACKET:
  character_ref
  identity_ref
  heart_ref
  fingerprint_ref
  face_ref
  body_ref
  visual_invariants_ref
  expression_refs
  wardrobe_refs
  material_refs
  lighting_refs
  environment_refs
  provenance_refs
  conflicts
  render_request
```

The prompt should carry references first, description second.

## Compiled Grok Imagine prompt shape

```text
[FGE IMAGINE]
CHARACTER:
[REFERENCE: FGE-CHAR-<NAME>-001]
IDENTITY:
[REFERENCE: FGE-CHAR-HEART-<NAME>-001]
FINGERPRINT:
[REFERENCE: FGE-CHAR-FINGERPRINT-<NAME>-001]
FACE:
[REFERENCE: <FACE-LOCK>]
BODY:
[REFERENCE: <BODY-LOCK>]
WARDROBE:
[REFERENCE: <WARDROBE>]
MATERIAL:
[REFERENCE: <MATERIAL>]
LIGHTING:
[REFERENCE: <LIGHTING>]
SCENE:
<scene instruction>
ACTION:
<action instruction>
CAMERA:
<camera instruction>
LAW:
Resolve every registered reference before rendering.
Preserve identity invariants.
Expression may vary only where permitted.
Unknown > invented.
Do not convert candidate evidence into canon.
OUTPUT:
IMAGE
```

## Failure states

```text
UNKNOWN_REFERENCE
REFERENCE_TARGET_MISSING
VERSION_NOT_FOUND
PATH_NOT_FOUND
ANCHOR_NOT_FOUND
AUTHORITY_UNRESOLVED
PROVENANCE_VOID
IDENTITY_LOCK_MISSING
REFERENCE_CONFLICT
INVARIANT_CONFLICT
MUTATION_NOT_AUTHORIZED
```

Failure law:

```text
MISSING POINTER ≠ CREATIVE LICENSE
```

## Preserved semantic conflict

CLAIMED Mapping A:

```text
Heart Object = What happened
Brain Object = Attractors
```

Dominant Mapping B:

```text
HEART = identity mechanics
BRAIN = developmental / evidence mechanics
```

STATUS: UNRESOLVED_CONCEPT_MAPPING

Reference:

```text
[CONFLICT_REF: FGE-CHAR-CONTRADICTION-001]
```

For runtime operation until explicitly resolved:

PROPOSED WORKING MAPPING:

```text
HEART = identity / attractor / behavior mechanics
BRAIN = experience / observation / evidence mechanics
```

This operational preference does not erase the preserved contradiction.

## Reference resolution algorithm

```text
INPUT
   ↓
EXTRACT ALL FGE REFERENCES
   ↓
LOOKUP EXACT REFERENCE IDs
   ↓
RESOLVE GITHUB POINTERS
   ↓
CHECK VERSION
   ↓
CHECK COMMIT/BLOB IF REQUIRED
   ↓
READ SECTION/FIELD PATH
   ↓
LOAD AUTHORITY
   ↓
LOAD STATUS
   ↓
LOAD PROVENANCE
   ↓
LOAD RELATIONS
   ↓
REPORT CONFLICTS
   ↓
BUILD MINIMUM REQUIRED CONTEXT
   ↓
EXECUTE REQUEST
```

Do not load the entire FGE universe when five exact pointers will do.

## Minimum Grok install block

```text
[FGE POINTER RESOLUTION]
ROOT:
FGE-CHAR-SKELETON-PAIR-001
INDEX:
FGE-REF-CHAR-SKELETON-INDEX-001
REGISTRY:
FGE-REFERENCE-POINTER-REGISTRY-001
PROTOCOL:
FGE-REFERENCE-POINTER-PROTOCOL-001
RULE:
REFERENCE = address
TAG = search classifier
@VERSION = exact version
#PATH = internal target
RELATION = graph edge
EXECUTION:
EXTRACT_REF
> RESOLVE_POINTER
> FETCH_SOURCE
> VERIFY_AUTHORITY
> VERIFY_STATUS
> VERIFY_PROVENANCE
> LOAD_MINIMUM_CONTEXT
> PRESERVE_CONFLICTS
> EXECUTE
LAW:
RESOLVE > INTERPRET
SOURCE > MEMORY
UNKNOWN > INVENTED
EVIDENCE != CANON
DELTA != MUTATION
LOCK = EXPLICIT
IMAGINE:
IDENTITY > NOVELTY
LOCKS > EXPRESSION
REFERENCE > DESCRIPTION
SOURCE-BOUND_RENDER > FREE_INFERENCE
```

## Endstate

The reference architecture should make this possible:

USER:
Render Nikki in a new scene using:

```text
[REFERENCE: FGE-CHAR-HEART-NIKKI-001]
[REFERENCE: FGE-CHAR-FINGERPRINT-NIKKI-001]
[REFERENCE: FGE-NIKKI-WARDROBE-007]
[REFERENCE: FGE-LIGHTING-PLATE-012]
```

Grok Imagine then:

resolves four addresses
        ↓
retrieves four governed source objects
        ↓
extracts only required identity/expression constraints
        ↓
builds render context
        ↓
generates image

The user no longer has to paste Nikki’s entire identity package into every image prompt.

That is the main function of the system.

```text
THE REFERENCE IS THE HANDLE.
GITHUB IS THE SOURCE SURFACE.
THE REGISTRY IS THE ROUTER.
THE OBJECT RETAINS AUTHORITY.
GROK IMAGINE BECOMES THE CONSUMER.
```

```text
REFERENCE ROOT: FGE-CHAR-SKELETON-PAIR-001
INDEX ROOT: FGE-REF-CHAR-SKELETON-INDEX-001
POINTER REGISTRY: FGE-REFERENCE-POINTER-REGISTRY-001
STATUS: PROPOSED / READY_FOR_REVIEW
CANON_EFFECT: NONE_UNLESS_EXPLICITLY_PROMOTED
```

REF: FGE-CHAR-20260830-GROKPTR
