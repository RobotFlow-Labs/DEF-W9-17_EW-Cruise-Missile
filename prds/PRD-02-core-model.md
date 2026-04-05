# PRD-02: Core Model

> Module: EW-Cruise-Missile | Priority: P0
> Depends on: PRD-01
> Status: DONE

## Objective

Implement the core multi-layer interference simulation engine and DRL-compatible coordinator.

## Context (from paper)

The model combines EW perturbation, cyber interference, deception signatures, and an AI coordinator that selects actions over a composite action space.

Paper references:
- Section 2.2.2: EW perturbation model.
- Section 2.2.3: cyber data/weight perturbation.
- Section 2.2.4: deception signal generation.
- Section 2.3: DRL coordinator and composite action space.

## Acceptance Criteria

- [x] EW, cyber, and deception modules implemented as composable functions.
- [x] Composite action representation implemented.
- [x] Episode step function computes deviation and resource cost.
- [x] DRL-compatible policy network implemented (torch path with heuristic fallback).

## Files to Create

- `src/anima_ew_cruise_missile/modules/ew.py`
- `src/anima_ew_cruise_missile/modules/cyber.py`
- `src/anima_ew_cruise_missile/modules/deception.py`
- `src/anima_ew_cruise_missile/env.py`
- `src/anima_ew_cruise_missile/coordinator.py`
- `tests/test_env.py`
