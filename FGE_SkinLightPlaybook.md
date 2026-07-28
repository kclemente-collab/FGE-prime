# FGE SKIN & LIGHT RENDERING PLAYBOOK
## Grok Generation — Character Realism Master Instruction
### Agent Skill Module: RENDER-002

---

> *"Skin is not a surface. It is a volume.
> Light doesn't hit it — light enters it."*

---

## WHY THIS PLAYBOOK EXISTS

Every FGE character lives or dies
on skin and light.

A card with perfect materials and wrong skin
reads as digital.

A card with perfect skin and physical light
reads as real.

This playbook closes that gap.
It teaches Grok to render skin
the way V-Ray and Arnold do —
as a living volumetric material
that light travels through,
not a texture light bounces off.

---

## PART ONE — SKIN AS PHYSICS

### The Core Truth
```
Skin is not opaque.
Light enters the surface.
It scatters inside the tissue.
It exits in a different place.

That scattering is what makes
skin look alive.

Without it:
skin looks like plastic.
rubber. painted mask.

With it:
skin has warmth.
depth. life.
the red glow at ear edges.
the translucent fingertip.
the warm shadow under the jaw.

This is Subsurface Scattering (SSS).
It is non-negotiable for FGE characters.
```

---

### THE SSS INSTRUCTION FOR GROK

```
Core phrase — use in every character render:

"Skin physics: subsurface scattering active.
Light enters the skin surface,
scatters through dermis and epidermis,
exits at a nearby point.

Visible SSS indicators required:
- Ear edges: warm red-orange when backlit
- Fingertips and knuckles: translucent warmth
- Under jaw and nose: soft warm shadow,
  not hard — light bleeds through thin tissue
- Forehead: slight oiliness from sebum layer
- Cheekbones: warm subsurface flush
- Lips: semi-translucent, deeper color inside

Skin layers (render all three):
- Epidermis: outer layer, slight oiliness,
  catches specular highlight
- Dermis: middle layer, where SSS scatters,
  warm red-brown tones
- Hypodermis: deepest, affects shadow warmth

Random Walk SSS method:
light path is not uniform —
it wanders through tissue
creating natural variation.
No two areas scatter identically."
```

---

### SKIN BY CHARACTER

Each FGE character has specific skin physics.
These are constitutional — not suggestions.

**ZEN NOWHERE**
```
Ethnicity: Dark Latin-Asian synthesis
Tone: Deep warm olive — two continents
SSS depth: Medium-high
Sebum layer: Present — natural not oily
Highlight: Restrained — single cheekbone catch
Shadow: Warm, never cold
Micro-detail: Pore visibility at cheekbone,
              jaw, forehead
Backlit indicator: Warm amber at ear edges
Unique quality: Skin that has been in sun
                from two different directions —
                warmth that doesn't have
                a single geographic origin
Zen formula:
"Deep warm olive skin, dark Latin-Asian
synthesis. SSS medium-high depth.
Warm amber translucency at ear edges
when backlit. Single specular catch
on dominant cheekbone. Pore detail
visible at forehead and jaw.
Skin that has been under two suns.
Youth from hydration not products."
```

**RAVEN VOSS**
```
Tone: Deep brown, high melanin
SSS depth: Deep — light travels further
           before exiting
Highlight: Liquid chrome quality —
           high specular on cheekbone,
           brow, lip edge
Shadow: Deep, rich, not muddy
Micro-detail: High pore definition,
              smooth between pores
Backlit: Deep warm burgundy at ear edges
Unique quality: Skin that is simultaneously
                armor and invitation
Raven formula:
"Deep brown skin, high melanin depth.
SSS deep penetration — warm burgundy
translucency at backlit edges.
Liquid chrome specular quality
on cheekbone and brow.
Shadow is rich not dark —
depth not absence.
Skin as armor. Skin as invitation.
Both simultaneously."
```

---

### MICRO-PORE DETAIL INSTRUCTION

