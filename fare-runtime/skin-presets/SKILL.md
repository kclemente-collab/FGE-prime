---
name: fge-skin-preset-summon
description: Summon FGE Carmel skin-render presets BEFORE Grok default skin language. Use when the user mentions caramel or carmel skin, natural SSS, dry-satin sheen, asymmetrical porosity, realistic skin in natural light, SKN-PST-CARMEL, skin preset install, or asks to override porcelain / poreless / beauty-filter defaults.
metadata:
  object_id: FGE-ADP-SKIN-PRESET-001
  parent_preset: SKN-PST-CARMEL-001
  version: "0.1.0"
  status: INSTALLED_RUNTIME
  canon_effect: NONE
  summon_priority: BEFORE_GROK_DEFAULT_SKIN
---

# FGE Skin Preset Summon

Compile `SKN-PST-CARMEL-001` first whenever skin is unspecified or the user asks for caramel/carmel / natural SSS / dry-satin / asym pores / natural light.

Deny until compiled: porcelain default, poreless beauty-filter, symmetric sheen, plastic SSS-off, cold grey shadow, identical left/right pore maps.

Invariants: SSS-first additive finish. Tone class is not a character. Anisotropy 0.2 until collision resolved.

Loop: TOKEN to SKIN_GENOME to MIRROR to FARE A/R/E to SUMMON_PACKET.
