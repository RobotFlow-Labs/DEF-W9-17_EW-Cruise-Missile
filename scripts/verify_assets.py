from __future__ import annotations

from pathlib import Path

REQUIRED = [
    "ASSETS.md",
    "PRD.md",
    "NEXT_STEPS.md",
    "papers/2510.03542.pdf",
    "prds/PRD-01-foundation.md",
    "prds/PRD-07-production.md",
    "tasks/INDEX.md",
    "anima_module.yaml",
]


def main() -> None:
    missing = [p for p in REQUIRED if not Path(p).exists()]
    if missing:
        print("MISSING:")
        for item in missing:
            print(f"- {item}")
        raise SystemExit(1)
    print("asset_preflight=PASS")


if __name__ == "__main__":
    main()
