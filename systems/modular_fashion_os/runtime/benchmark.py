"""Gate performance claims on verified external UE5 benchmark evidence."""

from __future__ import annotations

from typing import Any, Dict


def evaluate_ue5_benchmark(evidence: Dict[str, Any]) -> Dict[str, Any]:
    """Return a publishability decision; never infer missing measurements."""
    required = (
        "run_id",
        "ue5_version",
        "hardware_profile",
        "sample_count",
        "baseline_gpu_frame_ms",
        "occlusion_gpu_frame_ms",
    )
    missing = [field for field in required if evidence.get(field) in (None, "")]
    verified = evidence.get("evidence_status") == "VERIFIED_UE5_RUN"
    if missing or not verified:
        return {
            "claim_publishable": False,
            "status": "SUPPRESSED_PENDING_MEASUREMENT",
            "missing": missing,
            "measured_reduction_percent": None,
        }
    sample_count = int(evidence["sample_count"])
    baseline = float(evidence["baseline_gpu_frame_ms"])
    occluded = float(evidence["occlusion_gpu_frame_ms"])
    if sample_count < 30 or baseline <= 0 or occluded < 0:
        return {
            "claim_publishable": False,
            "status": "INSUFFICIENT_EVIDENCE",
            "missing": [],
            "measured_reduction_percent": None,
        }
    reduction = round(((baseline - occluded) / baseline) * 100.0, 2)
    return {
        "claim_publishable": True,
        "status": "MEASURED",
        "missing": [],
        "measured_reduction_percent": reduction,
    }
