import { useState, useRef } from "react";

const CATEGORIES = [
  "All", "Stone", "Onyx", "Pearl", "Gemstone",
  "Metal", "Sheen", "Organic", "Fabric",
  "Atmospheric", "Card FX", "FGE Signature"
];

const materials = [
  // ── STONE ──────────────────────────────────────────────────────────────
  {
    id: "carrara", name: "Carrara Marble", category: "Stone",
    tags: ["SSS", "veining", "classic", "translucent"],
    accent: "#c8b89a", character: "World Standard",
    bg: "linear-gradient(135deg,#f5f5f0 0%,#e8e4dc 30%,#f0ede6 60%,#e4e0d8 100%)",
    vein: "repeating-linear-gradient(25deg,transparent 0px,transparent 18px,rgba(180,170,155,.3) 18px,rgba(180,170,155,.3) 19px,transparent 19px,transparent 35px,rgba(160,150,135,.2) 35px,rgba(160,150,135,.2) 36px)",
    prompt: {
      core: "Carrara white marble, fine grey veining on warm white, subsurface scattering, translucent depth, organic crack patterns",
      lighting: "single directional light, soft shadows, light penetrates surface",
      quality: "physically based material, Arnold render quality, 8K texture, tactile surface",
      fge: "FGE world standard material, classical luxury with history, the baseline everything is measured against",
      grok: "Render Carrara marble — white ground, fine grey veining, SSS glow, photorealistic 8K. FGE aesthetic: luxury that has survived something."
    }
  },
  {
    id: "nero", name: "Nero Marquina", category: "Stone",
    tags: ["dramatic", "gold veining", "power", "statement"],
    accent: "#c8aa50", character: "World Architecture",
    bg: "linear-gradient(135deg,#1a1a1a 0%,#0d0d0d 40%,#1f1f1f 70%,#111 100%)",
    vein: "repeating-linear-gradient(35deg,transparent 0px,transparent 22px,rgba(200,170,80,.4) 22px,rgba(200,170,80,.4) 23px,transparent 23px,transparent 45px,rgba(180,150,60,.25) 45px,rgba(180,150,60,.25) 46px)",
    prompt: {
      core: "Nero Marquina black marble, dramatic gold and white veining, deep black ground, mirror polish",
      lighting: "dramatic single light, strong specular, deep shadows, gold veins catch light",
      quality: "Octane material quality, physically based render, 8K, mirror-like polish",
      fge: "FGE near-black palette, electric gold accent, dangerous luxury, the world's floor",
      grok: "Nero Marquina black marble — deep black, gold veining, mirror polish, dramatic light. FGE: near-black with electric accent, power without apology."
    }
  },
  {
    id: "black-galaxy", name: "Black Galaxy Granite", category: "Stone",
    tags: ["cosmic", "speckled", "crystalline", "grounded"],
    accent: "#d4a840", character: "World Exterior",
    bg: "linear-gradient(135deg,#0f0f0f 0%,#141414 50%,#0a0a0a 100%)",
    vein: "radial-gradient(circle at 20% 30%,rgba(212,168,64,.8) 1px,transparent 2px),radial-gradient(circle at 60% 70%,rgba(180,140,50,.6) 1px,transparent 2px),radial-gradient(circle at 80% 20%,rgba(220,180,70,.7) 1px,transparent 2px),radial-gradient(circle at 40% 80%,rgba(160,130,40,.5) 1px,transparent 2px),radial-gradient(circle at 55% 45%,rgba(200,160,60,.6) 1px,transparent 2px)",
    prompt: {
      core: "Black Galaxy granite, deep black base, gold and bronze mineral speckles, crystalline inclusions, cosmic star-field pattern",
      lighting: "multiple light sources, each crystal catches differently, depth in surface",
      quality: "crystalline detail, physically based, 8K mineral texture",
      fge: "FGE cosmic energy, earned luxury, the universe compressed to stone",
      grok: "Black Galaxy granite — deep black, gold mineral speckles catching light like stars. FGE: cosmic dark energy, the street compressed to luxury."
    }
  },
  {
    id: "travertine", name: "Honed Travertine", category: "Stone",
    tags: ["porous", "Mediterranean", "matte", "ancient"],
    accent: "#c4a878", character: "World Background",
    bg: "linear-gradient(135deg,#d4c4a8 0%,#c8b898 30%,#d0bc9c 60%,#bca888 100%)",
    vein: "radial-gradient(ellipse at 30% 40%,rgba(100,80,50,.4) 3px,transparent 4px),radial-gradient(ellipse at 70% 60%,rgba(120,90,55,.3) 2px,transparent 3px),radial-gradient(ellipse at 50% 20%,rgba(90,70,45,.35) 4px,transparent 5px)",
    prompt: {
      core: "Honed travertine, warm beige porous surface, natural pit holes, sedimentary layers, matte Mediterranean finish",
      lighting: "diffuse soft light, matte surface absorbs rather than reflects, warm tone",
      quality: "porous material detail, physically based matte shader, 8K",
      fge: "FGE ancient luxury — something that has existed longer than wealth, warmth with age",
      grok: "Honed travertine — warm beige, natural pits, matte Mediterranean surface. FGE: ancient before luxury existed, warm and porous with history."
    }
  },
  // ── ONYX ───────────────────────────────────────────────────────────────
  {
    id: "honey-onyx", name: "Honey Onyx", category: "Onyx",
    tags: ["backlit", "glowing", "amber", "translucent max"],
    accent: "#f0b840", character: "World Lighting",
    bg: "linear-gradient(135deg,#c4822a 0%,#e8a84a 25%,#b87030 50%,#d4943c 75%,#c07828 100%)",
    vein: "repeating-linear-gradient(15deg,transparent 0px,transparent 12px,rgba(255,220,120,.5) 12px,rgba(255,220,120,.5) 13px,transparent 13px,transparent 28px,rgba(180,110,20,.3) 28px,rgba(180,110,20,.3) 29px)",
    prompt: {
      core: "Honey onyx, extreme translucency, amber and gold layered bands, backlit internal glow, warm light scattering through surface",
      lighting: "backlit from behind, warm amber light transmission, glowing edges, subsurface luminosity",
      quality: "volumetric light scatter, maximum SSS, physically based, 8K",
      fge: "FGE warm electric accent — luxury that glows from the inside, warmth you cannot fake",
      grok: "Honey onyx backlit — extreme translucency, amber bands glowing from within. FGE: the electric accent made material, warmth earned not installed."
    }
  },
  {
    id: "black-onyx", name: "Black Onyx", category: "Onyx",
    tags: ["void", "gemstone", "absolute black", "power"],
    accent: "#3a3a4a", character: "Main Villain Implied",
    bg: "linear-gradient(135deg,#0a0a0a 0%,#151515 30%,#080808 60%,#121212 100%)",
    vein: "repeating-linear-gradient(20deg,transparent 0px,transparent 30px,rgba(40,40,50,.6) 30px,rgba(40,40,50,.6) 31px,transparent 31px,transparent 55px)",
    prompt: {
      core: "Black onyx gemstone, near-perfect black, barely visible band layers, deep lustre, gemstone polish, void-like depth",
      lighting: "minimal light, single specular point highlight, deep absorbing surface",
      quality: "gemstone render, extreme depth, physically based, 8K",
      fge: "FGE absolute — power without announcement, the villain's material, darkness that chose itself",
      grok: "Black onyx — near-perfect black, gemstone polish, barely visible depth layers. FGE: absolute power, the material of those who need no introduction."
    }
  },
  // ── PEARL ──────────────────────────────────────────────────────────────
  {
    id: "south-sea-pearl", name: "South Sea Pearl", category: "Pearl",
    tags: ["nacre", "organic", "soft glow", "orient"],
    accent: "#e8ddd0", character: "Luxury Standard",
    bg: "radial-gradient(ellipse at 35% 35%,#f8f4ee 0%,#ede8e0 40%,#d8d0c4 70%,#c8c0b4 100%)",
    vein: "linear-gradient(135deg,rgba(255,255,255,.6) 0%,transparent 40%,rgba(220,210,195,.4) 60%,transparent 100%)",
    prompt: {
      core: "South Sea pearl, organic nacre layers, soft orient sheen, warm cream to pink iridescence, silky diffuse glow",
      lighting: "soft diffuse light, multiple nacre layer reflections, gentle orient shimmer",
      quality: "organic nacre shader, soft SSS, 8K",
      fge: "FGE silk shirt energy — soft luxury that earned its glow through layers of time",
      grok: "South Sea pearl — organic nacre, warm cream iridescence, silky orient glow. FGE: the silk shirt made material, soft luxury with structural depth."
    }
  },
  {
    id: "tahitian-pearl", name: "Tahitian Black Pearl", category: "Pearl",
    tags: ["dark iridescence", "peacock", "rare", "Raven Voss"],
    accent: "#00b464", character: "Raven Voss",
    bg: "radial-gradient(ellipse at 35% 35%,#2a2a2a 0%,#1a1a1a 40%,#0f0f0f 70%,#080808 100%)",
    vein: "linear-gradient(135deg,rgba(0,180,100,.4) 0%,transparent 30%,rgba(80,60,180,.3) 50%,transparent 70%,rgba(0,150,80,.3) 100%)",
    prompt: {
      core: "Tahitian black pearl, deep charcoal base, green peacock overtone iridescence, dark orient shimmer, mysterious nacre depth",
      lighting: "precise light reveals green overtone, dark depth with surface luminosity",
      quality: "dark nacre shader, iridescent overtone, organic gemstone render, 8K",
      fge: "Raven Voss material — shadow with iridescent truth underneath, darkness that contains multitudes",
      grok: "Tahitian black pearl — deep charcoal, green peacock overtone iridescence. FGE Raven Voss: shadow exterior, electric truth revealed by light."
    }
  },
  // ── GEMSTONE ───────────────────────────────────────────────────────────
  {
    id: "fire-opal", name: "Fire Opal", category: "Gemstone",
    tags: ["iridescent", "spectral", "prismatic", "talisman"],
    accent: "#ff6b35", character: "Talisman Center",
    bg: "linear-gradient(135deg,#ff6b35 0%,#f7931e 20%,#fcee21 40%,#39b54a 60%,#1c75bc 80%,#9e1f63 100%)",
    vein: "linear-gradient(45deg,rgba(255,255,255,.3) 0%,transparent 50%,rgba(255,255,255,.2) 100%)",
    prompt: {
      core: "Fire opal gemstone, intense play of color, spectral iridescence shifting orange to red to green to blue, internal fire, prismatic diffraction",
      lighting: "light source reveals full spectrum, color shifts with angle, internal combustion glow",
      quality: "gemstone render, volumetric color scatter, iridescent shader, 8K",
      fge: "FGE talisman center gem — the electric accent at its maximum, impossible color that changes truth depending on angle",
      grok: "Fire opal — full spectral play of color, internal fire, prismatic shift with angle. FGE: the talisman center, the universe's impossible electric detail."
    }
  },
  {
    id: "labradorite", name: "Labradorite", category: "Gemstone",
    tags: ["labradorescence", "electric flash", "dark base", "constitutional"],
    accent: "#0096ff", character: "Constitutional Signature",
    bg: "linear-gradient(135deg,#2a2d35 0%,#1e2128 40%,#252830 70%,#1a1d24 100%)",
    vein: "linear-gradient(45deg,rgba(0,150,255,.5) 0%,rgba(0,200,150,.4) 25%,rgba(100,50,200,.3) 50%,rgba(0,180,255,.4) 75%,transparent 100%)",
    prompt: {
      core: "Labradorite, labradorescence — electric blue and teal metallic flash across dark grey base, schiller effect, angle-dependent color shift",
      lighting: "directional light triggers full labradorescence, blue-green metallic flash, dark base contrast",
      quality: "iridescent shader, angle-dependent color, physically based, 8K",
      fge: "FGE constitutional material — dark surface hiding electric truth, the talisman stone, what you are vs what you reveal",
      grok: "Labradorite — dark grey base, electric blue-green flash reveals on light angle. FGE constitutional: dark outside, electric truth within. The talisman material."
    }
  },
  {
    id: "malachite", name: "Malachite", category: "Gemstone",
    tags: ["green banding", "toxic beauty", "hypnotic", "serpent"],
    accent: "#00a050", character: "Shadow Serpent",
    bg: "linear-gradient(135deg,#1a4a1a 0%,#2a6a2a 25%,#0f380f 50%,#1e5a1e 75%,#153015 100%)",
    vein: "repeating-linear-gradient(90deg,transparent 0px,transparent 8px,rgba(0,180,80,.4) 8px,rgba(0,180,80,.4) 10px,transparent 10px,transparent 20px,rgba(0,120,50,.3) 20px,rgba(0,120,50,.3) 22px)",
    prompt: {
      core: "Malachite stone, deep green banding, concentric circular patterns, toxic saturated green, hypnotic repeating layers, polished surface",
      lighting: "even studio light reveals full band pattern, strong green saturation, wet-look polish",
      quality: "gemstone polish, banding detail, physically based, 8K",
      fge: "Shadow Serpent material — toxic beauty, the pattern you cannot look away from, danger wearing the color of life",
      grok: "Malachite — deep green banding, hypnotic concentric pattern, polished toxic beauty. FGE Shadow Serpent: danger wearing the color of life, impossible to look away."
    }
  },
  {
    id: "lapis", name: "Lapis Lazuli", category: "Gemstone",
    tags: ["ancient", "gold pyrite", "deep blue", "night sky"],
    accent: "#c8a030", character: "World Night",
    bg: "linear-gradient(135deg,#1a2060 0%,#0f1545 30%,#1e2870 60%,#0a1035 100%)",
    vein: "radial-gradient(circle at 25% 35%,rgba(200,160,40,.8) 2px,transparent 3px),radial-gradient(circle at 65% 55%,rgba(180,140,30,.6) 1px,transparent 2px),radial-gradient(circle at 80% 25%,rgba(220,180,50,.7) 2px,transparent 3px),repeating-linear-gradient(40deg,transparent 0px,transparent 25px,rgba(255,255,255,.08) 25px,rgba(255,255,255,.08) 26px)",
    prompt: {
      core: "Lapis lazuli, deep ultramarine blue, gold pyrite flecks scattered through surface, white calcite veins, ancient stone weight",
      lighting: "gold pyrite catches light against deep blue, night sky depth",
      quality: "semi-precious stone render, gold fleck detail, 8K",
      fge: "FGE world night material — the Vegas sky compressed to stone, gold in the dark, ancient before luxury was invented",
      grok: "Lapis lazuli — deep ultramarine blue, gold pyrite flecks like stars, ancient weight. FGE: the night sky made stone, gold hiding in darkness."
    }
  },
  {
    id: "obsidian", name: "Volcanic Obsidian", category: "Gemstone",
    tags: ["volcanic", "glass", "razor", "void", "villain"],
    accent: "#2a1a3a", character: "Main Villain",
    bg: "linear-gradient(135deg,#0a0508 0%,#100810 40%,#080408 70%,#0c060c 100%)",
    vein: "linear-gradient(135deg,rgba(80,20,100,.2) 0%,transparent 40%,rgba(60,10,80,.15) 60%,transparent 100%)",
    prompt: {
      core: "Volcanic obsidian, natural glass from volcanic origin, conchoidal fracture pattern, razor-sharp edges, deep black with subtle purple sheen",
      lighting: "single light source, glass-like specular, razor edge highlights, volcanic origin depth",
      quality: "natural glass shader, fracture detail, physically based, 8K",
      fge: "Main Villain material — formed in violence, beautiful and dangerous, natural glass that cuts without trying",
      grok: "Volcanic obsidian — natural black glass, conchoidal fracture, razor edges with purple depth. FGE Main Villain: formed in violence, cuts without trying."
    }
  },
  {
    id: "rutilated-quartz", name: "Rutilated Quartz", category: "Gemstone",
    tags: ["captured lightning", "clear", "gold needles", "forge"],
    accent: "#d4a030", character: "The Forge",
    bg: "linear-gradient(135deg,rgba(240,235,220,.9) 0%,rgba(255,250,240,.95) 40%,rgba(235,230,215,.9) 70%,rgba(245,240,225,.95) 100%)",
    vein: "repeating-linear-gradient(35deg,transparent 0px,transparent 8px,rgba(180,130,20,.6) 8px,rgba(180,130,20,.6) 9px,transparent 9px,transparent 20px,rgba(160,110,15,.4) 20px,rgba(160,110,15,.4) 21px)",
    prompt: {
      core: "Rutilated quartz, clear quartz crystal with gold titanium needle inclusions, lightning captured in glass, transparent with internal gold filaments",
      lighting: "light passes through crystal, gold needles catch and redirect light, internal sparkle",
      quality: "crystal transparency shader, inclusion detail, volumetric light, 8K",
      fge: "The Forge material — something trapped inside something clear, generation and judgment simultaneously visible",
      grok: "Rutilated quartz — clear crystal, gold needle inclusions like trapped lightning. FGE Forge: generation and judgment simultaneously, something powerful trapped in transparency."
    }
  },
  {
    id: "tiger-eye", name: "Tiger Eye", category: "Gemstone",
    tags: ["chatoyancy", "silk band", "gold brown", "moving light"],
    accent: "#c07820", character: "Legendary Tier",
    bg: "linear-gradient(135deg,#6a3a10 0%,#a06020 25%,#7a4815 50%,#c07828 75%,#8a5018 100%)",
    vein: "repeating-linear-gradient(90deg,transparent 0px,transparent 4px,rgba(255,200,80,.3) 4px,rgba(255,200,80,.3) 5px,transparent 5px,transparent 10px)",
    prompt: {
      core: "Tiger eye gemstone, chatoyancy effect — silk-like moving light band across gold and brown surface, cat's eye optical phenomenon, warm mineral tones",
      lighting: "moving light source reveals chatoyancy band, shifts across surface like living silk",
      quality: "chatoyancy shader, moving light band, physically based, 8K",
      fge: "FGE Legendary material — warmth and danger in one surface, the light that moves when you move",
      grok: "Tiger eye — chatoyancy silk band moving across gold-brown surface. FGE Legendary: warmth carrying danger, the light that shifts when you shift."
    }
  },
  // ── METAL ──────────────────────────────────────────────────────────────
  {
    id: "liquid-chrome", name: "Liquid Chrome", category: "Metal",
    tags: ["mirror", "liquid", "stretch-snap", "Raven Voss"],
    accent: "#e0e8f0", character: "Raven Voss Hot Metric",
    bg: "linear-gradient(135deg,#c0c8d8 0%,#e8eef8 30%,#a0b0c8 60%,#d0d8e8 100%)",
    vein: "linear-gradient(45deg,rgba(255,255,255,.8) 0%,transparent 30%,rgba(200,210,230,.6) 50%,transparent 70%,rgba(255,255,255,.5) 100%)",
    prompt: {
      core: "Liquid chrome surface, mirror-like metallic finish, stretch and snap quality, wet chrome appearance, perfect specular reflection, fluid metal",
      lighting: "environment reflections in surface, studio reflections, wet metal gleam",
      quality: "chrome shader, perfect specular, environment mapping, 8K",
      fge: "Raven Voss Hot Metric — liquid chrome stretch-snap, the material of her power, mirror that shows you what she allows",
      grok: "Liquid chrome — mirror-like wet metal, perfect specular, stretch-snap quality. FGE Raven Voss: the material of her power, you see yourself in it on her terms."
    }
  },
  {
    id: "sterling-silver", name: "Sterling Silver", category: "Metal",
    tags: ["matte silver", "Zen Nowhere", "minimalist", "talisman chain"],
    accent: "#c8ccd8", character: "Zen Nowhere",
    bg: "linear-gradient(135deg,#a8acb8 0%,#c4c8d4 30%,#989ca8 60%,#b8bcc8 100%)",
    vein: "linear-gradient(45deg,rgba(255,255,255,.4) 0%,transparent 40%,rgba(200,204,216,.3) 60%,transparent 100%)",
    prompt: {
      core: "Sterling silver, warm grey metallic, subtle brushed finish, minimalist clean surface, not mirror — dignified matte sheen",
      lighting: "soft directional light, restrained specular, dignified reflection",
      quality: "brushed metal shader, restrained sheen, physically based, 8K",
      fge: "Zen Nowhere chain material — minimalist, doesn't announce itself, catches light once and then you stop looking",
      grok: "Sterling silver minimalist — warm grey, brushed not mirror, dignified sheen. FGE Zen Nowhere: doesn't announce itself, you notice it once then forget until it matters."
    }
  },
  {
    id: "aged-brass", name: "Aged Brass", category: "Metal",
    tags: ["patina", "oxidized", "warm gold", "earned"],
    accent: "#a07830", character: "Constitutional Accent",
    bg: "linear-gradient(135deg,#7a5820 0%,#a07838 25%,#6a4818 50%,#906830 75%,#785020 100%)",
    vein: "radial-gradient(ellipse at 40% 30%,rgba(0,80,40,.4) 8px,transparent 12px),radial-gradient(ellipse at 70% 65%,rgba(0,60,30,.3) 6px,transparent 10px)",
    prompt: {
      core: "Aged brass with green patina in recesses, warm gold base, oxidized copper-green in corners and crevices, earned tarnish, natural patina over time",
      lighting: "warm light on brass high points, cool shadow in oxidized recesses, two-tone depth",
      quality: "patina detail, physically based aged metal, 8K",
      fge: "FGE constitutional accent — warm gold that has been through something, the repair made visible, age as luxury",
      grok: "Aged brass — warm gold base, green copper patina in recesses. FGE: the repair made visible, age as earned luxury, gold that survived."
    }
  },
  {
    id: "kintsugi-gold", name: "Kintsugi Gold Fill", category: "Metal",
    tags: ["repair", "gold in cracks", "broken luxury", "constitutional"],
    accent: "#d4a020", character: "Constitutional Signature",
    bg: "linear-gradient(135deg,#f0ede6 0%,#e4e0d8 40%,#ece8e0 70%,#d8d4cc 100%)",
    vein: "linear-gradient(60deg,transparent 0%,transparent 45%,rgba(200,160,20,.95) 45%,rgba(220,180,30,1) 47%,transparent 47%,transparent 70%,rgba(185,145,15,.85) 70%,rgba(205,165,25,.9) 72%,transparent 72%),repeating-linear-gradient(25deg,transparent 0px,transparent 18px,rgba(180,170,155,.25) 18px,rgba(180,170,155,.25) 19px)",
    prompt: {
      core: "Kintsugi repair — cracked marble or ceramic surface, stress fractures filled with liquid gold, gold seams running through broken surface, repaired and more valuable",
      lighting: "gold repairs catch light stronger than base surface, warm accent glow in repair lines",
      quality: "gold liquid in cracks, tactile depth, physically based, 8K",
      fge: "FGE constitutional law made material — broken and more valuable because of it, the world's founding aesthetic in physical form",
      grok: "Kintsugi gold repair — cracked white marble, gold liquid filling every fracture. FGE constitutional: broken and more valuable, the world's aesthetic law in stone."
    }
  },
  // ── SHEEN ──────────────────────────────────────────────────────────────
  {
    id: "wet-surface", name: "Wet Sheen", category: "Sheen",
    tags: ["rain", "reflective", "street", "Zen Nowhere scene"],
    accent: "#8ab0d0", character: "Scene Atmosphere",
    bg: "linear-gradient(135deg,#1a2030 0%,#242838 30%,#1c2235 60%,#202535 100%)",
    vein: "linear-gradient(180deg,rgba(120,160,200,.6) 0%,transparent 30%,rgba(100,140,190,.4) 60%,transparent 100%)",
    prompt: {
      core: "Wet surface sheen, rain-soaked pavement or stone, reflective water film, ambient light reflects in wet surface, depth of pooled reflection",
      lighting: "environmental reflections in water film, rim lighting from wet edges, night or dusk atmosphere",
      quality: "wet surface shader, reflection depth, physically based, 8K",
      fge: "Zen Nowhere scene material — the street made beautiful by rain, ground-level luxury, sand on boots in every scene",
      grok: "Wet street surface — rain film, environmental reflections, dusk atmosphere. FGE Zen Nowhere: the street made beautiful, sand and rain, where he actually comes from."
    }
  },
  {
    id: "satin-sheen", name: "Satin Sheen", category: "Sheen",
    tags: ["soft gloss", "fabric light", "luxury", "silk adjacent"],
    accent: "#d0c4b0", character: "Wardrobe Standard",
    bg: "linear-gradient(135deg,#c8bca8 0%,#ddd0bc 30%,#c0b49e 60%,#d4c8b4 100%)",
    vein: "linear-gradient(45deg,rgba(255,255,255,.5) 0%,transparent 40%,rgba(220,210,195,.4) 60%,transparent 100%)",
    prompt: {
      core: "Satin surface sheen, soft gloss finish, fabric-like light catch, not mirror — luxurious semi-gloss, smooth with depth",
      lighting: "soft directional light, fabric-quality specular, gentle highlight roll-off",
      quality: "satin shader, soft gloss, physically based, 8K",
      fge: "FGE wardrobe standard — the sheen of silk that has been worn, luxury with body heat in it",
      grok: "Satin sheen — soft gloss, fabric-quality light catch, not mirror but luminous. FGE: luxury with body heat in it, worn not displayed."
    }
  },
  {
    id: "patent-leather", name: "Patent Leather", category: "Sheen",
    tags: ["mirror leather", "gloss", "aggressive luxury", "confrontational"],
    accent: "#202020", character: "Confrontational Tier",
    bg: "linear-gradient(135deg,#080808 0%,#181818 30%,#0c0c0c 60%,#141414 100%)",
    vein: "linear-gradient(135deg,rgba(255,255,255,.4) 0%,transparent 20%,rgba(200,200,200,.2) 40%,transparent 60%,rgba(255,255,255,.3) 80%,transparent 100%)",
    prompt: {
      core: "Patent leather surface, high-gloss mirror finish on black leather, aggressive specular, lacquered quality, fashion-forward confrontational finish",
      lighting: "single strong light creates mirror reflection, aggressive gloss, deep black depth",
      quality: "lacquer shader, mirror leather finish, physically based, 8K",
      fge: "FGE confrontational material — the one that offends people, too much, too shiny, deliberately aggressive luxury",
      grok: "Patent leather — mirror gloss on deep black, aggressive specular, confrontational finish. FGE: too much on purpose, the material that offends someone and obsesses someone else."
    }
  },
  {
    id: "holographic", name: "Holographic Foil", category: "Sheen",
    tags: ["spectral", "card FX", "rainbow shift", "edition marker"],
    accent: "#ff80ff", character: "Card Edition FX",
    bg: "linear-gradient(135deg,#ff0080 0%,#ff8000 20%,#ffff00 40%,#00ff80 60%,#0080ff 80%,#8000ff 100%)",
    vein: "linear-gradient(45deg,rgba(255,255,255,.4) 0%,transparent 50%,rgba(255,255,255,.3) 100%)",
    prompt: {
      core: "Holographic foil surface, full spectrum rainbow shift, iridescent metallic, angle-dependent color change, card foil quality, spectral prismatic reflection",
      lighting: "multiple light angles show different spectrum zones, prismatic light diffraction",
      quality: "holographic shader, spectral foil, angle-dependent, 8K",
      fge: "FGE edition marker material — the card that announces itself, scarcity made visible, the electric detail at maximum",
      grok: "Holographic foil — full spectrum rainbow, angle shifts reveal different colors, card foil quality. FGE edition: scarcity made visible, the universe announcing a limited truth."
    }
  },
  // ── ORGANIC ────────────────────────────────────────────────────────────
  {
    id: "cobra-skin", name: "Cobra Skin", category: "Organic",
    tags: ["scaled", "iridescent", "dangerous", "Zen Nowhere belt"],
    accent: "#c8a840", character: "Zen Nowhere",
    bg: "linear-gradient(135deg,#2a2010 0%,#3a3018 25%,#201808 50%,#342810 75%,#281e08 100%)",
    vein: "repeating-linear-gradient(0deg,transparent 0px,transparent 6px,rgba(180,140,40,.3) 6px,rgba(180,140,40,.3) 7px,transparent 7px,transparent 14px),repeating-linear-gradient(90deg,transparent 0px,transparent 6px,rgba(160,120,30,.2) 6px,rgba(160,120,30,.2) 7px)",
    prompt: {
      core: "Cobra skin texture, overlapping scales in regular pattern, iridescent quality under light, dark brown-black base with gold scale edges, organic reptile texture",
      lighting: "raking light reveals scale depth, iridescent edge highlight on each scale",
      quality: "organic scale shader, iridescent detail, physically based, 8K",
      fge: "Zen Nowhere belt material — danger worn casually, organic luxury, the creature that moves without warning",
      grok: "Cobra skin — overlapping scales, dark base, gold iridescent edges catch light. FGE Zen Nowhere belt: danger worn casually, organic luxury on a man who needs none of it."
    }
  },
  {
    id: "worn-leather", name: "Worn Leather", category: "Organic",
    tags: ["aged", "earned", "Zen Nowhere boots", "lived-in"],
    accent: "#6a3a18", character: "Zen Nowhere",
    bg: "linear-gradient(135deg,#3a2010 0%,#4a2e18 30%,#301808 60%,#402818 100%)",
    vein: "radial-gradient(ellipse at 30% 40%,rgba(20,10,5,.5) 4px,transparent 8px),radial-gradient(ellipse at 70% 60%,rgba(15,8,3,.4) 3px,transparent 6px),radial-gradient(ellipse at 50% 20%,rgba(25,12,5,.45) 5px,transparent 9px)",
    prompt: {
      core: "Worn leather surface, aged brown, natural creases and wear marks, formerly expensive quality still visible, dust in the grain, lived-in texture",
      lighting: "raking light reveals grain and wear, warm brown tones, history in every crease",
      quality: "organic leather shader, grain detail, wear map, physically based, 8K",
      fge: "Zen Nowhere boots — worn leather with sand in the grain, luxury that walked somewhere real, formerly expensive worn like it's nothing",
      grok: "Worn leather — aged brown, natural creases, dust in grain, formerly expensive. FGE Zen Nowhere: luxury that walked somewhere real, the boots that always have sand."
    }
  },
  {
    id: "fur-texture", name: "Dark Fur", category: "Organic",
    tags: ["Raven Voss coat", "luxury organic", "depth", "volume"],
    accent: "#2a1a0a", character: "Raven Voss",
    bg: "linear-gradient(135deg,#1a0f08 0%,#251508 30%,#150a05 60%,#201208 100%)",
    vein: "repeating-linear-gradient(10deg,transparent 0px,transparent 2px,rgba(60,35,15,.4) 2px,rgba(60,35,15,.4) 3px,transparent 3px,transparent 6px),repeating-linear-gradient(100deg,transparent 0px,transparent 3px,rgba(40,25,10,.3) 3px,rgba(40,25,10,.3) 4px)",
    prompt: {
      core: "Dark fur texture, deep brown-black, individual strand depth, luxury coat quality, volume and density, organic warmth in cold luxury",
      lighting: "light catches individual fur strands, depth of volume, rim lighting reveals texture",
      quality: "fur shader, strand detail, volumetric depth, physically based, 8K",
      fge: "Raven Voss coat material — organic luxury at its most powerful, warmth as armor, the fur that moves like it has an opinion",
      grok: "Dark luxury fur — deep brown-black, individual strand depth, volumetric coat quality. FGE Raven Voss: warmth as armor, organic luxury that moves with intention."
    }
  },
  {
    id: "sheepskin", name: "Sheepskin / Worn Fingertip", category: "Organic",
    tags: ["Zen Nowhere hands", "tactile", "worked", "fingertip"],
    accent: "#c8b090", character: "Zen Nowhere",
    bg: "linear-gradient(135deg,#c0a880 0%,#d4bc94 30%,#b09870 60%,#c8b08a 100%)",
    vein: "radial-gradient(ellipse at 40% 40%,rgba(80,60,30,.3) 3px,transparent 5px),radial-gradient(ellipse at 65% 55%,rgba(70,50,25,.25) 2px,transparent 4px)",
    prompt: {
      core: "Sheepskin worn leather fingertip texture, worked surface, tactile warmth, soft but toughened, cream to tan tones, organic fingerprint-scale detail",
      lighting: "soft raking light reveals surface texture, warm organic tones",
      quality: "organic skin shader, micro surface detail, physically based, 8K",
      fge: "Zen Nowhere hands — sheepskin fingertips worn from strings and work, perfect cuticles, the contradiction that tells the whole story",
      grok: "Sheepskin worn fingertip — worked tactile surface, warm cream-tan, micro-texture. FGE Zen Nowhere hands: worn from strings, perfect cuticles, the one contradiction."
    }
  },
  // ── FABRIC ─────────────────────────────────────────────────────────────
  {
    id: "tattered-silk", name: "Tattered Silk", category: "Fabric",
    tags: ["worn luxury", "Zen Nowhere shirt", "movement", "torn edge"],
    accent: "#e8dcc0", character: "Zen Nowhere",
    bg: "linear-gradient(135deg,#e8dcc0 0%,#f0e8d0 30%,#dcd0b0 60%,#e4d8c0 100%)",
    vein: "repeating-linear-gradient(90deg,transparent 0px,transparent 3px,rgba(180,160,100,.15) 3px,rgba(180,160,100,.15) 4px,transparent 4px),repeating-linear-gradient(0deg,transparent 0px,transparent 4px,rgba(160,140,80,.1) 4px,rgba(160,140,80,.1) 5px)",
    prompt: {
      core: "Tattered silk fabric, formerly expensive ivory or slate, slight sheen, irregular worn edges, fine woven structure visible, movement quality",
      lighting: "soft diffuse light, silk sheen on high points, translucency at thin worn areas",
      quality: "fabric shader, silk weave detail, translucency map, physically based, 8K",
      fge: "Zen Nowhere shirt — tattered silk that chose its condition, luxury that survived something and kept moving",
      grok: "Tattered silk — ivory, slight sheen, irregular worn edges, fine weave. FGE Zen Nowhere shirt: luxury that chose its condition, survived something and kept moving."
    }
  },
  {
    id: "aged-linen", name: "Aged Linen", category: "Fabric",
    tags: ["worn", "natural", "Zen Nowhere blazer", "tobacco"],
    accent: "#a08060", character: "Zen Nowhere",
    bg: "linear-gradient(135deg,#8a6840 0%,#a07848 25%,#785830 50%,#967040 75%,#8a6238 100%)",
    vein: "repeating-linear-gradient(90deg,transparent 0px,transparent 2px,rgba(120,90,50,.25) 2px,rgba(120,90,50,.25) 3px,transparent 3px,transparent 5px),repeating-linear-gradient(0deg,transparent 0px,transparent 3px,rgba(100,75,40,.2) 3px,rgba(100,75,40,.2) 4px)",
    prompt: {
      core: "Aged linen fabric, tobacco to desert sand tones, natural fiber texture visible, worn at stress points, formerly fitted, natural wrinkling",
      lighting: "natural light reveals fiber texture, matte surface, warm tones",
      quality: "fabric shader, natural fiber detail, wear map, physically based, 8K",
      fge: "Zen Nowhere blazer — aged linen that survived something, the suit that refused to be a suit, worn like it's nothing",
      grok: "Aged linen blazer — tobacco tones, natural fiber, worn stress points. FGE Zen Nowhere: the suit that refused to be a suit, worn like a choice not a circumstance."
    }
  },
  // ── ATMOSPHERIC ────────────────────────────────────────────────────────
  {
    id: "desert-dust", name: "Desert Dust Haze", category: "Atmospheric",
    tags: ["heat", "haze", "Zen Nowhere environment", "golden hour"],
    accent: "#d4904a", character: "Zen Nowhere Scene",
    bg: "linear-gradient(135deg,#c4803a 0%,#d89848 25%,#b87030 50%,#cC8840 75%,#a86828 100%)",
    vein: "radial-gradient(ellipse at 50% 50%,rgba(255,200,100,.15) 0%,transparent 60%),linear-gradient(180deg,rgba(200,160,80,.1) 0%,transparent 100%)",
    prompt: {
      core: "Desert dust atmosphere, heat haze distortion, golden hour light through dust particles, warm amber air, suspended particulate, atmospheric depth",
      lighting: "golden hour directional light, dust catches backlight, warm volumetric atmosphere",
      quality: "volumetric atmosphere, particle scatter, physically based, 8K",
      fge: "Zen Nowhere environment — the air he comes from, heat haze between nowhere and now here, golden hour that never fully arrives",
      grok: "Desert dust atmosphere — heat haze, golden hour through suspended particles, warm amber air. FGE Zen Nowhere: the atmosphere between nowhere and now here."
    }
  },
  {
    id: "night-rain", name: "Night Rain Atmosphere", category: "Atmospheric",
    tags: ["rain", "night", "neon reflection", "Vegas world"],
    accent: "#4080c0", character: "Vegas World",
    bg: "linear-gradient(135deg,#0a1020 0%,#101828 30%,#080e1c 60%,#0c1424 100%)",
    vein: "repeating-linear-gradient(85deg,transparent 0px,transparent 15px,rgba(80,140,220,.15) 15px,rgba(80,140,220,.15) 16px,transparent 16px,transparent 30px)",
    prompt: {
      core: "Night rain atmosphere, wet surfaces reflecting neon, rainfall streaks, city light refraction in rain drops, dark blue-black air",
      lighting: "neon color reflections in wet surfaces, rain backlit by city light, deep night atmosphere",
      quality: "atmospheric rain shader, reflection detail, volumetric night, 8K",
      fge: "Vegas world atmosphere — the world Raven Voss stands above, night rain on penthouse glass, luxury looking down at beautiful chaos",
      grok: "Night rain city atmosphere — neon reflections in wet surfaces, rainfall backlit, deep blue-black air. FGE Vegas world: luxury looking down at beautiful chaos."
    }
  },
  {
    id: "heat-haze", name: "Heat Distortion", category: "Atmospheric",
    tags: ["shimmer", "distortion", "anticipatory", "Zen Nowhere entry"],
    accent: "#e8c060", character: "Zen Nowhere Scene Law",
    bg: "linear-gradient(135deg,#e8d080 0%,#f0dc90 30%,#d8c070 60%,#ecd888 100%)",
    vein: "repeating-linear-gradient(90deg,transparent 0px,transparent 20px,rgba(255,240,160,.2) 20px,rgba(255,240,160,.2) 21px)",
    prompt: {
      core: "Heat shimmer distortion, transparent heat haze ripple, air distortion from extreme temperature, miragelike wavering, anticipatory atmosphere",
      lighting: "backlit heat creates shimmer bands, warm light distortion, the air before something happens",
      quality: "distortion shader, heat shimmer, transparent atmospheric effect, 8K",
      fge: "Zen Nowhere Scene Law visual — Status Collapse atmosphere, the air distorts before he enters, anticipatory freeze made visible",
      grok: "Heat shimmer distortion — transparent wavering air, backlit shimmer. FGE Zen Nowhere Scene Law: the air that changes before he enters, anticipatory freeze made visible."
    }
  },
  // ── CARD FX ────────────────────────────────────────────────────────────
  {
    id: "gold-foil-border", name: "Gold Foil Border", category: "Card FX",
    tags: ["card frame", "luxury border", "embossed", "edition"],
    accent: "#c8a030", character: "Card Standard",
    bg: "linear-gradient(135deg,#a07820 0%,#c89830 25%,#907010 50%,#b88828 75%,#a07820 100%)",
    vein: "repeating-linear-gradient(45deg,transparent 0px,transparent 4px,rgba(255,220,80,.4) 4px,rgba(255,220,80,.4) 5px,transparent 5px,transparent 10px)",
    prompt: {
      core: "Gold foil card border, embossed luxury frame, warm yellow gold, slight texture variation, card-grade finish, edition number engraved",
      lighting: "raking light reveals emboss depth, warm gold catch, subtle shadow in recesses",
      quality: "foil stamp shader, emboss detail, physically based, 8K",
      fge: "FGE card frame standard — every card wears this border, the universe's signature on every edition",
      grok: "Gold foil embossed card border — warm yellow gold, slight emboss texture, edition-grade finish. FGE: the universe's signature worn on every card."
    }
  },
  {
    id: "dark-card-bg", name: "Dark Card Background", category: "Card FX",
    tags: ["card base", "noir", "depth", "atmospheric"],
    accent: "#2a2020", character: "Card Standard",
    bg: "linear-gradient(135deg,#100c0c 0%,#181010 30%,#0c0808 60%,#141010 100%)",
    vein: "radial-gradient(ellipse at 50% 50%,rgba(40,20,20,.4) 0%,transparent 70%)",
    prompt: {
      core: "Dark card background, deep noir black with subtle warm undertone, atmospheric depth, textured surface not flat, card-grade material quality",
      lighting: "minimal ambient, deep shadows, card is a window into a dark world",
      quality: "deep material shader, subtle surface texture, physically based, 8K",
      fge: "FGE card base — the world behind every character, darkness they emerge from, the universe's natural state",
      grok: "Dark card background — deep noir black, warm undertone, atmospheric surface texture. FGE: the world every character emerges from, darkness as natural state."
    }
  },
  {
    id: "marble-card-bg", name: "Marble Card Background", category: "Card FX",
    tags: ["Kintsugi", "white card", "constitutional", "Feral Gloss"],
    accent: "#c8a030", character: "Constitutional Card",
    bg: "linear-gradient(135deg,#f0ede6 0%,#e8e4dc 30%,#f4f0e8 60%,#e0dcd4 100%)",
    vein: "repeating-linear-gradient(25deg,transparent 0px,transparent 18px,rgba(180,170,155,.25) 18px,rgba(180,170,155,.25) 19px,transparent 19px,transparent 35px),linear-gradient(60deg,transparent 0%,transparent 55%,rgba(200,160,20,.8) 55%,rgba(220,180,30,.9) 57%,transparent 57%)",
    prompt: {
      core: "White marble card background with Kintsugi gold detail, fine grey veining, one gold repair line crossing surface, constitutional material quality",
      lighting: "even soft light, gold repair catches warm accent, marble SSS glow",
      quality: "marble SSS shader, gold inlay detail, physically based, 8K",
      fge: "FGE constitutional card — the document made card, Kintsugi law made background, broken and more valuable",
      grok: "Marble card background, Kintsugi gold repair line — white marble, grey veining, one gold fracture crossing. FGE constitutional: the law made material."
    }
  },
  // ── FGE SIGNATURE ──────────────────────────────────────────────────────
  {
    id: "fge-talisman", name: "FGE Talisman Material", category: "FGE Signature",
    tags: ["chrome cross", "serpent", "iridescent gem", "logo"],
    accent: "#a0c0e0", character: "Universe Symbol",
    bg: "linear-gradient(135deg,#c0ccd8 0%,#d8e4f0 30%,#a8b8c8 60%,#c8d4e0 100%)",
    vein: "linear-gradient(135deg,rgba(255,255,255,.7) 0%,transparent 30%,rgba(200,220,240,.5) 50%,transparent 70%,rgba(255,255,255,.4) 100%)",
    prompt: {
      core: "Chrome cross with coiled serpent, iridescent center gemstone, liquid chrome surface, serpent body wrapping cross base, fire opal or spectral gem at center intersection",
      lighting: "studio light, chrome reflects environment, gem center shows full spectrum, serpent has separate surface quality",
      quality: "chrome shader + gemstone shader combined, multi-material object, physically based, 8K",
      fge: "FGE universe symbol — every material of the universe converges in this object, the talisman Zen Nowhere wears, the sigil of the world",
      grok: "FGE talisman — chrome cross, coiled serpent wrapping base, fire opal center gem. Multi-material: chrome body, organic serpent, spectral gem. Universe symbol worn by Zen Nowhere."
    }
  },
  {
    id: "fge-world-texture", name: "Feral Gloss Signature", category: "FGE Signature",
    tags: ["constitutional", "rugged rich", "tension", "the world itself"],
    accent: "#c8a050", character: "The World",
    bg: "linear-gradient(135deg,#1a1208 0%,#2a1e0c 25%,#120c04 50%,#221808 75%,#1c1408 100%)",
    vein: "repeating-linear-gradient(30deg,transparent 0px,transparent 15px,rgba(200,160,60,.2) 15px,rgba(200,160,60,.2) 16px,transparent 16px,transparent 32px),radial-gradient(ellipse at 60% 40%,rgba(200,160,60,.15) 0%,transparent 50%)",
    prompt: {
      core: "Feral Gloss signature material — deep dark base suggesting stone and leather simultaneously, warm gold undertone, surface that has been through something, rugged luxury tension",
      lighting: "low warm light, one electric accent catch, depth that suggests history",
      quality: "multi-material composite, aged luxury shader, physically based, 8K",
      fge: "The world itself as material — rugged but rich, not rich like wealth not rugged like dirt, the tension between those two things is the surface",
      grok: "Feral Gloss Empire signature texture — dark base, warm gold undertone, rugged luxury tension. FGE: rugged but rich, the surface of a world that has been through something and chose to be beautiful anyway."
    }
  },
];

