# FGE FOUNDATION SET — PRODUCTION ORDER (GROK)

Order ID: FGE-PROD-DECK-001 · Source authority: FGE-CONST-COMM-001 + FGE-CONST-LOCK-001 v1.1
Role of this line: PRODUCTION ONLY. Render to spec. Never alter locked elements. Flag drift, never resolve it.

---

## 1. OUTPUT SPECIFICATION

- **File type: PNG, lossless.** Card faces carry material signatures (obsidian depth, pearl iridescence, kintsugi gold, thin-film effects) — lossy compression destroys them. Never JPEG at generation stage.
- **Output class: single art panel per card. NOT an infographic.** No layout, no diagram, no labels.
- **Aspect: 2:3 portrait.** Minimum 1536 × 2304 px; generate at the highest resolution the window allows.
- **No text of any kind in the image.** No titles, numbers, logos, frames, or borders. Typography and the gold frame are applied later in a separate composition pass. If a generation produces text, it fails automatically.
- **Field: obsidian-black ground, tenebrist single-source lighting, hyperreal material rendering.** Every face must look wall-worthy alone, unframed.
- **File naming on export:** `[species]-[##]-[descriptor]-v1.png` → e.g. `artifact-01-mirror-fracture-v1.png`, `scene-02-mirror-cathedral-v1.png`, `character-01-isolde-voss-v1.png`

---

## 2. HOW THE CARDS WORK TOGETHER

Two species only:

- **NARRATIVE CARDS = subjects.** Characters and Scenes. The things that exist.
- **ARTIFACT CARDS = operators.** The transformations. They act on subjects, never on each other.

**An Assembly** = 1 Character + 1 Scene + 1–3 Artifacts.
Rules: one Artifact per domain, maximum one Dominant-weight Artifact per Assembly.
Artifacts always apply in this fixed order, regardless of how they're listed:

**FORM → ENVIRONMENT → MATERIAL → LIGHT → NARRATIVE**

Weights are render guidance: **Dominant (3)** commands the image. **Supporting (2)** transforms visibly but coexists. **Accent (1)** is detail-level seasoning.

**Locks override everything.** Locked character elements (listed per character below) are never altered by any Artifact, any stack, any prompt phrasing. If a render drifts on a locked element, the output is flagged and escalated — it is never self-corrected or reinterpreted on this line.

---

## 3. BATCH A — ARTIFACT CARD FACES (10 prompts, run first)

No characters appear in these. No lock exposure. Cheapest reviews. Run these in the next available window.

**ART-01 · MIRROR FRACTURE (Material · Dominant) — ✦ MINTED by Director decree 2026-06-10**
Canonical effect (as ratified from the minted face): fracture trapped INSIDE the glass — an internal radial starburst of fracture lines suspended within the material, the surface intact, the violence contained. No gold bleed. Card face is final; no further generation required. Reference prompt for derivative renders:
FGE Artifact card face — MIRROR FRACTURE. A monolithic shard of clear mirror-glass standing in absolute black void, an internal radial starburst of fracture lines trapped inside the intact glass, fractures radiating from a dense center point, every internal fracture catching a cold edge light, faint warm tones deep in the fracture core, thin-film ghosting at the shard's edges, tenebrist single-source lighting, hyperreal material rendering, centered totemic composition, 2:3 portrait, no text.

**ART-02 · KINTSUGI ASCENSION (Material · Supporting)**
FGE Artifact card face — KINTSUGI ASCENSION. A shattered slab of cracked Calacatta marble suspended in black void, every fracture filled with luminous molten gold, the gold seams glowing from within as the slab's fragments lift and separate slightly in ascension, warm metallic gold against cold white stone, tenebrist lighting, hyperreal material rendering, centered totemic composition, 2:3 portrait, no text.

**ART-03 · OBSIDIAN VEIL (Material · Supporting)**
FGE Artifact card face — OBSIDIAN VEIL. A flowing sheet of liquid volcanic glass suspended mid-drape in black void, surface deepening into layered internal reflections, conchoidal fracture edges catching a single cold key light, depth visible inside the black material like a frozen night sea, tenebrist lighting, hyperreal obsidian rendering, centered totemic composition, 2:3 portrait, no text.

