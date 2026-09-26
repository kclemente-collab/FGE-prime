"""JSON Schema validation at Modular Fashion OS authority boundaries."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

from jsonschema import Draft202012Validator, FormatChecker


PACKAGE_ROOT = Path(__file__).resolve().parent
ENVELOPE_SCHEMA = PACKAGE_ROOT / "contracts" / "fashion_asset_envelope.schema.json"
CHARACTER_PROJECTION_SCHEMA = (
    PACKAGE_ROOT / "contracts" / "character_chip_fashion_projection.schema.json"
)


class ContractValidationError(ValueError):
    """Raised when a payload fails its declared JSON Schema contract."""


@lru_cache(maxsize=None)
def _validator(schema_path: str) -> Draft202012Validator:
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate_json_contract(instance: Dict[str, Any], schema_path: Path) -> None:
    """Validate an object and report every discovered contract violation."""
    errors = sorted(
        _validator(str(schema_path)).iter_errors(instance),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    if not errors:
        return
    details = []
    for error in errors:
        path = ".".join(str(part) for part in error.absolute_path) or "$"
        details.append(f"{path}: {error.message}")
    raise ContractValidationError("Contract validation failed: " + "; ".join(details))


def validate_envelope(envelope: Dict[str, Any]) -> None:
    validate_json_contract(envelope, ENVELOPE_SCHEMA)


def validate_character_projection(projection: Dict[str, Any]) -> None:
    validate_json_contract(projection, CHARACTER_PROJECTION_SCHEMA)
