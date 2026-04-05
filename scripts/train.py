from __future__ import annotations

import argparse
from pathlib import Path

from anima_ew_cruise_missile.config import load_config
from anima_ew_cruise_missile.coordinator import DRLCoordinator, PolicyNetwork
from anima_ew_cruise_missile.env import MultiLayerInterferenceEnv

def _load_torch():
    import torch  # type: ignore
    return torch


def train_with_torch(config_path: str, episodes: int, seed: int, out_path: str, torch) -> None:
    cfg = load_config(config_path)
    env = MultiLayerInterferenceEnv(cfg)
    coordinator = DRLCoordinator(cfg.action_levels, seed=seed)

    policy = PolicyNetwork(input_dim=9, output_dim=len(coordinator.actions))
    optimizer = torch.optim.Adam(policy.parameters(), lr=1e-3)
    coordinator.attach_policy(policy)

    for ep in range(episodes):
        obs = env.reset(seed=seed + ep)
        done = False
        log_probs = []
        rewards = []
        while not done:
            x = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)
            logits = policy(x)
            probs = torch.softmax(logits, dim=-1)
            dist = torch.distributions.Categorical(probs)
            idx = dist.sample()
            action = coordinator.actions[int(idx.item())]
            obs, reward, done, _info = env.step(action)
            log_probs.append(dist.log_prob(idx))
            rewards.append(float(reward))

        returns = []
        running = 0.0
        for reward in reversed(rewards):
            running = reward + 0.99 * running
            returns.append(running)
        returns.reverse()
        returns_t = torch.tensor(returns, dtype=torch.float32)
        if returns_t.std().item() > 1e-8:
            returns_t = (returns_t - returns_t.mean()) / (returns_t.std() + 1e-8)

        loss = -torch.stack([lp * rt for lp, rt in zip(log_probs, returns_t)]).sum()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    torch.save(policy.state_dict(), out)
    print(f"Saved policy checkpoint to {out}")


def train_no_torch(config_path: str, episodes: int, seed: int) -> None:
    cfg = load_config(config_path)
    env = MultiLayerInterferenceEnv(cfg)
    coordinator = DRLCoordinator(cfg.action_levels, seed=seed)

    rewards = []
    for ep in range(episodes):
        obs = env.reset(seed=seed + ep)
        done = False
        total = 0.0
        while not done:
            action = coordinator.select_action(obs, explore_eps=0.3)
            obs, reward, done, _ = env.step(action)
            total += reward
        rewards.append(total)
    print(f"torch not available; completed heuristic training loop, mean reward={sum(rewards)/len(rewards):.3f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Train EW-Cruise-Missile coordinator")
    parser.add_argument("--config", default="configs/paper.toml")
    parser.add_argument("--episodes", type=int, default=40)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--out", default="checkpoints/policy.pt")
    parser.add_argument("--backend", choices=["heuristic", "torch"], default="heuristic")
    args = parser.parse_args()

    if args.backend == "heuristic":
        train_no_torch(args.config, args.episodes, args.seed)
        return

    torch = _load_torch()
    train_with_torch(args.config, args.episodes, args.seed, args.out, torch)


if __name__ == "__main__":
    main()