**ART-04 · PEARL BLOOM (Material · Supporting)**
FGE Artifact card face — PEARL BLOOM. A sphere of clear nacre in black void, thin-film iridescence blooming across its surface in slow waves of rose, teal, and gold interference color, internal light diffusing through translucent pearl layers, soft single key light, hyperreal thin-film optics, centered totemic composition, 2:3 portrait, no text.

**ART-05 · LABRADORITE SURGE (Material · Accent)**
FGE Artifact card face — LABRADORITE SURGE. A rough-cut slab of dark labradorite in black void, a sudden surge of electric blue-green labradorescence flashing across its surface at a raking angle, the internal fire visible only where the single light strikes, the rest of the stone nearly black, hyperreal mineral optics, centered totemic composition, 2:3 portrait, no text.

**ART-06 · CHROME SANCTIFY (Material · Supporting)**
FGE Artifact card face — CHROME SANCTIFY. A rising column of liquid chrome in black void, mirror-polished metal in mid-flow holding a perfect distorted reflection of a single cold light source, surface tension rendered with machined precision, droplets suspended at its crown, hyperreal liquid-metal rendering, tenebrist lighting, centered totemic composition, 2:3 portrait, no text.

**ART-07 · SOLAR BLOOM (Light · Dominant)**
FGE Artifact card face — SOLAR BLOOM. A single overwhelming warm golden light source erupting at center frame in absolute black void, radial bloom consuming the darkness, lens-real flare structure, dust motes igniting in the beam, the boundary between gold light and obsidian black rendered as the entire subject, 2:3 portrait, no text.

**ART-08 · TENEBRIST CROWN (Light · Accent)**
FGE Artifact card face — TENEBRIST CROWN. A thin, hard rim of cold white light tracing the silhouette of an unseen form in absolute black void, the light itself the only subject, a halo-edge of illumination against total darkness, chiaroscuro at its most extreme, 2:3 portrait, no text.

**ART-09 · OBSIDIAN CROWN (Form · Accent)**
FGE Artifact card face — OBSIDIAN CROWN. A regal crown of fractured volcanic glass floating in black void, shards arranged in sharp ascending geometry, hairline gold seams binding the fractures, cold key light catching the glass edges, beauty forged in violence and sharpness by design, hyperreal material rendering, centered totemic composition, 2:3 portrait, no text.

**ART-10 · DUST CORRUPTION (Environment · Dominant)**
FGE Artifact card face — DUST CORRUPTION. A horizon line dissolving into crimson particulate ash, the air itself thick with suspended dust catching a dying light, ground surfaces crumbling to powder mid-frame, deep obsidian shadow consuming the lower third, oppressive atmospheric density, tenebrist palette of crimson and black, 2:3 portrait, no text.

---

## 4. BATCH B — SCENE CARD FACES (5 prompts, run second)

Worlds without subjects. No figures anywhere in frame.

**SCN-01 · CRIMSON DESERT**
FGE Scene card face — CRIMSON DESERT. An endless desert of deep crimson sand under a black sky, dune ridges carved sharp by wind, the aftermath of ancient wars implied by half-buried obsidian monoliths, a low dying light raking across the ridges, ash drifting in the air, empty of figures, immense scale, tenebrist palette of crimson and black, hyperreal terrain rendering, 2:3 portrait, no text.

**SCN-02 · MIRROR CATHEDRAL**
FGE Scene card face — MIRROR CATHEDRAL. A vast gothic interior built entirely of mirrored planes, columns and vaulting reflecting each other into infinite recursive depth, a single cold shaft of light descending through the central vault, every reflective surface edged with hairline gold seams, empty of figures, immense scale, tenebrist lighting, hyperreal architectural rendering, 2:3 portrait, no text.

