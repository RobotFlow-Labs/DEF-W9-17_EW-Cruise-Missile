from __future__ import annotations

import argparse
import json

from .config import load_config
from .infer import run_scenario


def evaluate(config_path: str, episodes_per_scenario: int, seed: int) -> dict:
    cfg = load_config(config_path)
    scenario_order = ["baseline", "ew_only", "cyber_only", "multi_layer"]
    by_scenario = {}

    for idx, scenario in enumerate(scenario_order):
        by_scenario[scenario] = run_scenario(
            config_path=config_path,
            scenario=scenario,
            episodes=episodes_per_scenario,
            seed=seed + idx * 1000,
        )

    baseline = by_scenario["baseline"]
    multi = by_scenario["multi_layer"]

    single_layer_ref = max(by_scenario["ew_only"]["mean_resource_used"], by_scenario["cyber_only"]["mean_resource_used"])
    resource_delta_pct = 100.0 * (multi["mean_resource_used"] - single_layer_ref) / max(single_layer_ref, 1e-6)

    comparison = {
        "paper_targets": {
            "baseline_deviation_deg": cfg.paper_targets.baseline_deviation_deg,
            "multilayer_deviation_deg": cfg.paper_targets.multilayer_deviation_deg,
            "baseline_success_pct": cfg.paper_targets.baseline_success_pct,
            "multilayer_success_pct": cfg.paper_targets.multilayer_success_pct,
            "resource_delta_range_pct": [
                cfg.paper_targets.resource_delta_pct_min,
                cfg.paper_targets.resource_delta_pct_max,
            ],
        },
        "measured": {
            "baseline_deviation_deg": baseline["mean_deviation_deg"],
            "multilayer_deviation_deg": multi["mean_deviation_deg"],
            "baseline_success_pct": baseline["success_rate_pct"],
            "multilayer_success_pct": multi["success_rate_pct"],
            "resource_delta_pct": round(resource_delta_pct, 2),
        },
    }

    return {
        "episodes_per_scenario": episodes_per_scenario,
        "scenarios": by_scenario,
        "comparison": comparison,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate EW-Cruise-Missile scenarios")
    parser.add_argument("--config", default="configs/paper.toml")
    parser.add_argument("--episodes-per-scenario", type=int, default=100)
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args()

    report = evaluate(args.config, args.episodes_per_scenario, args.seed)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
