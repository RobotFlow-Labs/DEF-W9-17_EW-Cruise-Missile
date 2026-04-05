# PRD-03: Inference Pipeline

> Module: EW-Cruise-Missile | Priority: P0
> Depends on: PRD-02
> Status: DONE

## Objective

Provide deterministic CLI inference over one or more episodes to return deviations, success rates, and resource usage.

## Context (from paper)

The paper reports scenario-level aggregate performance and emphasizes adaptive configuration against changing environment.

Paper references:
- Abstract: reported scenario metrics over 400 runs.
- Section 2.3: action selection per step.

## Acceptance Criteria

- [x] CLI runs single scenario episodes with configurable seeds.
- [x] Output includes average deviation, success rate, and resource consumption.
- [x] Supports baseline, single-layer, and multi-layer modes.

## Files to Create

- `src/anima_ew_cruise_missile/infer.py`
- `scripts/train.py`
- `tests/test_infer.py`