```
The difference between AI skin
and real skin is pore structure.

Tell Grok:

"Micro-pore detail active.
Skin is not smooth — it has topography.

Pore distribution:
- Forehead: medium pore density,
  slight texture
- Nose: higher density, visible structure
- Cheeks: fine texture, smooth between pores
- Jaw: medium, slight follicle shadow
- Under eyes: near-smooth, thin skin

Pore behavior in light:
- Highlight areas: pores catch slight shadow
  creating texture in the bright zones
- Shadow areas: pores less visible,
  depth takes over
- Transition zone (terminator):
  maximum pore visibility —
  this is where texture reads most clearly

Sebum layer:
Thin natural oil on skin surface.
Not greasy. Not dry.
Creates micro-specular highlights
in the thousands across the face.
This is the life quality of skin."
```

---

## PART TWO — LIGHT AS PHYSICS

### The Core Shift
```
Old thinking: ray tracing
Light shoots from source, hits surface, bounces.

New standard: path tracing
Light paths are calculated probabilistically.
Every possible light path sampled.
Result: cinematic truth.

The upgrade for Grok:
Stop asking for "good lighting."
Start describing physical light behavior.
```

---

### THE PATH TRACING INSTRUCTION

```
Core phrase:

"Lighting method: path tracing.
Not ray tracing. Not baked.
Path tracing — every light path
calculated probabilistically.

What this means for the render:
- Shadows are not black —
  they are filled by bounced light
  from every nearby surface
- Materials affect each other —
  gold reflects warm onto nearby skin
- Atmosphere scatters light —
  the air between light and subject
  has volume
- Multiple light sources interact —
  no single source is pure,
  they all affect each other

Cinematic realism target.
Movie-quality frame.
Not a photograph. Not a painting.
A frame from a film that was actually shot."
```

---

### THE FOUR LIGHT SOURCES — FGE STANDARD

Every FGE character render uses
this four-source architecture:

```
SOURCE 1 — KEY LIGHT
The primary story light.
Defines the character's mood.

Position: [specific angle — always specify]
Quality: [hard / soft / directional]
Color temperature: [warm / neutral / cool]
Function: creates the main shadow,
          defines the face structure

FGE default:
Warm directional, 45 degrees above,
30 degrees to dominant side.
Golden hour quality.
Color temp: 3200K-4000K

SOURCE 2 — FILL LIGHT
Lifts shadows. Never erases them.

Intensity: 25-40% of key
Position: opposite side of key
Quality: soft, diffuse
Function: reveals shadow detail
          without flattening the face

FGE default:
Cool bounce fill — as if sky or
environment is the source.
Not a light placed there —
a reflection of the world.

SOURCE 3 — RIM LIGHT
Separates subject from background.
Defines the silhouette.

Position: behind and to one side
Intensity: can exceed key for drama
Quality: hard edge preferred
Function: the character exists
          in three-dimensional space

FGE default:
Hard rim, warm or electric accent color.
This is the talisman flash.
The one moment of electric detail.

SOURCE 4 — ATMOSPHERIC LIGHT
The world itself as a light source.

Source: sky, environment, city glow,
        bounced interior
Function: fills the deepest shadows
          with the color of the world
          the character inhabits

FGE default:
Deep ochre or near-black ambient.
The world's color is always present
in the deepest shadow.
```

---

### LIGHT BY SCENE TYPE

