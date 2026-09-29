import json
from pathlib import Path

from runtime.intake import fge_intake_router as router


REPO_ROOT = Path(__file__).resolve().parents[1]


def make_root(tmp_path):
    config = json.loads((REPO_ROOT / "storage_makeover" / "config" / "routing-rules.json").read_text(encoding="utf-8"))
    config_path = tmp_path / "storage_makeover" / "config" / "routing-rules.json"
    config_path.parent.mkdir(parents=True)
    config_path.write_text(json.dumps(config), encoding="utf-8")
    (tmp_path / "intake" / "inbox").mkdir(parents=True)
    return tmp_path, config_path, config


def test_code_routes_with_high_confidence(tmp_path):
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
    assert decision.physical_class == "IMAGE"
    assert decision.route_state == "HOLD"
    assert decision.hold_reason == "BINARY_PUBLICATION_UNVERIFIED"


def test_infographic_image_still_obeys_public_binary_guard(tmp_path):
    root, _, config = make_root(tmp_path)
    source = root / "intake" / "inbox" / "private-plate.png"
    source.write_bytes(b"image-placeholder")
    sidecar = source.with_name(source.name + ".fge.json")
    sidecar.write_text(
        json.dumps({"object_class": "INFOGRAPHIC", "domain": "signals"}),
        encoding="utf-8",
    )
    decision = router.plan_decision(source, root, config)
    assert decision.object_class == "INFOGRAPHIC_MANIFEST"
    assert decision.physical_class == "IMAGE"
    assert decision.route_state == "HOLD"
    assert decision.hold_reason == "BINARY_PUBLICATION_UNVERIFIED"


def test_standard_public_infographic_media_can_route(tmp_path):
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
    assert decision.physical_class == "IMAGE"
    assert decision.route_state == "ROUTE"
    assert "infographics" in decision.destination


def test_restricted_media_holds_even_when_public_ok_true(tmp_path):
    root, _, config = make_root(tmp_path)
    source = root / "intake" / "inbox" / "restricted.png"
    source.write_bytes(b"image-placeholder")
    sidecar = source.with_name(source.name + ".fge.json")
    sidecar.write_text(
        json.dumps(
            {
                "object_class": "IMAGE",
                "sensitivity": "INTIMATE_PRIVATE",
                "age_state": "VERIFIED_ADULT",
                "public_ok": True,
                "origin_class": "RAW_SOURCE",
            }
        ),
        encoding="utf-8",
    )
    decision = router.plan_decision(source, root, config)
    assert decision.route_state == "HOLD"
    assert decision.hold_reason == "SENSITIVE_OR_PRIVATE_MEDIA"


def test_binary_document_requires_explicit_public_ok(tmp_path):
    root, _, config = make_root(tmp_path)
    source = root / "intake" / "inbox" / "spec.pdf"
    source.write_bytes(b"pdf-placeholder")
    decision = router.plan_decision(source, root, config)
    assert decision.physical_class == "DOCUMENT"
    assert decision.route_state == "HOLD"
    assert decision.hold_reason == "BINARY_PUBLICATION_UNVERIFIED"


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


def test_existing_destination_is_never_overwritten(tmp_path):
    root, config_path, config = make_root(tmp_path)
    source = root / "intake" / "inbox" / "adapter.py"
    source.write_text("VALUE = 2\n", encoding="utf-8")
    expected = root / "storage_makeover" / "routed" / "code" / "unclassified" / "adapter.py"
    expected.parent.mkdir(parents=True)
    expected.write_text("ORIGINAL\n", encoding="utf-8")
    events = router.run(root, config_path, apply=True)
    assert expected.read_text(encoding="utf-8") == "ORIGINAL\n"
    routed = root / events[0]["final_destination"]
    assert routed != expected
    assert routed.read_text(encoding="utf-8") == "VALUE = 2\n"
