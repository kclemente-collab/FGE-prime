#!/usr/bin/env python3
"""FGE Discovery Bridge v0.1

DISCOVER -> EXTRACT IDS -> MATCH REGISTRY -> CLASSIFY -> REPORT EXCEPTIONS

Does not author missing content.
Does not merge conflicts.
Does not infer authority or canon.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

ID_RE = re.compile(r"FGE-(?:[A-Z0-9]+-)+\d{3,}")
TEXT_SUFFIXES = {".md", ".json", ".yml", ".yaml", ".py", ".txt", ".html"}

CLASSES = (
    "REGISTERED_RESOLVABLE",
    "REGISTERED_SOURCE_MISSING",
    "UNREGISTERED_SOURCE_FOUND",
    "DUPLICATE_CLAIM",
    "CONFLICT",
    "DEPRECATED",
    "UNKNOWN",
)


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def scan_paths(root: Path) -> List[Dict[str, Any]]:
    found: List[Dict[str, Any]] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rel = str(path)
        for match in ID_RE.findall(text):
            found.append({"id": match, "path": rel})
        if ID_RE.search(path.name):
            found.append({"id": path.name, "path": rel, "filename_hit": True})
    return found


def classify(registry: Dict[str, Any], hits: List[Dict[str, Any]]) -> Dict[str, Any]:
    records = {r["reference_id"]: r for r in registry.get("records", [])}
    aliases = {}
    for rec in records.values():
        for alias in rec.get("aliases") or []:
            aliases[alias] = rec["reference_id"]
    by_id = {}
    for hit in hits:
        m = ID_RE.search(hit["id"])
        if not m:
            continue
        rid = m.group(0)
        by_id.setdefault(rid, []).append(hit["path"])
    rows = []
    counts = Counter()
    for rid, paths in sorted(by_id.items()):
        canonical = aliases.get(rid, rid)
        rec = records.get(canonical)
        unique_paths = sorted(set(paths))
        if rec is None:
            cls = "UNREGISTERED_SOURCE_FOUND"
        elif rec["resolution_state"] == "SOURCE_MISSING":
            cls = "REGISTERED_SOURCE_MISSING"
        elif rec["resolution_state"] == "DEPRECATED_TARGET":
            cls = "DEPRECATED"
        elif rec["resolution_state"] == "RESOLVABLE":
            cls = "REGISTERED_RESOLVABLE"
        else:
            cls = "UNKNOWN"
        rows.append({
            "reference_id": rid,
            "canonical_id": canonical,
            "class": cls,
            "paths": unique_paths[:20],
            "path_count": len(unique_paths),
            "notes": (f"alias_of={canonical}" if rid != canonical else None),
        })
        counts[cls] += 1
    queue = [r for r in rows if r["class"] in {
        "UNREGISTERED_SOURCE_FOUND", "REGISTERED_SOURCE_MISSING", "CONFLICT", "UNKNOWN", "DUPLICATE_CLAIM"
    }]
    return {
        "total_distinct_ids": len({r["reference_id"] for r in rows}),
        "counts": {k: counts.get(k, 0) for k in CLASSES},
        "director_queue": queue[:200],
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--registry", default="00_governance/references/FGE_REFERENCE_POINTER_REGISTRY_v1.json")
    args = parser.parse_args()
    registry = load_json(Path(args.registry))
    hits = scan_paths(Path(args.root))
    report = classify(registry, hits)
    print(json.dumps({
        "bridge": "FGE-DISCOVERY-BRIDGE-001",
        "version": "0.1.0",
        "total_objects_discovered": report["total_distinct_ids"],
        "registered_resolvable": report["counts"]["REGISTERED_RESOLVABLE"],
        "source_missing": report["counts"]["REGISTERED_SOURCE_MISSING"],
        "unregistered_source_found": report["counts"]["UNREGISTERED_SOURCE_FOUND"],
        "duplicate": report["counts"]["DUPLICATE_CLAIM"],
        "conflict": report["counts"]["CONFLICT"],
        "unknown": report["counts"]["UNKNOWN"],
        "deprecated": report["counts"]["DEPRECATED"],
        "director_queue_count": len(report["director_queue"]),
        "director_queue": report["director_queue"][:50],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
