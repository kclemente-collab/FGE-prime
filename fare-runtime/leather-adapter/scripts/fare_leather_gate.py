#!/usr/bin/env python3
"""FGE-ADP-LEATHER-FARE-001 — FARE A/R/E gate for leather DMIs."""
from __future__ import annotations
import json, sys
from typing import Any
HEART_HEX = "#4A2C11"
COLOR_SHIFT_CAP = 25.0
STRETCH_CAP = 1.45
UV2_GUTTER = 0.05

def fare_evaluate(color_shift_pct: float, uv2_drift: float, stretch_factor: float, heart_hex: str = HEART_HEX) -> dict[str, Any]:
    a_pass = color_shift_pct <= COLOR_SHIFT_CAP
    r_pass = uv2_drift <= UV2_GUTTER
    e_pass = stretch_factor <= STRETCH_CAP
    passed = a_pass and r_pass and e_pass
    return {
        "Evaluation_ID": "FARE-VAL-LEATHER-003",
        "Target_Heart_ID": "FGE-CHAR-HEART-002",
        "Pipeline_Action": {
            "Output_Gate": "VALIDATED_PASS" if passed else "FAILED",
            "Weight_Influence": "FARE.9",
            "Next_Kernel": "FGE: P=BUILD" if passed else "HALT_NOSILENT_DRIFT",
            "Rank_Delta": 0 if passed else -1,
            "Heart_Rewrite": False,
        },
        "observed": {"color_shift_pct": color_shift_pct, "uv2_drift": uv2_drift, "stretch_factor": stretch_factor},
        "heart_hex": heart_hex,
    }

if __name__ == "__main__":
    color = float(sys.argv[1]) if len(sys.argv) > 1 else 18.0
    uv2 = float(sys.argv[2]) if len(sys.argv) > 2 else 0.02
    stretch = float(sys.argv[3]) if len(sys.argv) > 3 else 1.35
    print(json.dumps(fare_evaluate(color, uv2, stretch), indent=2))
