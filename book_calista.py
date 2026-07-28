# -*- coding: utf-8 -*-
"""
BOOK 004 — CALISTA VOSS | CANON SEED (official character-canon source)
Anchor: CALISTA VOSS / 3RD HEIR / TEMPORAL DESIGNATION: WARM ECHO / FGE-CHAR-004.
Theme: warmecho. Material (from her posters): PHOTONIC SIGNATURE iridescent warm,
GLOSS LEVEL feral. Lineage Archive v.07.

CANON LINK (critical): Calista is UPSTREAM of Isolde. Isolde Voss was precipitated
as a byproduct of CALISTA's creation process. Calista is the source; Isolde is the
residue. This makes them co-dependent registry entries (Isolde dossier flagged this).
Open thread: does Calista know Isolde is her byproduct?

Arc: origin -> radiance -> lineage -> echo.
Voice: warm where her siblings are cold. Regal, luminous, the heir who casts echoes.
"""

BOOK = {
    "theme": "warmecho",
    "subject": "CALISTA VOSS",
    "subtitle": "The Warm Echo",
    "collection": "Warm Echo Lineage",
    "char_id": "FGE-CHAR-004",
    "edition": "Edition 001 of 777",
    "classification": "3rd Heir \u00b7 Temporal Designation: Warm Echo \u00b7 Living Relic",
    "provenance": "FGE Immortality Layer \u00b7 Lineage Archive v.07 \u00b7 Origin-Source of Isolde",

    "spine_tie_in": (
        "Calista Voss, 3RD HEIR, Temporal Designation WARM ECHO, FGE-CHAR-004. "
        "Photonic signature: iridescent warm. Gloss level: feral. Upstream origin-source "
        "of Isolde \u2014 Isolde was precipitated as a byproduct of Calista's creation. "
        "Where the Voss line runs to cold relics, Calista is the warm one: regal, "
        "luminous, the heir whose radiance casts echoes that become people. Green eyes, "
        "raven hair, warm bronze iridescent skin, gold-and-oxblood couture, cathedral world."
    ),
    "arc": "origin -> radiance -> lineage -> echo",

    "intro_heading": "The Warm Echo",
    "intro_eyebrow": "THE LINEAGE PROTOCOL",
    "intro_body": [
        "She is the third heir, and the warm one. Where the line before her cooled into "
        "obsidian and omega-green, Calista holds the temperature of the source \u2014 "
        "iridescent, warm, feral in her gloss, regal in her stillness.",
        "This archive is a lineage record. Every plate is a study of radiance dense "
        "enough to leave residue: light that did not merely fall on her but continued "
        "past her, and in continuing, precipitated a sister she may not know she made.",
        "An echo is not a lesser sound. It is proof the original was loud enough to return.",
    ],
    "intro_stats": [
        ("Narrative Weight", "9.7 / 10"),
        ("Designation", "Warm Echo \u00b7 3rd Heir"),
        ("Photonic Signature", "Iridescent Warm"),
        ("Lineage", "Origin-Source \u2192 Isolde"),
    ],

    "assets_dir": "assets_calista",
    "cover": "CALISTA_portrait.jpg",
    "centerfold": None,          # awaiting a landscape frame; hold spread
    "centerfold_mode": "hero",
    "centerfold_data": {
        "title": "The Lineage Window",
        "fragment": (
            "Archive Fragment \u2014 the source does not look back at what it has cast. "
            "Calista Voss, third heir, warm echo, stands in the rose-window light and "
            "does not yet ask what precipitated in her wake. Lineage Archive v.07."
        ),
        "left": ("ORIGIN", "The warm source"),
        "mid": ("HEIR", "Third of the Voss line"),
        "right": ("ECHO", "The residue named Isolde"),
    },

    "plates": [
        {"image": "CALISTA_lineage_poster.jpg", "title": "Lineage Archive v.07", "clean": True, "line": ""},
        {"image": "CALISTA_artifact_poster.jpg", "title": "The Artifact Record", "clean": True, "line": ""},
    ],
}
