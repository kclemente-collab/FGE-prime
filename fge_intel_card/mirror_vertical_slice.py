from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


class MirrorBoundaryError(RuntimeError):
    pass


@dataclass(frozen=True)
class MirrorRequest:
    card_id: str
    operation: str
    source_anchor: str
    source_character_id: str


@dataclass(frozen=True)
class SourceEvidence:
    subject: str
    anchor_id: str
    character_id: str
    provenance: str
    repository: str
    path: str
    source_commit: str


class MirrorExecutor:
    """Read-only executor boundary. It may project bound source evidence; it may not author identity."""

    def execute(self, request: MirrorRequest, source: SourceEvidence) -> Dict[str, Any]:
        if request.operation != "CARD.MIRROR":
            raise MirrorBoundaryError("ROUTE_MISMATCH")
        if request.source_anchor != source.anchor_id:
            raise MirrorBoundaryError("SOURCE_ANCHOR_MISMATCH")
        if request.source_character_id != source.character_id:
            raise MirrorBoundaryError("SOURCE_CHARACTER_MISMATCH")
        return {
            "kind": "CHARACTER_MIRROR_EVIDENCE",
            "card_id": request.card_id,
            "operation": request.operation,
            "subject": source.subject,
            "anchor_id": source.anchor_id,
            "character_id": source.character_id,
            "source": {
                "repository": source.repository,
                "path": source.path,
                "source_commit": source.source_commit,
            },
            "authority_projection": "BOUND_REFERENCE_ONLY",
            "canon_effect": "NONE",
            "authority_effect": "NONE",
            "source_mutation": False,
        }


class MirrorValidator:
    """Independent validation boundary. Validation cannot authorize or mutate canon."""

    def validate(self, request: MirrorRequest, source: SourceEvidence, output: Dict[str, Any]) -> Dict[str, Any]:
        checks = {
            "card_id_exact": output.get("card_id") == request.card_id,
            "route_exact": output.get("operation") == "CARD.MIRROR",
            "source_anchor_exact": output.get("anchor_id") == source.anchor_id == "SB_330",
            "source_character_id_exact": output.get("character_id") == source.character_id,
            "source_provenance_mentions_anchor": "SB_330" in source.provenance,
            "source_subject_raven": source.subject == "RAVEN VOSS",
            "no_source_mutation": output.get("source_mutation") is False,
            "canon_effect_none": output.get("canon_effect") == "NONE",
            "authority_effect_none": output.get("authority_effect") == "NONE",
        }
        return {"checks": checks, "verdict": "PASS" if all(checks.values()) else "FAIL"}


class EvidenceGatedReceiptEmitter:
    """A PASS receipt exists only when executor evidence exists and validator verdict is PASS."""

    def emit(self, proof_id: str, test_id: str, request: MirrorRequest, source: SourceEvidence,
             output: Dict[str, Any], validation: Dict[str, Any], timestamp_utc: str) -> Dict[str, Any]:
        if not output:
            raise MirrorBoundaryError("NO_EXECUTOR_EVIDENCE")
        if validation.get("verdict") != "PASS":
            raise MirrorBoundaryError("VALIDATION_NOT_PASS")
        return {
            "proof_id": proof_id,
            "test_id": test_id,
            "status": "PASS",
            "target_card": request.card_id,
            "operation": request.operation,
            "source_binding": {
                "anchor_id": source.anchor_id,
                "character_id": source.character_id,
                "repository": source.repository,
                "path": source.path,
                "source_commit": source.source_commit,
            },
            "executor": {
                "boundary": "MIRROR_EXECUTOR",
                "input_authority": "source_binding_only",
                "output_kind": output["kind"],
                "mutates_source": False,
                "canon_effect": "NONE",
                "authority_effect": "NONE",
            },
            "validation": {"boundary": "MIRROR_VALIDATOR", **validation},
            "receipt_gate": {
                "requires_executor_evidence": True,
                "requires_validator_pass": True,
                "synthetic_receipt_forbidden": True,
                "gate": "OPEN",
            },
            "mirror_output": {
                "subject": output["subject"],
                "anchor": output["anchor_id"],
                "character_id": output["character_id"],
                "authority_projection": output["authority_projection"],
            },
            "timestamp_utc": timestamp_utc,
            "promotion": False,
        }
