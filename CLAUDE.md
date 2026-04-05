# 17_EW-Cruise-Missile

ANIMA defense module implementing a multi-layer interference simulator and coordinator inspired by:

- arXiv:2510.03542
- Title: A Multi-Layer Electronic and Cyber Interference Model for AI-Driven Cruise Missiles: The Case of Khuzestan Province

## Goal

Provide a production-oriented software baseline that:

1. Models EW, cyber, and deception interference layers.
2. Coordinates interference actions with a DRL-compatible policy.
3. Reproduces paper-aligned scenario trends in simulation.
4. Exposes CLI + API interfaces for downstream CUDA optimization and deployment.

## Module Package

`src/anima_ew_cruise_missile`

## Entry Points

- Training: `python scripts/train.py --config configs/paper.toml`
- Inference run: `python -m anima_ew_cruise_missile.infer --config configs/default.toml`
- Evaluation: `python -m anima_ew_cruise_missile.eval --config configs/paper.toml`
- API: `uvicorn anima_ew_cruise_missile.serve:app --host 0.0.0.0 --port 8080`
