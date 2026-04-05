from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import random

import numpy as np

from .types import EnvironmentState, LayerAction

@dataclass
class ActionSpace:
    levels: list[float]

    def all_actions(self) -> list[LayerAction]:
        return [LayerAction(*vals) for vals in product(self.levels, repeat=3)]


def _load_torch():
    try:  # pragma: no cover - optional dependency
        import torch  # type: ignore
        from torch import nn  # type: ignore
    except Exception:
        return None, None
    return torch, nn


class PolicyNetwork:
    """Simple MLP policy over flattened state with lazy torch import."""

    def __init__(self, input_dim: int, output_dim: int):
        torch, nn = _load_torch()
        if torch is None or nn is None:
            raise RuntimeError("torch is required for PolicyNetwork")
        self.torch = torch
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, output_dim),
        )

    def __call__(self, x):
        return self.net(x)

    def parameters(self):
        return self.net.parameters()

    def state_dict(self):
        return self.net.state_dict()


class DRLCoordinator:
    """Action selector that supports learned policy or heuristic fallback."""

    def __init__(self, levels: list[float], seed: int = 0):
        self.action_space = ActionSpace(levels)
        self.actions = self.action_space.all_actions()
        self.rng = random.Random(seed)
        self.policy = None

    def attach_policy(self, policy) -> None:
        self.policy = policy

    def select_action(self, obs: np.ndarray, explore_eps: float = 0.05) -> LayerAction:
        if self.rng.random() < explore_eps:
            return self.rng.choice(self.actions)

        if self.policy is not None:
            torch = getattr(self.policy, "torch", None)
            if torch is not None:
                x = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)
                with torch.no_grad():
                    logits = self.policy(x)
                idx = int(torch.argmax(logits, dim=-1).item())
                return self.actions[idx]

        return self.heuristic_action(
            temperature=float(obs[5]),
            humidity=float(obs[6]),
            wind_speed=float(obs[7]),
            dist=float(obs[4]),
        )

    def heuristic_action(self, temperature: float, humidity: float, wind_speed: float, dist: float) -> LayerAction:
        hi = max(self.action_space.levels)
        mid = self.action_space.levels[len(self.action_space.levels) // 2]
        lo = min(self.action_space.levels)

        ew = hi if wind_speed > 7.0 or humidity > 0.7 else mid
        cyber = hi if dist > 700.0 else mid
        deception = hi if temperature > 42.0 else lo
        return LayerAction(ew_level=ew, cyber_level=cyber, deception_level=deception)


def fixed_action(mode: str, levels: list[float]) -> LayerAction:
    lo = min(levels)
    hi = max(levels)
    if mode == "baseline":
        return LayerAction(lo, lo, lo)
    if mode == "ew_only":
        return LayerAction(hi, lo, lo)
    if mode == "cyber_only":
        return LayerAction(lo, hi, lo)
    if mode == "deception_only":
        return LayerAction(lo, lo, hi)
    if mode == "multi_layer":
        return LayerAction(hi, hi, hi)
    raise ValueError(f"Unknown fixed mode: {mode}")


def env_to_obs_hint(env: EnvironmentState) -> np.ndarray:
    return np.array([0.0, 0.0, 0.0, 0.0, 1000.0, env.temperature_c, env.humidity, env.wind_speed, 0.0])
