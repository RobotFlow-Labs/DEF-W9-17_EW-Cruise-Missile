from __future__ import annotations

import argparse


def recommend_batch_size(gpu_mem_gb: float, target_util: float = 0.75) -> int:
    usable = gpu_mem_gb * target_util
    # Conservative heuristic for this module's baseline policy model + simulator overhead.
    if usable < 8:
        return 32
    if usable < 14:
        return 64
    if usable < 18:
        return 96
    return 128


def main() -> None:
    parser = argparse.ArgumentParser(description="Recommend batch size for EW-Cruise-Missile")
    parser.add_argument("--gpu-mem-gb", type=float, default=23.0)
    parser.add_argument("--target", type=float, default=0.75)
    args = parser.parse_args()
    rec = recommend_batch_size(args.gpu_mem_gb, args.target)
    print(f"recommended_batch_size={rec}")


if __name__ == "__main__":
    main()
