from anima_ew_cruise_missile.infer import run_scenario


def test_infer_returns_expected_keys():
    out = run_scenario("configs/debug.toml", scenario="adaptive", episodes=3, seed=42)
    assert out["scenario"] == "adaptive"
    assert "mean_deviation_deg" in out
    assert "success_rate_pct" in out
    assert out["episodes"] == 3
