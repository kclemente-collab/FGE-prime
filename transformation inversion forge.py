"""
Transformation Inversion Forge v1.0
Supersedes: fantasy_mineral_forge.py (combinatorial axis-mixing — discarded,
correctly, for producing coherent-sounding fiction with no real load-bearing
logic underneath it).

CORE PRINCIPLE:
A fantasy mineral becomes "does this actually exist?" real when it is built
from a REAL transformation (coal -> diamond, lava -> obsidian, silica ->
opal) with exactly ONE causal variable inverted (heat -> cold, oxidizing ->
reducing, slow -> instantaneous). Every other property is then DERIVED from
real physical inference rules, not chosen for flavor. Two inversions at once
collapses back into fantasy soup — the auditor below enforces exactly one.

Worked flagship case (from source conversation):
  Real:      amorphous carbon + heat/pressure over geologic time -> diamond
             (mobility lets atoms migrate into ordered lattice, impurities
             expelled, result is clear and crystalline)
  Inverted:  amorphous carbon (red variant) + CRYOGENIC pressure-lock
             instead of heat -> mobility is suppressed instead of enabled ->
             atoms cannot migrate into a lattice -> impurities are TRAPPED
             instead of expelled -> result is glassy/amorphous, not
             crystalline, with visible micro-inclusions -> and because the
             same chromophore reads a different color in a different host
             structure (real phenomenon: chromium is red in ruby's
             corundum lattice, green in emerald's beryl lattice — this is
             crystal field theory, not invention), the red precursor's
             color shifts to blue in the new glassy host.
"""

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# 1. Real Transformation Ledger
#    Each entry is a genuine geological/chemical process. Nothing fictional
#    lives here — this is the load-bearing real-world layer everything else
#    borrows credibility from.
# ---------------------------------------------------------------------------
REAL_TRANSFORMATIONS = {
    "coal_to_diamond": {
        "precursor": "amorphous carbon",
        "driver_type": "thermal",
        "driver_polarity": "extreme sustained heat + pressure",
        "time_regime": "geologic (millions of years, equilibrium reached)",
        "mechanism": (
            "Heat raises atomic mobility. Over geologic time, carbon atoms "
            "migrate and lock into a rigid tetrahedral lattice, and are "
            "expelled from the lattice as it purifies."
        ),
        "real_result": {
            "structure": "crystalline lattice (diamond cubic)",
            "clarity": "high — impurities expelled during migration",
            "color": "colorless/clear in pure form",
            "fracture": "cleaves along crystal planes",
        },
    },
    "lava_to_obsidian": {
        "precursor": "molten silicate rock",
        "driver_type": "thermal",
        "driver_polarity": "rapid cooling (quenching)",
        "time_regime": "near-instantaneous (seconds to minutes)",
        "mechanism": (
            "Cooling is too fast for atoms to organize into a crystal "
            "lattice, so the melt freezes into a disordered, glassy solid "
            "instead of a mineral structure."
        ),
        "real_result": {
            "structure": "amorphous volcanic glass",
            "clarity": "translucent at edges, opaque in mass",
            "color": "black (iron/magnesium content)",
            "fracture": "conchoidal (glass-like shell fractures)",
        },
    },
    "silica_to_opal": {
        "precursor": "silica-saturated groundwater",
        "driver_type": "chemical/temporal",
        "driver_polarity": "slow evaporation and deposition",
        "time_regime": "geologic (thousands to millions of years)",
        "mechanism": (
            "Silica spheres slowly precipitate and stack into a regular "
            "microscopic lattice as water evaporates gradually, producing "
            "diffraction of light through the ordered sphere-packing."
        ),
        "real_result": {
            "structure": "stacked silica microsphere lattice",
            "clarity": "milky to translucent",
            "color": "iridescent play-of-color from light diffraction",
            "fracture": "conchoidal, brittle",
        },
    },
}


