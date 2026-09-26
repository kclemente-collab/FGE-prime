from __future__ import annotations

import hashlib
import json
import os
import tempfile
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


ENGINE_ID = "FGE-RECOMBINATION-ENGINE-001"
ENGINE_VERSION = "0.1.0"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class EngineEvent:
    event_id: str
    timestamp: str
    event_type: str
    object_id: str
    status: str
    canon_effect: str
    payload: Dict[str, Any]
    previous_event_hash: Optional[str]
    event_hash: str


class AppendOnlyJsonlLedger:
    """
    Append-only JSONL event ledger with a cryptographic hash chain.

    This does not make the file physically immutable. It makes mutation
    detectable during verification and keeps the engine write pattern append-only.
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)

    def _read_raw(self) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
        return rows

    def read_stream(self) -> List[EngineEvent]:
        return [EngineEvent(**row) for row in self._read_raw()]

    def tail_hash(self) -> Optional[str]:
        rows = self._read_raw()
        return rows[-1]["event_hash"] if rows else None

    def append(
        self,
        event_type: str,
        object_id: str,
        payload: Dict[str, Any],
        *,
        status: str = "PROPOSED",
        canon_effect: str = "NONE",
    ) -> EngineEvent:
        previous = self.tail_hash()
        body = {
            "event_id": str(uuid.uuid4()),
            "timestamp": utc_now(),
            "event_type": event_type,
            "object_id": object_id,
            "status": status,
            "canon_effect": canon_effect,
            "payload": payload,
            "previous_event_hash": previous,
        }
        event_hash = sha256_text(canonical_json(body))
        event = EngineEvent(**body, event_hash=event_hash)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(canonical_json(asdict(event)) + "\n")
        return event

    def verify_chain(self) -> Tuple[bool, List[str]]:
        errors: List[str] = []
        previous: Optional[str] = None
        for idx, row in enumerate(self._read_raw(), start=1):
            claimed = row["event_hash"]
            body = {k: v for k, v in row.items() if k != "event_hash"}
            recomputed = sha256_text(canonical_json(body))
            if claimed != recomputed:
                errors.append(f"line {idx}: event hash mismatch")
            if row.get("previous_event_hash") != previous:
                errors.append(f"line {idx}: previous hash mismatch")
            previous = claimed
        return not errors, errors


@dataclass(frozen=True)
class Atom:
    atom_id: str
    atom_type: str
    source_path: str
    source_hash: str
    normalized_ir: Dict[str, Any]
    semantic_metadata: Dict[str, Any]
    dependency_refs: List[str]
    side_effects: List[str]
    provenance: Dict[str, Any]


@dataclass(frozen=True)
class Slot:
    slot_id: str
    target_path: str
    target_language: str
    interface_contract: Dict[str, Any]
    accepted_atom_types: List[str]
    forbidden_side_effects: List[str]
    authority: str = "TARGET_ARCHITECTURE"


@dataclass(frozen=True)
class FitDecision:
    atom_id: str
    slot_id: str
    compatible: bool
    score: float
    reasons: List[str]
    unresolved: List[str]


class RecombinationEngine:
    def __init__(self, ledger: AppendOnlyJsonlLedger):
        self.ledger = ledger

    def extract_atom(
        self,
        *,
        source_path: str,
        raw_source: str,
        atom_type: str,
        normalized_ir: Dict[str, Any],
        semantic_metadata: Dict[str, Any],
        dependency_refs: Optional[List[str]] = None,
        side_effects: Optional[List[str]] = None,
        extractor: str = "STRUCTURAL_EXTRACTOR",
    ) -> Atom:
        source_hash = sha256_text(raw_source)
        identity_basis = {
            "source_hash": source_hash,
            "atom_type": atom_type,
            "normalized_ir": normalized_ir,
        }
        atom_id = f"ATOM-{sha256_text(canonical_json(identity_basis))[:20].upper()}"
        atom = Atom(
            atom_id=atom_id,
            atom_type=atom_type,
            source_path=source_path,
            source_hash=source_hash,
            normalized_ir=normalized_ir,
            semantic_metadata=semantic_metadata,
            dependency_refs=dependency_refs or [],
            side_effects=side_effects or [],
            provenance={
                "extractor": extractor,
                "engine_id": ENGINE_ID,
                "engine_version": ENGINE_VERSION,
            },
        )
        self.ledger.append(
            "ATOM_EXTRACTED",
            atom_id,
            asdict(atom),
            status="OBSERVED",
            canon_effect="NONE",
        )
        return atom

    def register_slot(self, slot: Slot) -> None:
        self.ledger.append(
            "SLOT_REGISTERED",
            slot.slot_id,
            asdict(slot),
            status="AUTHORIZED",
            canon_effect="NONE",
        )

    def evaluate_fit(self, atom: Atom, slot: Slot) -> FitDecision:
        reasons: List[str] = []
        unresolved: List[str] = []
        score = 1.0

        if atom.atom_type not in slot.accepted_atom_types:
            reasons.append("ATOM_TYPE_NOT_ACCEPTED")
            score -= 0.50

        forbidden = sorted(set(atom.side_effects) & set(slot.forbidden_side_effects))
        if forbidden:
            reasons.append(f"FORBIDDEN_SIDE_EFFECTS:{','.join(forbidden)}")
            score -= 0.35

        expected_inputs = set(slot.interface_contract.get("inputs", {}).keys())
        observed_inputs = set(atom.semantic_metadata.get("inputs", {}).keys())
        missing_inputs = sorted(expected_inputs - observed_inputs)
        if missing_inputs:
            unresolved.append(f"MISSING_INPUT_MAPPING:{','.join(missing_inputs)}")
            score -= min(0.10 * len(missing_inputs), 0.30)

        expected_outputs = set(slot.interface_contract.get("outputs", {}).keys())
        observed_outputs = set(atom.semantic_metadata.get("outputs", {}).keys())
        missing_outputs = sorted(expected_outputs - observed_outputs)
        if missing_outputs:
            unresolved.append(f"MISSING_OUTPUT_MAPPING:{','.join(missing_outputs)}")
            score -= min(0.10 * len(missing_outputs), 0.30)

        score = max(0.0, min(score, 1.0))
        decision = FitDecision(
            atom_id=atom.atom_id,
            slot_id=slot.slot_id,
            compatible=(score >= 0.75 and not forbidden),
            score=round(score, 3),
            reasons=reasons,
            unresolved=unresolved,
        )
        self.ledger.append(
            "FIT_EVALUATED",
            f"{atom.atom_id}->{slot.slot_id}",
            asdict(decision),
            status="INFERRED",
            canon_effect="NONE",
        )
        return decision

    def propose_recombination(
        self,
        *,
        atom: Atom,
        slot: Slot,
        transformed_code: str,
        adapter_metadata: Dict[str, Any],
        fit: FitDecision,
        generator: str = "LLM_ADAPTER",
    ) -> str:
        if not fit.compatible:
            raise ValueError("Fit decision is not compatible; recombination blocked.")

        proposal_id = f"RECOMB-{sha256_text(atom.atom_id + slot.slot_id + transformed_code)[:20].upper()}"
        payload = {
            "proposal_id": proposal_id,
            "atom_id": atom.atom_id,
            "slot_id": slot.slot_id,
            "target_path": slot.target_path,
            "target_language": slot.target_language,
            "transformed_code": transformed_code,
            "adapter_metadata": adapter_metadata,
            "generator": generator,
            "source_hash": atom.source_hash,
            "fit_score": fit.score,
        }
        self.ledger.append(
            "RECOMBINATION_PROPOSED",
            proposal_id,
            payload,
            status="PROPOSED",
            canon_effect="NONE",
        )
        return proposal_id

    def record_validation(
        self,
        *,
        proposal_id: str,
        checks: Dict[str, Any],
        pass_required: bool = True,
    ) -> str:
        passed = all(bool(v) for v in checks.values()) if pass_required else True
        receipt_id = f"VAL-{sha256_text(proposal_id + canonical_json(checks))[:20].upper()}"
        self.ledger.append(
            "VALIDATION_RECEIPT",
            receipt_id,
            {
                "receipt_id": receipt_id,
                "proposal_id": proposal_id,
                "checks": checks,
                "passed": passed,
            },
            status="VERIFIED" if passed else "FAILED",
            canon_effect="NONE",
        )
        return receipt_id


class CodebaseProjector:
    """
    Builds only from validated recombination proposals.

    Existing target files are never overwritten unless overwrite=True.
    That flag is deliberately off by default.
    """

    def __init__(self, ledger: AppendOnlyJsonlLedger):
        self.ledger = ledger

    def _validated_proposals(self) -> Dict[str, Dict[str, Any]]:
        proposals: Dict[str, Dict[str, Any]] = {}
        passed: set[str] = set()

        for event in self.ledger.read_stream():
            if event.event_type == "RECOMBINATION_PROPOSED":
                proposals[event.payload["proposal_id"]] = event.payload
            elif event.event_type == "VALIDATION_RECEIPT" and event.payload.get("passed"):
                passed.add(event.payload["proposal_id"])

        return {pid: p for pid, p in proposals.items() if pid in passed}

    def project(self, root: str | Path, *, overwrite: bool = False) -> List[str]:
        root = Path(root)
        root.mkdir(parents=True, exist_ok=True)
        written: List[str] = []

        for proposal_id, proposal in self._validated_proposals().items():
            rel = Path(proposal["target_path"])
            target = root / rel
            if target.exists() and not overwrite:
                raise FileExistsError(f"Projection collision blocked: {target}")

            target.parent.mkdir(parents=True, exist_ok=True)
            fd, tmp_name = tempfile.mkstemp(prefix=".fge-", dir=str(target.parent))
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as tmp:
                    tmp.write(proposal["transformed_code"])
                    tmp.flush()
                    os.fsync(tmp.fileno())
                os.replace(tmp_name, target)
            finally:
                if os.path.exists(tmp_name):
                    os.unlink(tmp_name)

            written.append(str(target))
            self.ledger.append(
                "PROJECTION_WRITTEN",
                proposal_id,
                {
                    "proposal_id": proposal_id,
                    "target_path": str(target),
                    "content_hash": sha256_text(proposal["transformed_code"]),
                    "overwrite": overwrite,
                },
                status="VERIFIED",
                canon_effect="NONE",
            )
        return written


if __name__ == "__main__":
    work = Path("./fge_recomb_demo")
    ledger = AppendOnlyJsonlLedger(work / "ledger.jsonl")
    engine = RecombinationEngine(ledger)

    atom = engine.extract_atom(
        source_path="LEGACY_SYS/TAX_CALC.PRG",
        raw_source="IF REGION EQUAL 'TX' THEN MULTIPLY VAL BY 0.0825.",
        atom_type="BUSINESS_RULE",
        normalized_ir={
            "operation": "regional_tax_override",
            "rules": [{"region": "TX", "rate": 0.0825}],
        },
        semantic_metadata={
            "intent": "Calculate regional tax override.",
            "inputs": {"base_amount": "float", "region_code": "str"},
            "outputs": {"tax_total": "float"},
        },
        side_effects=[],
    )

    slot = Slot(
        slot_id="calculateRegionalTaxOverride",
        target_path="src/services/taxCalculationService.ts",
        target_language="TypeScript",
        interface_contract={
            "inputs": {"base_amount": "number", "region_code": "string"},
            "outputs": {"tax_total": "number"},
        },
        accepted_atom_types=["BUSINESS_RULE"],
        forbidden_side_effects=["NETWORK", "FILESYSTEM_WRITE", "GLOBAL_MUTATION"],
    )
    engine.register_slot(slot)

    fit = engine.evaluate_fit(atom, slot)

    proposal_id = engine.propose_recombination(
        atom=atom,
        slot=slot,
        fit=fit,
        transformed_code=(
            "export function calculateRegionalTaxOverride("
            "base_amount: number, region_code: string): number {\n"
            "  const rate = region_code === 'TX' ? 0.0825 : 0.05;\n"
            "  return base_amount * rate;\n"
            "}\n"
        ),
        adapter_metadata={
            "mapping": {
                "base_amount": "base_amount",
                "region_code": "region_code",
                "tax_total": "return_value",
            }
        },
    )

    engine.record_validation(
        proposal_id=proposal_id,
        checks={
            "static_analysis": True,
            "unit_tests": True,
            "differential_test": True,
            "dependency_closure": True,
            "security_scan": True,
        },
    )

    ok, errors = ledger.verify_chain()
    assert ok, errors

    projector = CodebaseProjector(ledger)
    projected = projector.project(work / "projection")
    print(json.dumps({"projected": projected, "ledger_valid": ok}, indent=2))
