# EW-Cruise-Missile - Asset Manifest

## Paper

- Title: A Multi-Layer Electronic and Cyber Interference Model for AI-Driven Cruise Missiles: The Case of Khuzestan Province
- ArXiv: 2510.03542
- Authors: Pouriya Alimoradi, Ali Barati, Hamid Barati
- PDF: `papers/2510.03542.pdf`

## Status

ALMOST

Rationale:
- Paper is present and parsed.
- Public reference implementation repository was not identified from the paper metadata/arXiv page.
- Module software baseline is implemented locally and ready for CUDA-side optimization/training.

## Code Repositories

- Public reference repo: NOT FOUND (as of 2026-04-04 checks).
- Local implementation repo: this module directory.

## Pretrained Weights

The paper does not provide explicit public weight artifacts.

| Model | Size | Source | Path on Server | Status |
|---|---:|---|---|---|
| DRL coordinator policy (module-specific) | TBD | trained in-module | /mnt/forge-data/models/ew_cruise_missile/ | MISSING |

## Datasets

The paper describes simulation-based evaluation (400 runs, four scenarios) and does not declare a public dataset package.

| Dataset | Size | Split | Source | Path | Status |
|---|---:|---|---|---|---|
| Synthetic scenario generator (this module) | small | train/val/test via seeds | local code | ./data/ (generated) | READY |

## Hyperparameters (from paper)

The paper gives qualitative DRL framing and high-level setup but does not publish a complete hyperparameter table.

| Param | Value | Paper Section |
|---|---|---|
| RL family | DQN/PPO/DDPG (candidate) | 2.3 |
| Reward objective | max deviation, min target acquisition, penalize resource overuse | 2.3 |
| Scenarios | 4 | Abstract |
| Simulation runs | 400 | Abstract |

## Expected Metrics (from paper)

| Benchmark | Metric | Paper Value | Our Target |
|---|---|---:|---:|
| Baseline (no interference) | average angular deviation (deg) | 0.25 | <= 0.5 |
| Multi-layer interference | average angular deviation (deg) | 8.65 | >= 7.5 |
| Baseline (no interference) | target acquisition success (%) | 92.7 | >= 85 |
| Multi-layer interference | target acquisition success (%) | 31.5 | <= 40 |
| Multi-layer vs single-layer | resource consumption delta (%) | +25 to +30 | +20 to +35 |

## Notes

- Final numerical parity should be treated as a calibration target in CUDA training runs.
- Local CPU simulations are used for architecture and pipeline validation.