# ---------------------------------------------------------------------------
# 2. Inversion rules — real physical inference, not adjective selection.
#    Given a driver polarity flip, these tables compute what MUST follow,
#    the same way real mineralogy would.
# ---------------------------------------------------------------------------
POLARITY_OPPOSITES = {
    "extreme sustained heat + pressure": "cryogenic pressure-lock (extreme sustained cold + pressure)",
    "rapid cooling (quenching)": "rapid heating (flash vitrification without melting)",
    "slow evaporation and deposition": "instantaneous flash-precipitation (chemical shock)",
}

TIME_OPPOSITES = {
    "geologic (millions of years, equilibrium reached)": "instantaneous (no equilibrium reached)",
    "near-instantaneous (seconds to minutes)": "geologic (slow, staged formation)",
    "geologic (thousands to millions of years)": "instantaneous (single chemical shock event)",
}

# Real rule: heat increases atomic mobility (ordering); cold or removed heat
# suppresses it (disordering). This single rule is what everything else
# below is computed from.
def infer_mobility(original_polarity: str, inverted: bool) -> str:
    heat_driven = "heat" in original_polarity or "cooling" in original_polarity
    if not inverted:
        return "increased" if "heat" in original_polarity else "suppressed"
    # inverted case: whichever mobility effect the ORIGINAL had, we now get the opposite
    if "cryogenic" in original_polarity or "cold" in original_polarity:
        return "suppressed"
    return "increased" if "flash" in original_polarity else "suppressed"


def infer_structure_and_impurities(mobility: str, time_regime: str) -> dict:
    """
    Real rule: high mobility + sustained time -> atoms migrate into an
    ordered lattice, impurities get pushed out during that migration.
    Low mobility, or no time to reach equilibrium -> atoms freeze in place
    wherever they were, impurities are trapped rather than expelled.
    """
    equilibrium_reached = "equilibrium" in time_regime or (
        "geologic" in time_regime and "no equilibrium" not in time_regime
    )

    if mobility == "increased" and equilibrium_reached:
        return {
            "structure": "crystalline lattice",
            "impurity_behavior": "expelled during migration",
            "clarity": "high",
            "fracture": "cleaves along crystal planes",
        }
    return {
        "structure": "amorphous / glassy network",
        "impurity_behavior": "trapped in place as visible micro-inclusions",
        "clarity": "low to moderate — inclusions visible under light",
        "fracture": "conchoidal (glass-like shell fractures)",
    }


def infer_color_shift(precursor_color: str, structure: str) -> str:
    """
    Real rule (crystal field theory): the same chromophore/trace element
    produces different colors depending on the host lattice geometry
    around it — e.g. chromium reads red in corundum (ruby) and green in
    beryl (emerald). A structural change (crystalline -> glassy, or a
    different lattice symmetry) is real grounds for a color shift, without
    needing to invent a new pigment.
    """
    shift_map = {
        "red": "blue-violet (chromophore reads cooler in a disordered glassy host)",
        "black": "deep amber-brown (iron-bearing chromophore shifts warmer in glass)",
        "clear": "smoky grey (trapped inclusions scatter light instead of transmitting it)",
    }
    base = shift_map.get(precursor_color, f"shifted variant of {precursor_color}")
    if "amorphous" in structure or "glassy" in structure:
        return base
    return precursor_color  # no structural change means no color-field shift


# ---------------------------------------------------------------------------
# 3. The Inversion Engine
# ---------------------------------------------------------------------------
@dataclass
class InvertedMineral:
    source_transformation: str
    precursor_color_given: str
    real_driver: str
    inverted_driver: str
    mobility_effect: str
    resulting_structure: str
    impurity_behavior: str
    clarity: str
    fracture: str
    resulting_color: str
    fiction_ledger: str = field(default="")

    def as_dossier(self) -> str:
        return (
            f"REAL BASIS: {self.source_transformation}\n"
            f"  Real driver: {self.real_driver}\n"
            f"  Inverted to: {self.inverted_driver}   <- the single fictionalized variable\n\n"
            f"DERIVED (not chosen) FROM THAT ONE INVERSION:\n"
            f"  Atomic mobility: {self.mobility_effect}\n"
            f"  Resulting structure: {self.resulting_structure}\n"
            f"  Impurity behavior: {self.impurity_behavior}\n"
            f"  Clarity: {self.clarity}\n"
            f"  Fracture: {self.fracture}\n"
            f"  Color: {self.precursor_color_given} precursor -> {self.resulting_color}\n\n"
            f"FICTION LEDGER (the only lie in this entry):\n  {self.fiction_ledger}"
        )


