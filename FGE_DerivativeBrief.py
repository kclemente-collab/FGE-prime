from pydantic import BaseModel
from typing import List, Literal, Optional
from datetime import datetime

class DerivativeTarget(BaseModel):
    """Defines a single derivative output format with layout and priority."""
    format: str  # e.g. "POSTER", "4_CARD_SET", "MOBILE_CARD", "SLIDE"
    layout: str  # e.g. "FGE_DOCKET_VERTICAL", "FGE_CARD_GRID", "COMPACT_VERTICAL", "WIDE_HORIZONTAL"
    priority: Literal["HIGH", "MEDIUM", "LOW"]
    notes: Optional[str] = None

class FGE_DerivativeBrief(BaseModel):
    """
    FGE Derivative Brief — Structured directive for generating collector-grade
    derivative assets from a parent talisman or control board asset.
    
    Enforces canon compliance through required_modules and registry_link.
    Supports multi-format production pipelines aligned with FGE Constitution.
    """
    parent_asset_id: str = "FGE-TALISMAN-CONTROL-BOARD-001"
    derivative_family_id: str = "FGE-FAMILY-TALISMAN-CONTROL-001"
    purpose: str = "collector display + operational monitoring"
    audience: str = "premium collector + character designers"
    output_targets: List[DerivativeTarget] = [
        DerivativeTarget(format="POSTER", layout="FGE_DOCKET_VERTICAL", priority="HIGH"),
        DerivativeTarget(format="4_CARD_SET", layout="FGE_CARD_GRID", priority="HIGH"),
        DerivativeTarget(format="MOBILE_CARD", layout="COMPACT_VERTICAL", priority="MEDIUM"),
        DerivativeTarget(format="SLIDE", layout="WIDE_HORIZONTAL", priority="LOW")
    ]
    required_modules: List[str] = [
        "identity", "lineage", "runtime_hooks", "body_lock", 
        "facial_anchor", "value_scores", "talisman_skin"
    ]
    registry_link: bool = True
    created_at: datetime = datetime.utcnow()
    version: str = "1.0"
    notes: Optional[str] = "Auto-generated from FGE Constitution Production Layer ingestion. Enforces provenance and module compliance for all talisman-family derivatives."

# Example instantiation helper
def create_talisman_control_board_brief() -> FGE_DerivativeBrief:
    """Factory for the primary Talisman Control Board derivative brief."""
    return FGE_DerivativeBrief(
        parent_asset_id="FGE-TALISMAN-CONTROL-BOARD-001",
        derivative_family_id="FGE-FAMILY-TALISMAN-CONTROL-001",
        purpose="collector display + operational monitoring of talisman states and lineage hooks",
        audience="premium collector + character designers + runtime operators"
    )
