#!/usr/bin/env python3
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DISPATCH_REGISTER = ROOT / "journalist" / "dispatches" / "dispatch_register.jsonl"
BUS_DIR = ROOT / "journalist" / "signal_bus"
SIGNALS = BUS_DIR / "signals.jsonl"
ACKS = BUS_DIR / "acks.jsonl"
RECEIPTS = BUS_DIR / "receipts.jsonl"
STATE = BUS_DIR / "state.json"
JOURNAL_FEEDBACK = ROOT / "journalist" / "dispatches" / "feedback_register.jsonl"

MIN_SIGNAL_FIELDS = [
    "SIGNAL_ID", "SOURCE", "STATUS", "SUBJECT", "ROUTE_TO",
    "WHY_IT_MATTERS", "CANON_EFFECT", "AUTHORITY_EFFECT"
]

VALID_ACKS = {
    "UNREAD", "READ", "ACCEPTED_FOR_ACTION", "DEFERRED",
    "NOT_APPLICABLE", "BLOCKED", "SUPERSEDED", "RESOLVED"
}

VALID_PRIORITY = {"P0_CRITICAL", "P1_BLOCKING", "P2_ACTIONABLE", "P3_INFORMATIONAL", "P4_ARCHIVAL"}
VALID_SCOPE = {"LOCAL", "DOMAIN", "CROSS_THREAD", "CROSS_RUNTIME", "SYSTEM", "DIRECTOR"}
VALID_DELTA = {
    "NONE", "NEW_FACT", "NEW_EVIDENCE", "NEW_CONTRADICTION", "NEW_UNKNOWN",
    "UNKNOWN_RESOLVED", "AUTHORITY_CLARIFIED", "DEPENDENCY_DISCOVERED", "ACTION_UNLOCKED"
}


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def ensure_files():
    DISPATCH_REGISTER.parent.mkdir(parents=True, exist_ok=True)
    BUS_DIR.mkdir(parents=True, exist_ok=True)
    for p in [DISPATCH_REGISTER, SIGNALS, ACKS, RECEIPTS, JOURNAL_FEEDBACK]:
        p.touch(exist_ok=True)
    if not STATE.exists():
        STATE.write_text(json.dumps({"processed_dispatch_ids": [], "signal_hashes": []}, indent=2) + "\n")


