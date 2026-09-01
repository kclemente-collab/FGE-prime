# FGE-ADP-LEATHER-FARE-001

Leather Matrix adapter for FARE Runtime.

- Matrix: FGE-MAT-LEATHER-FARE-001
- Status: IMPLEMENTED
- Canon effect: NONE
- Parent runtime: FGE-FARE-001 (fare-runtime/)

Loop: TOKEN → HEART fingerprint → BRAIN delta → FARE A/R/E → DMI packet

Locked invariants: PoreFrequency 4.0, MaxStretch 1.45, Heart hex #4A2C11, UV2 overlays, HEX-anchored token parse, no Horizontal Blend delete, no silent Heart rewrite.

Scripts:
- scripts/compile_fge_leather_token.py
- scripts/fare_leather_gate.py
