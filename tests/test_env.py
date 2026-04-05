from anima_ew_cruise_missile.config import load_config
from anima_ew_cruise_missile.coordinator import fixed_action
from anima_ew_cruise_missile.env import MultiLayerInterferenceEnv


def test_env_step_runs():
    cfg = load_config("configs/debug.toml")
    env = MultiLayerInterferenceEnv(cfg)
    obs = env.reset(seed=11)
    action = fixed_action("baseline", cfg.action_levels)
    next_obs, reward, done, info = env.step(action)

    assert obs.shape == next_obs.shape
    assert isinstance(reward, float)
    assert "deviation_deg" in info
    assert done in (True, False)


def test_multilayer_uses_more_resources_than_baseline():
    cfg = load_config("configs/debug.toml")
    env = MultiLayerInterferenceEnv(cfg)

    b = env.run_episode(lambda _obs, _step: fixed_action("baseline", cfg.action_levels), seed=2)
    m = env.run_episode(lambda _obs, _step: fixed_action("multi_layer", cfg.action_levels), seed=2)

    assert m.resource_used > b.resource_used
