"""Command-line interface."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import ConfigurationError, load_config
from .io import read_events, write_outputs
from .pipeline import DataValidationError, run_data_layer


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run CRISP Data Layer v1.")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/default.yaml"),
        help="YAML configuration file (default: config/default.yaml)",
    )
    parser.add_argument(
        "--no-excel",
        action="store_true",
        help="Write CSV files only; skip the styled Excel workbook.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        config = load_config(args.config)
        raw = read_events(config)
        result = run_data_layer(raw, config)
        paths = write_outputs(result, config, export_excel=not args.no_excel)
    except (ConfigurationError, DataValidationError, FileNotFoundError, ValueError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    print("CRISP Data Layer v1 completed.")
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