```
ZEN NOWHERE — DESERT NOIR
Key: Late golden hour, hard directional
     from upper left, warm 3200K
Fill: Cool blue sky bounce, 30% intensity
Rim: Hard warm rim, catches talisman
Atmosphere: Dust particles in golden light,
            volumetric heat haze

Grok phrase:
"Late golden hour, single hard key light
upper left warm 3200K. Cool sky bounce fill
30%. Hard warm rim light — catches chrome
talisman in one electric flash. Volumetric
dust in golden air. Path tracing quality."

---

RAVEN VOSS — PENTHOUSE NOIR
Key: Single artificial source, cool-neutral,
     high angle, hard quality
Fill: City glow from below — warm neon
      colors bleed up from the street
Rim: Window light, cool blue-white
Atmosphere: Night city air, slight humidity,
            neon color scatter

Grok phrase:
"Single cool overhead key, hard quality.
City neon warm fill bleeding up from below.
Cool blue-white window rim. Night city
atmosphere — humidity with neon scatter.
Deep shadow with warm city undertone.
Path tracing. Film noir quality."

---

CARD HERO SHOT — MAXIMUM REALISM
Key: Studio softbox quality, controlled,
     warm neutral
Fill: Reflector bounce, 40% intensity
Rim: Two-sided rim for complete
     subject separation
Atmosphere: Clean studio air —
            the character is the atmosphere

Grok phrase:
"Controlled studio — large softbox key,
warm neutral. Reflector fill 40%.
Two-sided rim separation.
Clean air. Character is the only
atmospheric element.
V-Ray physical accuracy.
Hero shot. Definitive edition."
```

---

### STATE-OF-THE-ART LIGHT — 2026 STANDARDS

From the research — these are the
current render standards to invoke:

```
UE5 LUMEN + PATH TRACER
→ Real-time global illumination
  for scene setup
→ Path Tracer for final movie-quality frames
→ Invoke: "UE5 Lumen GI + Path Tracer final.
           Movie-quality frame.
           Real-time GI in scene,
           path traced final output."

D5 RENDER PATH TRACING
→ Fastest real-time path tracing
→ Preview in under 5 seconds
→ Invoke: "D5 real-time path tracing.
           Speed and quality balanced.
           Preview iteration speed,
           final output quality."

OCTANE 2026 SPECTRAL
→ Light as physical waves not colored rays
→ Most accurate reflections and skin tones
→ Invoke: "OctaneRender 2026 spectral mode.
           Light calculated as physical waves.
           Skin tones: maximum accuracy.
           Reflections: physically perfect.
           This is the most accurate
           version of this scene."

NVIDIA ReSTIR PT
→ 2-3x faster path tracing
→ Reuses light samples across frames
→ Invoke: "NVIDIA ReSTIR PT enhanced.
           Light samples reused for quality.
           Path tracing at maximum efficiency.
           2026 standard rendering."
```

---

## PART THREE — SKIN SCANNING INTELLIGENCE

### What The Hardware Research Means For Grok

The JuvaMap and Shape Tactics scanners
use spectral imaging to capture:
pores, wrinkles, pigmentation, oil levels.

This is what your prompts should demand.

```
TRANSLATE SCANNER SPECS TO GROK:

JuvaMap 17-indicator spectral →
"Capture 17 skin quality dimensions:
pores, wrinkles, pigmentation, oil level,
melanin depth, vascular visibility,
UV damage map, hydration level,
texture uniformity, follicle shadow,
sebum distribution, translucency zones,
micro-relief, color evenness,
elasticity suggestion, lip hydration,
under-eye thickness.
Not all visible simultaneously —
but all present in the render."

Shape Tactics 28MP HD →
"Micro-pore detail at 28-megapixel quality.
Individual pore visible.
Oil level mapping — where skin
is dryer vs more sebum-active.
Pore shadow detail at maximum resolution."
```

---

### THE SKIN QUALITY SCORING SYSTEM

Rate every character render across
these skin dimensions before finalizing:

```
DIMENSION               TARGET FOR FGE

SSS depth               Visible — light scatters
                        not just reflects

Micro-pore detail       Present in transition zone
                        between light and shadow

Sebum layer             Subtle specular in thousands
                        of micro-highlights

Shadow warmth           Warm not black
                        filled by bounced color

Translucency zones      Visible at ear, fingertip,
                        nostril edge, lip

Skin-specific color     Each zone has its tone:
                        forehead ≠ cheek ≠ jaw

Random Walk variation   No two areas identical —
                        life quality present

Constitutional fit      Does the skin belong
                        to this character's
                        origin and history?
```

---

## PART FOUR — THE COMPLETE CHARACTER FORMULA

This is the master prompt structure.
Use this for every FGE character final render.