def read_jsonl(path):
    rows = []
    if not path.exists():
        return rows
    for lineno, raw in enumerate(path.read_text().splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            rows.append((lineno, json.loads(raw)))
        except json.JSONDecodeError as exc:
            rows.append((lineno, {"_parse_error": str(exc), "_raw": raw}))
    return rows


def append_jsonl(path, obj):
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n")


def stable_hash(obj):
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def load_state():
    ensure_files()
    try:
        return json.loads(STATE.read_text())
    except Exception:
        return {"processed_dispatch_ids": [], "signal_hashes": []}


def save_state(state):
    STATE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


def normalize_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def derive_route(dispatch):
    explicit = normalize_list(dispatch.get("route_to") or dispatch.get("ROUTE_TO"))
    if explicit:
        return explicit
    affects = normalize_list(dispatch.get("affects") or dispatch.get("AFFECTS"))
    if affects:
        return affects
    if dispatch.get("director_decision_required") is True:
        return ["DIRECTOR"]
    return ["JOURNALIST"]


def derive_priority(dispatch):
    explicit = dispatch.get("priority") or dispatch.get("PRIORITY")
    if explicit in VALID_PRIORITY:
        return explicit
    if dispatch.get("blocker"):
        return "P1_BLOCKING"
    if dispatch.get("next_admissible_action"):
        return "P2_ACTIONABLE"
    return "P3_INFORMATIONAL"


def derive_scope(dispatch, routes):
    explicit = dispatch.get("scope") or dispatch.get("SCOPE")
    if explicit in VALID_SCOPE:
        return explicit
    if "DIRECTOR" in routes:
        return "DIRECTOR"
    if len(routes) > 1:
        return "CROSS_THREAD"
    return "DOMAIN"


def make_signal(dispatch):
    dispatch_id = dispatch.get("dispatch_id") or dispatch.get("DISPATCH_ID") or dispatch.get("id")
    if not dispatch_id:
        return None, "BLOCKED_SIGNAL_SCHEMA: missing dispatch identity"

    source = dispatch.get("source") or dispatch.get("SOURCE")
    subject = dispatch.get("subject") or dispatch.get("SUBJECT")
    why = dispatch.get("why_it_matters") or dispatch.get("WHY_IT_MATTERS")
    status = dispatch.get("status") or dispatch.get("STATUS") or "UNKNOWN"
    routes = derive_route(dispatch)

    if not source or not subject or not why:
        return None, "BLOCKED_SIGNAL_SCHEMA: missing source/subject/why_it_matters"

    delta = dispatch.get("knowledge_delta") or dispatch.get("KNOWLEDGE_DELTA") or "NEW_EVIDENCE"
    if delta not in VALID_DELTA:
        delta = "NEW_EVIDENCE"

    provenance = dispatch.get("provenance") or dispatch.get("PROVENANCE") or {"dispatch_id": dispatch_id}
    signal_basis = {
        "dispatch_id": dispatch_id,
        "source": source,
        "subject": subject,
        "observation": dispatch.get("observation") or dispatch.get("OBSERVATION"),
        "evidence": dispatch.get("evidence") or dispatch.get("EVIDENCE"),
        "routes": routes,
        "delta": delta,
    }
    digest = stable_hash(signal_basis)[:16]

    canon_effect = dispatch.get("canon_effect") or dispatch.get("CANON_EFFECT") or "NONE"
    authority_effect = dispatch.get("authority_effect") or dispatch.get("AUTHORITY_EFFECT") or "NONE"

    signal = {
        "SIGNAL_ID": f"FGE-SIGNAL-{digest.upper()}",
        "TIMESTAMP": utc_now(),
        "SOURCE": source,
        "DERIVED_FROM": dispatch_id,
        "PROVENANCE": provenance,
        "TYPE": dispatch.get("type") or dispatch.get("TYPE") or ("BLOCKER" if dispatch.get("blocker") else "CHANGE"),
        "STATUS": status,
        "PRIORITY": derive_priority(dispatch),
        "SCOPE": derive_scope(dispatch, routes),
        "SUBJECT": subject,
        "OBSERVATION": dispatch.get("observation") or dispatch.get("OBSERVATION"),
        "EVIDENCE": dispatch.get("evidence") or dispatch.get("EVIDENCE"),
        "AFFECTS": normalize_list(dispatch.get("affects") or dispatch.get("AFFECTS")),
        "ROUTE_TO": routes,
        "WHY_IT_MATTERS": why,
        "KNOWLEDGE_DELTA": delta,
        "BLOCKER": dispatch.get("blocker") or dispatch.get("BLOCKER"),
        "NEXT_ADMISSIBLE_ACTION": dispatch.get("next_admissible_action") or dispatch.get("NEXT_ADMISSIBLE_ACTION"),
        "CANON_EFFECT": canon_effect,
        "AUTHORITY_EFFECT": authority_effect,
        "ACK_REQUIRED": bool(dispatch.get("ack_required", True)),
        "ACK_STATUS": "UNREAD",
        "ESCALATION_POLICY": dispatch.get("escalation_policy") or "DIRECTOR_IF_BLOCKED_OR_AUTHORITY_CONFLICT",
        "EXPIRY_OR_RECHECK": dispatch.get("expiry_or_recheck"),
        "CONTRADICTIONS": normalize_list(dispatch.get("contradictions")),
        "UNKNOWN_FIELDS": normalize_list(dispatch.get("unknown_fields")),
    }
    return signal, None


def validate_signal(signal):
    missing = [k for k in MIN_SIGNAL_FIELDS if k not in signal or signal[k] in (None, "", [])]
    return missing


def run_bus():
    ensure_files()
    state = load_state()
    processed = set(state.get("processed_dispatch_ids", []))
    hashes = set(state.get("signal_hashes", []))
    emitted = 0
    blocked = 0

    for lineno, dispatch in read_jsonl(DISPATCH_REGISTER):
        if "_parse_error" in dispatch:
            blocked += 1
            continue
        dispatch_id = dispatch.get("dispatch_id") or dispatch.get("DISPATCH_ID") or dispatch.get("id")
        if dispatch_id and dispatch_id in processed:
            continue
        signal, error = make_signal(dispatch)
        if error:
            blocked += 1
            if dispatch_id:
                processed.add(dispatch_id)
            continue
        missing = validate_signal(signal)
        if missing:
            blocked += 1
            processed.add(dispatch_id)
            continue
        fingerprint = stable_hash({k: signal[k] for k in ["SOURCE", "SUBJECT", "ROUTE_TO", "KNOWLEDGE_DELTA", "EVIDENCE", "STATUS"]})
        if fingerprint in hashes:
            processed.add(dispatch_id)
            continue
        append_jsonl(SIGNALS, signal)
        hashes.add(fingerprint)
        processed.add(dispatch_id)
        emitted += 1

    state["processed_dispatch_ids"] = sorted(processed)
    state["signal_hashes"] = sorted(hashes)
    state["last_run_at"] = utc_now()
    state["last_run_emitted"] = emitted
    state["last_run_blocked"] = blocked
    save_state(state)
    print(json.dumps({"status": "OK", "emitted": emitted, "blocked": blocked, "processed": len(processed)}, indent=2))


def cmd_validate():
    ensure_files()
    errors = []
    for lineno, signal in read_jsonl(SIGNALS):
        if "_parse_error" in signal:
            errors.append({"line": lineno, "error": signal["_parse_error"]})
            continue
        missing = validate_signal(signal)
        if missing:
            errors.append({"line": lineno, "missing": missing})
        if signal.get("ACK_STATUS") not in VALID_ACKS:
            errors.append({"line": lineno, "bad_ack": signal.get("ACK_STATUS")})
        if signal.get("PRIORITY") not in VALID_PRIORITY:
            errors.append({"line": lineno, "bad_priority": signal.get("PRIORITY")})
        if signal.get("SCOPE") not in VALID_SCOPE:
            errors.append({"line": lineno, "bad_scope": signal.get("SCOPE")})
    print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors}, indent=2))
    raise SystemExit(0 if not errors else 1)