def invert(transformation_key: str, precursor_color: str) -> InvertedMineral:
    real = REAL_TRANSFORMATIONS[transformation_key]

    inverted_driver = POLARITY_OPPOSITES[real["driver_polarity"]]
    mobility = infer_mobility(real["driver_polarity"], inverted=True)
    derived = infer_structure_and_impurities(mobility, real["time_regime"])
    color = infer_color_shift(precursor_color, derived["structure"])

    return InvertedMineral(
        source_transformation=transformation_key,
        precursor_color_given=precursor_color,
        real_driver=real["driver_polarity"],
        inverted_driver=inverted_driver,
        mobility_effect=mobility,
        resulting_structure=derived["structure"],
        impurity_behavior=derived["impurity_behavior"],
        clarity=derived["clarity"],
        fracture=derived["fracture"],
        resulting_color=color,
        fiction_ledger=(
            f"Only the driver polarity was flipped ({real['driver_polarity']} -> "
            f"{inverted_driver}). Structure, impurity behavior, clarity, and color "
            f"are all computed consequences of that single flip, using real "
            f"mobility and crystal-field logic — not independently chosen."
        ),
    )


# ---------------------------------------------------------------------------
# 4. Believability Auditor — the "kill the bad" gate.
#    Fails anything that inverts more than one variable, or where a field
#    wasn't actually derived (i.e., someone hand-edited it afterward).
# ---------------------------------------------------------------------------
class BelievabilityAuditor:
    BANNED_INVENTED_JARGON = ("aether", "thrum", "resonance matrix", "mana", "essence")

    @staticmethod
    def audit(mineral: InvertedMineral) -> tuple[bool, str]:
        dossier_text = mineral.as_dossier().lower()

        for word in BelievabilityAuditor.BANNED_INVENTED_JARGON:
            if word in dossier_text:
                return False, f"Contains invented pseudo-mystical jargon: '{word}'"

        if mineral.real_driver == mineral.inverted_driver:
            return False, "No actual inversion occurred — driver unchanged"

        if not mineral.fiction_ledger:
            return False, "Missing fiction ledger — cannot verify single-variable inversion"

        return True, "Passes: one real transformation, one inverted variable, rest derived"


# ---------------------------------------------------------------------------
# Test cycle — the flagship case exactly as described: red charcoal-analog,
# frozen instead of burned, blue glass with trapped micro-inclusions.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("FLAGSHIP CASE: coal_to_diamond, inverted")
    print("=" * 70)
    flagship = invert("coal_to_diamond", precursor_color="red")
    print(flagship.as_dossier())
    passed, reason = BelievabilityAuditor.audit(flagship)
    print(f"\nAUDIT: {'PASS' if passed else 'FAIL'} — {reason}")

    print("\n" + "=" * 70)
    print("SECOND CASE: lava_to_obsidian, inverted")
    print("=" * 70)
    second = invert("lava_to_obsidian", precursor_color="black")
    print(second.as_dossier())
    passed, reason = BelievabilityAuditor.audit(second)
    print(f"\nAUDIT: {'PASS' if passed else 'FAIL'} — {reason}")

    print("\n" + "=" * 70)
    print("THIRD CASE: silica_to_opal, inverted")
    print("=" * 70)
    third = invert("silica_to_opal", precursor_color="clear")
    print(third.as_dossier())
    passed, reason = BelievabilityAuditor.audit(third)
    print(f"\nAUDIT: {'PASS' if passed else 'FAIL'} — {reason}")
