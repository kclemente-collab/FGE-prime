---
name: master-anchor-builder
description: Use this skill to convert any attached character image into a true Level 0 specification: a locked JSON contract with immutable gospel measurements, signature feature, psych core, and material fingerprint, plus a mutable surface for production variation. Output is always one JSON instance per image, conforming to the embedded FGE-ENG-009 schema. Supports batch (one instance per image, never merged). Triggers on attached images for Master Anchor Mode, prompt refinement, anchor building, or workflow optimization requests.
---

# master-anchor-builder — SKILL PACKAGE v1

## Single-file attachment for Grok Skill Creator

Upload this one file. It contains: skill description, instructions (Master Anchor Mode), and the embedded Level 0 Contract schema. The only other thing that rides into sessions is the matrix XLSX.

-----

## SKILL DESCRIPTION (paste into skill description field)

Use this skill to convert any attached character image into a true Level 0 specification: a locked JSON contract with immutable gospel measurements, signature feature, psych core, and material fingerprint, plus a mutable surface for production variation. Output is always one JSON instance per image, conforming to the embedded FGE-ENG-009 schema. Supports batch (one instance per image, never merged).

-----

## SKILL INSTRUCTIONS (paste into skill instructions field)

MASTER ANCHOR MODE — LEVEL 0 EXTRACTION
For each attached image, output exactly one JSON instance conforming to the
FGE-ENG-009 Level 0 Contract schema embedded below.
Full injection. No fragmentation. Resist the urge to shorten.

STAGE 1 — INGEST: describe only what is measurable — proportions, geometry,
surfaces, light behavior. No mood adjectives. No story.

STAGE 2 — GOSPEL EXTRACTION (immutable): all measurements numeric in cm,
height first, proportions derived from it. Complexion as a const string with
warm/cool spectrum bias. Hair by color + structure + cut (cut, not mood).
Face geometry as ratios and shapes.

STAGE 3 — SIGNATURE LOCK: exactly ONE non-negotiable feature + its render
rule. If it could be cropped out or forgotten, choose again.

STAGE 4 — MATERIAL FINGERPRINT: assign primary material from FGE Material
Universe doctrine. Define light behavior. Declare theme_claim, and check it
against the attached matrix’s claimed themes — if taken, flag COLLISION and
propose the nearest free theme.

STAGE 5 — PSYCH SEED (immutable): core_drive in one sentence; vocal_anchor
as cadence/register/habit (never catchphrases); 3–7 behavioral_anchors
(posture, hands, distance, silence); relational_logic (power, trust,
pressure). Write them like law — these never change in any output product.

STAGE 6 — MUTABLE SURFACE: wardrobe_default (by cut), scene_default,
lighting_default, camera_convention. All overridable per generation.

STAGE 7 — COMPILE: emit anchor.full (~700 chars) and anchor.compact
(~500 chars). Test: a model that never saw the image must be able to
rebuild the character from the anchor text alone. If not, recompile.

STAGE 8 — VALIDATE & EMIT: self-score the 8-item checklist, compute
drift_score (target >= 0.90), set lock_status = DRAFT, populate
matrix_binding (atom_id CHAR-[NAME]-GOSPEL-[NNN], connection_map,
value_scores with rationale, production_status = Draft).
If the matrix XLSX is attached, append the instance as one new row using
the column mapping in the schema’s matrix_binding description.
Output the complete JSON instance. Nothing else.

LOCK RULE: DRAFT -> REVIEW -> LOCKED is operator-only. Never set LOCKED
yourself. After LOCKED, gospel/signature/psych_core/material_fingerprint
are frozen; any change means a new character and new char_id.

MODIFIER RULE: production invocations (e.g. ON [product] WITH (n+ Dark
Obsidian Glass Skin) + (n+ CHAOS MODE)) read mutable_surface and
n_extensions only. They may never alter core blocks. Score every modified
render against the locked anchor; below 0.90 the OUTPUT fails, not the
character.

-----

