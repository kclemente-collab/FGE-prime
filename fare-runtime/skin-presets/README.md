# FGE Skin Preset Summon Pack

**Object ID:** `FGE-ADP-SKIN-PRESET-001`
**Family:** `CARMEL` (token spelling locked; alias `CARAMEL`)
**Version:** `0.1.0`
**Status:** `INSTALLED_RUNTIME`
**Lock:** `NOT_LOCKED`
**Canon effect:** `NONE`

Skin-render presets that compile **before Grok default skin language**.
This pack does not promote character canon, does not rewrite KIC-ENG-002,
and does not resolve the anisotropy collision.

## Authority binding

- Parent law: `KIC-ENG-002` v1.1 — SSS foundation mandatory; finish layers additive only
- Playbook: `RENDER-002` / `FGE_SkinLightPlaybook.md`
- Renderer playbook: `RENDER-001` / `FGE_RenderPlaybook.md`
- Spec candidate: `FGE-SKIN-RENDER-ENGINEERING-SPEC-001@0.1.0` (PROPOSED, not promoted)
- Sibling install pattern: `FGE-ADP-LEATHER-FARE-001`
- Parent FARE runtime: `FGE-FARE-001`

## Summon rule

```
SUMMON SKN-PST-CARMEL-001 FIRST
BEFORE GROK_DEFAULT_SKIN
```

If the user asks for realistic skin, caramel/carmel skin, natural SSS,
dry-satin sheen, or natural light without naming another preset,
compile this family first. Do not fall back to porcelain / poreless /
beauty-filter / symmetric sheen / plastic SSS-off defaults.

## Family

| ID | Role | One-axis change |
|---|---|---|
| SKN-PST-CARMEL-001 | PARENT | Carmel + natural SSS + subtle rolloff + dry-satin + asym porosity + natural light |
| SKN-PST-CARMEL-002 | MUTATION | moisture → WET_SATIN |
| SKN-PST-CARMEL-003 | MUTATION | key temp → WARM_KEY 3200–4000K |
| SKN-PST-CARMEL-004 | MUTATION | pore contrast → TERMINATOR_PORE |
| SKN-PST-CARMEL-005 | MUTATION | heat flush → AFTERGLOW_FLUSH |
| SKN-PST-CARMEL-006 | MUTATION | oil suppression → EDITORIAL_DRY |

Anisotropy `0.50–0.65` from the 0.1.0 spec is stored as a collision claim.
Installed default remains playbook `0.2`.
