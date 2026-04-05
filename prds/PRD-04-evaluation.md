# PRD-04: Evaluation

> Module: EW-Cruise-Missile | Priority: P1
> Depends on: PRD-03
> Status: DONE

## Objective

Implement a benchmark runner for four scenarios and compare results against paper targets.

## Context (from paper)

The paper claims 400 simulation runs over four scenarios and reports key deltas between no-interference and multi-layer interference.

Paper references:
- Abstract: 400 runs, 4 scenarios, key metrics.
- Conclusion: multi-layer significantly outperforms single-layer disruptions.

## Acceptance Criteria

- [x] Evaluation runner supports 4 scenarios.
- [x] Metrics table includes deviation, success, and resource deltas.
- [x] Paper-target comparison report generated in stdout.

## Files to Create

- `src/anima_ew_cruise_missile/eval.py`
- `tests/test_eval.py`
