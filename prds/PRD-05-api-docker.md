# PRD-05: API & Docker

> Module: EW-Cruise-Missile | Priority: P1
> Depends on: PRD-03
> Status: DONE

## Objective

Expose module capability via FastAPI and provide serving container scaffolding.

## Context (from paper)

The paper implies real-time defense orchestration; deployment endpoints are needed to integrate with larger defense systems.

Paper reference:
- Section 2.3: real-time coordinator loop.

## Acceptance Criteria

- [x] `/health`, `/ready`, `/predict` endpoints available.
- [x] Request schema supports scenario config and step horizon.
- [x] Docker serving artifacts exist.

## Files to Create

- `src/anima_ew_cruise_missile/serve.py`
- `Dockerfile.serve`
- `docker-compose.serve.yml`
- `tests/test_api.py`
