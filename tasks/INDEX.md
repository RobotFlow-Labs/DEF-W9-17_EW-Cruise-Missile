# EW-Cruise-Missile Task Index

## Build Order

| Task | Title | Depends | Status |
|---|---|---|---|
| PRD-0101 | Define domain types and resources | None | DONE |
| PRD-0102 | Build config loading and validation | PRD-0101 | DONE |
| PRD-0103 | Synthetic data episode generator | PRD-0102 | DONE |
| PRD-0201 | EW module implementation | PRD-0103 | DONE |
| PRD-0202 | Cyber module implementation | PRD-0201 | DONE |
| PRD-0203 | Deception module implementation | PRD-0202 | DONE |
| PRD-0204 | Environment step dynamics | PRD-0203 | DONE |
| PRD-0205 | DRL-compatible coordinator | PRD-0204 | DONE |
| PRD-0301 | Inference CLI | PRD-0205 | DONE |
| PRD-0302 | Training entrypoint | PRD-0205 | DONE |
| PRD-0401 | Scenario benchmark runner | PRD-0301 | DONE |
| PRD-0501 | FastAPI service endpoints | PRD-0301 | DONE |
| PRD-0502 | Docker serve scaffolding | PRD-0501 | DONE |
| PRD-0601 | ROS2 node skeleton | PRD-0501 | DONE |
| PRD-0602 | ANIMA module manifest | PRD-0601 | DONE |
| PRD-0701 | Asset and runtime preflight scripts | PRD-0401 | DONE |
| PRD-0702 | Tests and quality gates | PRD-0701 | DONE |
