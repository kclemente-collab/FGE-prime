# FGE GitHub candidate runtime (public-safe)

This is a **sanitized, read-only contract preflight** for FGE CharacterOS. It preserves the declared architecture without publishing private source ZIPs, image references, dossiers or HB master data.

The original local package is `FGE_GitHub_Actions_Runtime_v0.1.0.zip`. Its source-locked 20-check preflight is **not** replicated in GitHub because those checks require the withheld private source snapshots. This public substitute validates only 12 candidate contract invariants. Do not equate its passing status with source verification.

Run: `python3 -m unittest discover -s tests -p 'test_fge_runtime.py' -v` and `python3 runtime/motherboard/preflight.py`.

No secrets, external dispatch, persistent registry writes, Pages deployment, or canon mutation. Release remains HOLD even if the public checks pass. Director review required before promoting or publishing any private source or enabling execution.
