#!/usr/bin/env python3
"""
Epoch 0.1 Validator Engine — Minimal CLI (v0.1)
Pure stdlib implementation for immediate enforceability.

This is the first executable layer of CharacterOS governance.
It proves the constitution can be checked by machine without human interpretation.

Usage:
  python epoch0.1_validator.py --artifact path/to/artifact.json --type VOCAB-001
  python epoch0.1_validator.py --artifact path/to/seed.json --type SPEC-001 --graph dependency_graph.json

Exit codes:
  0 = PASS (compliant)
  1 = HARD ERROR (violation of LAW / CDR / Gate)
  2 = USAGE / FILE ERROR
"""

import argparse
import json
import sys
from pathlib import Path

SCHEMAS_DIR = Path(__file__).parent.parent / "schemas"
GRAPH_PATH = Path(__file__).parent.parent / "dependency_graph.json"

def load_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"ERROR: Cannot load {p}: {e}", file=sys.stderr)
        sys.exit(2)

def validate_required_fields(data: dict, required: list, artifact_type: str):
    missing = [f for f in required if f not in data or data[f] is None]
    if missing:
        print(f"HARD ERROR ({artifact_type}): Missing required fields: {missing}")
        print("Violation: LAW-001 (Specifications must declare version/owner/dependencies)")
        return False
    return True

def validate_vocab_constraint(data: dict, artifact_type: str):
    # Placeholder: In full version this would cross-check every string field against VOCAB-001
    # For v0.1 we enforce the structural presence of owner/version as proxy for governance hygiene
    if "owner" not in data or "version" not in data:
        print(f"HARD ERROR ({artifact_type}): owner and version are mandatory (LAW-001 + VOCAB-001 alignment)")
        return False
    return True

def validate_registry_isolation(data: dict, artifact_type: str):
    # v0.1: Check that classification fields do not invent their own enums
    # Full version will resolve against REG-001 / REG-002
    if artifact_type == "SPEC-001":
        if "material_fingerprint" in data and isinstance(data["material_fingerprint"], str):
            if data["material_fingerprint"] == "":
                print("HARD ERROR (SPEC-001): material_fingerprint cannot be empty string. Must reference REG-001.")
                return False
    return True

def validate_contract_boundary(data: dict, artifact_type: str):
    # v0.1: Ensure modules declare input/output via schema objects (not free-form prose)
    if artifact_type == "CON-001":
        if not isinstance(data.get("input_schema"), dict) or not isinstance(data.get("output_schema"), dict):
            print("HARD ERROR (CON-001): input_schema and output_schema must be objects (LAW-004)")
            return False
    return True

def main():
    parser = argparse.ArgumentParser(description="Epoch 0.1 CharacterOS Governance Validator")
    parser.add_argument("--artifact", required=True, help="Path to the JSON artifact to validate")
    parser.add_argument("--type", required=True, choices=["VOCAB-001", "REG-001", "REG-002", "CON-001", "SPEC-001"],
                        help="Artifact type / schema to validate against")
    parser.add_argument("--graph", default=str(GRAPH_PATH), help="Path to dependency_graph.json")
    args = parser.parse_args()

    artifact_path = Path(args.artifact)
    if not artifact_path.exists():
        print(f"ERROR: Artifact not found: {artifact_path}", file=sys.stderr)
        sys.exit(2)

    data = load_json(artifact_path)
    schema_path = SCHEMAS_DIR / f"{args.type.lower().replace('-', '_')}.schema.json"

    if not schema_path.exists():
        print(f"ERROR: No schema found for {args.type} at {schema_path}", file=sys.stderr)
        sys.exit(2)

    schema = load_json(schema_path)

    # Structural validation (required fields from schema)
    required = schema.get("required", [])
    if not validate_required_fields(data, required, args.type):
        sys.exit(1)

    # Governance layer checks
    checks = [
        validate_vocab_constraint(data, args.type),
        validate_registry_isolation(data, args.type),
        validate_contract_boundary(data, args.type),
    ]

    if not all(checks):
        sys.exit(1)

    # Dependency graph awareness (v0.1 stub — full version walks edges)
    print(f"PASS: {args.type} at {artifact_path} complies with Epoch 0.1 MCP structural + governance rules.")
    print("Note: Full vocabulary cross-check, registry resolution, and graph traversal are in v0.2.")
    sys.exit(0)

if __name__ == "__main__":
    main()