#!/usr/bin/env python3
"""
CEC UNIFIED CONTROL DASHBOARD v2
Single Screen Civilization Interface

Merges:
- Registry (population)
- Field (relational physics)
- Events (discontinuities)
- Memory (irreversible history / scar tissue)

Designed for sub-1-second comprehension of the entire synthetic identity civilization state.
"""

import os
import sys
from datetime import datetime
from typing import Optional, Any

# --- Graceful imports for existing architecture ---
try:
    from asset_registry import AssetRegistry
except ImportError:
    AssetRegistry = None

try:
    from cec_multi_asset_field_v1 import CECAssetField
except ImportError:
    CECAssetField = None

try:
    from cec_event_engine_v2 import CECEventEngine
except ImportError:
    CECEventEngine = None

try:
    from cec_persistent_world_memory_v1 import WorldMemory, PersistentWorldMemoryEngine
except ImportError:
    WorldMemory = None
    PersistentWorldMemoryEngine = None


class CECUnifiedDashboard:
    """
    Unified Control Surface for the CEC synthetic civilization.
    Every layer visible at a glance.
    """

    def __init__(self, registry: Any = None, field: Any = None, memory_engine: Any = None):
        self.registry = registry
        self.field = field
        self.memory_engine = memory_engine
        self.cycle = 0

    # ------------------------------------------------------------------
    # WORLD HEALTH BAR (Top-level civilization status)
    # ------------------------------------------------------------------
    def render_world_health(self):
        if not self.registry or not hasattr(self.registry, "_assets") or not self.registry._assets:
            print("\n🌍 WORLD HEALTH")
            print("----------------------")
            print("[NO POPULATION]     0.00")
            return

        assets = list(self.registry._assets.values())
        if not assets:
            print("\n🌍 WORLD HEALTH\n----------------------\n[EMPTY REGISTRY]")
            return

        avg_risk = sum(getattr(a, "synthesis_risk", 0.5) for a in assets) / len(assets)
        canon_locked = sum(1 for a in assets if getattr(a, "canon_lock", False)) / len(assets)
        health_score = max(0.0, min(1.0, (1 - avg_risk) * 0.65 + canon_locked * 0.35))

        bar_length = 22
        filled = int(health_score * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)

        status = "STABLE"
        if health_score < 0.55:
            status = "VOLATILE"
        if health_score < 0.35:
            status = "FRACTURED"
        if health_score < 0.20:
            status = "CRITICAL"

        print("\n🌍 WORLD HEALTH")
        print("----------------------")
        print(f"[{bar}] {round(health_score, 2)}  →  {status}")

    # ------------------------------------------------------------------
    # REGISTRY / POPULATION SNAPSHOT
    # ------------------------------------------------------------------
    def render_registry(self):
        print("\n👥 POPULATION STATE")
        print("----------------------")
        if not self.registry or not hasattr(self.registry, "_assets") or not self.registry._assets:
            print("[No assets in registry]")
            return

        for asset in self.registry._assets.values():
            cid = getattr(asset, "character_id", "UNKNOWN")[:16]
            risk = round(getattr(asset, "synthesis_risk", 0.0), 2)
            price = round(getattr(asset, "mavin_price", 0.0), 1)
            canon = "✅" if getattr(asset, "canon_lock", False) else "❌"
            print(f"{cid:<16} | RISK:{risk:.2f} | PRICE:${price:>6.1f} | CANON:{canon}")

    # ------------------------------------------------------------------
    # FIELD STATE (Relational Physics)
    # ------------------------------------------------------------------
    def render_field(self):
        print("\n🌐 FIELD STATE")
        print("----------------------")
        if not self.field:
            print("[Field not connected]")
            return

        assets = list(self.registry._assets.values()) if self.registry else []
        if not assets:
            print("[No assets]")
            return

        avg_risk = sum(getattr(a, "synthesis_risk", 0.0) for a in assets) / len(assets)
        avg_price = sum(getattr(a, "mavin_price", 0.0) for a in assets) / len(assets)
        print(f"Avg Risk     : {avg_risk:.3f}")
        print(f"Avg Price    : ${avg_price:.2f}")

        # Simple arbitrage pressure summary if available
        if hasattr(self.field, "compute_arbitrage_pressure"):
            try:
                pressure = self.field.compute_arbitrage_pressure()
                high_pressure = [k for k, v in pressure.items() if v > 0.05]
                if high_pressure:
                    print(f"High Pressure: {', '.join(high_pressure[:3])}")
            except Exception:
                pass

    # ------------------------------------------------------------------
    # EVENT FEED (Recent Shocks)
    # ------------------------------------------------------------------
    def render_events(self):
        print("\n⚡ RECENT EVENTS")
        print("----------------------")
        if not self.field or not hasattr(self.field, "event_engine"):
            print("[No event engine attached]")
            return

        history = getattr(self.field.event_engine, "history", [])
        if not history:
            print("[No events recorded yet]")
            return

        for entry in history[-6:]:
            cycle = entry.get("cycle", "?")
            event = entry.get("event", "UNKNOWN")
            print(f"Cycle {cycle:>3} → {event}")

    # ------------------------------------------------------------------
    # MEMORY / SCAR TISSUE LAYER
    # ------------------------------------------------------------------
    def render_memory(self):
        print("\n📜 WORLD MEMORY (Scar Tissue)")
        print("----------------------")
        if not self.memory_engine:
            print("[No persistent memory engine]")
            return

        # Support both WorldMemory and PersistentWorldMemoryEngine
        mem = getattr(self.memory_engine, "memory", self.memory_engine)
        if hasattr(mem, "current_regime"):
            print(f"Current Regime : {mem.current_regime}")
        if hasattr(mem, "fracture_count"):
            print(f"Fracture Count : {mem.fracture_count}")
        if hasattr(mem, "get_effective_drift_floor"):
            print(f"Drift Floor    : +{mem.get_effective_drift_floor():.3f}")

        # Show recent regime transitions if available
        if hasattr(mem, "regime_history") and mem.regime_history:
            last = mem.regime_history[-1]
            print(f"Last Shift     : {last.get('from')} → {last.get('to')} (cycle {last.get('cycle')})")

    # ------------------------------------------------------------------
    # MINI RISK MAP (Visual pressure field)
    # ------------------------------------------------------------------
    def render_risk_map(self):
        print("\n📊 RISK FIELD MAP")
        print("----------------------")
        if not self.registry or not hasattr(self.registry, "_assets") or not self.registry._assets:
            print("[No assets]")
            return

        for asset in self.registry._assets.values():
            cid = getattr(asset, "character_id", "UNKNOWN")[:14]
            risk = getattr(asset, "synthesis_risk", 0.0)
            bars = int(risk * 18)
            bar = "█" * bars + "░" * (18 - bars)
            print(f"{cid:<14} | {bar} {risk:.2f}")

    # ------------------------------------------------------------------
    # MAIN RENDER
    # ------------------------------------------------------------------
    def render(self, cycle: Optional[int] = None):
        if cycle is not None:
            self.cycle = cycle

        os.system("clear")
        print("══════════════════════════════════════════════════════════════")
        print("   CEC UNIFIED CONTROL DASHBOARD v2 — SYNTHETIC CIVILIZATION")
        print("══════════════════════════════════════════════════════════════")
        print(f"TIME: {datetime.utcnow().isoformat(timespec='seconds')}   |   CYCLE: {self.cycle}")
        print("══════════════════════════════════════════════════════════════")

        self.render_world_health()
        self.render_registry()
        self.render_field()
        self.render_events()
        self.render_memory()
        self.render_risk_map()

        print("\n══════════════════════════════════════════════════════════════")
        print("Commands: [q]uit | [r]efresh | [s]tep field | [e]vent injection")
        print("══════════════════════════════════════════════════════════════\n")

    # ------------------------------------------------------------------
    # Convenience live runner (for quick testing)
    # ------------------------------------------------------------------
    def run_live(self, steps: int = 20, step_callback=None):
        """Run a live simulation loop with dashboard updates."""
        if not self.field or not hasattr(self.field, "step"):
            print("[Demo] No real field.step() available — running mock simulation instead.")
            # Mock simulation: slightly increase risk on some assets to simulate activity
            for i in range(steps):
                if self.registry and hasattr(self.registry, "_assets"):
                    for asset in self.registry._assets.values():
                        current_risk = getattr(asset, "synthesis_risk", 0.2)
                        # Simulate mild drift + occasional event
                        asset.synthesis_risk = round(min(0.95, current_risk + 0.015), 3)
                        if i % 4 == 0 and hasattr(asset, "canon_lock"):
                            if asset.synthesis_risk > 0.45:
                                asset.canon_lock = False
                self.render(cycle=i)
                try:
                    import time
                    time.sleep(0.65)
                except KeyboardInterrupt:
                    print("\n[Interrupted]")
                    break
            return

        for i in range(steps):
            result = self.field.step()
            if self.memory_engine and hasattr(self.memory_engine, "process_event"):
                event_name = result.get("event")
                if event_name:
                    self.memory_engine.process_event(event_name, self.field, cycle=i)

            self.render(cycle=i)
            if step_callback:
                step_callback(i, result)

            try:
                import time
                time.sleep(0.75)
            except KeyboardInterrupt:
                print("\n[Interrupted]")
                break


