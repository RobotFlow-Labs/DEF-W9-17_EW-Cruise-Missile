from __future__ import annotations

import random

from ..types import EnvironmentState


def deception_offset_m(deception_level: float, env: EnvironmentState, rng: random.Random) -> tuple[float, float]:
    """Generate fake-target displacement in meters.

    Higher humidity and heat make thermal/electromagnetic decoys more convincing.
    """
    climate_gain = 1.0 + 0.004 * max(0.0, env.temperature_c - 25.0) + 0.35 * env.humidity
    radius = deception_level * 95.0 * climate_gain
    angle = rng.uniform(0.0, 6.283185307179586)
    return radius * __import__("math").cos(angle), radius * __import__("math").sin(angle)


def deception_resource_cost(deception_level: float) -> float:
    return 0.5 * (deception_level ** 1.25)
