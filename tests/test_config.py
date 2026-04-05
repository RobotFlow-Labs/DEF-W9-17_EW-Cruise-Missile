from anima_ew_cruise_missile.config import load_config


def test_load_default_config():
    cfg = load_config("configs/default.toml")
    assert cfg.scenario.steps > 0
    assert len(cfg.action_levels) >= 2
    assert cfg.paper_targets.multilayer_deviation_deg > cfg.paper_targets.baseline_deviation_deg