# ----------------------------------------------------------------------
# DEMO / SELF-TEST (runs if executed directly)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("Initializing CEC Unified Dashboard v2 demo...")

    # Try to use real classes; fall back to minimal mocks if imports fail
    registry = None
    field = None
    memory_engine = None

    try:
        if AssetRegistry:
            registry = AssetRegistry()
            # Create a couple of characters if the registry supports .create
            if hasattr(registry, "create"):
                registry.create(
                    character_id="CHAR-ISO-BLACK-YOUTH-001",
                    seed_id="CSC-0001",
                    era_variant="Black Era Youth",
                    personality_module="PS-ISO-2.1",
                    behavior_module="BD-ISO-2.3",
                    physical_module="PH-ISO-BLACK-YOUTH-3.1"
                )
                registry.create(
                    character_id="CHAR-NOVA-NEON-001",
                    seed_id="CSC-0002",
                    era_variant="Neon Drift Youth",
                    personality_module="PS-NOVA",
                    behavior_module="BD-NOVA",
                    physical_module="PH-NOVA-NEON"
                )
    except Exception as e:
        print(f"[Warning] Could not fully initialize real registry: {e}")
        registry = None

    # Create minimal mock assets if real registry failed or is empty
    if not registry or not getattr(registry, "_assets", {}):
        print("[Demo Mode] Using mock assets for dashboard preview.")
        from dataclasses import dataclass, field as dataclass_field
        from typing import List

        @dataclass
        class MockAsset:
            character_id: str
            synthesis_risk: float = 0.18
            mavin_price: float = 95.0
            canon_lock: bool = True
            identity_integrity: float = 0.87
            violation_flags: List[str] = dataclass_field(default_factory=list)

        class MockRegistry:
            def __init__(self):
                self._assets = {
                    "CHAR-ISO-BLACK-YOUTH-001": MockAsset("CHAR-ISO-BLACK-YOUTH-001", 0.19, 127.0, True, 0.91),
                    "CHAR-NOVA-NEON-001": MockAsset("CHAR-NOVA-NEON-001", 0.31, 68.0, False, 0.74, ["GLOBAL_DEVIATION"]),
                    "CHAR-GEN-003": MockAsset("CHAR-GEN-003", 0.24, 81.0, True, 0.82),
                }

        registry = MockRegistry()

    # Attach field and memory if possible
    if CECAssetField and registry:
        try:
            field = CECAssetField(registry)
            if CECEventEngine:
                field.event_engine = CECEventEngine()
        except Exception:
            field = None

    if PersistentWorldMemoryEngine:
        try:
            memory_engine = PersistentWorldMemoryEngine()
        except Exception:
            memory_engine = None

    dashboard = CECUnifiedDashboard(registry, field, memory_engine)

    # Run a short live demo
    print("\nStarting short live demo (press Ctrl+C to stop early)...\n")
    dashboard.run_live(steps=12)