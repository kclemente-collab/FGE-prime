# -*- coding: utf-8 -*-
"""
============================================================================
FGE LOOKBOOK — BOOK INPUT SHEET   (copy this file per product)
============================================================================
This is the ONLY file you edit to make a new book. Fill it in, run:
    python3 build_kit.py book_lilith_noir.py
Everything else (spine, quality, frame language) is locked in theme.py / build_kit.py.

HANDOFF NOTE: This kit does not share memory with your narrative-engine thread.
Whatever the engine produces (canon, voice rules, character bible) must be pasted
into SPINE_TIE_IN below so Claude can write copy that ties into it. The input file
IS the connective tissue between the engine and the book.
============================================================================
"""

BOOK = {
    # ---- IDENTITY (required) -------------------------------------------
    "theme":       "noir",                 # key from theme.py THEMES
    "subject":     "LILITH NOIR",          # cover title
    "subtitle":    "A Tale of Quiet Power",
    "collection":  "Noir Dynasty",
    "char_id":     "FGE-CHAR-001",
    "edition":     "Edition 001 of 777",
    "classification": "Primary Character · Living Relic",
    "provenance":  "FGE Immortality Layer · Verified Canon",

    # ---- NARRATIVE SEED (required) -------------------------------------
    # Paste the spine from your narrative engine here. Claude writes all plate
    # copy to tie into this. If left as "" Claude infers from images (riskier).
    "spine_tie_in": (
        "Lilith Noir, the Eclipse Empress of the Noir Dynasty. Voice: terse, mythic, "
        "archival. She did not seek power; it found her in the ashes of a fallen throne. "
        "Theme of quiet, inevitable dominion. Match the register of: "
        "'She was not born to rule, nor did she seek the crown.'"
    ),
    "arc": "emergence -> ascension -> dominion -> myth",   # sequencing guide

    # ---- INTRO PAGE COPY (optional; Claude writes if left None) --------
    "intro_heading": "The Eclipse Empress",
    "intro_eyebrow": "THE LIVING RELIC PROTOCOL",
    "intro_body": None,    # None -> Claude writes 3 paragraphs from spine_tie_in
    "intro_stats": [("Narrative Weight","9.4 / 10"), ("Status","Active")],  # None -> Claude fills

    # ---- IMAGES (required) ---------------------------------------------
    # Just list filenames in the order you want them. Roles auto-assigned:
    #   cover     = first landscape-free strong portrait, OR set "cover" key
    #   centerfold= first landscape image, OR set "centerfold" key
    #   plates    = the rest, in order
    # Captions: leave "line" as None and Claude writes it from the spine.
    "assets_dir": "assets",
    "cover":      "IMG_8086.jpeg",     # optional override; else auto
    "centerfold": "IMG_8094.jpeg",     # optional override; else first landscape
    "plates": [
        {"image": "IMG_8081.jpeg", "title": None, "line": None},
        {"image": "IMG_8087.jpeg", "title": None, "line": None},
        {"image": "IMG_8090.jpeg", "title": None, "line": None},
        {"image": "IMG_8088.jpeg", "title": None, "line": None},
        {"image": "IMG_8092.jpeg", "title": None, "line": None},
        {"image": "IMG_8086.jpeg", "title": None, "line": None},
        {"image": "IMG_8085.jpeg", "title": None, "line": None},
        {"image": "IMG_8093.jpeg", "title": None, "line": None},
        {"image": "IMG_8089.jpeg", "title": None, "line": None},
        {"image": "IMG_8096.jpeg", "title": None, "line": None},
        {"image": "IMG_8095.jpeg", "title": None, "line": None},
    ],
}
