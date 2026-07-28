#!/usr/bin/env python3
"""
FGE OS Health Monitor v0.2 — Prompt + Ledger + MavenOS
Chief Executive Apprentice — Executable Integration Model

Extends v0.1 (PromptLedgerHealthMonitor) with MavenOS as the commercial translation layer.

This model now represents the core three-layer spine:
  Prompt OS (governed creation) → Ledger OS (persistent state) → MavenOS (market translation)

Key additions in v0.2:
- Generalized to accept any number of OS modules (easy extension to RenderOS, DOC BRAIN, etc.)
- MavenOS-specific analysis: translation readiness, commercial potential scoring
- Simulated handoff quality check between Ledger → MavenOS
- Stub for what MavenOS would produce (positioning, packaging directives, buyer assets)
- Same clean JSON + executive text output formats for Notion / pipeline use

This is the validated integration prototype. Run it, review the MavenOS section,
then feed real post-gospel-cycle snapshots to test the handoff logic.
"""

import json
import sys
from datetime import datetime, timezone
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any, Optional

# =============================================================================
# DATA MODEL
# =============================================================================

@dataclass
class SystemStatus:
    name: str
    status: str
    type: str
    last_activity: str
    health: int
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# =============================================================================
# FGE OS HEALTH MONITOR v0.2
# =============================================================================

