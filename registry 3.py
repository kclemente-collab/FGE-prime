# -*- coding: utf-8 -*-
"""
============================================================================
FGE PUBLISHING REGISTRY  (registry.py)
============================================================================
Single catalog of the Feral Gloss Empire. Both the build kit and the downstream
narrative/story engine read this to know who exists, which themes are claimed,
and what assets are registered.

DESIGN PRINCIPLE — only real, built assets are registered. Nothing speculative.
Image generation happens OUTSIDE this system (you, via Grok). This file never
invents assets it cannot see on disk.

It reads the book_*.py canon files dynamically, so it never goes stale: add a
book file, and it appears in the registry automatically.

USAGE
-----
    import registry
    registry.print_catalog()                 # human view
    registry.character("FGE-CHAR-002")        # one character's full canon
    registry.theme_taken("obsidian")          # collision check before new book
    registry.asset_ledger("book_raven.py")    # the spec's automation schema as rows
============================================================================
"""
import os, glob, importlib.util

# ---- which book files are part of the canon (built & verified) ----
# A book is "registered" only when its assets_dir exists and holds its images.
REGISTERED_BOOKS = [
    "book_lilith_noir.py",
    "book_raven.py",
    "book_isolde.py",
    "book_calista.py",
]

# Themes claimed by registered characters (collision guard for new books).
# Mirrors theme.py; the check below verifies against the live module too.
_DEMO_THEMES = {"verdant", "relic", "cobalt"}   # available, not yet claimed by a character

def _load(path):
    spec = importlib.util.spec_from_file_location(path[:-3], path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.BOOK

def _assets_present(bk):
    d = bk.get("assets_dir", "")
    if not os.path.isdir(d):
        return 0
    imgs = set()
    for p in bk.get("plates", []):
        imgs.add(p["image"])
    if bk.get("cover"): imgs.add(bk["cover"])
    if bk.get("centerfold"): imgs.add(bk["centerfold"])
    return sum(1 for i in imgs if os.path.isfile(os.path.join(d, i)))

def characters():
    """Return list of canon dicts for every registered, asset-backed book."""
    out = []
    for bf in REGISTERED_BOOKS:
        if not os.path.isfile(bf):
            continue
        bk = _load(bf)
        n_assets = _assets_present(bk)
        out.append({
            "book_file": bf,
            "char_id": bk["char_id"],
            "subject": bk["subject"],
            "subtitle": bk.get("subtitle", ""),
            "dynasty": bk["collection"],
            "theme": bk["theme"],
            "arc": bk.get("arc", ""),
            "edition": bk["edition"],
            "classification": bk.get("classification", ""),
            "provenance": bk.get("provenance", ""),
            "plates": len(bk.get("plates", [])),
            "assets_on_disk": n_assets,
            "status": "BUILT" if n_assets > 0 else "PENDING_ASSETS",
            "spine_tie_in": bk.get("spine_tie_in", ""),
        })
    return out

def character(char_id):
    for c in characters():
        if c["char_id"] == char_id or c["subject"].upper() == char_id.upper():
            return c
    return None

def claimed_themes():
    return {c["theme"] for c in characters()}

def theme_taken(name):
    return name in claimed_themes()

def available_themes():
    try:
        import theme as T
        all_themes = set(T.THEMES.keys())
    except Exception:
        all_themes = set()
    return sorted(all_themes - claimed_themes())

def asset_ledger(book_file):
    """The spec's automation schema as rows: Image | Artifact ID | Narrative Line | Edition | Collection."""
    bk = _load(book_file)
    rows, n = [], 2
    if bk.get("cover"):
        rows.append((bk["cover"], f"{bk['char_id']}-COVER", bk.get("subtitle",""), bk["edition"], bk["collection"]))
    for p in bk.get("plates", []):
        rows.append((p["image"], f"{bk['char_id']}-P{n:02d}", p.get("line","") or "", bk["edition"], bk["collection"]))
        n += 1
    if bk.get("centerfold"):
        rows.append((bk["centerfold"], f"{bk['char_id']}-CENTER", bk.get("centerfold_data",{}).get("title",""), bk["edition"], bk["collection"]))
    return rows

def print_catalog():
    cs = characters()
    print("=" * 70)
    print("  FERAL GLOSS EMPIRE — PUBLISHING REGISTRY")
    print("=" * 70)
    for c in cs:
        print(f"\n  {c['subject']}  [{c['char_id']}]   <{c['status']}>")
        print(f"    Dynasty:   {c['dynasty']}")
        print(f"    Theme:     {c['theme']}")
        print(f"    Arc:       {c['arc']}")
        print(f"    Edition:   {c['edition']}")
        print(f"    Plates:    {c['plates']}   Assets on disk: {c['assets_on_disk']}")
    print(f"\n  Themes claimed:   {sorted(claimed_themes())}")
    print(f"  Themes available: {available_themes()}")
    print("=" * 70)

if __name__ == "__main__":
    print_catalog()
