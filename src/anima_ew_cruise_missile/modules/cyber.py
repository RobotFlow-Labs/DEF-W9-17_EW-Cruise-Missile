from __future__ import annotations

import random


def cyber_data_injection_deg(cyber_level: float, rng: random.Random) -> float:
    """Injected data bias from communication tampering."""
    return rng.gauss(0.0, cyber_level * 2.6)


def cyber_model_sabotage_deg(cyber_level: float, rng: random.Random) -> float:
    """Approximation of onboard model-weight perturbation effect."""
    return rng.uniform(-1.0, 1.0) * (cyber_level ** 1.3) * 2.1


def cyber_resource_cost(cyber_level: float) -> float:
    return 0.45 * (cyber_level ** 1.2)
