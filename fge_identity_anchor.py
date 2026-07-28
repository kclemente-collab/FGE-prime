#!/usr/bin/env python3
"""
FGE IdentityAnchor v1.0 - Immutable Core Identity Contract
Part of CharacterOS / LedgerOS foundation for Feral Gloss Empire.

Provides:
- Frozen Pydantic model for tamper-evident character identity
- Context-aware serialization (buyer, prompt_foundry, internal)
- Cryptographic integrity via SHA256
- Factory for safe locked creation
- Supporting BuildGenome manufacturing recipe
- Exporter utilities

This module strengthens long-term canon consistency, enables clean commercial outputs,
and integrates with DOC BRAIN, master-anchor-builder, and executable Identity OS.
"""

from pydantic import BaseModel, Field, ConfigDict, SerializationInfo, field_serializer
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

class IdentityAnchor(BaseModel):
    """
    Immutable core identity of a character.
    Once created and locked via create_locked(), this model cannot be modified.
    Enforces cryptographic integrity and context-aware serialization for different consumers
    (internal governance, buyer packages, prompt engineering pipelines).
    """
    model_config = ConfigDict(
        frozen=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        json_encoders={datetime: lambda v: v.isoformat()}
    )

    # === Identification ===
    anchor_id: str = Field(..., description="e.g. ANCHOR-ISOLDE-NOIR-v1.0 or CSC-0001")
    version: str = Field(..., description="Semantic version of this anchor contract")
    character_name: str
    archetype: str

    # === Physical Core (Immutable Gospel Measurements) ===
    height_cm: float = Field(..., gt=0, description="Height in centimeters")
    body_measurements: Dict[str, float] = Field(
        ..., description="Core body metrics e.g. {'bust': 92.0, 'waist': 62.0, 'hips': 94.0}"
    )
    facial_features: Dict[str, float] = Field(
        ..., description="Anthropometric facial metrics from fge-facial-analysis or genome sheet"
    )
    skin_tone: str
    hair_color: str
    eye_color: str

    # === Signature (Non-Negotiable Canon) ===
    signature_material: str = Field(
        ..., description="Primary material doctrine: Obsidian, Kintsugi, Pearl, Dragon, etc."
    )
    signature_feature: str = Field(..., description="Defining visual, behavioral, or narrative signature")

    # === Behavioral ===
    behavioral_anchors: List[str] = Field(default_factory=list)
    vocal_style: Optional[str] = None

    # === Governance (Locked State) ===
    locked_at: datetime = Field(..., description="UTC timestamp when this anchor was locked")
    locked_by: str
    cryptographic_hash: str = Field(..., description="SHA256 integrity hash of core fields")
    canon_status: str = Field(default="LOCKED", description="LOCKED | DRAFT | DEPRECATED | RITUAL")

    # === Internal Only (Never exposed in exports) ===
    internal_notes: Optional[str] = Field(default=None, exclude=True)

    @field_serializer("*", when_used="json")
    def serialize_for_context(self, value: Any, info: SerializationInfo) -> Any:
        """Smart serialization that redacts or transforms fields based on consumer context."""
        context = info.context or {}
        field_name = info.field_name

        # Buyer-facing view: cleaner, redacted for commercial / investor deliverables
        if context.get("view") == "buyer":
            if field_name in {"cryptographic_hash", "internal_notes", "locked_by"}:
                return None
            if field_name == "locked_at" and isinstance(value, datetime):
                return value.strftime("%Y-%m-%d")

        # Prompt Foundry view: strict, minimal fields for generation pipelines
        if context.get("view") == "prompt_foundry":
            if field_name in {"internal_notes", "locked_by", "canon_status"}:
                return None
            # cryptographic_hash kept for traceability in foundry workflows

        return value

    def compute_hash(self) -> str:
        """
        Compute deterministic SHA256 hash over canonical core fields.
        Excludes governance and internal fields so hash remains stable across minor metadata changes.
        """
        data = self.model_dump(
            exclude={"cryptographic_hash", "locked_at", "internal_notes"},
            mode="json"
        )
        canonical_json = json.dumps(data, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()

    @classmethod
    def create_locked(
        cls,
        anchor_id: str,
        version: str,
        character_name: str,
        archetype: str,
        height_cm: float,
        body_measurements: Dict[str, float],
        facial_features: Dict[str, float],
        skin_tone: str,
        hair_color: str,
        eye_color: str,
        signature_material: str,
        signature_feature: str,
        locked_by: str,
        behavioral_anchors: Optional[List[str]] = None,
        vocal_style: Optional[str] = None,
        canon_status: str = "LOCKED",
        internal_notes: Optional[str] = None,
    ) -> "IdentityAnchor":
        """
        Factory method to safely create a locked IdentityAnchor.
        Handles timestamping, placeholder hash, then injects the real computed hash.
        This is the ONLY way to instantiate a production IdentityAnchor.
        """
        now = datetime.now(timezone.utc)

        # Create with placeholder hash (will be excluded from hash computation anyway)
        anchor = cls(
            anchor_id=anchor_id,
            version=version,
            character_name=character_name,
            archetype=archetype,
            height_cm=height_cm,
            body_measurements=body_measurements,
            facial_features=facial_features,
            skin_tone=skin_tone,
            hair_color=hair_color,
            eye_color=eye_color,
            signature_material=signature_material,
            signature_feature=signature_feature,
            behavioral_anchors=behavioral_anchors or [],
            vocal_style=vocal_style,
            locked_at=now,
            locked_by=locked_by,
            cryptographic_hash="PENDING-COMPUTATION",
            canon_status=canon_status,
            internal_notes=internal_notes,
        )

        # Compute the authoritative hash over the now-complete core data
        real_hash = anchor.compute_hash()

        # Return a new frozen instance with the correct hash injected
        return anchor.model_copy(update={"cryptographic_hash": real_hash})

    def verify_integrity(self) -> bool:
        """Runtime check: does the stored hash still match the computed hash of current fields?"""
        return self.cryptographic_hash == self.compute_hash()

    def to_ledger_entry(self) -> Dict[str, Any]:
        """Minimal projection suitable for LedgerOS ingestion."""
        return {
            "anchor_id": self.anchor_id,
            "version": self.version,
            "character_name": self.character_name,
            "locked_at": self.locked_at.isoformat(),
            "cryptographic_hash": self.cryptographic_hash,
            "canon_status": self.canon_status,
        }


class BuildGenome(BaseModel):
    """
    Temporary manufacturing recipe used during character assembly / gospel cycle progression.
    Feeds the engine (Atelier, RenderOS, matrix prompt engines) but is NOT part of the locked identity.
    """
    model_config = ConfigDict(validate_assignment=True)

    build_id: str
    targets: Dict[str, Any]                    # e.g. {"sex": "female", "age_appearance": 28, "body_archetype": "athletic-siren"}
    variation_rules: Dict[str, float]          # e.g. {"height_std": 2.5, "muscle_variance": 0.1}
    style_direction: Dict[str, float]          # e.g. {"luxury": 0.9, "editorial": 0.7, "cinematic": 0.8}

    # Optional manufacturing overrides
    forced_signature_material: Optional[str] = None
    additional_constraints: List[str] = Field(default_factory=list)

    # Metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str


class CharacterExporter:
    """Stateless utility for producing context-specific representations of anchors and genomes."""

    @staticmethod
    def to_internal(anchor: IdentityAnchor) -> dict:
        """Full internal representation for governance, LedgerOS, and DOC BRAIN."""
        return anchor.model_dump(mode="json")

    @staticmethod
    def to_buyer(anchor: IdentityAnchor) -> dict:
        """Clean, redacted view suitable for commercial packages, investor materials, and public-facing deliverables."""
        return anchor.model_dump(
            mode="json",
            context={"view": "buyer"},
            exclude={"internal_notes", "cryptographic_hash"}
        )

    @staticmethod
    def to_prompt_foundry(anchor: IdentityAnchor) -> dict:
        """Minimal, strict view optimized for prompt engineering, matrix engines, and RenderOS pipelines."""
        return anchor.model_dump(
            mode="json",
            context={"view": "prompt_foundry"}
        )

    @staticmethod
    def build_genome_to_yaml(genome: BuildGenome) -> str:
        """Human-readable recipe export for Atelier workflows or documentation."""
        import yaml
        return yaml.dump(genome.model_dump(mode="json"), sort_keys=False, allow_unicode=True)

    @staticmethod
    def anchor_to_json_file(anchor: IdentityAnchor, output_dir: Path, view: str = "internal") -> Path:
        """Persist a single anchor export to disk for durability and cross-tool use."""
        output_dir.mkdir(parents=True, exist_ok=True)
        safe_name = anchor.anchor_id.replace(":", "_").replace("/", "_")
        if view == "buyer":
            data = CharacterExporter.to_buyer(anchor)
            filename = f"{safe_name}_buyer.json"
        elif view == "prompt_foundry":
            data = CharacterExporter.to_prompt_foundry(anchor)
            filename = f"{safe_name}_prompt_foundry.json"
        else:
            data = CharacterExporter.to_internal(anchor)
            filename = f"{safe_name}_internal.json"

        filepath = output_dir / filename
        filepath.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return filepath


# =============================================================================
# Self-test / Example (run with: python fge_identity_anchor.py)
# =============================================================================
if __name__ == "__main__":
    import json as json_module

    print("=" * 70)
    print("FGE IdentityAnchor v1.0 - Self Test & Example")
    print("=" * 70)

    # 1. JSON Schema export (for documentation / validation in DOC BRAIN)
    print("\n[1] IdentityAnchor JSON Schema (for DOC BRAIN / validation)")
    anchor_schema = IdentityAnchor.model_json_schema()
    schema_path = Path("/home/workdir/artifacts/fge_identity_anchor_schema.json")
    schema_path.write_text(json_module.dumps(anchor_schema, indent=2), encoding="utf-8")
    print(f"   Schema written to: {schema_path}")

    # 2. Create a production-grade locked anchor (Isolde Noir example aligned with Isolde Voss CSC-0001)
    print("\n[2] Creating locked IdentityAnchor via factory...")
    anchor = IdentityAnchor.create_locked(
        anchor_id="ANCHOR-ISOLDE-NOIR-v1.0",
        version="1.0",
        character_name="Isolde Noir",
        archetype="Shadow Sovereign",
        height_cm=172.0,
        body_measurements={"bust": 92.0, "waist": 62.0, "hips": 94.0},
        facial_features={"eye_distance": 32.4, "jaw_width": 11.8, "cheekbone_height": 48.2},
        skin_tone="Porcelain - Night Tone",
        hair_color="Obsidian Black",
        eye_color="Aurora Green",
        signature_material="Obsidian",
        signature_feature="Cracked Kintsugi patterns on skin with ritual fracture lines",
        locked_by="Keith Clemente",
        behavioral_anchors=["Composed", "Strategic", "Predatory grace", "Ritual precision"],
        vocal_style="Low, measured, with velvet edge",
        internal_notes="Level 0 Gospel Anchor candidate. Cross-reference with CSC-0001 Isolde Voss crystal seed.",
    )

    print(f"   Created: {anchor.anchor_id}")
    print(f"   Integrity verified: {anchor.verify_integrity()}")
    print(f"   Locked at (UTC): {anchor.locked_at.isoformat()}")
    print(f"   Hash (first 16): {anchor.cryptographic_hash[:16]}...")

    # 3. Demonstrate the three canonical views
    print("\n[3] Export Views")

    print("\n   --- INTERNAL (governance / LedgerOS / DOC BRAIN) ---")
    internal = CharacterExporter.to_internal(anchor)
    print(json_module.dumps(internal, indent=2)[:800] + "\n   ... (truncated)")

    print("\n   --- BUYER (commercial packages, investor materials) ---")
    buyer = CharacterExporter.to_buyer(anchor)
    print(json_module.dumps(buyer, indent=2))

    print("\n   --- PROMPT FOUNDRY (RenderOS, matrix engines, Atelier) ---")
    foundry = CharacterExporter.to_prompt_foundry(anchor)
    print(json_module.dumps(foundry, indent=2))

    # 4. Persist examples to disk
    print("\n[4] Persisting exports to artifacts/...")
    out_dir = Path("/home/workdir/artifacts/fge_identity_anchors")
    p_internal = CharacterExporter.anchor_to_json_file(anchor, out_dir, "internal")
    p_buyer = CharacterExporter.anchor_to_json_file(anchor, out_dir, "buyer")
    p_foundry = CharacterExporter.anchor_to_json_file(anchor, out_dir, "prompt_foundry")
    print(f"   Internal:      {p_internal}")
    print(f"   Buyer:         {p_buyer}")
    print(f"   Prompt Foundry:{p_foundry}")

    # 5. BuildGenome example
    print("\n[5] BuildGenome example (manufacturing recipe)")
    genome = BuildGenome(
        build_id="BUILD-ISOLDE-NOIR-2026-07-15",
        targets={"sex": "female", "age_appearance": 27, "body_archetype": "athletic-siren", "height_target_cm": 172.0},
        variation_rules={"height_std": 1.8, "bust_variance": 1.5, "waist_tightness": 0.8},
        style_direction={"luxury": 0.95, "editorial": 0.75, "cinematic_tenebrism": 0.9, "kintsugi_ritual": 1.0},
        created_by="Keith Clemente"
    )
    print(CharacterExporter.build_genome_to_yaml(genome))

    print("\n" + "=" * 70)
    print("Self-test complete. Module is ready for integration into CharacterOS / fge-character-ledger-atelier.")
    print("=" * 70)
