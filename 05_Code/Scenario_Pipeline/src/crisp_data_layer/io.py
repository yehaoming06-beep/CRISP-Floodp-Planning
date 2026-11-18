"""Input and output helpers for CSV, Excel, and JSON payloads."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from .config import AppConfig
from .pipeline import DataLayerResult


def read_events(config: AppConfig) -> pd.DataFrame:
    path = config.input.path
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    raise ValueError("Input must be a .csv file.")


def _json_safe(value: Any) -> Any:
    if value is None or value is pd.NA:
        return None
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        return None if not np.isfinite(value) else float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    return value


def _frame_payload(frame: pd.DataFrame) -> dict[str, Any]:
    return {
        "columns": [str(column) for column in frame.columns],
        "rows": [[_json_safe(value) for value in row] for row in frame.itertuples(index=False, name=None)],
    }


def _find_node() -> str:
    configured = os.environ.get("CRISP_NODE_EXECUTABLE")
    if configured:
        return configured
    found = shutil.which("node")
    if found:
        return found
    raise RuntimeError(
        "Node.js is required for styled Excel export. Set CRISP_NODE_EXECUTABLE to its path."
    )


def write_outputs(result: DataLayerResult, config: AppConfig, *, export_excel: bool = True) -> list[Path]:
    output_dir = config.output.directory
    output_dir.mkdir(parents=True, exist_ok=True)
    frames = {
        "event_results": result.event_results,
        "scenario_summary": result.scenario_summary,
        "indicator_diagnostics": result.indicator_diagnostics,
        "model_parameters": result.model_parameters,
        "cleaning_log": result.cleaning_log,
    }
    paths: list[Path] = []
    for name, frame in frames.items():
        path = output_dir / f"{name}.csv"
        frame.to_csv(path, index=False, encoding="utf-8")
        paths.append(path)

    if export_excel:
        payload_path = output_dir / ".workbook_payload.json"
        payload = {
            "method": {
                "title": "CRISP Data Layer v1",
                "description": "Min-Max normalization; CRITIC weights; H_t weighted sum; one-dimensional K-means (K=3).",
                "tau_1": result.thresholds[0],
                "tau_2": result.thresholds[1],
                "source_config": str(config.source_path),
                "source_data": str(config.input.path),
                "indicator_names": list(config.columns.indicator_names),
            },
            "sheets": {
                "Raw Input": _frame_payload(result.raw_events),
                "Event Results": _frame_payload(result.event_results),
                "Scenario Summary": _frame_payload(result.scenario_summary),
                "Indicator Diagnostics": _frame_payload(result.indicator_diagnostics),
                "Model Parameters": _frame_payload(result.model_parameters),
                "Cleaning Log": _frame_payload(result.cleaning_log),
            },
        }
        payload_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        workbook_path = output_dir / config.output.excel_filename
        script = Path(__file__).with_name("export_workbook.mjs")
        try:
            completed = subprocess.run(
                [_find_node(), str(script), str(payload_path), str(workbook_path)],
                check=False,
                capture_output=True,
                text=True,
            )
            if completed.returncode != 0:
                detail = completed.stderr.strip() or completed.stdout.strip()
                raise RuntimeError(f"Excel export failed: {detail}")
        finally:
            payload_path.unlink(missing_ok=True)
        workbook_path.with_name(workbook_path.name + ".inspect.ndjson").unlink(missing_ok=True)
        paths.append(workbook_path)
    return paths
