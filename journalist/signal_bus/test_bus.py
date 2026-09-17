import json
import tempfile
from pathlib import Path
import importlib.util

BUS_PATH = Path(__file__).with_name("bus.py")
spec = importlib.util.spec_from_file_location("lara_bus", BUS_PATH)
bus = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bus)


def test_make_signal_routes_and_firebreak():
    dispatch = {
        "dispatch_id": "D1",
        "source": "TEST",
        "status": "VERIFIED",
        "subject": "Raven face blocker",
        "observation": "Face validation failed",
        "evidence": ["receipt-1"],
        "affects": ["CASTING", "RENDER"],
        "route_to": ["CASTING", "RENDER"],
        "why_it_matters": "Blocks approval",
        "knowledge_delta": "NEW_EVIDENCE",
        "blocker": "FACE_LOCK",
        "next_admissible_action": "Compare authoritative face reference",
        "canon_effect": "NONE",
        "authority_effect": "NONE"
    }
    signal, error = bus.make_signal(dispatch)
    assert error is None
    assert signal["ROUTE_TO"] == ["CASTING", "RENDER"]
    assert signal["PRIORITY"] == "P1_BLOCKING"
    assert signal["CANON_EFFECT"] == "NONE"
    assert signal["AUTHORITY_EFFECT"] == "NONE"
    assert not bus.validate_signal(signal)


def test_unknown_route_falls_back_to_journalist():
    dispatch = {
        "dispatch_id": "D2",
        "source": "TEST",
        "status": "CLAIMED",
        "subject": "Unrouted observation",
        "why_it_matters": "Needs classification"
    }
    signal, error = bus.make_signal(dispatch)
    assert error is None
    assert signal["ROUTE_TO"] == ["JOURNALIST"]


def test_missing_identity_blocks():
    signal, error = bus.make_signal({"source": "TEST", "subject": "x", "why_it_matters": "y"})
    assert signal is None
    assert "BLOCKED_SIGNAL_SCHEMA" in error


def test_stable_hash_is_order_neutral():
    assert bus.stable_hash({"a": 1, "b": 2}) == bus.stable_hash({"b": 2, "a": 1})