class FGEOSHealthMonitor:
    """
    Unified executable monitor for the FGE core OS layers.

    v0.2 adds MavenOS integration analysis on top of the Prompt + Ledger foundation.
    Designed to surface integration health, handoff readiness, and commercial translation risk.
    """

    def __init__(self, raw_systems: List[Dict[str, Any]]):
        self.raw_input = raw_systems
        self.systems: List[SystemStatus] = [SystemStatus(**s) for s in raw_systems]
        self.generated_at = datetime.now(timezone.utc)
        self.target_health = 92

    # -------------------------------------------------------------------------
    # SCORING (reused from v0.1, slightly tuned)
    # -------------------------------------------------------------------------

    def _compute_recency_score(self, last_activity: str) -> float:
        try:
            dt_str = last_activity.replace('Z', '+00:00')
            last_dt = datetime.fromisoformat(dt_str)
            if last_dt.tzinfo is None:
                last_dt = last_dt.replace(tzinfo=timezone.utc)
            delta_seconds = (self.generated_at - last_dt).total_seconds()
            days_ago = max(0.0, delta_seconds / 86400.0)
            score = 100.0 - (days_ago * 9.5)
            return max(0.0, min(100.0, score))
        except Exception:
            return 55.0

    def _calculate_adjusted_health(self, base_health: int, recency: float) -> int:
        blended = (0.65 * base_health) + (0.35 * recency)
        return int(round(max(0, min(100, blended))))

    # -------------------------------------------------------------------------
    # MAVENOS-SPECIFIC INTEGRATION LOGIC
    # -------------------------------------------------------------------------

    def _get_module(self, name: str) -> Optional[Dict[str, Any]]:
        for m in self._raw_analyze_modules():
            if m["name"] == name:
                return m
        return None

    def _raw_analyze_modules(self) -> List[Dict[str, Any]]:
        """Internal helper to get base module reports without full orchestration."""
        modules = []
        for sys in self.systems:
            recency = self._compute_recency_score(sys.last_activity)
            adjusted = self._calculate_adjusted_health(sys.health, recency)
            modules.append({
                "name": sys.name,
                "type": sys.type,
                "status": sys.status,
                "base_health": sys.health,
                "recency_score": round(recency, 1),
                "adjusted_health": adjusted,
                "days_since_activity": round(
                    (self.generated_at - datetime.fromisoformat(
                        sys.last_activity.replace('Z', '+00:00')
                    ).replace(tzinfo=timezone.utc)).total_seconds() / 86400.0, 2
                ) if sys.last_activity else None
            })
        return modules

    def _compute_mavenos_integration(self, modules: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        MavenOS integration analysis.
        This is the core new logic for v0.2 — evaluates how ready the upstream
        (Prompt + Ledger) is to feed commercial translation.
        """
        prompt = next((m for m in modules if m["name"] == "Prompt OS"), None)
        ledger = next((m for m in modules if m["name"] == "Ledger OS"), None)
        maven = next((m for m in modules if m["name"] == "MavenOS"), None)

        integration = {
            "mavenos_present": maven is not None,
            "upstream_ready": False,
            "translation_potential": 0,
            "handoff_quality": "unknown",
            "recommended_maven_actions": [],
            "simulated_output_example": None
        }

        if not prompt or not ledger:
            integration["handoff_quality"] = "insufficient_upstream_data"
            return integration

        upstream_min = min(prompt["adjusted_health"], ledger["adjusted_health"])
        integration["upstream_ready"] = upstream_min >= 80
        integration["translation_potential"] = int(round(
            (prompt["adjusted_health"] * 0.4 + ledger["adjusted_health"] * 0.6)
        ))

        if maven:
            # Simulate handoff quality based on upstream vs Maven health
            if integration["upstream_ready"] and maven["adjusted_health"] >= 75:
                integration["handoff_quality"] = "strong"
            elif integration["upstream_ready"]:
                integration["handoff_quality"] = "moderate"
            else:
                integration["handoff_quality"] = "blocked_by_upstream"

            # Maven-specific recommendations
            if integration["translation_potential"] < 80:
                integration["recommended_maven_actions"].append(
                    "Delay commercial packaging until upstream health recovers above 80."
                )
            else:
                integration["recommended_maven_actions"].append(
                    "Proceed with Maven translation for highest-value gospel cycles first."
                )

            # Stub: what MavenOS would actually produce
            if integration["handoff_quality"] in ("strong", "moderate"):
                integration["simulated_output_example"] = {
                    "positioning_statement": "Feral Gloss Empire CharacterOS + LedgerOS spine now instrumented with real-time health observability. Enables production-grade gospel cycle tracking and commercial asset generation with measurable reliability.",
                    "target_buyer": "Serious AI creative tool builders and FGE canon operators seeking sellable character/product pipelines.",
                    "primary_assets": [
                        "Signature Edition Character Ledger + Health Monitor bundle (Gumroad)",
                        "Buyer education SOP: 'From Gospel Cycle to Packaged Product in <4 hours'",
                        "Notion template: FGE OS Telemetry Dashboard v0.2"
                    ],
                    "pricing_tier": "Tier 1 Micro-fracture — $47–$97",
                    "moat_language": "Only system with closed-loop Prompt → Ledger → Maven observability and ritual-structured gospel progression."
                }

        return integration

    # -------------------------------------------------------------------------
    # MAIN ANALYSIS
    # -------------------------------------------------------------------------

    def analyze(self) -> Dict[str, Any]:
        report: Dict[str, Any] = {
            "generated_at": self.generated_at.isoformat(),
            "version": "0.2",
            "input_snapshot_count": len(self.systems),
            "overall_health": 0.0,
            "target_health": self.target_health,
            "modules": self._raw_analyze_modules(),
            "flags": [],
            "recommendations": [],
            "integration": {},
            "next_actions": []
        }

        # Overall health (average of adjusted)
        if report["modules"]:
            total = sum(m["adjusted_health"] for m in report["modules"])
            report["overall_health"] = round(total / len(report["modules"]), 1)

        # Per-module flags (same as v0.1)
        for m in report["modules"]:
            if m["adjusted_health"] < 85:
                report["flags"].append(
                    f"HEALTH_BELOW_85: {m['name']} at {m['adjusted_health']} — review recommended."
                )
            if m["status"] != "active":
                report["flags"].append(f"STATUS_NOT_ACTIVE: {m['name']} is '{m['status']}'.")

        if report["overall_health"] < 88:
            report["flags"].append(
                "PLATFORM_HEALTH_WARNING: Composite below 88. Risk to downstream commercial output."
            )

        # MavenOS integration analysis (the new core)
        report["integration"] = self._compute_mavenos_integration(report["modules"])

        if report["integration"]["mavenos_present"]:
            intg = report["integration"]
            if intg["handoff_quality"] == "blocked_by_upstream":
                report["flags"].append(
                    "MAVENOS_HANDOFF_BLOCKED: Upstream (Prompt/Ledger) health too low for reliable commercial translation."
                )
            elif intg["handoff_quality"] == "moderate":
                report["recommendations"].append(
                    "MavenOS can proceed on highest-confidence cycles only. Add manual QC gate before packaging."
                )

            if intg["simulated_output_example"]:
                report["recommendations"].append(
                    "MavenOS stub generated sample positioning + asset list (see integration.simulated_output_example)."
                )

        # General recommendations
        report["recommendations"].append(
            "After next real gospel cycle, re-snapshot all three layers and compare handoff_quality movement."
        )
        report["recommendations"].append(
            "Once stable, freeze the Ledger → MavenOS input contract and promote v0.2 monitor into DOC BRAIN."
        )

        # Next actions
        report["next_actions"] = [
            "1. Define minimal Ledger fields required by MavenOS (gospel_stage, completeness_score, value_props, etc.).",
            "2. Run one end-to-end cycle with real data and validate simulated_output_example quality.",
            "3. Extend monitor with RenderOS node once MavenOS handoff is proven.",
            "4. When overall_health > 90 and handoff_quality = 'strong' for 3 snapshots → freeze schema."
        ]

        return report

    # -------------------------------------------------------------------------
    # OUTPUT
    # -------------------------------------------------------------------------

    def to_json(self, pretty: bool = True) -> str:
        data = self.analyze()
        if pretty:
            return json.dumps(data, indent=2, ensure_ascii=False)
        return json.dumps(data, ensure_ascii=False)

    def to_text_report(self) -> str:
        r = self.analyze()
        lines = []
        lines.append("=" * 72)
        lines.append("FGE OS HEALTH MONITOR v0.2 — PROMPT + LEDGER + MAVENOS")
        lines.append(f"Generated: {r['generated_at']} | Version: {r['version']}")
        lines.append("=" * 72)
        lines.append("")
        lines.append(f"OVERALL HEALTH: {r['overall_health']} / 100   (Target: {r['target_health']})")
        lines.append("")

        lines.append("MODULE BREAKDOWN:")
        for m in r["modules"]:
            icon = "✅" if m["adjusted_health"] >= 90 else "⚠️" if m["adjusted_health"] >= 85 else "🔴"
            lines.append(
                f"  {icon} {m['name']:<12} | Base: {m['base_health']:>3} | Recency: {m['recency_score']:>5.1f} | "
                f"Adjusted: {m['adjusted_health']:>3} | {m['days_since_activity']:.1f}d ago"
            )
        lines.append("")

        # Integration section (new in v0.2)
        intg = r.get("integration", {})
        if intg.get("mavenos_present"):
            lines.append("MAVENOS INTEGRATION STATUS:")
            lines.append(f"  Upstream Ready     : {'YES' if intg['upstream_ready'] else 'NO'}")
            lines.append(f"  Translation Potential: {intg['translation_potential']}/100")
            lines.append(f"  Handoff Quality    : {intg['handoff_quality'].upper()}")
            if intg.get("simulated_output_example"):
                ex = intg["simulated_output_example"]
                lines.append("")
                lines.append("  SIMULATED MAVENOS OUTPUT (stub):")
                lines.append(f"    Positioning: {ex['positioning_statement'][:80]}...")
                lines.append(f"    Assets     : {', '.join(ex['primary_assets'][:2])}...")
                lines.append(f"    Tier       : {ex['pricing_tier']}")
            lines.append("")

        if r["flags"]:
            lines.append("FLAGS / RISKS:")
            for f in r["flags"]:
                lines.append(f"  • {f}")
            lines.append("")

        if r["recommendations"]:
            lines.append("RECOMMENDATIONS:")
            for rec in r["recommendations"]:
                lines.append(f"  → {rec}")
            lines.append("")

        lines.append("NEXT ACTIONS:")
        for a in r["next_actions"]:
            lines.append(f"  {a}")

        lines.append("")
        lines.append("=" * 72)
        lines.append("v0.2 adds MavenOS commercial translation analysis and handoff simulation.")
        lines.append("Feed fresh snapshots after real cycles to validate integration quality.")
        lines.append("=" * 72)
        return "\n".join(lines)


# =============================================================================
# ENTRY POINT — includes example MavenOS stub for demonstration
# =============================================================================

DEFAULT_INPUT_V02 = [
    {
        "name": "Prompt OS",
        "status": "active",
        "type": "governed_prompt_pack",
        "last_activity": "2026-06-29T14:22:00Z",
        "health": 88
    },
    {
        "name": "Ledger OS",
        "status": "active",
        "type": "ledger_entry",
        "last_activity": "2026-06-29T14:18:00Z",
        "health": 85
    },
    {
        "name": "MavenOS",
        "status": "active",
        "type": "market_translation_layer",
        "last_activity": "2026-06-28T10:05:00Z",
        "health": 72,
        "notes": "Stub entry for integration testing. Real health will come from packaging runs."
    }
]


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--stdin":
        try:
            raw = json.load(sys.stdin)
        except Exception as e:
            print(f"ERROR: Failed to parse stdin JSON: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        raw = DEFAULT_INPUT_V02
        print("Running v0.2 on embedded 3-layer snapshot (Prompt + Ledger + MavenOS stub).", file=sys.stderr)

    monitor = FGEOSHealthMonitor(raw)
    print(monitor.to_json())

    print("\n" + monitor.to_text_report(), file=sys.stderr)


if __name__ == "__main__":
    main()
