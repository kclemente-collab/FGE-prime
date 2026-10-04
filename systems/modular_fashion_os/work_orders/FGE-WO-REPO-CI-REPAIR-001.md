# FGE Repository-Wide CI Repair Work Order

**Object:** `FGE-WO-REPO-CI-REPAIR-001`  
**Status:** `PARTIALLY_REPAIRED / SEPARATE_WORK_REMAINS`  
**Canon effect:** `NONE`  
**Scope boundary:** Outside `FGE-SYS-MODULAR-FASHION-OS-001`

## Verified failures

The repository-wide `Python application` workflow continues to fail before pytest. The original trace identified syntax or indentation errors in `build.py`, `build 2.py`, `build 3.py`, and `fge_v2_core.py`.

PR #2, `Install FARE v0.6 Serialization Ledger Sandbox`, is `MERGED / CLOSED` at commit `ee57afd592ded0e6a65076253dd52a820437bd61`; its Python workflow run #18 failed. The sandbox files are web-native, but the workflow scans the entire repository.

### Exact defects

- `fge_v2_core.py`: `RESOLVED_BY_EXTERNAL_COMMIT`. Commit `615620c7cc5bf16a6a62cebee924e83e00280833` restored and indented the test harness. Its Modular Fashion OS workflow run #20 passed, while repository-wide Python workflow run #24 still failed.
- `build.py`, `build 2.py`, `build 3.py`: an outer multiline f-string contains an inner f-string whose HTML quotes are backslash-escaped. Precompute that joined HTML fragment before entering the outer f-string, then interpolate the variable.

Changing only the `print` statement cannot restore repository-wide CI because it is already a regular string and three independent build-file parser errors remain.

## Required disposition

Create a separate branch, establish whether each file is active source or archival material, repair or exclude it through an explicit repository policy, then restore a green repository-wide workflow. Do not mix those unrelated edits into the Modular Fashion OS implementation authority.
