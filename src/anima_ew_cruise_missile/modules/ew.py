from __future__ import annotations

import random

from ..types import EnvironmentState


def ew_heading_perturbation_deg(env: EnvironmentState, ew_level: float, rng: random.Random) -> float:
    """Return heading perturbation in degrees caused by EW.

    Modeled as a mix of random jamming plus climate-amplified propagation effects.
    """
    climate_factor = 1.0 + 0.008 * max(0.0, env.temperature_c - 30.0) + 0.5 * env.humidity
    wind_factor = 1.0 + min(0.35, env.wind_speed / 40.0)
    sigma = ew_level * 3.8 * climate_factor * wind_factor
    return rng.gauss(0.0, sigma)


def ew_resource_cost(ew_level: float) -> float:
    return 0.55 * (ew_level ** 1.4)
