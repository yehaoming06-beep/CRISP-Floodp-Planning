"""Configuration loading and validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

import yaml


class ConfigurationError(ValueError):
    """Raised when a configuration file is invalid."""


@dataclass(frozen=True)
class InputConfig:
    path: Path


@dataclass(frozen=True)
class ColumnConfig:
    event_id: str
    rainfall: str
    sea_level: str
    third_indicator: str
    third_indicator_name: str

    @property
    def indicator_columns(self) -> tuple[str, str, str]:
        return self.rainfall, self.sea_level, self.third_indicator

    @property
    def indicator_names(self) -> tuple[str, str, str]:
        return "rainfall", "sea_level", self.third_indicator_name

    @property
    def flood_depth(self) -> str:
        """Backward-compatible source-column alias for the primary R-W-F config."""
        if self.third_indicator_name != "flood_depth":
            raise AttributeError("The configured third indicator is not flood_depth.")
        return self.third_indicator


@dataclass(frozen=True)
class CleaningConfig:
    missing_strategy: str
    duplicate_event_id: str


@dataclass(frozen=True)
class CriticConfig:
    standard_deviation_ddof: int


@dataclass(frozen=True)
class KMeansConfig:
    k: int
    random_state: int
    n_init: int
    max_iter: int


@dataclass(frozen=True)
class ScenarioConfig:
    representative_statistic: str


@dataclass(frozen=True)
class OutputConfig:
    directory: Path
    excel_filename: str


@dataclass(frozen=True)
class AppConfig:
    input: InputConfig
    columns: ColumnConfig
    cleaning: CleaningConfig
    critic: CriticConfig
    kmeans: KMeansConfig
    scenarios: ScenarioConfig
    output: OutputConfig
    source_path: Path


def _mapping(value: Any, key: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ConfigurationError(f"Configuration section '{key}' must be a mapping.")
    return value


def _resolve(base: Path, value: Any, key: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError(f"Configuration value '{key}' must be a non-empty path.")
    path = Path(value).expanduser()
    return path if path.is_absolute() else (base / path).resolve()


def load_config(path: str | Path) -> AppConfig:
    """Load YAML configuration, resolving paths relative to the YAML file."""
    source_path = Path(path).expanduser().resolve()
    if not source_path.exists():
        raise ConfigurationError(f"Configuration file not found: {source_path}")
    with source_path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)
    raw = _mapping(raw, "root")
    base = source_path.parent

    input_raw = _mapping(raw.get("input"), "input")
    columns_raw = _mapping(raw.get("columns"), "columns")
    cleaning_raw = _mapping(raw.get("cleaning", {}), "cleaning")
    critic_raw = _mapping(raw.get("critic", {}), "critic")
    kmeans_raw = _mapping(raw.get("kmeans", {}), "kmeans")
    scenarios_raw = _mapping(raw.get("scenarios", {}), "scenarios")
    output_raw = _mapping(raw.get("output"), "output")

    required_columns = ("event_id", "rainfall", "sea_level")
    missing_keys = [key for key in required_columns if not columns_raw.get(key)]
    if missing_keys:
        raise ConfigurationError(f"Missing column mappings: {', '.join(missing_keys)}")
    third_keys = [key for key in ("third_indicator", "flood_depth", "storm_surge") if columns_raw.get(key)]
    if len(third_keys) != 1:
        raise ConfigurationError(
            "columns must define exactly one third indicator mapping: "
            "third_indicator, flood_depth, or storm_surge."
        )
    third_key = third_keys[0]
    third_name = (
        str(columns_raw.get("third_indicator_name", "third_indicator"))
        if third_key == "third_indicator"
        else third_key
    )
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", third_name):
        raise ConfigurationError(
            "columns.third_indicator_name must be a valid identifier."
        )

    missing_strategy = str(cleaning_raw.get("missing_strategy", "drop")).lower()
    if missing_strategy not in {"drop", "median"}:
        raise ConfigurationError("cleaning.missing_strategy must be 'drop' or 'median'.")
    duplicate_strategy = str(cleaning_raw.get("duplicate_event_id", "error")).lower()
    if duplicate_strategy not in {"error", "keep_first", "keep_last"}:
        raise ConfigurationError(
            "cleaning.duplicate_event_id must be error, keep_first, or keep_last."
        )
    ddof = int(critic_raw.get("standard_deviation_ddof", 0))
    if ddof not in {0, 1}:
        raise ConfigurationError("critic.standard_deviation_ddof must be 0 or 1.")

    k = int(kmeans_raw.get("k", 3))
    if k != 3:
        raise ConfigurationError("Data Layer v1 fixes kmeans.k at 3.")
    n_init = int(kmeans_raw.get("n_init", 50))
    max_iter = int(kmeans_raw.get("max_iter", 300))
    if n_init < 1 or max_iter < 1:
        raise ConfigurationError("kmeans.n_init and kmeans.max_iter must be positive.")

    representative = str(scenarios_raw.get("representative_statistic", "mean")).lower()
    if representative not in {"mean", "median"}:
        raise ConfigurationError(
            "scenarios.representative_statistic must be 'mean' or 'median'."
        )

    excel_filename = str(output_raw.get("excel_filename", "crisp_data_layer_results.xlsx"))
    if Path(excel_filename).name != excel_filename or not excel_filename.lower().endswith(".xlsx"):
        raise ConfigurationError("output.excel_filename must be a plain .xlsx filename.")

    return AppConfig(
        input=InputConfig(
            path=_resolve(base, input_raw.get("path"), "input.path"),
        ),
        columns=ColumnConfig(
            event_id=str(columns_raw["event_id"]),
            rainfall=str(columns_raw["rainfall"]),
            sea_level=str(columns_raw["sea_level"]),
            third_indicator=str(columns_raw[third_key]),
            third_indicator_name=third_name,
        ),
        cleaning=CleaningConfig(missing_strategy, duplicate_strategy),
        critic=CriticConfig(ddof),
        kmeans=KMeansConfig(
            k=k,
            random_state=int(kmeans_raw.get("random_state", 42)),
            n_init=n_init,
            max_iter=max_iter,
        ),
        scenarios=ScenarioConfig(representative),
        output=OutputConfig(
            directory=_resolve(base, output_raw.get("directory"), "output.directory"),
            excel_filename=excel_filename,
        ),
        source_path=source_path,
    )
