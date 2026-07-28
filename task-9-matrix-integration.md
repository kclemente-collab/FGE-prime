# Task 9 — Prompt Engine Matrix v2.0 Integration

## What & Why

The Render Elite editor currently accepts a freeform concept text box and three Feral Gloss
sliders. This task replaces that interface with a full 7-layer Matrix operator panel backed by
the Prompt Engine Matrix v2.0 doctrine. Every generation is now assembled deterministically
from structured layer selections rather than freeform text, producing doctrine-compliant,
drift-free outputs every time.

The N+3 Depth slider is redefined: it now directly selects the Atmospheric Interchange Module
tier (n+1 baseline / n+3 creative / n+5 empire-grade), injecting the correct assembly template
automatically into every variation prompt.

The Hormone Spine replaces the raw Intensity slider. The Action-Tension module replaces the
raw Tension slider. The concept text box becomes an optional override only.

---

## Done Looks Like

- The editor sidebar shows the 7-layer Matrix panel replacing the current concept/slider area
- Each layer has the correct input type (dropdown, button picker, multi-select)
- Selecting layers assembles a doctrine-compliant prompt automatically — no manual typing required
- The N+3 Depth slider maps to Atmospheric Interchange tier: 1–2 = n+1, 3–4 = n+3, 5 = n+5
- The Hormone Spine thermostat (1–5) replaces the Intensity slider
- The Action-Tension selector replaces the Tension slider
- The assembled prompt is visible in a read-only "Assembled Prompt" preview before generation
- Freeform concept text box remains as an optional override appended after the assembled prompt
- All 3 Feral Gloss variations still generate — Clean / Balanced / Intense — using the assembled prompt as base
- Style Memory BOOST/AVOID lines still append last
- Character roster loads pre-fill all Matrix layer defaults for that character

---

## Out of Scope

- Lika Confession Wrapper UI (separate task)
- Accept/Reject Rule Sheet v1.1 automated enforcement (separate task)
- Hormone Spine levels 4–5 UI exposure (architecture built, UI surfaces 1–3 only for now)
- Custom realm creation UI (predefined list only)
- Saving custom Matrix presets per session
- Motion/AnimateDiff integration (Task 8)

---

## Layer Definitions & UI Components

### Layer 1 — Realm Anchor

**UI:** Single-select dropdown

**Options:**
```
The Nocturnal Veil       — Toronto Grid
The Gilded Threshold     — Royal Chamber Dominion  
The Ocular Sanctum       — Mirrored Penthouse Void
The Haloed Eclipse       — Lunar Oracle Spire
Obsidian Temple          — Ancient dark stone sanctum
Neon Abyss               — Deep neon-lit urban void
Velvet Haze              — Soft diffused luxury interior
Prism Fracture           — Crystalline light-split environment
Crimson Fang             — High-contrast red-black dominance space
Eternal Forge            — Molten industrial cathedral
Bellagio Power Floor     — Elite casino power environment
200-Story Loft           — Penthouse above city with full glass exposure
```

**Prompt injection:** Realm name + atmospheric descriptor prepended to assembled prompt.

---

### Layer 2 — Body-Part Selector

**UI:** Multi-select chip grid (select 1–3)

**Options:**
```
Thighs          — haunches, pillars, stems, power-beams
Arms/Shoulders  — upper deltoid, muscle architecture
Wrists/Hands    — talons, vises, finger micro-variations
Lips            — tongues, lips
Belly           — lower back, lumbar arch
Chest           — collarbone, neck
```

**Prompt injection:** Selected parts injected as focal anchor descriptors.

---

### Layer 3 — Pose Foundation

**UI:** 6-button exclusive picker + tension state selector

**6 Immutable Foundations:**
```
1. Dominance Lean
2. Reclined Control
3. Twist Reveal        (default — high tension)
4. Ascension Stretch
5. Predator Stalk
6. Locked Embrace
```

**Tension State (sub-selector):**
```
Relaxed / Micro / Full
```

**Prompt injection — Full Grammar (always assembled in this order):**
```
[Foundation] + asymmetric twist + [Tension State] tension + 
finger spacing 2–3mm + breath expansion + chin tilt + expression alignment
```

This grammar is non-negotiable and always fully expanded in the prompt regardless of
which foundation is selected.

---

### Layer 4 — Camera Doctrine

**UI:** Primary module dropdown + optional modifier checkboxes

**Primary modules (choose one):**
```
Eye-Level Intimacy      — direct engagement, mid-torso to head crop, slight off-axis tilt
Low-Angle Power         — presence/scale emphasis, upward sculpting
Macro Focus             — fingertip trace, goosebumps, lace cling, fur strands, Focal Depth 3–4
Progressive Push-Zoom   — rack from wide to tight on tension point
Profile/Side View       — layered silhouette + relational clarity
Orbit Motion            — subtle parallax reveal
Locked Frame Drift      — slow controlled spatial movement
```