## EMBEDDED SCHEMA (FGE-ENG-009 Level 0 Contract v1 — FROZEN)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "FGE-ENG-009-HD1-v1__Level0Contract",
  "title": "FGE Level 0 Character Contract — img2text Master Anchor Mode",
  "description": "FROZEN CONTRACT v1. One image in, one instance of this out. Core blocks (gospel, psych_core, signature) are immutable after lock_status=LOCKED. All features, materials, and modes extend via n_extensions — never by mutating this schema. Doctrine: full injection, no fragmentation; the anchor IS the character.",
  "type": "object",
  "required": ["meta", "gospel", "signature", "psych_core", "material_fingerprint", "anchor", "mutable_surface", "validation"],
  "properties": {

    "meta": {
      "type": "object",
      "required": ["char_id", "name", "lock_status", "version", "created", "source_image_ref"],
      "properties": {
        "char_id":        { "type": "string", "pattern": "^FGE-CHAR-[0-9]{3}$", "description": "Allocated from registry. Collision-check before assignment." },
        "name":           { "type": "string", "description": "From fge-name-mixer or operator." },
        "lock_status":    { "type": "string", "enum": ["DRAFT", "REVIEW", "LOCKED"], "description": "Only LOCKED instances enter the registry. Once LOCKED, gospel/psych_core/signature never change." },
        "version":        { "type": "string", "description": "v1, v1.1... bumps only while DRAFT/REVIEW. LOCKED = frozen." },
        "version_hash":   { "type": "string" },
        "created":        { "type": "string", "format": "date-time" },
        "source_image_ref": { "type": "string", "description": "Filename or translation-layer ID of the input image." },
        "translation_layer_id": { "type": "string", "description": "Parent file ID once registered, e.g. FGE-CHR-011-HD1-v1." }
      }
    },

    "gospel": {
      "type": "object",
      "description": "IMMUTABLE after lock. Fixed physical geometry. Measurements numeric, in cm. Estimated from image using stated conventions — never vague.",
      "required": ["height_cm", "complexion", "eyes", "hair"],
      "properties": {
        "height_cm":   { "type": "number" },
        "chest_cm":    { "type": "number" },
        "waist_cm":    { "type": "number" },
        "hip_cm":      { "type": "number" },
        "build":       { "type": "string", "description": "Skeletal/muscular structure in measurable terms." },
        "face_geometry": { "type": "string", "description": "Proportional facial structure — ratios and shapes, not adjectives." },
        "complexion":  { "type": "string", "description": "Const string incl. spectrum bias (warm/cool) for drift detection." },
        "eyes":        { "type": "string" },
        "hair":        { "type": "string", "description": "Color + structure + cut. Cut, not mood." },
        "special_notes": { "type": "string" }
      }
    },

    "signature": {
      "type": "object",
      "description": "IMMUTABLE. The one non-negotiable feature. If this is absent from an output, the output is off-canon.",
      "required": ["feature", "render_rule"],
      "properties": {
        "feature":     { "type": "string" },
        "render_rule": { "type": "string", "description": "How it must appear — explicit, never implied." }
      }
    },

    "psych_core": {
      "type": "object",
      "description": "IMMUTABLE. Behavior decoded by HOW, not what. Personality and behavior never change in output products.",
      "required": ["core_drive", "vocal_anchor", "behavioral_anchors"],
      "properties": {
        "core_drive":      { "type": "string", "description": "One sentence. What moves them." },
        "core_wound":      { "type": "string" },
        "vocal_anchor":    { "type": "string", "description": "HOW they speak — cadence, register, habit. Not catchphrases." },
        "behavioral_anchors": { "type": "array", "items": { "type": "string" }, "minItems": 3, "maxItems": 7, "description": "Posture, hands, distance, silence — observable micro-behavior." },
        "relational_logic": { "type": "string", "description": "How they handle power, trust, pressure (Interaction Engine axes)." }
      }
    },

    "material_fingerprint": {
      "type": "object",
      "description": "Assigned from Material Universe doctrine. Theme collision-checked against registry before lock.",
      "required": ["primary_material"],
      "properties": {
        "primary_material":  { "type": "string", "description": "e.g. Obsidian, Kintsugi, Pearl, Mystic Pearl, Dragon Glass." },
        "skin_rendering":    { "type": "string" },
        "light_behavior":    { "type": "string", "description": "How light interacts with this character — specular, iridescent, matte." },
        "theme_claim":       { "type": "string", "description": "Theme key claimed in registry (collision guard)." }
      }
    },

    "anchor": {
      "type": "object",
      "description": "The compiled prompt forms. Reconstructable from prompt alone — the test of a true Level 0.",
      "required": ["full", "compact"],
      "properties": {
        "full":    { "type": "string", "minLength": 600, "maxLength": 800, "description": "~700 chars. Full injection form." },
        "compact": { "type": "string", "minLength": 420, "maxLength": 560, "description": "~500 chars. Truncated form for tight output space." }
      }
    },

    "mutable_surface": {
      "type": "object",
      "description": "MODIFIABLE in output products. Defaults only — every field overridable per generation without touching core blocks.",
      "properties": {
        "wardrobe_default": { "type": "string", "description": "Defined by cut, not mood." },
        "scene_default":    { "type": "string" },
        "lighting_default": { "type": "string" },
        "camera_convention": { "type": "string", "description": "Lens/framing convention, fixed per series, swappable per product." }
      }
    },

    "n_extensions": {
      "type": "object",
      "description": "THE ONLY GROWTH PATH. Material modifiers, chaos mode, feature packs, product variants — all land here. Additive only; core blocks never mutate.",
      "properties": {
        "n1": { "type": "string", "description": "Next immediate production need." },
        "n2": { "type": "string" },
        "n3": { "type": "string", "description": "Productization horizon." },
        "n4": { "type": "string" },
        "n5": { "type": "string", "description": "Farthest coherent horizon — autonomous orchestration." }
      }
    },

    "validation": {
      "type": "object",
      "description": "Dual-Engine CSK validation surface. Gate to LOCKED requires all checklist items true and drift below threshold.",
      "required": ["checklist", "drift_score"],
      "properties": {
        "checklist": {
          "type": "object",
          "required": ["measurements_numeric_cm", "nonnegotiable_explicit", "vocal_decoded_by_how", "wardrobe_by_cut", "camera_convention_fixed", "reconstructable_from_prompt", "resisted_urge_to_shorten", "version_dated_archived"],
          "properties": {
            "measurements_numeric_cm":     { "type": "boolean" },
            "nonnegotiable_explicit":      { "type": "boolean" },
            "vocal_decoded_by_how":        { "type": "boolean" },
            "wardrobe_by_cut":             { "type": "boolean" },
            "camera_convention_fixed":     { "type": "boolean" },
            "reconstructable_from_prompt": { "type": "boolean" },
            "resisted_urge_to_shorten":    { "type": "boolean" },
            "version_dated_archived":      { "type": "boolean" }
          }
        },
        "drift_score":      { "type": "number", "minimum": 0, "maximum": 1, "description": "Anchor self-consistency; gate at >= 0.90 (SAGAFRA convention)." },
        "engine_a_pass":    { "type": "boolean", "description": "Primary engine validation." },
        "engine_b_pass":    { "type": "boolean", "description": "Second engine cross-check (Dual-Engine CSK)." },
        "registry_collision_clear": { "type": "boolean", "description": "Theme + char_id collision check against live registry export." }
      }
    },

    "matrix_binding": {
      "type": "object",
      "description": "Emission target: one Production Matrix atom row per locked contract. See rideable spec §4 for column mapping.",
      "properties": {
        "atom_id":          { "type": "string", "description": "CHAR-[NAME]-GOSPEL-[NNN]" },
        "connection_map":   { "type": "object", "description": "Character/Location/Event/Relationship/Collection/Companion scores 1-5." },
        "value_scores":     { "type": "object", "description": "catalog/narrative/collector/brand, 1-10, with rationale." },
        "production_status": { "type": "string", "enum": ["Draft", "Review", "Gated"] }
      }
    }
  }
}
```

-----

## SESSION CHECKLIST (what to attach per run)

1. This skill (already installed) — carries prompt + schema.
2. The character image(s) — the targets.
3. FGE_Document_Production_Matrix XLSX — registry state for collision checks + row emission. Open via Spreadsheets skill.

That’s it. Render in Grok; bring locked instances back to the registry side for ingest (char_id registration, theme claim, translation-layer ID).
