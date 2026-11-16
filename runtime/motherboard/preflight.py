#!/usr/bin/env python3
"""Public, read-only candidate contract validator. Never promotes canon or dispatches."""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def validate():
    raw = (HERE / "manifest.json").read_bytes()
    data = json.loads(raw)
    a = data["architecture"]
    gates = data["gates"]
    checks = {
        "IDENTITY_LOCK": data["object_id"] == "FGE-GITHUB-MOTHERBOARD-RUNTIME-001",
        "CANDIDATE_AUTHORITY": data["state"] == "CANDIDATE" and data["authority"] == "PROPOSE_ONLY" and data["director_veto"] is True,
        "SIX_ORDERED_STAGES": a["stages"] == ["INGEST", "RESOLVE", "GENOME", "SEED", "RENDER", "SHIP"],
        "SEVEN_DISTINCT_PORTS": len(a["ports"]) == len(set(a["ports"])) == 7,
        "DECLARED_REFERENCE_COUNT": a["declared_character_references"] == 4,
        "CANDIDATE_CONNECTION_COUNT": a["candidate_connections"] == 8,
        "FIVE_HOLD_GATES": set(gates) == {"identity", "schema", "authority", "compatibility", "output_proof"} and all(x == "HOLD" for x in gates.values()),
        "HB_UNBOUND": "HB_MASTER" in data["missing"] and "AUTHORITATIVE_CHARACTER_ID" in data["missing"],
        "NO_EXTERNAL_WRITES": data["activation"]["live_dispatch"] is False and data["activation"]["canon_write"] is False and data["activation"]["external_registry_write"] is False,
        "NO_LEASES": data["activation"]["leases_activated"] == 0,
        "NO_AUTH_GAIN": data["canon_effect"] == "NONE" and data["release_gate"] == "HOLD",
        "NO_PRIVATE_SOURCE_PUBLICATION": data["provenance"]["source_bytes_published"] is False and data["source_disclosure"] == "PUBLIC_METADATA_ONLY",
    }
    return {
        "object_id": data["object_id"],
        "scope": "PUBLIC_SANITIZED_PREFLIGHT",
        "manifest_sha256": hashlib.sha256(raw).hexdigest(),
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "structural_result": "PASS" if all(checks.values()) else "FAIL",
        "release_gate": "HOLD",
        "runtime_attestation": "NOT_PROVEN",
        "canon_write": False,
        "external_dispatches": 0,
        "rcpt": "PUBLIC_CONTRACT_CHECK_ONLY",
        "nrcpt": "SOURCE_BYTES_AND_LIVE_EXECUTION_NOT_ATTESTED",
    }


if __name__ == "__main__":
    report = validate()
    print(json.dumps(report, indent=2))
    sys.exit(0 if report["structural_result"] == "PASS" else 1)