const CopyButton = ({ text, label, accent }) => {
  const [copied, setCopied] = useState(false);
  const copy = () => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  return (
    <button onClick={copy} style={{
      padding: "5px 10px", borderRadius: "5px", fontSize: "10px",
      cursor: "pointer", border: `1px solid ${accent}44`,
      background: copied ? `${accent}22` : "transparent",
      color: copied ? accent : "#555",
      transition: "all 0.15s", whiteSpace: "nowrap",
    }}>
      {copied ? "✓ Copied" : label}
    </button>
  );
};

export default function MaterialUniverse() {
  const [selected, setSelected] = useState(null);
  const [category, setCategory] = useState("All");
  const [search, setSearch] = useState("");
  const [mode, setMode] = useState("grok");

  const filtered = materials.filter(m => {
    const matchCat = category === "All" || m.category === category;
    const matchSearch = !search || m.name.toLowerCase().includes(search.toLowerCase()) ||
      m.tags.some(t => t.toLowerCase().includes(search.toLowerCase())) ||
      m.character.toLowerCase().includes(search.toLowerCase());
    return matchCat && matchSearch;
  });

  const Swatch = ({ m }) => (
    <div onClick={() => setSelected(selected?.id === m.id ? null : m)}
      style={{
        cursor: "pointer", borderRadius: "10px", overflow: "hidden",
        border: selected?.id === m.id ? `1px solid ${m.accent}` : "1px solid rgba(255,255,255,0.07)",
        transition: "all 0.2s", background: "#0f0f0f",
        transform: selected?.id === m.id ? "scale(1.02)" : "scale(1)",
      }}>
      <div style={{ height: "90px", background: m.bg, position: "relative", overflow: "hidden" }}>
        <div style={{ position: "absolute", inset: 0, background: m.vein }} />
        <div style={{
          position: "absolute", inset: 0,
          background: "linear-gradient(transparent 50%, rgba(0,0,0,0.75))"
        }} />
        <div style={{ position: "absolute", bottom: 0, left: 0, right: 0, padding: "6px 8px" }}>
          <div style={{ fontSize: "11px", fontWeight: 700, color: "#fff", fontFamily: "Georgia,serif", lineHeight: 1.2 }}>
            {m.name}
          </div>
          <div style={{ fontSize: "9px", color: m.accent, textTransform: "uppercase", letterSpacing: "0.1em" }}>
            {m.category}
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div style={{ minHeight: "100vh", background: "#080808", color: "#e0e0e0", fontFamily: "'Helvetica Neue',Arial,sans-serif" }}>
      {/* Header */}
      <div style={{
        padding: "20px 16px 12px",
        borderBottom: "1px solid rgba(255,255,255,0.06)",
        background: "#0c0c0c",
        position: "sticky", top: 0, zIndex: 100,
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "10px" }}>
          <div>
            <div style={{ fontSize: "9px", letterSpacing: "0.3em", color: "#444", textTransform: "uppercase" }}>
              FERAL GLOSS EMPIRE
            </div>
            <div style={{
              fontSize: "18px", fontWeight: 800, fontFamily: "Georgia,serif",
              background: "linear-gradient(135deg,#fff 0%,#888 100%)",
              WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
              letterSpacing: "-0.02em",
            }}>
              Material Universe
            </div>
          </div>
          <div style={{ display: "flex", gap: "6px", alignItems: "center" }}>
            <div style={{ fontSize: "10px", color: "#333" }}>{materials.length} materials</div>
            {["grok", "draw"].map(m => (
              <button key={m} onClick={() => setMode(m)} style={{
                padding: "5px 10px", borderRadius: "5px", fontSize: "10px",
                cursor: "pointer", border: "1px solid rgba(255,255,255,0.1)",
                background: mode === m ? "rgba(255,255,255,0.1)" : "transparent",
                color: mode === m ? "#fff" : "#444",
                textTransform: "uppercase", letterSpacing: "0.08em",
              }}>{m === "grok" ? "Grok" : "Draw Things"}</button>
            ))}
          </div>
        </div>

        {/* Search */}
        <input
          value={search} onChange={e => setSearch(e.target.value)}
          placeholder="Search material, character, tag..."
          style={{
            width: "100%", padding: "8px 12px", borderRadius: "8px",
            background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.08)",
            color: "#ccc", fontSize: "12px", outline: "none", boxSizing: "border-box",
          }}
        />

        {/* Category Filter */}
        <div style={{ display: "flex", gap: "5px", marginTop: "10px", overflowX: "auto", paddingBottom: "2px" }}>
          {CATEGORIES.map(cat => {
            const count = cat === "All" ? materials.length : materials.filter(m => m.category === cat).length;
            return (
              <button key={cat} onClick={() => setCategory(cat)} style={{
                padding: "4px 10px", borderRadius: "20px", fontSize: "9px", whiteSpace: "nowrap",
                cursor: "pointer", border: "1px solid rgba(255,255,255,0.08)",
                background: category === cat ? "rgba(255,255,255,0.12)" : "transparent",
                color: category === cat ? "#fff" : "#444",
                textTransform: "uppercase", letterSpacing: "0.08em",
              }}>{cat} <span style={{ opacity: 0.5 }}>{count}</span></button>
            );
          })}
        </div>
      </div>

      <div style={{ display: "flex", height: "calc(100vh - 170px)" }}>
        {/* Grid */}
        <div style={{
          flex: selected ? "0 0 42%" : "1",
          overflowY: "auto", padding: "12px",
          transition: "flex 0.3s ease",
        }}>
          <div style={{
            display: "grid",
            gridTemplateColumns: selected ? "1fr 1fr" : "repeat(3, 1fr)",
            gap: "8px",
          }}>
            {filtered.map(m => <Swatch key={m.id} m={m} />)}
          </div>
          {filtered.length === 0 && (
            <div style={{ textAlign: "center", color: "#333", paddingTop: "40px", fontSize: "12px" }}>
              No materials match "{search}"
            </div>
          )}
        </div>

        {/* Detail */}
        {selected && (
          <div style={{
            flex: "0 0 58%", borderLeft: "1px solid rgba(255,255,255,0.06)",
            overflowY: "auto", padding: "16px", background: "#0a0a0a",
          }}>
            {/* Large Swatch */}
            <div style={{
              height: "140px", borderRadius: "10px", overflow: "hidden",
              background: selected.bg, position: "relative", marginBottom: "12px",
              border: `1px solid ${selected.accent}33`,
            }}>
              <div style={{ position: "absolute", inset: 0, background: selected.vein }} />
              <div style={{
                position: "absolute", inset: 0,
                background: "linear-gradient(135deg,rgba(255,255,255,0.04) 0%,transparent 50%)",
              }} />
              <div style={{
                position: "absolute", bottom: 0, left: 0, right: 0, padding: "12px",
                background: "linear-gradient(transparent,rgba(0,0,0,0.85))",
              }}>
                <div style={{ fontSize: "16px", fontFamily: "Georgia,serif", color: "#fff", fontWeight: 700 }}>
                  {selected.name}
                </div>
                <div style={{ display: "flex", gap: "8px", alignItems: "center", marginTop: "2px" }}>
                  <span style={{ fontSize: "9px", color: selected.accent, textTransform: "uppercase", letterSpacing: "0.12em" }}>
                    {selected.category}
                  </span>
                  <span style={{ fontSize: "9px", color: "#444" }}>→</span>
                  <span style={{ fontSize: "9px", color: "#666" }}>{selected.character}</span>
                </div>
              </div>
            </div>

            {/* Tags */}
            <div style={{ display: "flex", gap: "4px", flexWrap: "wrap", marginBottom: "14px" }}>
              {selected.tags.map(tag => (
                <span key={tag} style={{
                  fontSize: "9px", padding: "3px 7px",
                  background: `${selected.accent}18`, color: selected.accent,
                  borderRadius: "4px", textTransform: "uppercase", letterSpacing: "0.08em",
                }}>{tag}</span>
              ))}
            </div>

            {/* Mode Toggle */}
            <div style={{
              display: "flex", gap: "6px", marginBottom: "12px",
              padding: "8px", background: "rgba(255,255,255,0.02)",
              borderRadius: "8px", border: "1px solid rgba(255,255,255,0.04)",
            }}>
              <div style={{ fontSize: "9px", color: "#333", textTransform: "uppercase", letterSpacing: "0.1em", alignSelf: "center", marginRight: "4px" }}>
                Mode:
              </div>
              {["grok", "draw"].map(m => (
                <button key={m} onClick={() => setMode(m)} style={{
                  padding: "4px 10px", borderRadius: "5px", fontSize: "10px",
                  cursor: "pointer", border: `1px solid ${mode === m ? selected.accent + "66" : "rgba(255,255,255,0.06)"}`,
                  background: mode === m ? `${selected.accent}18` : "transparent",
                  color: mode === m ? selected.accent : "#444",
                }}>{m === "grok" ? "Grok Mode" : "Draw Things"}</button>
              ))}
            </div>

            {mode === "grok" ? (
              <div>
                <div style={{ fontSize: "10px", color: "#333", textTransform: "uppercase", letterSpacing: "0.15em", marginBottom: "8px" }}>
                  Grok Prompt
                </div>
                <div style={{
                  padding: "12px", borderRadius: "8px",
                  background: "rgba(255,255,255,0.03)",
                  border: `1px solid ${selected.accent}22`,
                  fontSize: "12px", color: "#999", lineHeight: "1.7",
                  marginBottom: "8px",
                }}>
                  {selected.prompt.grok}
                </div>
                <CopyButton text={selected.prompt.grok} label="Copy Grok Prompt" accent={selected.accent} />
              </div>
            ) : (
              <div>
                <div style={{ fontSize: "10px", color: "#333", textTransform: "uppercase", letterSpacing: "0.15em", marginBottom: "8px" }}>
                  Draw Things Blocks
                </div>
                {[
                  { key: "core", label: "Core Material" },
                  { key: "lighting", label: "Lighting" },
                  { key: "quality", label: "Render Quality" },
                  { key: "fge", label: "FGE Layer" },
                ].map(({ key, label }) => (
                  <div key={key} style={{
                    marginBottom: "6px", borderRadius: "7px",
                    border: "1px solid rgba(255,255,255,0.05)", overflow: "hidden",
                  }}>
                    <div style={{
                      display: "flex", justifyContent: "space-between", alignItems: "center",
                      padding: "6px 10px", background: "rgba(255,255,255,0.02)",
                      borderBottom: "1px solid rgba(255,255,255,0.04)",
                    }}>
                      <span style={{ fontSize: "9px", color: "#444", textTransform: "uppercase", letterSpacing: "0.1em" }}>
                        {label}
                      </span>
                      <CopyButton text={selected.prompt[key]} label="Copy" accent={selected.accent} />
                    </div>
                    <div style={{ padding: "8px 10px", fontSize: "11px", color: "#777", lineHeight: "1.6" }}>
                      {selected.prompt[key]}
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Full Prompt */}
            <div style={{ marginTop: "10px" }}>
              <CopyButton
                text={mode === "grok"
                  ? selected.prompt.grok
                  : `${selected.prompt.core}\n${selected.prompt.lighting}\n${selected.prompt.quality}\n${selected.prompt.fge}`}
                label={`Copy Full ${mode === "grok" ? "Grok" : "Draw Things"} Prompt`}
                accent={selected.accent}
              />
            </div>

            {/* Settings */}
            <div style={{
              marginTop: "12px", padding: "10px 12px", borderRadius: "8px",
              background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.04)",
            }}>
              <div style={{ fontSize: "9px", color: "#2a2a2a", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: "5px" }}>
                {mode === "grok" ? "Source Platforms" : "Draw Things Settings"}
              </div>
              {mode === "grok" ? (
                <div style={{ fontSize: "10px", color: "#444", lineHeight: "1.8" }}>
                  Primary: Grok Image Gen — paste prompt directly<br />
                  Reference: poly.cam → 8K seamless base texture<br />
                  Validate: polyhaven.com → free PBR reference<br />
                  Advanced: tripo3d.ai → full PBR material set
                </div>
              ) : (
                <div style={{ fontSize: "10px", color: "#444", lineHeight: "1.8" }}>
                  Model: Realistic Vision V6 or Juggernaut XL<br />
                  Sampler: DPM++ 2M Karras · Steps: 30 · CFG: 7<br />
                  Size: 768x768 or 768x1152
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
