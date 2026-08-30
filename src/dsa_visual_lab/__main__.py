"""Command-line entry point for the visual lab."""

from __future__ import annotations

import argparse

from dsa_visual_lab.gui.app import check_runtime, launch


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Interactive Data Structures & Algorithms Visual Lab",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="run a no-window startup check",
    )
    args = parser.parse_args()

    if args.check:
        print(check_runtime())
        return

    launch()


if __name__ == "__main__":
    main()
