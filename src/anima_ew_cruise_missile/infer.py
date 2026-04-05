from __future__ import annotations

import argparse
import json

from .config import load_config
from .coordinator import DRLCoordinator, fixed_action
from .env import MultiLayerInterferenceEnv


SCENARIOS = ["baseline", "ew_only", "cyber_only", "deception_only", "multi_layer", "adaptive"]


def run_scenario(config_path: str, scenario: str, episodes: int, seed: int) -> dict:
    cfg = load_config(config_path)
    env = MultiLayerInterferenceEnv(cfg)
    coordinator = DRLCoordinator(cfg.action_levels, seed=seed)

    results = []
    for i in range(episodes):
        ep_seed = seed + i
        if scenario in SCENARIOS[:-1]:
            fixed = fixed_action(scenario, cfg.action_levels)
            action_fn = lambda _obs, _step, action=fixed: action
        else:
            action_fn = lambda obs, _step: coordinator.select_action(obs, explore_eps=0.0)

        results.append(env.run_episode(action_fn, seed=ep_seed, scenario_name=scenario))

    mean_deviation = sum(r.mean_deviation_deg for r in results) / len(results)
    success_rate = 100.0 * sum(1 for r in results if r.success) / len(results)
    resource = sum(r.resource_used for r in results) / len(results)

    return {
        "scenario": scenario,
        "episodes": episodes,
        "mean_deviation_deg": round(mean_deviation, 3),
        "success_rate_pct": round(success_rate, 2),
        "mean_resource_used": round(resource, 3),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run EW-Cruise-Missile inference scenarios")
    parser.add_argument("--config", default="configs/default.toml")
    parser.add_argument("--scenario", choices=SCENARIOS, default="adaptive")
    parser.add_argument("--episodes", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    print(json.dumps(run_scenario(args.config, args.scenario, args.episodes, args.seed), indent=2))


if __name__ == "__main__":
    main()
