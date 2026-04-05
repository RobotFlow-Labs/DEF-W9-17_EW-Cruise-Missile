# PRD-01: Foundation

> Module: EW-Cruise-Missile | Priority: P0
> Depends on: None
> Status: DONE

## Objective

Establish project skeleton, typed domain models, config system, and synthetic data generation for simulation episodes.

## Context (from paper)

The paper defines state vectors for missile and environment and a layered interference pipeline.

Paper references:
- Section 2.1: overall three-layer framework.
- Section 2.2.1: missile state and environmental state vectors.

## Acceptance Criteria

- [x] Typed state/action/resource models exist.
- [x] TOML config loading and validation works.
- [x] Synthetic episode initialization supports environmental variation.
- [x] Unit tests for config and state construction pass.

## Files to Create

- `src/anima_ew_cruise_missile/types.py`
- `src/anima_ew_cruise_missile/config.py`
- `src/anima_ew_cruise_missile/data.py`
- `configs/default.toml`, `configs/debug.toml`, `configs/paper.toml`
- `tests/test_config.py`, `tests/test_types.py`

## Test Plan

- `pytest tests/test_config.py tests/test_types.py -q`