**Default optical profile (always injected):**
```
Hasselblad X2D 85mm f/1.4 equivalent, shallow depth of field, 
razor focus on eyes + micro-texture + specular points
```

**Modifiers (multi-select, optional):**
```
Dutch tilt (tension) / Aerial overview / Fisheye compression / Film-grain cutaway panels
```

---

### Layer 5 — Hormone Spine

**UI:** 5-step thermostat slider replacing current Intensity slider

**Levels (surface 1–3 in UI, build architecture for 1–5):**
```
Level 1 — Simmer          Subtle flush, micro-tremors
Level 2 — Rising Heat     Visible neck flush, elevated breath  
Level 3 — Magnetic Burn   Chest/neck/inner flush, dilated pupils, accelerated breath (DEFAULT)
Level 4 — Overdrive       [Architecture only — not surfaced in UI yet]
Level 5 — Riptide         [Architecture only — not surfaced in UI yet]
```

**Spine Markers (always injected regardless of level):**
```
flush gradients, pupil dilation, micro-tremors, 
earned liquid stretch-snap, pet reaction sync
```

---

### Layer 6 — Action-Tension Module

**UI:** Single-select button group replacing current Tension slider

**Options:**
```
Sustained Grip      — controlled pressure hold
Sharp Impact        — sudden force application  
Explosive Release   — rapid tension discharge
```

**Dynamics (always injected):**
```
tension-clinging film + stretch-snap + rivulet threading + diamond specular
```

---

### Layer 7 — Arousal & Response

**UI:** Auto-generated from Hormone Spine level — no manual selection

**Level 1–2 output:**
```
Witnessed Quiver + subtle Hormone Blaze
```

**Level 3 output (default):**
```
Witnessed Quiver + Hormone Blaze + Micro-Tremor Cascade + Raised Flesh Map
```

**Level 4–5 output (architecture only):**
```
Full: Flushed Surface Response + Tension-Bump Field + peak earned physics
```

---

## Atmospheric Interchange — N+3 Depth Mapping

The existing N+3 Depth slider (1–5) now maps to Atmospheric Interchange tiers:

| Depth Value | Tier | Assembly Template Used |
|-------------|------|----------------------|
| 1–2 | n+1 Baseline | Moon Rays + Steam + Cumulonimbus + Crowd as Arteries (stable) |
| 3–4 | n+3 Creative | Fractured prismatic rays + pearlescent steam + lightning wall + living crowd |
| 5 | n+5 Empire | Persistent evolving rays + memory steam + scaling storm + fully alive ecosystem |

**Full assembly templates per tier are defined in the Atmospheric Interchange Modules v1.0
document and must be injected verbatim into the prompt at the correct position.**

---

## Prompt Assembly Order

The final assembled prompt must follow this exact layer order:

```
1. [Realm Anchor + atmospheric descriptor]
2. [Character name + Sacred Fingerprint from roster]
3. [Pose Foundation + full grammar]
4. [Camera Doctrine primary + default optical profile + modifiers]
5. [Hormone Spine level markers + spine markers]
6. [Action-Tension + fluid-skin dynamics]
7. [Arousal & Response auto-output]
8. [Atmospheric Interchange template for selected N+3 tier]
9. [Style Memory BOOST lines]
10. [Freeform concept override if provided]
11. [Style Memory AVOID lines as negative prompt]
```

**This order is non-negotiable.** The prompt builder must assemble in exactly this sequence.

---

## Assembled Prompt Preview Component

Add a read-only expandable text area below the Matrix panel labeled:

```
ASSEMBLED PROMPT  [expand ▾]
```

