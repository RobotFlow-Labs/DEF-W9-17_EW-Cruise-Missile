from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib

from .types import EnvironmentState, PaperTargets, ScenarioConfig


@dataclass
class ModuleConfig:
    scenario: ScenarioConfig
    environment: EnvironmentState
    action_levels: list[float]
    paper_targets: PaperTargets
    seed: int


def _req(dct: dict, key: str):
    if key not in dct:
        raise KeyError(f"Missing config key: {key}")
    return dct[key]


def load_config(path: str | Path) -> ModuleConfig:
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(config_path)

    with config_path.open("rb") as f:
        raw = tomllib.load(f)

    sim = _req(raw, "simulation")
    target = _req(raw, "target")
    env = _req(raw, "environment")
    actions = _req(raw, "actions")
    paper_targets = _req(raw, "paper_targets")

    scenario = ScenarioConfig(
        steps=int(_req(sim, "steps")),
        dt=float(_req(sim, "dt")),
        success_radius=float(_req(sim, "success_radius")),
        initial_speed=float(_req(sim, "initial_speed")),
        target_x=float(_req(target, "x")),
        target_y=float(_req(target, "y")),
        deviation_reward_scale=float(_req(sim, "deviation_reward_scale")),
        resource_penalty_scale=float(_req(sim, "resource_penalty_scale")),
    )

    env_state = EnvironmentState(
        temperature_c=float(_req(env, "temperature_c")),
        humidity=float(_req(env, "humidity")),
        wind_speed=float(_req(env, "wind_speed")),
        wind_dir_deg=float(_req(env, "wind_dir_deg")),
    )

    targets = PaperTargets(
        baseline_deviation_deg=float(_req(paper_targets, "baseline_deviation_deg")),
        multilayer_deviation_deg=float(_req(paper_targets, "multilayer_deviation_deg")),
        baseline_success_pct=float(_req(paper_targets, "baseline_success_pct")),
        multilayer_success_pct=float(_req(paper_targets, "multilayer_success_pct")),
        resource_delta_pct_min=float(_req(paper_targets, "resource_delta_pct_min")),
        resource_delta_pct_max=float(_req(paper_targets, "resource_delta_pct_max")),
    )

    levels = [float(v) for v in _req(actions, "levels")]
    if not levels:
        raise ValueError("actions.levels must contain at least one value")

    return ModuleConfig(
        scenario=scenario,
        environment=env_state,
        action_levels=levels,
        paper_targets=targets,
        seed=int(_req(sim, "seed")),
    )
