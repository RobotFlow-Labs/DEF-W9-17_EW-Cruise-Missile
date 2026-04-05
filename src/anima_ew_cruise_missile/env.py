from __future__ import annotations

from dataclasses import asdict
from math import atan2, cos, degrees, hypot, pi, radians, sin
import random

import numpy as np

from .config import ModuleConfig
from .data import generate_environment_state, generate_initial_missile_state
from .modules.cyber import cyber_data_injection_deg, cyber_model_sabotage_deg, cyber_resource_cost
from .modules.deception import deception_offset_m, deception_resource_cost
from .modules.ew import ew_heading_perturbation_deg, ew_resource_cost
from .types import EpisodeResult, LayerAction, MissileState, ResourceState


def _wrap_pi(angle: float) -> float:
    while angle > pi:
        angle -= 2 * pi
    while angle < -pi:
        angle += 2 * pi
    return angle


class MultiLayerInterferenceEnv:
    """Simulation environment for layered interference against AI-guided missile behavior."""

    def __init__(self, cfg: ModuleConfig):
        self.cfg = cfg
        self.rng = random.Random(cfg.seed)
        self.ms: MissileState | None = None
        self.env = cfg.environment
        self.resources = ResourceState()
        self.step_index = 0
        self.deviation_trace_deg: list[float] = []

    def reset(self, seed: int | None = None) -> np.ndarray:
        if seed is not None:
            self.rng.seed(seed)
        self.ms = generate_initial_missile_state(self.cfg.scenario, self.rng)
        self.env = generate_environment_state(self.cfg.environment, self.rng)
        self.resources = ResourceState()
        self.step_index = 0
        self.deviation_trace_deg = []
        return self.observe()

    def observe(self) -> np.ndarray:
        if self.ms is None:
            raise RuntimeError("Call reset() first")
        dist = hypot(self.cfg.scenario.target_x - self.ms.x, self.cfg.scenario.target_y - self.ms.y)
        obs = np.array(
            [
                self.ms.x,
                self.ms.y,
                self.ms.speed,
                self.ms.heading_rad,
                dist,
                self.env.temperature_c,
                self.env.humidity,
                self.env.wind_speed,
                self.resources.resource_used,
            ],
            dtype=np.float32,
        )
        return obs

    def step(self, action: LayerAction) -> tuple[np.ndarray, float, bool, dict]:
        if self.ms is None:
            raise RuntimeError("Call reset() first")

        self.step_index += 1

        # Real target and deceptive offset.
        dx, dy = deception_offset_m(action.deception_level, self.env, self.rng)
        fake_target_x = self.cfg.scenario.target_x + dx
        fake_target_y = self.cfg.scenario.target_y + dy

        desired_heading = atan2(self.cfg.scenario.target_y - self.ms.y, self.cfg.scenario.target_x - self.ms.x)
        perceived_heading = atan2(fake_target_y - self.ms.y, fake_target_x - self.ms.x)

        # EW + cyber perturb missile guidance estimate.
        heading_bias_deg = self.rng.gauss(0.0, 0.65)
        heading_bias_deg += ew_heading_perturbation_deg(self.env, action.ew_level, self.rng)
        heading_bias_deg += cyber_data_injection_deg(action.cyber_level, self.rng)
        heading_bias_deg += cyber_model_sabotage_deg(action.cyber_level, self.rng)
        synergy = 1.0 + 0.9 * min(action.ew_level, action.cyber_level, action.deception_level)
        heading_bias_deg *= synergy
        perceived_heading += radians(heading_bias_deg)

        # Guidance update with bounded turn rate.
        max_turn = radians(5.0)
        turn_err = _wrap_pi(perceived_heading - self.ms.heading_rad)
        turn_cmd = max(-max_turn, min(max_turn, turn_err))
        self.ms.heading_rad = _wrap_pi(self.ms.heading_rad + turn_cmd)

        # Move missile.
        self.ms.x += self.ms.speed * self.cfg.scenario.dt * cos(self.ms.heading_rad)
        self.ms.y += self.ms.speed * self.cfg.scenario.dt * sin(self.ms.heading_rad)

        # Compute metrics.
        deviation_deg = abs(degrees(_wrap_pi(self.ms.heading_rad - desired_heading)))
        self.deviation_trace_deg.append(deviation_deg)
        dist = hypot(self.cfg.scenario.target_x - self.ms.x, self.cfg.scenario.target_y - self.ms.y)

        # Resource accounting.
        layer_costs = [
            ew_resource_cost(action.ew_level),
            cyber_resource_cost(action.cyber_level),
            deception_resource_cost(action.deception_level),
        ]
        dominant = max(layer_costs)
        resource_cost = dominant + 0.15 * (sum(layer_costs) - dominant)
        self.resources.resource_used += resource_cost

        reward = (
            deviation_deg * self.cfg.scenario.deviation_reward_scale
            - resource_cost * self.cfg.scenario.resource_penalty_scale
        )

        done = self.step_index >= self.cfg.scenario.steps or dist <= self.cfg.scenario.success_radius
        info = {
            "deviation_deg": deviation_deg,
            "distance_m": dist,
            "resource_used": self.resources.resource_used,
            "resource_cost": resource_cost,
            "step": self.step_index,
            "action": asdict(action),
        }
        return self.observe(), reward, done, info

    def run_episode(self, action_fn, seed: int | None = None, scenario_name: str = "custom") -> EpisodeResult:
        obs = self.reset(seed=seed)
        done = False
        final_info = {}
        while not done:
            action = action_fn(obs, self.step_index)
            obs, _reward, done, final_info = self.step(action)

        final_dev = float(final_info.get("deviation_deg", 999.0))
        success = final_dev <= 2.2
        return EpisodeResult(
            scenario=scenario_name,
            mean_deviation_deg=float(np.mean(self.deviation_trace_deg)) if self.deviation_trace_deg else 0.0,
            success=bool(success),
            resource_used=float(self.resources.resource_used),
            final_distance_m=float(final_info.get("distance_m", 0.0)),
        )
