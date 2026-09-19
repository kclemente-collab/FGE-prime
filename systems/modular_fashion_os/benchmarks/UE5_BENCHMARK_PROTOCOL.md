# UE5 Occlusion Benchmark Protocol

**Object:** `FGE-BENCH-UE5-OCCLUSION-001`  
**Status:** `PENDING_EXTERNAL_UE5_RUN`  
**Claim state:** `SUPPRESSED_PENDING_MEASUREMENT`

Run the same character, wardrobe stack, animation, camera and quality settings twice:

1. Baseline — clipping masks and lower-layer deactivation disabled.
2. Candidate — compiled clipping/occlusion payload enabled.

Discard 300 warm-up frames. Capture at least 600 measured frames through Unreal Insights. Record median GPU frame time and retain the `.utrace`, project commit, UE5 version and hardware profile with the result.

No percentage claim is publishable until `evidence_status` is explicitly changed to `VERIFIED_UE5_RUN` and the benchmark evaluator accepts the measurements.
