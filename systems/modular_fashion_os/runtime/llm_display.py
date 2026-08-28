"""Compile a stored Fashion Asset Envelope into an LLM runtime packet.

The display layer is read-only with respect to persisted authority. It may emit
PROPOSED deltas but never marks them authorized, locked or canonical.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List, Optional


UNKNOWN = "UNKNOWN"


def _value(value: Any) -> Any:
    if value is None or value == "":
        return UNKNOWN
    return value


def _as_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


def _unknown_paths(envelope: Dict[str, Any]) -> List[str]:
    explicit = envelope.get("validation", {}).get("unknowns", [])
    return [str(item) for item in explicit]


def compile_display_packet(
    envelope: Dict[str, Any],
    *,
    target_runtime: str = "LLM_GENERIC",
    character_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Return an authority-safe packet optimized for LLM reasoning/presentation."""
    identity = envelope.get("identity", {})
    garment = envelope.get("garment", {})
    representations = envelope.get("representations", {})
    validation = envelope.get("validation", {})

    packet: Dict[str, Any] = {
        "packet_type": "FGE_FASHION_LLM_DISPLAY_PACKET",
        "packet_version": "0.1.0",
        "authority": "EPHEMERAL_DISPLAY_ONLY",
        "canon_effect": "NONE",
        "source": {
            "object_id": _value(envelope.get("object_id")),
            "asset_id": _value(identity.get("asset_id")),
            "version": _value(envelope.get("version")),
            "source_status": _value(envelope.get("status")),
            "source_canon_effect": _value(envelope.get("canon_effect")),
        },
        "display": {
            "name": _value(identity.get("display_name")),
            "class": _value(identity.get("asset_class")),
            "brand": _value(identity.get("brand")),
            "rarity": _value(identity.get("rarity")),
        },
        "fit": garment.get("fit", {}),
        "layering": garment.get("layering", {}),
        "coverage": garment.get("coverage", {}),
        "material": garment.get("material", {}),
        "physics": garment.get("physics", {}),
        "customization": garment.get("customization", {}),
        "rights": envelope.get("rights", {}),
        "representations": {
            "source": _as_list(representations.get("source")),
            "runtime": _as_list(representations.get("runtime")),
            "adapters": _as_list(representations.get("adapters")),
        },
        "validation": {
            "state": _value(validation.get("state")),
            "gates": validation.get("gates", {}),
            "conflicts": _as_list(validation.get("conflicts")),
            "unknowns": _unknown_paths(envelope),
        },
        "runtime_request": {
            "target": target_runtime,
            "character_context_supplied": character_context is not None,
        },
        "governance": {
            "unknown_over_invented": True,
            "preserve_conflicts": True,
            "may_propose_deltas": True,
            "may_authorize_deltas": False,
            "may_mutate_character_identity": False,
            "may_mutate_storage": False,
        },
        "proposed_deltas": [],
    }

    if character_context is not None:
        packet["character_context"] = {
            "character_id": _value(character_context.get("character_id")),
            "character_version": _value(character_context.get("version")),
            "rig_profile": _value(character_context.get("rig_profile")),
            "body_profile": _value(character_context.get("body_profile")),
            "wardrobe_policy": character_context.get("wardrobe_policy", {}),
            "authority": "REFERENCE_ONLY",
        }

    return packet


def build_llm_runtime_text(packet: Dict[str, Any]) -> str:
    """Return a portable LLM runtime block that can be pasted into any model."""
    rules = """FGE FASHION DISPLAY RUNTIME\nROLE=READ_ONLY_INTERPRETER\nLAW=UNKNOWN>INVENT|CONFLICT>PRESERVE|GENERATED!=CANON\nMAY=DESCRIBE|COMPARE|RECOMMEND|PROPOSE_DELTA|SELECT_COMPATIBLE_REPRESENTATION\nMUST_NOT=AUTHORIZE|LOCK|MUTATE_STORAGE|MUTATE_CHARACTER_IDENTITY\nOUTPUT=DISPLAY+COMPATIBILITY+UNKNOWNS+CONFLICTS+PROPOSED_DELTAS\n"""
    return rules + "\nPACKET=\n" + json.dumps(packet, indent=2, ensure_ascii=False, sort_keys=True)


def propose_delta(packet: Dict[str, Any], path: str, value: Any, reason: str) -> Dict[str, Any]:
    """Attach a non-authoritative candidate change to a display packet."""
    delta = {
        "path": path,
        "candidate_value": value,
        "reason": reason,
        "status": "PROPOSED",
        "canon_effect": "NONE",
    }
    packet.setdefault("proposed_deltas", []).append(delta)
    return packet
