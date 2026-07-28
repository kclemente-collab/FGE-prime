# FGE Lineage Object — Thin Spec v0.1

**Status:** PRE-DOCTRINE / TEST-ENABLING ONLY
**Purpose:** The minimum set of rules required to make the Raven SB_330 hand-trace *falsifiable*.
**Not in scope (deferred until test holds):** five-field binding ceremony, L0–L3 reconciliation, regulatory/trust framing, Gumroad packaging.
**One question this spec must let us answer:** *Does a held object deepen, mechanically, without anyone narrating it?*

---

## Element 1 — The Accrual Rule (formula)

An object's worth is a function of its **position in the append-only lineage tree**, not its narrative and not its mint date.

```
DEPTH(obj)      = number of LOCKED descendants below obj in the tree
ORIGIN(obj)     = 1 / (hops from obj to its line's origin + 1)    # origin itself = 1.0
RARITY(cluster) = 1 / (count of LOCKED objects sharing obj.frequency_cluster)

VALUE(obj) = (w_d · DEPTH) + (w_o · ORIGIN · DEPTH) + (w_r · RARITY)
```

Default weights for the test: `w_d = 1.0`, `w_o = 2.0`, `w_r = 0.5`.

**Why ORIGIN multiplies DEPTH and doesn't just add:** an origin object with no descendants is *potential*, not *value*. Value is earned only when the line actually grows beneath it. This is the rule that makes Raven (SB_330) the most load-bearing object that *can* exist — but only once descent accrues. It encodes your invariant-kernel logic: meaning accumulates, it is not granted at mint.

**Falsification target:** if VALUE rises for an object whose owner did nothing — purely because *other* locked descendants entered the line — the accrual mechanic works. If VALUE only moves when the holder acts, the spine is dead and "owning = reading" is false.

---

## Element 2 — The Lock Gate (one law)

> **LAW:** A derivation deepens an ancestor's VALUE **if and only if** the derivation passes canon lock (compile → validate → **lock**). Unlocked derivations are invisible to the tree. They do not count toward DEPTH, do not affect RARITY, and cannot be cited as ancestors.

This is the single line that separates a spine from a pile. Without it, growth is unfalsifiable — everything accrues, so nothing means anything. With it, a junk descendant cannot dilute a line because it never enters the line.

**Test consequence:** during the Raven trace, any descendant not yet locked is scored as **not present**. We measure VALUE against locked-only descent. If you find yourself wanting to "count it anyway because it's almost locked," that is the gate doing its job — log it and exclude it.

---

## Element 3 — The Detective Output Contract

The canon evaluator (Atelier Brain) **prices; it does not create.** Given an object's sbid and its tree position, it returns this and nothing else:

```json
{
  "sbid": "SB_330",
  "value": 0.0,
  "components": { "depth": 0, "origin": 1.0, "rarity": 0.0 },
  "position": { "origin_distance": 0, "locked_descendants": 0 },
  "grade": "ANCHOR | DEEP | DERIVED | LEAF",
  "narrative_emitted": false
}
```

- `narrative_emitted` MUST be `false`. If the evaluator ever produces prose to justify worth, the contract is violated and "lore without speaking it" has failed.
- `grade` is a *read* of position, never an authored judgment:
  - **ANCHOR** — origin_distance 0
  - **DEEP** — has locked descendants
  - **DERIVED** — has a locked ancestor and locked descendants
  - **LEAF** — locked, no descendants yet
- This JSON is the thing you stare at during the test. The pass condition is subjective but bounded: *does this read as accrued lore, with zero narrative present?*

---

## The Test Protocol (what v0.1 exists to enable)

1. Place **Raven / SB_330 / Obsidian** as the line origin.
2. Enumerate its **real, currently-locked** descendants — by hand, lock-gated.
3. Compute VALUE for Raven and for 2–3 mid-tree objects using Element 1.
4. Emit the Element 3 JSON for each.
5. Judge the one question: **did Raven's VALUE rise solely from descendants accruing beneath it, with `narrative_emitted: false` throughout?**

**Pass →** earn `FGE-LINEAGE-OBJECT-001` (full doctrine).
**Fail →** we changed three rules, not a doctrine. North star intact.
