from __future__ import annotations

from dataclasses import replace
import random

from .types import EnvironmentState, MissileState, ScenarioConfig


def generate_initial_missile_state(cfg: ScenarioConfig, rng: random.Random) -> MissileState:
    y_offset = rng.uniform(-150.0, 150.0)
    heading = rng.uniform(-0.03, 0.03)
    return MissileState(x=0.0, y=y_offset, z=50.0, speed=cfg.initial_speed, heading_rad=heading)


def generate_environment_state(base: EnvironmentState, rng: random.Random) -> EnvironmentState:
    return replace(
        base,
        temperature_c=base.temperature_c + rng.uniform(-3.0, 3.0),
        humidity=max(0.05, min(0.98, base.humidity + rng.uniform(-0.05, 0.05))),
        wind_speed=max(0.0, base.wind_speed + rng.uniform(-1.5, 1.5)),
        wind_dir_deg=(base.wind_dir_deg + rng.uniform(-8.0, 8.0)) % 360,
    )
