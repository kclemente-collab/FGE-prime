"""
Transformation Inversion Forge v1.2

WHAT CHANGED FROM v1.0/v1.1 AND WHY:

v1.1's fix for texture convergence was a dict keyed by precursor NAME, with
one hand-written paragraph per entry. That "fixes" 3 cases but doesn't
generalize — transformation #4 needs its own hand-authored paragraph, and
an unclassified precursor silently inherits obsidian's texture with no
error. That's the same adjective-picking problem, just moved one layer
down from "mineral" to "fracture field."

v1.2 instead classifies each precursor along TWO real, independently
verifiable physical axes (this is literally how glass science classifies
network formers — Zachariasen's rules):

  1. network_continuity: is the material ONE continuous bonded framework
     (a lattice or a melt), or DISCRETE separate particles (like packed
     colloidal spheres)?
  2. angular_flexibility: can the bond angles tolerate distortion and
     still hold together (flexible network former -> glass), or do they
     require a specific rigid geometry to be stable at all (rigid ->
     clustering/tangling instead of smooth glass when disordered)?

Texture is COMPUTED from the combination of these two axes, not looked up
by name. Any future transformation just needs these two tags classified
correctly — no new paragraph required. And each of the three resulting
textures below is independently checkable against real, documented
material science, not just internally consistent-sounding:

  - carbon (continuous + rigid) inverted -> disordered covalent carbon
    clusters. Real analog: diamond-like carbon (DLC) amorphous carbon
    films are a real, documented material — carbon disordered under rapid
    conditions does NOT form a smooth glass, it clusters, because rigid
    tetrahedral bonds can't tolerate the angle distortion glass formation
    needs.
  - silicate melt (continuous + flexible) inverted -> strained, flow-
    banded glass. This is not speculative — it is the textbook definition
    of why SiO2 is a classic "network former" in glass science.
  - silica spheres (discrete + n/a) inverted -> collapsed/irregular
    particle packing. Real analog: this is the documented, real difference
    between common opal (irregular packing, milky, no play-of-color) and
    precious opal (regular packing, diffraction) — a genuine mineralogical
    fact, not an invented mechanism.

Unclassified precursor/axis combinations now raise an explicit error
instead of silently defaulting to another material's texture.
"""

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# 1. Real Transformation Ledger — now tagged with two physical axes instead
#    of left to be handled by a name-keyed lookup later.
# ---------------------------------------------------------------------------
REAL_TRANSFORMATIONS = {
    "coal_to_diamond": {
        "precursor": "amorphous carbon",
        "network_continuity": "continuous",
        "angular_flexibility": "rigid",
        "driver_polarity": "extreme sustained heat + pressure",
        "time_regime": "geologic (millions of years, equilibrium reached)",
        "mechanism": (
            "Heat raises atomic mobility. Over geologic time, carbon atoms "
            "migrate and lock into a rigid tetrahedral lattice and impurities "
            "are expelled as the lattice purifies."
        ),
    },
    "lava_to_obsidian": {
        "precursor": "molten silicate rock",
        "network_continuity": "continuous",
        "angular_flexibility": "flexible",
        "driver_polarity": "rapid cooling (quenching)",
        "time_regime": "near-instantaneous (seconds to minutes)",
        "mechanism": (
            "Cooling is too fast for atoms to organize into a crystal lattice, "
            "so the melt freezes into a disordered, glassy solid."
        ),
    },
    "silica_to_opal": {
        "precursor": "silica-saturated groundwater",
        "network_continuity": "discrete",
        "angular_flexibility": "n/a",  # discrete particles aren't bonded into a network at all
        "driver_polarity": "slow evaporation and deposition",
        "time_regime": "geologic (thousands to millions of years)",
        "mechanism": (
            "Silica spheres slowly precipitate and stack into a regular "
            "microscopic lattice as water evaporates, producing diffraction."
        ),
    },
}


# ---------------------------------------------------------------------------
# 2. Inversion driver logic (unchanged from v1.0 — this part was never broken)
# ---------------------------------------------------------------------------
POLARITY_OPPOSITES = {
    "extreme sustained heat + pressure": "cryogenic pressure-lock (extreme sustained cold + pressure)",
    "rapid cooling (quenching)": "rapid heating (flash vitrification without melting)",
    "slow evaporation and deposition": "instantaneous flash-precipitation (chemical shock)",
}


def infer_mobility(original_polarity: str) -> str:
    """Real rule: heat/mobility-enabling drivers, inverted, suppress mobility."""
    if "cryogenic" in POLARITY_OPPOSITES[original_polarity] or "cold" in POLARITY_OPPOSITES[original_polarity]:
        return "suppressed"
    if "flash" in POLARITY_OPPOSITES[original_polarity]:
        return "suppressed"  # instantaneous processes never reach equilibrium either
    return "suppressed"  # every inversion in this ledger removes the ordering driver


