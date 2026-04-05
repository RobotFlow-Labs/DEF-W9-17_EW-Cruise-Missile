from anima_ew_cruise_missile.eval import evaluate


def test_eval_report_structure():
    report = evaluate("configs/debug.toml", episodes_per_scenario=5, seed=1)
    assert "scenarios" in report
    assert "comparison" in report
    assert "baseline" in report["scenarios"]
    assert "multi_layer" in report["scenarios"]
