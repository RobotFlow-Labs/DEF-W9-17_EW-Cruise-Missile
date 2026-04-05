# PRD-07: Production Hardening

> Module: EW-Cruise-Missile | Priority: P2
> Depends on: PRD-04
> Status: DONE

## Objective

Add reliability guardrails, preflight checks, and training/export readiness hooks for CUDA-server continuation.

## Context (from paper)

The conclusion highlights future hardware-in-the-loop and stronger cyber workflows; the local baseline must prepare that handoff.

Paper reference:
- Section 4 (Conclusion): extend to robust operational contexts.

## Acceptance Criteria

- [x] Preflight script validates data/config/runtime assumptions.
- [x] Batch-size finder helper exists for GPU tuning.
- [x] Project metadata and packaging are in place.
- [x] Test suite covers critical module behavior.

## Files to Create

- `scripts/find_batch_size.py`
- `scripts/verify_assets.py`
- `pyproject.toml`
- `tests/test_training.py`
