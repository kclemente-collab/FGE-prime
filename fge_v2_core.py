import json
import re
from typing import List, Dict, Optional
from pydantic import BaseModel, Field, field_validator
from fastapi import FastAPI, HTTPException

# ==========================================
# 1. STANDARDIZED DATA MODELS (SCHEMA)
# ==========================================
class MaterialMatrix(BaseModel):
    primary: str
    secondary: Optional[str] = None
    trim: Optional[str] = None

class PaletteEngine(BaseModel):
    dominant: str
    secondary: Optional[str] = None
    accent: str

    @field_validator('dominant', 'secondary', 'accent')
    @classmethod
    def validate_color_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if v.startswith("#") and not re.match(r"^#[0-9a-fA-F]{6}$", v):
            raise ValueError(f"Invalid Hex color code format: {v}")
        return v

class SubSurfaceCyberware(BaseModel):
    """The brand new Layer Type: Internal Technical Embellishments"""
    node_id: str = Field(..., description="Unique anatomical sub-surface node ID")
    luminescence: bool = Field(False, description="Sub-dermal glowing state")
    circuit_material: str = Field(..., description="e.g., Liquid Gold, Graphene Threads")
    cooling_type: str = Field("Passive", description="e.g., Cryo-fluid, Heat Sink")

class FashModuleInbound(BaseModel):
    character_id: str
    archetype: str
    silhouette: str
    
    # Structural Layer Stack (Updated with Sub-Surface layer)
    sub_surface_cyberware: List[SubSurfaceCyberware] = Field(default_factory.list)