- Collapsed by default, shows first 2 lines
- Expanded shows full assembled prompt
- Copy button top-right
- Updates live as any layer selection changes
- Gold accent border (#c8a96e) to signal it's doctrine-output not user input

---

## Server-Side Changes

In `artifacts/api-server/src/routes/render-elite.ts`:

Replace the existing prompt builder with a `MatrixPromptAssembler` class:

```ts
// artifacts/api-server/src/lib/matrix-assembler.ts  ← NEW FILE

export interface MatrixSelection {
  realm: string;
  bodyParts: string[];
  poseFoundation: string;
  tensionState: 'relaxed' | 'micro' | 'full';
  cameraModule: string;
  cameraModifiers: string[];
  hormoneLevel: 1 | 2 | 3 | 4 | 5;
  actionTension: string;
  nplus3Depth: 1 | 2 | 3 | 4 | 5;
  conceptOverride?: string;
}

export class MatrixPromptAssembler {
  assemble(selection: MatrixSelection, character: CharacterProfile, styleMemory: StyleMemory): string
  getAtmosphericTemplate(depth: 1|2|3|4|5): string
  getArousalResponse(hormoneLevel: number): string
}
```

The existing freeform `concept` field remains in the API for backward compatibility but
is treated as `conceptOverride` when a full `matrixSelection` object is provided.

---

## Request Schema Extension

Add to render request:

```ts
matrixSelection: z.object({
  realm: z.string(),
  bodyParts: z.array(z.string()).min(1).max(3),
  poseFoundation: z.enum([
    'dominance_lean', 'reclined_control', 'twist_reveal',
    'ascension_stretch', 'predator_stalk', 'locked_embrace'
  ]),
  tensionState: z.enum(['relaxed', 'micro', 'full']),
  cameraModule: z.string(),
  cameraModifiers: z.array(z.string()),
  hormoneLevel: z.number().int().min(1).max(5).default(3),
  actionTension: z.enum(['sustained_grip', 'sharp_impact', 'explosive_release']),
  conceptOverride: z.string().optional(),
}).optional()
```

When `matrixSelection` is present, it overrides freeform `concept` for prompt assembly.
When absent, existing behavior is preserved (backward compatible).

---

## Character Roster Pre-fill

Each character profile gains a `matrixDefaults` field:

```ts
matrixDefaults: {
  realm: string,
  poseFoundation: string,
  tensionState: string,
  cameraModule: string,
  hormoneLevel: number,
  actionTension: string,
}
```

Loading a character from the roster pre-fills all Matrix layer selections automatically.

**Vantrex defaults:**
```
realm: "The Nocturnal Veil"
poseFoundation: "predator_stalk"
tensionState: "full"
cameraModule: "low_angle_power"
hormoneLevel: 4  // architecture only, clamped to 3 in UI
actionTension: "explosive_release"
```

**Veilroot Warden defaults:**
```
realm: "Eternal Forge"
poseFoundation: "ascension_stretch"
tensionState: "micro"
cameraModule: "profile_side_view"
hormoneLevel: 2
actionTension: "sustained_grip"
```

**Ironroot Behemoth defaults:**
```
realm: "Obsidian Temple"
poseFoundation: "dominance_lean"
tensionState: "full"
cameraModule: "low_angle_power"
hormoneLevel: 3
actionTension: "sustained_grip"
```

**Nyxveil Echo defaults:**
```
realm: "The Ocular Sanctum"
poseFoundation: "twist_reveal"
tensionState: "micro"
cameraModule: "orbit_motion"
hormoneLevel: 2
actionTension: "explosive_release"
```

---

## UI Layout — Matrix Panel

Replace the current concept/slider section in the sidebar with:

```
─────────────────────────────
MATRIX OPERATOR
─────────────────────────────
REALM ANCHOR
[dropdown ▾]

BODY FOCUS
[Thighs] [Arms] [Hands] [Lips] [Belly] [Chest]

POSE FOUNDATION
[Dom Lean] [Reclined] [Twist▸] [Ascend] [Stalk] [Embrace]
Tension: [Relaxed] [Micro●] [Full]

CAMERA
[dropdown ▾]
□ Dutch tilt  □ Aerial  □ Fisheye  □ Film grain

HORMONE SPINE  ●──────  3
[1 Simmer ──────────── 3 Burn]

ACTION-TENSION
[Sustained] [Impact] [Explosive●]

N+3 DEPTH  ────●─  3
[n+1 ──────── n+3 ──────── n+5]

ASSEMBLED PROMPT  [▾]
─────────────────────────────
[▶ RUN RENDER ELITE]
─────────────────────────────
```

---

## Relevant Files

```
artifacts/api-server/src/lib/matrix-assembler.ts    ← NEW: prompt assembly engine
artifacts/api-server/src/lib/atmospheric-templates.ts ← NEW: n+1/n+3/n+5 templates
artifacts/api-server/src/routes/render-elite.ts     ← wire MatrixPromptAssembler
lib/api-spec/openapi.yaml                           ← extend request with matrixSelection
artifacts/render-elite-editor/src/App.tsx           ← replace concept panel with Matrix UI
artifacts/render-elite-editor/src/components/MatrixPanel.tsx ← NEW: Matrix operator component
```

---

## Definition of Done Checklist

- [ ] All 7 layers render in sidebar with correct input types
- [ ] Selecting any layer updates the Assembled Prompt preview in real time
- [ ] Assembled prompt follows the 11-step layer order exactly
- [ ] N+3 Depth 1–2 injects n+1 atmospheric template
- [ ] N+3 Depth 3–4 injects n+3 atmospheric template  
- [ ] N+3 Depth 5 injects n+5 atmospheric template verbatim
- [ ] Hormone Spine surfaces levels 1–3 only in UI
- [ ] Layer 7 Arousal Response auto-generates from Hormone level
- [ ] Freeform concept override appends after assembled prompt
- [ ] Character roster load pre-fills all Matrix defaults
- [ ] Vantrex / Veilroot / Ironroot / Nyxveil defaults correct
- [ ] MatrixPromptAssembler is a standalone class, not inlined in route
- [ ] Backward compatible — existing concept field still works without matrixSelection
- [ ] matrixSelection included in request schema as optional
- [ ] Assembled prompt visible in read-only expandable preview
- [ ] Style Memory BOOST/AVOID still appends in correct position (9th and 11th)
