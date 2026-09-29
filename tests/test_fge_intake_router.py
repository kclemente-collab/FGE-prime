import importlib.util
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "runtime" / "intake" / "fge_intake_router.py"
SPEC = importlib.util.spec_from_file_location("fge_intake_router", MODULE_PATH)
router = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(router)


def make_root(tmp_path):
    config = json.loads((REPO_ROOT / "storage_makeover" / "config" / "routing-rules.json").read_text(encoding="utf-8"))
    config_path = tmp_path / "storage_makeover" / "config" / "routing-rules.json"
    config_path.parent.mkdir(parents=True)
    config_path.write_text(json.dumps(config), encoding="utf-8")
    (tmp_path / "intake" / "inbox").mkdir(parents=True)
    return tmp_path, config_path, config


def test_code_routes_with_review_or_better(tmp_path):
    root, _, config = make_root(tmp_path)
    source = root / "intake" / "inbox" / "tool.py"
    source.write_text("print('ok')\n", encoding="utf-8")
    decision = router.plan_decision(source, root, config)
    assert decision.object_class == "CODE"
    assert decision.route_state == "ROUTE"
    assert decision.destination.endswith("tool.py")


def test_unknown_holds_fail_closed(tmp_path):
    root, _, config = make_root(tmp_path)
    source = root / "intake" / "inbox" / "mystery.blobx"
    source.write_bytes(b"mystery")
    decision = router.plan_decision(source, root, config)
    assert decision.route_state == "HOLD"
    assert decision.hold_reason == "UNKNOWN_ROUTE"


def test_media_without_sidecar_holds_in_public_repo(tmp_path):
    root, _, config = make_root(tmp_path)
    source = root / "intake" / "inbox" / "image.png"
    source.write_bytes(b"not-a-real-png-but-hashable")
    decision = router.plan_decision(source, root, config)
    assert decision.object_class == "IMAGE"
    assert decision.route_state == "HOLD"
    assert decision.hold_reason == "MEDIA_PUBLICATION_UNVERIFIED"


def test_standard_public_media_with_origin_can_route(tmp_path):
    root, _, config = make_root(tmp_path)
    source = root / "intake" / "inbox" / "plate.png"
    source.write_bytes(b"image-placeholder")
    sidecar = source.with_name(source.name + ".fge.json")
    sidecar.write_text(
        json.dumps(
            {
                "object_class": "INFOGRAPHIC",
                "domain": "signals",
                "sensitivity": "STANDARD",
                "public_ok": True,
                "origin_class": "GENERATED_OUTPUT",
            }
        ),
        encoding="utf-8",
    )
    decision = router.plan_decision(source, root, config)
    assert decision.object_class == "INFOGRAPHIC_MANIFEST"
    assert decision.route_state == "ROUTE"
    assert "infographics" in decision.destination


def test_pointer_cannot_substitute_for_character_id(tmp_path):
    root, _, config = make_root(tmp_path)
    source = root / "intake" / "inbox" / "character.json"
    source.write_text("{}", encoding="utf-8")
    sidecar = source.with_name(source.name + ".fge.json")
    sidecar.write_text(
        json.dumps(
            {
                "object_class": "STRUCTURED_DATA",
                "primary_character_id": "FGE-CHAR-0005",
                "enterprise_asset_pointer": "FGE-CHAR-0005",
            }
        ),
        encoding="utf-8",
    )
    decision = router.plan_decision(source, root, config)
    assert decision.route_state == "HOLD"
    assert decision.hold_reason == "POINTER_IDENTITY_SUBSTITUTION"


def test_apply_moves_source_and_writes_receipt_and_index(tmp_path):
    root, config_path, config = make_root(tmp_path)
    source = root / "intake" / "inbox" / "adapter.py"
    source.write_text("VALUE = 1\n", encoding="utf-8")
    events = router.run(root, config_path, apply=True)
    assert len(events) == 1
    assert events[0]["route_state"] == "ROUTE"
    assert not source.exists()
    assert (root / events[0]["final_destination"]).exists()
    assert (root / config["index"]).exists()
    receipts = list((root / config["route_receipts"]).glob("*.json"))
    assert len(receipts) == 1