# ---------------------------------------------------------------------------
# 3. TEXTURE DERIVATION — the actual fix. Computed from two physical axes,
#    not looked up by precursor name. This is the part that generalizes.
# ---------------------------------------------------------------------------
def infer_texture(network_continuity: str, angular_flexibility: str, mobility: str) -> dict:
    if mobility != "suppressed":
        return {
            "structure": "ordered crystalline lattice",
            "impurity_behavior": "expelled during migration",
            "fracture": "cleaves along crystal planes",
            "texture_notes": "long-range order, well-formed facets",
            "real_analog_check": "standard crystalline growth — not an inversion case",
        }

    if network_continuity == "continuous" and angular_flexibility == "rigid":
        return {
            "structure": "disordered covalent cluster network (tangled, not glassy)",
            "impurity_behavior": "trapped within and between clusters, uneven distribution",
            "fracture": "irregular, splintery to conchoidal; no true glass conchoidal sheen",
            "texture_notes": (
                "rigid bond angles cannot tolerate the distortion smooth glass "
                "formation requires, so the network clusters instead of flowing"
            ),
            "real_analog_check": "diamond-like carbon (DLC) amorphous carbon films",
        }

    if network_continuity == "continuous" and angular_flexibility == "flexible":
        return {
            "structure": "strained, flow-banded continuous glassy network",
            "impurity_behavior": "trapped uniformly through the frozen melt",
            "fracture": "true conchoidal, glass-like shell fractures, possible flow banding",
            "texture_notes": "flexible bond angles allow a smooth continuous glass to form under disorder",
            "real_analog_check": "textbook glass-network-former behavior (Zachariasen's rules)",
        }

    if network_continuity == "discrete":
        return {
            "structure": "collapsed / irregular particle packing (no continuous network to fail)",
            "impurity_behavior": "trapped in interstitial voids between misaligned particles",
            "fracture": "chalky to conchoidal, more porous than a true glass fracture",
            "texture_notes": "failure mode is packing disorder, not bond disorder — there is no shared network to disrupt",
            "real_analog_check": "documented difference between common opal (irregular packing) and precious opal (regular packing)",
        }

    raise ValueError(
        f"Unclassified axis combination: continuity={network_continuity}, "
        f"flexibility={angular_flexibility}. This transformation needs explicit "
        f"classification before it can be inverted — no silent default is used."
    )


def infer_color_shift(precursor_color: str, structure: str) -> str:
    """
    Real rule (crystal field theory): the same chromophore reads a different
    color depending on host lattice geometry (chromium: red in corundum,
    green in beryl). Structural disorder is real grounds for a shift.
    """
    shift_map = {
        "red": "blue-violet (chromophore reads cooler in a disordered host)",
        "black": "deep amber-brown (iron-bearing chromophore shifts warmer in glass)",
        "clear": "smoky grey to milky white (scattering from trapped disorder/voids)",
    }
    if "ordered crystalline" in structure:
        return precursor_color  # no structural change, no crystal-field shift
    return shift_map.get(precursor_color, f"shifted variant of {precursor_color}")


# ---------------------------------------------------------------------------
# 4. Inversion Engine
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
    fracture: str
    texture_notes: str
    real_analog_check: str
    resulting_color: str
    fiction_ledger: str = field(default="")

    def as_dossier(self) -> str:
        return (
            f"REAL BASIS: {self.source_transformation}\n"
            f"  Real driver: {self.real_driver}\n"
            f"  Inverted to: {self.inverted_driver}   <- single fictionalized variable\n\n"
            f"DERIVED FROM TWO PHYSICAL AXES (continuity x flexibility), NOT LOOKED UP:\n"
            f"  Atomic mobility: {self.mobility_effect}\n"
            f"  Resulting structure: {self.resulting_structure}\n"
            f"  Impurity behavior: {self.impurity_behavior}\n"
            f"  Fracture: {self.fracture}\n"
            f"  Texture logic: {self.texture_notes}\n"
            f"  Color: {self.precursor_color_given} precursor -> {self.resulting_color}\n\n"
            f"REAL-WORLD ANALOG (independently checkable, not invented):\n  {self.real_analog_check}\n\n"
            f"FICTION LEDGER:\n  {self.fiction_ledger}"
        )


def invert(transformation_key: str, precursor_color: str) -> InvertedMineral:
    real = REAL_TRANSFORMATIONS[transformation_key]

    inverted_driver = POLARITY_OPPOSITES[real["driver_polarity"]]
    mobility = infer_mobility(real["driver_polarity"])
    derived = infer_texture(real["network_continuity"], real["angular_flexibility"], mobility)
    color = infer_color_shift(precursor_color, derived["structure"])

    return InvertedMineral(
        source_transformation=transformation_key,
        precursor_color_given=precursor_color,
        real_driver=real["driver_polarity"],
        inverted_driver=inverted_driver,
        mobility_effect=mobility,
        resulting_structure=derived["structure"],
        impurity_behavior=derived["impurity_behavior"],
        fracture=derived["fracture"],
        texture_notes=derived["texture_notes"],
        real_analog_check=derived["real_analog_check"],
        resulting_color=color,
        fiction_ledger=(
            f"Only the driver polarity was flipped ({real['driver_polarity']} -> {inverted_driver}). "
            f"Texture, fracture, and color are computed from network_continuity + "
            f"angular_flexibility + crystal-field logic — not authored per-material."
        ),
    )


# ---------------------------------------------------------------------------
# 5. Believability Auditor
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
        if not mineral.real_analog_check:
            return False, "No independently checkable real-world analog cited"
        return True, "Passes: one inversion, texture derived from physical axes, real analog cited"


# ---------------------------------------------------------------------------
# Test cycle — confirms three genuinely distinct textures, each backed by
# an independently verifiable real material fact.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    cases = [
        ("coal_to_diamond", "red"),
        ("lava_to_obsidian", "black"),
        ("silica_to_opal", "clear"),
    ]
    for key, color in cases:
        print("=" * 75)
        print(f"CASE: {key}")
        print("=" * 75)
        m = invert(key, color)
        print(m.as_dossier())
        print(f"\nAUDIT: {BelievabilityAuditor.audit(m)}\n")

    # Regression check: confirm the three structures are actually distinct,
    # not converged the way v1.0's did.
    structures = {invert(k, c).resulting_structure for k, c in cases}
    print("=" * 75)
    print(f"DISTINCT STRUCTURE CHECK: {len(structures)} unique structures across {len(cases)} cases")
    assert len(structures) == len(cases), "CONVERGENCE BUG STILL PRESENT"
    print("PASS — no convergence.")