def cmd_ack(signal_id, status, runtime, thread):
    ensure_files()
    if status not in VALID_ACKS:
        raise SystemExit(f"Invalid ACK status: {status}")
    found = any(row.get("SIGNAL_ID") == signal_id for _, row in read_jsonl(SIGNALS) if "_parse_error" not in row)
    if not found:
        raise SystemExit(f"Unknown signal: {signal_id}")
    ack = {
        "ACK_ID": f"FGE-ACK-{stable_hash([signal_id, status, runtime, thread, utc_now()])[:16].upper()}",
        "SIGNAL_ID": signal_id,
        "STATUS": status,
        "RUNTIME": runtime,
        "THREAD": thread,
        "TIMESTAMP": utc_now(),
        "AUTHORITY_EFFECT": "NONE",
        "CANON_EFFECT": "NONE",
    }
    append_jsonl(ACKS, ack)
    print(json.dumps(ack, indent=2))


def cmd_receipt(signal_id, new_status, action, result):
    ensure_files()
    found = any(row.get("SIGNAL_ID") == signal_id for _, row in read_jsonl(SIGNALS) if "_parse_error" not in row)
    if not found:
        raise SystemExit(f"Unknown signal: {signal_id}")
    receipt = {
        "DELTA_RECEIPT_ID": f"FGE-DELTA-{stable_hash([signal_id, action, result, utc_now()])[:16].upper()}",
        "PARENT_SIGNAL": signal_id,
        "ACTION_TAKEN": action,
        "RESULT": result,
        "EVIDENCE": [],
        "NEW_STATUS": new_status,
        "NEW_BLOCKERS": [],
        "NEW_UNKNOWN": [],
        "NEW_SIGNALS_EMITTED": [],
        "CANON_EFFECT": "NONE",
        "AUTHORITY_EFFECT": "NONE",
        "TIMESTAMP": utc_now(),
    }
    append_jsonl(RECEIPTS, receipt)
    feedback = {
        "dispatch_id": f"FGE-FEEDBACK-{receipt['DELTA_RECEIPT_ID'].split('-')[-1]}",
        "timestamp": receipt["TIMESTAMP"],
        "source": "FGE-LARA-SIGNAL-BUS-IMPLEMENTATION-001",
        "status": new_status,
        "subject": f"Signal result: {signal_id}",
        "observation": result,
        "evidence": [{"delta_receipt": receipt["DELTA_RECEIPT_ID"]}],
        "affects": ["JOURNALIST"],
        "route_to": ["JOURNALIST"],
        "why_it_matters": "Closes the signal feedback loop and returns work result to the Journalist.",
        "knowledge_delta": "NEW_EVIDENCE",
        "canon_effect": "NONE",
        "authority_effect": "NONE",
        "ack_required": False,
    }
    append_jsonl(JOURNAL_FEEDBACK, feedback)
    print(json.dumps(receipt, indent=2))


def main():
    p = argparse.ArgumentParser(description="FGE Lara Signal Bus")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("run")
    sub.add_parser("validate")
    a = sub.add_parser("ack")
    a.add_argument("signal_id")
    a.add_argument("status")
    a.add_argument("runtime")
    a.add_argument("thread")
    r = sub.add_parser("receipt")
    r.add_argument("signal_id")
    r.add_argument("new_status")
    r.add_argument("action")
    r.add_argument("result")
    args = p.parse_args()
    if args.cmd == "run":
        run_bus()
    elif args.cmd == "validate":
        cmd_validate()
    elif args.cmd == "ack":
        cmd_ack(args.signal_id, args.status, args.runtime, args.thread)
    elif args.cmd == "receipt":
        cmd_receipt(args.signal_id, args.new_status, args.action, args.result)


if __name__ == "__main__":
    main()