**SCN-03 · GLASS FOREST**
FGE Scene card face — GLASS FOREST. A forest of towering translucent glass trees in black night, trunks and branches refracting a single moon-cold light source into prismatic fragments, the forest floor littered with fallen crystalline leaves catching faint iridescence, empty of figures, light passing through matter at landscape scale, hyperreal refraction rendering, 2:3 portrait, no text.

**SCN-04 · OBSIDIAN COAST**
FGE Scene card face — OBSIDIAN COAST. A volcanic-glass shoreline at night, black cliffs of layered obsidian meeting a dark sea, wave-polished glass surfaces holding deep internal reflections, a thin cold light on the horizon line, hairline gold veins visible in the cliff fractures, empty of figures, immense scale, hyperreal mineral rendering, 2:3 portrait, no text.

**SCN-05 · PEARL ATRIUM**
FGE Scene card face — PEARL ATRIUM. A vast interior atrium whose walls and dome are formed of layered nacre, soft iridescent light diffusing through translucent pearl surfaces in waves of rose, teal, and gold, a still reflecting pool at center, empty of figures, the soft luminous counterweight to a world of black glass, hyperreal thin-film rendering, 2:3 portrait, no text.

---

## 5. BATCH C — CHARACTER CARD FACE: ISOLDE VOSS (run last, canon line first)

Character cards wrap the existing Master Anchor. Structure — paste the locked anchor, then append:

```
[ISOLDE VOSS MASTER ANCHOR PROMPT — verbatim, inserted by Director]

+ CARD FACE DIRECTIVES: 2:3 portrait, subject centered, chest-up totemic
  composition, gaze direct to camera, obsidian-black void ground, single
  cold key light upper-left, tenebrist falloff, hyperreal Feral Gloss
  skin rendering, no text, no frame, no logo.
```

**HARD LOCKS — never altered by any artifact, prompt, or variation:**
- Uniform green eyes, exact. NO heterochromia, ever.
- Black hair, precise center part, single signature hair lock. Acceptable natural grey drift only. NO silver-dominant hair read.
- Perpetual faint smile.
- Feral Gloss skin with iridescent photonic blooms.

Any output drifting on these = flag and escalate. Do not regenerate toward your own interpretation.

All other Foundation characters (Calista, NyxVeil Echo, Veilroot Warden, Ironroot Behemoth, slots 06–10) are NOT cleared for card production until their dossiers and manifests exist. Do not improvise them.

---

## 6. EXAMPLE — HOW AN ASSEMBLY COMPILES

The inaugural Assembly: **ISOLDE VOSS × MIRROR FRACTURE × MIRROR CATHEDRAL**

Compile order: Scene establishes the world → Material artifact transforms it → character locks ride on top, untouched. The prompt assembles as:

```
[ISOLDE VOSS MASTER ANCHOR — verbatim]

standing in the Mirror Cathedral: a vast gothic interior built entirely
of mirrored planes reflecting into infinite recursive depth, a single
cold shaft of light descending through the central vault,

transformed by MIRROR FRACTURE (Dominant): radial fracture starbursts
trapped INSIDE the cathedral's mirrored planes, internal fracture lines
radiating through every intact reflective surface, her reflection
multiplied and fractured within the glass while the space itself holds —

HARD LOCKS UNCHANGED: uniform green eyes exact, black hair precise
center part with single signature lock, faint perpetual smile, Feral
Gloss skin with iridescent photonic blooms. The fracture transforms
the world and her reflections, never her body or face.

Output: hero poster, 2:3 portrait, tenebrist lighting, hyperreal
material rendering, no text.
```

This is the pattern for every future Assembly: scene grounds, artifacts transform in ladder order, locks ride untouched, output class declared last.

---

## 7. WINDOW SEQUENCE

1. Isolde lookbook shots 02–08 remain priority one. This order does not preempt them.
2. Batch A (10 artifact faces) — fill remaining window budget; ~2–3 windows.
3. Batch B (5 scene faces).
4. Batch C (Isolde card face) — canon line renders the anchor card first; production variants after.
5. Inaugural Assembly render — only after its three component cards exist and pass review.

— End of production order. Authority for all decisions remains with the Director. —
