#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import py_compile
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

SUITE_OBJECT_ID = "FGE-RECOMBINATION-REGRESSION-001"
SUITE_VERSION = "0.1.0"
TARGET_OBJECT = "FGE-RECOMBINATION-ENGINE-001@0.1.0"
TARGET_SHA256 = "269232700cb8ba1de66c3033e4b25a897c9d0ebadcc0d9fcf8ce58960bac590d"
EXPECTED_OUTPUT_SHA256 = "c39a990a0e1af57a1e0614e0bbc345fee925e913cb5e417c15afe66c101e6203"
CANON_EFFECT = "NONE"
AUTHORITY_EFFECT = "NONE"

ROOT = Path(__file__).resolve().parent
ENGINE_PATH = ROOT / "fge_recombination_engine.py"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_engine():
    spec = importlib.util.spec_from_file_location("fge_recombination_engine", ENGINE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("engine import spec unavailable")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def fixture(mod, root: Path, *, differential_test: bool = True, side_effects=None, atom_type="BUSINESS_RULE") -> dict[str, Any]:
    ledger = mod.AppendOnlyJsonlLedger(root / "ledger.jsonl")
    engine = mod.RecombinationEngine(ledger)
    atom = engine.extract_atom(
        source_path="LEGACY_SYS/TAX_CALC.PRG",
        raw_source="IF REGION EQUAL 'TX' THEN MULTIPLY VAL BY 0.0825.",
        atom_type=atom_type,
        normalized_ir={"operation": "regional_tax_override", "rules": [{"region": "TX", "rate": 0.0825}]},
        semantic_metadata={
            "intent": "Calculate regional tax override.",
            "inputs": {"base_amount": "float", "region_code": "str"},
            "outputs": {"tax_total": "float"},
        },
        side_effects=side_effects or [],
    )
    slot = mod.Slot(
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
    proposal_id = None
    receipt_id = None
    projected: list[str] = []
    output_sha = None
    if fit.compatible:
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
        receipt_id = engine.record_validation(
            proposal_id=proposal_id,
            checks={
                "syntax_build": True,
                "static_analysis": True,
                "unit_tests": True,
                "differential_test": differential_test,
                "dependency_closure": True,
                "security_scan": True,
            },
        )
        projector = mod.CodebaseProjector(ledger)
        projected = projector.project(root / "projection")
        if projected:
            output_sha = sha256_file(Path(projected[0]))
    chain_ok, chain_errors = ledger.verify_chain()
    events = ledger.read_stream()
    return {
        "ledger": ledger,
        "events": events,
        "atom": atom,
        "slot": slot,
        "fit": fit,
        "proposal_id": proposal_id,
        "receipt_id": receipt_id,
        "projected": projected,
        "output_sha256": output_sha,
        "chain_ok": chain_ok,
        "chain_errors": chain_errors,
    }


def test_source_integrity(mod) -> dict[str, Any]:
    actual = sha256_file(ENGINE_PATH)
    assert actual == TARGET_SHA256, (actual, TARGET_SHA256)
    assert mod.ENGINE_ID == "FGE-RECOMBINATION-ENGINE-001"
    assert mod.ENGINE_VERSION == "0.1.0"
    return {"source_sha256": actual}


def test_syntax_build(mod) -> dict[str, Any]:
    py_compile.compile(str(ENGINE_PATH), doraise=True)
    ast.parse(ENGINE_PATH.read_text(encoding="utf-8"))
    return {"compiled": True, "ast_parse": True}


def test_static_analysis(mod) -> dict[str, Any]:
    tree = ast.parse(ENGINE_PATH.read_text(encoding="utf-8"))
    funcs = {n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    required = {"canonical_json", "sha256_text", "extract_atom", "evaluate_fit", "propose_recombination", "record_validation", "project", "verify_chain"}
    missing = sorted(required - funcs)
    assert not missing, missing
    return {"required_functions_present": sorted(required)}


def test_dependency_closure(mod) -> dict[str, Any]:
    tree = ast.parse(ENGINE_PATH.read_text(encoding="utf-8"))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    stdlib = set(getattr(sys, "stdlib_module_names", ()))
    unresolved = sorted(name for name in imports if name not in stdlib and name != "__future__")
    assert not unresolved, unresolved
    return {"stdlib_only": True, "imports": sorted(imports)}


def test_security_scan(mod) -> dict[str, Any]:
    source = ENGINE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    forbidden_calls = {"eval", "exec", "compile", "__import__"}
    seen_forbidden = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in forbidden_calls:
            seen_forbidden.append(node.func.id)
    assert not seen_forbidden, seen_forbidden
    assert "subprocess" not in source
    assert "socket" not in source
    project_node = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "project")
    overwrite_arg = project_node.args.kwonlyargs[0].arg
    overwrite_default = project_node.args.kw_defaults[0]
    assert overwrite_arg == "overwrite"
    assert isinstance(overwrite_default, ast.Constant) and overwrite_default.value is False
    return {"forbidden_dynamic_execution": False, "overwrite_default": False}


def test_unit_identity_and_fit(mod) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as td1, tempfile.TemporaryDirectory() as td2:
        a = fixture(mod, Path(td1))
        b = fixture(mod, Path(td2))
    assert a["atom"].atom_id == b["atom"].atom_id
    assert a["proposal_id"] == b["proposal_id"]
    assert a["receipt_id"] == b["receipt_id"]
    assert a["fit"].compatible is True and a["fit"].score == 1.0
    return {"atom_id": a["atom"].atom_id, "proposal_id": a["proposal_id"], "validation_receipt_id": a["receipt_id"]}


def test_differential_projection(mod) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as td:
        run = fixture(mod, Path(td))
        assert run["chain_ok"], run["chain_errors"]
        assert len(run["projected"]) == 1
        assert run["output_sha256"] == EXPECTED_OUTPUT_SHA256
        assert all(event.canon_effect == "NONE" for event in run["events"])
    return {"output_sha256": run["output_sha256"], "canon_effect": "NONE"}


def test_negative_control(mod) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as td:
        run = fixture(mod, Path(td), differential_test=False)
        validation = [e for e in run["events"] if e.event_type == "VALIDATION_RECEIPT"][-1]
        assert validation.status == "FAILED"
        assert validation.payload["passed"] is False
        assert run["projected"] == []
        assert run["chain_ok"], run["chain_errors"]
        assert all(event.canon_effect == "NONE" for event in run["events"])
    return {"validation_status": "FAILED", "projection_blocked": True, "canon_effect": "NONE"}


def test_forbidden_side_effect_rejection(mod) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as td:
        run = fixture(mod, Path(td), side_effects=["NETWORK"])
        assert run["fit"].compatible is False
        assert run["proposal_id"] is None
        assert any("FORBIDDEN_SIDE_EFFECTS:NETWORK" == r for r in run["fit"].reasons)
        assert run["chain_ok"], run["chain_errors"]
    return {"compatible": False, "reason": "FORBIDDEN_SIDE_EFFECTS:NETWORK"}


def test_projection_collision_guard(mod) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        run = fixture(mod, root)
        assert len(run["projected"]) == 1
        projector = mod.CodebaseProjector(run["ledger"])
        blocked = False
        try:
            projector.project(root / "projection")
        except FileExistsError:
            blocked = True
        assert blocked
    return {"collision_blocked": True}


def test_ledger_tamper_detection(mod) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as td:
        run = fixture(mod, Path(td))
        ledger_path = run["ledger"].path
        rows = ledger_path.read_text(encoding="utf-8").splitlines()
        first = json.loads(rows[0])
        first["status"] = "TAMPERED"
        rows[0] = json.dumps(first, sort_keys=True, separators=(",", ":"))
        ledger_path.write_text("\n".join(rows) + "\n", encoding="utf-8")
        ok, errors = run["ledger"].verify_chain()
        assert ok is False
        assert errors
    return {"tamper_detected": True}


TESTS: list[tuple[str, Callable[[Any], dict[str, Any]]]] = [
    ("source_integrity", test_source_integrity),
    ("syntax_build", test_syntax_build),
    ("static_analysis", test_static_analysis),
    ("dependency_closure", test_dependency_closure),
    ("security_scan", test_security_scan),
    ("unit_identity_and_fit", test_unit_identity_and_fit),
    ("differential_projection", test_differential_projection),
    ("negative_control", test_negative_control),
    ("forbidden_side_effect_rejection", test_forbidden_side_effect_rejection),
    ("projection_collision_guard", test_projection_collision_guard),
    ("ledger_tamper_detection", test_ledger_tamper_detection),
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", default="all")
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    source_before = sha256_file(ENGINE_PATH)
    mod = load_engine()
    selected = TESTS if args.case == "all" else [item for item in TESTS if item[0] == args.case]
    if not selected:
        raise SystemExit(f"unknown case: {args.case}")

    results = []
    failed = 0
    for name, fn in selected:
        try:
            details = fn(mod)
            results.append({"name": name, "status": "PASS", "details": details})
        except Exception as exc:
            failed += 1
            results.append({"name": name, "status": "FAIL", "error": f"{type(exc).__name__}: {exc}"})

    source_after = sha256_file(ENGINE_PATH)
    summary = {
        "suite_object_id": SUITE_OBJECT_ID,
        "suite_version": SUITE_VERSION,
        "target_object": TARGET_OBJECT,
        "target_sha256_expected": TARGET_SHA256,
        "target_sha256_before": source_before,
        "target_sha256_after": source_after,
        "source_unchanged": source_before == source_after == TARGET_SHA256,
        "case_selector": args.case,
        "total": len(results),
        "passed": sum(1 for r in results if r["status"] == "PASS"),
        "failed": failed,
        "pass_rate": 1.0 if results and failed == 0 else (0.0 if not results else (len(results)-failed)/len(results)),
        "canon_effect": CANON_EFFECT,
        "authority_effect": AUTHORITY_EFFECT,
        "expected_output_sha256": EXPECTED_OUTPUT_SHA256,
        "results": results,
    }
    text = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if failed == 0 and summary["source_unchanged"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