```
"Renderer: [V-Ray / Arnold / Octane 2026]
Method: Path tracing — movie quality frame.

CHARACTER: [full physical description]

SKIN PHYSICS:
Subsurface scattering active — Random Walk method.
Skin is volumetric not surface.
Light enters, scatters, exits.

Epidermis: [oiliness level + specular quality]
Dermis: [SSS warmth + color]
Micro-pore: [density + distribution + zone detail]
Sebum layer: micro-specular in thousands

Translucency zones:
- Ear edges: [warm red/amber/burgundy — ethnicity specific]
- Fingertips: [translucent warmth]
- Under jaw: [soft warm shadow, light bleeds through]
- Lip edges: [semi-translucent depth]

LIGHTING — four source architecture:
Key: [position + quality + color temp]
Fill: [intensity + source logic + color]
Rim: [position + intensity + accent color]
Atmosphere: [world color in deepest shadow]

Light method: path tracing
Every shadow: filled by bounced light
Every material: affects adjacent surfaces
Atmosphere: volumetric — air has weight

ATMOSPHERE:
[environment type + particles + humidity + time]

FGE CONSTITUTIONAL:
Rugged but rich. This character's skin
has been somewhere real.
Every SSS zone confirms their origin.
Light reveals — does not flatter.
The tension between beauty and truth
is the render.

Output: Photorealistic. 8K.
Film grain: optional but recommended.
This is a hero shot. Definitive edition."
```

---

## PART FIVE — THE QUICK REFERENCE CARDS

*Copy these directly into Grok
for immediate quality uplift:*

```
SSS ACTIVATION:
"Skin: volumetric SSS active. Random Walk.
Light enters, scatters, exits.
Ear edges warm translucent.
Shadows warm not black."

PATH TRACING:
"Path tracing — not ray tracing.
Every light path probabilistic.
Shadows filled by bounced light.
Cinematic quality. Movie frame."

MICRO-PORE:
"Micro-pore detail. Individual pores visible
in transition zone. Sebum micro-specular.
Skin has topography not smoothness."

SPECTRAL SKIN:
"OctaneRender 2026 spectral.
Skin tones calculated from light wavelengths.
Most accurate skin render possible.
Color is physics not paint."

FOUR LIGHT:
"Four source lighting:
Key [position + temp].
Fill: 30-40% cool bounce.
Rim: hard, electric accent.
Atmosphere: world color in shadow."

COMPLETE QUICK:
"Arnold cinematic. SSS Random Walk.
Four source path traced lighting.
Micro-pore in transition zone.
Volumetric atmosphere.
Movie quality. FGE constitutional.
This skin has been somewhere real."
```

---

## MODULE IDENTITY

```
Module:     RENDER-002
Type:       Skill Module —
            Skin & Light Realism Playbook
Universe:   Feral Gloss Empire
Authority:  FGE Constitutional Law
            ET-CON-000001
Depends on: RENDER-001 (Renderer Playbook)
Engine:     Grok Primary
Version:    1.0 — 2026
Status:     Active

Invoke:     "Skin & Light Agent, active.
             Character: [name]"

Combine with:
→ RENDER-001 for renderer mode selection
→ TEX-AGENT-001 for material sourcing
→ FGE Constitution for character law
→ Character invoke templates
```

---

## THE FINAL INSIGHT

```
The scanner research confirms
what the best renderers already know:

Skin is a data set.
Not a color. Not a texture.
A map of 17+ physical properties
all responding to light simultaneously.

When you ask Grok to render skin —
you are asking it to simulate
a biological material with
volumetric physics, spectral response,
micro-topography, and living color.

The prompts in this playbook
give Grok the vocabulary to do that.

The result:

Characters that don't look generated.
Characters that look like they
have been somewhere real
and came back with the light
still on their skin.

That is the FGE standard.
That is the only acceptable output.
```

---

**RENDER-002 — FERAL GLOSS EMPIRE — 2026**
**SKIN IS VOLUMETRIC. LIGHT IS PHYSICAL.**
**NO REFUNDS — FINAL SALE**

---
*"The render is finished when the skin
looks like it has a temperature."*
