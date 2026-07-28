# -*- coding: utf-8 -*-
"""
FGE LOOKBOOK KIT — THEME SYSTEM
================================
Two layers:
  SPINE   = locked brand DNA. Identical in every FGE book. Do NOT edit per product.
  THEMES  = per-book variable tokens. This is what makes book #2 look unlike book #1
            while staying the same house and quality bar.

To make a new book look different: pick or define a THEME. Nothing in SPINE changes.
"""

# =========================================================================
# SPINE — LOCKED. The brand's permanent identity.
# =========================================================================
SPINE = {
    "empire":      "FERAL GLOSS EMPIRE",
    "series":      "Living Artifact Series",
    "display_font":"Cormorant Garamond",   # headings
    "body_font":   "EB Garamond",          # body / captions
    "ratio":       (2, 3),                  # master canvas portrait
    "page_w":      1000,
    "page_h":      1500,
    "google_fonts":"https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=EB+Garamond:ital,wght@0,400;0,500;1,400&display=swap",
    # furniture rules (positions, watermark opacity) are fixed in build_kit.py
    "watermark_opacity": 0.05,             # spec: 5–10%
    "watermark_text":    "FGE",
}

# =========================================================================
# THEMES — VARIABLE. One per book. Same language, different expression.
# =========================================================================
# Token contract (every theme must define all keys):
#   ink         base near-black ground
#   paper       page fill (slightly lifted from ink)
#   accent      the dynasty color (crimson, emerald, etc.)
#   gold        primary metallic line color
#   gold_hi     metallic highlight
#   text        body text color
#   surface     CSS background layer painted UNDER images on text pages
#               -> this is the "surface mixture": marble, vellum, obsidian, brushed metal
#   frame       "ornate" | "thin"  (same gold language, different weight)
#   rhythm      "centered" | "left" | "bleed"  (plate image placement)

def _surface_obsidian(ink):
    return f"radial-gradient(130% 100% at 70% 15%,#1a1722 0%,{ink} 62%)"

def _surface_marble(ink):
    return (f"linear-gradient(135deg, rgba(255,255,255,.04) 0%, transparent 40%),"
            f"radial-gradient(100% 80% at 20% 80%, rgba(255,255,255,.05), transparent 50%),"
            f"radial-gradient(120% 90% at 80% 20%, #1c1c22 0%, {ink} 60%)")

def _surface_vellum(ink):
    return (f"radial-gradient(120% 100% at 50% 0%, #20180f 0%, {ink} 55%),"
            f"repeating-linear-gradient(0deg, rgba(255,240,200,.015) 0 2px, transparent 2px 5px)")

def _surface_brushed(ink):
    return (f"repeating-linear-gradient(95deg, rgba(255,255,255,.03) 0 1px, transparent 1px 4px),"
            f"linear-gradient(180deg, #17171c, {ink})")

def _surface_obsidian_glass(ink):
    # WARM obsidian (Raven, Option A): black + gold ground that harmonizes with
    # mink/chains/bronze skin. Labradorite teal appears ONLY as a faint cool glint
    # (the eye-color echo), never as the dominant cast. Wet-glam caustic feel.
    return (f"radial-gradient(75% 55% at 72% 16%, rgba(201,162,75,.14), transparent 55%),"   # warm gold god-ray
            f"radial-gradient(60% 45% at 22% 78%, rgba(110,40,24,.12), transparent 55%),"     # deep warm fill
            f"radial-gradient(40% 30% at 50% 45%, rgba(42,138,130,.06), transparent 50%),"    # faint labradorite glint
            f"linear-gradient(150deg, #120d09 0%, {ink} 55%, #0c0a08 100%)")

THEMES = {
    # ---- Book 001 — exactly what we shipped ----
    "noir": {
        "ink": "#0a0a0d", "paper": "#111016", "accent": "#8a1f2b",
        "gold": "#c9a24b", "gold_hi": "#e7cf8f", "text": "#e8e3d8",
        "surface": _surface_obsidian("#0a0a0d"),
        "frame": "ornate", "rhythm": "centered",
    },
    # ---- emerald dynasty — cool, regal, marble ground ----
    "verdant": {
        "ink": "#06100c", "paper": "#0b1611", "accent": "#1f6b4f",
        "gold": "#c9a24b", "gold_hi": "#e7cf8f", "text": "#e4ece4",
        "surface": _surface_marble("#06100c"),
        "frame": "thin", "rhythm": "left",
    },
    # ---- oxblood / aged archive — warm, vellum, ornate-heavy ----
    "relic": {
        "ink": "#100806", "paper": "#1a0f0a", "accent": "#6e2418",
        "gold": "#caa257", "gold_hi": "#ecd79a", "text": "#ece0d2",
        "surface": _surface_vellum("#100806"),
        "frame": "ornate", "rhythm": "centered",
    },
    # ---- midnight / industrial — steel, brushed metal, thin frame ----
    "cobalt": {
        "ink": "#070a12", "paper": "#0c1019", "accent": "#274a8a",
        "gold": "#bfb08a", "gold_hi": "#e3d8b8", "text": "#dde2ec",
        "surface": _surface_brushed("#070a12"),
        "frame": "thin", "rhythm": "bleed",
    },
    # ---- RAVEN (Book 002) — WARM obsidian: black+gold+mink, wet-glam gloss ----
    # Option A: warm ground harmonizes with the anchor renders; labradorite teal
    # survives only as the eye-color accent (amber-gold -> grey-green eyes).
    # Same FGE gold rim (house DNA).
    "obsidian": {
        "ink": "#0a0806", "paper": "#100c08", "accent": "#2a8a82",
        "gold": "#c9a24b", "gold_hi": "#e7cf8f", "text": "#ece3d4",
        "surface": _surface_obsidian_glass("#0a0806"),
        "frame": "ornate", "rhythm": "bleed",
    },
}

def get_theme(name):
    if name not in THEMES:
        raise ValueError(f"Unknown theme '{name}'. Available: {list(THEMES)}")
    return THEMES[name]
