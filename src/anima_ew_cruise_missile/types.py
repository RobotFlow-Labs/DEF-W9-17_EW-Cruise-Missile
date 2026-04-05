from __future__ import annotations

from dataclasses import dataclass
from math import atan2, degrees, hypot


@dataclass
class MissileState:
    x: float
    y: float
    z: float
    speed: float
    heading_rad: float


@dataclass
class EnvironmentState:
    temperature_c: float
    humidity: float
    wind_speed: float
    wind_dir_deg: float


@dataclass
class ResourceState:
    ew_budget: float = 1.0
    cyber_budget: float = 1.0
    deception_budget: float = 1.0
    resource_used: float = 0.0


@dataclass
class LayerAction:
    ew_level: float
    cyber_level: float
    deception_level: float


@dataclass
class ScenarioConfig:
    steps: int
    dt: float
    success_radius: float
    initial_speed: float
    target_x: float
    target_y: float
    deviation_reward_scale: float
    resource_penalty_scale: float


@dataclass
class PaperTargets:
    baseline_deviation_deg: float
    multilayer_deviation_deg: float
    baseline_success_pct: float
    multilayer_success_pct: float
    resource_delta_pct_min: float
    resource_delta_pct_max: float


@dataclass
class EpisodeResult:
    scenario: str
    mean_deviation_deg: float
    success: bool
    resource_used: float
    final_distance_m: float


def distance_to_target(ms: MissileState, target_x: float, target_y: float) -> float:
    return hypot(target_x - ms.x, target_y - ms.y)


def desired_heading_deg(ms: MissileState, target_x: float, target_y: float) -> float:
    return degrees(atan2(target_y - ms.y, target_x - ms.x))
