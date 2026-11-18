"""Core implementation of the frozen CRISP Data Layer v1 method."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from .config import AppConfig


SCENARIO_NAMES = ("Moderate", "Severe", "Extreme")


class DataValidationError(ValueError):
    """Raised when event data cannot support the frozen method."""


@dataclass
class DataLayerResult:
    raw_events: pd.DataFrame
    event_results: pd.DataFrame
    scenario_summary: pd.DataFrame
    indicator_diagnostics: pd.DataFrame
    model_parameters: pd.DataFrame
    cleaning_log: pd.DataFrame

    @property
    def thresholds(self) -> tuple[float, float]:
        values = self.model_parameters.set_index("parameter")["value"]
        return float(values["tau_1"]), float(values["tau_2"])


def _clean_events(raw: pd.DataFrame, config: AppConfig) -> tuple[pd.DataFrame, pd.DataFrame]:
    columns = config.columns
    required = [columns.event_id, *columns.indicator_columns]
    missing = [name for name in required if name not in raw.columns]
    if missing:
        raise DataValidationError(f"Input is missing required columns: {', '.join(missing)}")

    working = raw.loc[:, required].copy()
    log: list[dict[str, Any]] = [
        {"metric": "input_rows", "value": len(working), "detail": "Rows read from source"}
    ]
    blank_ids = working[columns.event_id].isna() | working[columns.event_id].astype(str).str.strip().eq("")
    if blank_ids.any():
        raise DataValidationError(f"{int(blank_ids.sum())} row(s) have a missing event ID.")
    working[columns.event_id] = working[columns.event_id].astype(str).str.strip()

    duplicated = working[columns.event_id].duplicated(keep=False)
    duplicate_ids = sorted(working.loc[duplicated, columns.event_id].unique().tolist())
    if duplicate_ids and config.cleaning.duplicate_event_id == "error":
        preview = ", ".join(duplicate_ids[:5])
        raise DataValidationError(f"Duplicate event IDs found: {preview}")
    before_duplicates = len(working)
    if duplicate_ids:
        keep = "first" if config.cleaning.duplicate_event_id == "keep_first" else "last"
        working = working.drop_duplicates(columns.event_id, keep=keep)
    log.append(
        {
            "metric": "duplicate_rows_removed",
            "value": before_duplicates - len(working),
            "detail": config.cleaning.duplicate_event_id,
        }
    )

    for column in columns.indicator_columns:
        original_missing = int(working[column].isna().sum())
        converted = pd.to_numeric(working[column], errors="coerce").replace([np.inf, -np.inf], np.nan)
        invalid = int(converted.isna().sum()) - original_missing
        working[column] = converted
        log.append(
            {
                "metric": f"invalid_numeric_{column}",
                "value": max(invalid, 0),
                "detail": "Non-numeric or infinite values converted to missing",
            }
        )

    missing_cells = int(working.loc[:, columns.indicator_columns].isna().sum().sum())
    before_missing = len(working)
    if config.cleaning.missing_strategy == "drop":
        working = working.dropna(subset=list(columns.indicator_columns)).copy()
        imputed_cells = 0
    else:
        medians = working.loc[:, columns.indicator_columns].median(axis=0, skipna=True)
        if medians.isna().any():
            bad = medians[medians.isna()].index.tolist()
            raise DataValidationError(f"Cannot median-impute columns with no valid values: {bad}")
        working.loc[:, columns.indicator_columns] = working.loc[:, columns.indicator_columns].fillna(medians)
        imputed_cells = missing_cells
    log.extend(
        [
            {
                "metric": "rows_removed_for_missing_indicators",
                "value": before_missing - len(working),
                "detail": config.cleaning.missing_strategy,
            },
            {
                "metric": "indicator_cells_imputed",
                "value": imputed_cells,
                "detail": config.cleaning.missing_strategy,
            },
            {"metric": "clean_rows", "value": len(working), "detail": "Rows entering analysis"},
        ]
    )

    if len(working) < 3:
        raise DataValidationError("At least 3 clean events are required for K=3.")
    working = working.reset_index(drop=True)
    return working, pd.DataFrame(log)


def _minmax_and_critic(
    clean: pd.DataFrame, config: AppConfig
) -> tuple[pd.DataFrame, pd.DataFrame, np.ndarray]:
    source_columns = config.columns.indicator_columns
    indicator_names = config.columns.indicator_names
    matrix = clean.loc[:, source_columns].to_numpy(dtype=float)
    minima = matrix.min(axis=0)
    maxima = matrix.max(axis=0)
    ranges = maxima - minima
    constant = [indicator_names[i] for i, value in enumerate(ranges) if np.isclose(value, 0.0)]
    if constant:
        raise DataValidationError(
            "CRITIC is undefined for constant indicator column(s): " + ", ".join(constant)
        )
    normalized = (matrix - minima) / ranges
    normalized_df = pd.DataFrame(
        normalized,
        columns=[f"z_{name}" for name in indicator_names],
        index=clean.index,
    )

    std = normalized_df.std(axis=0, ddof=config.critic.standard_deviation_ddof).to_numpy()
    correlation = normalized_df.corr(method="pearson").to_numpy()
    if not np.isfinite(correlation).all():
        raise DataValidationError("CRITIC correlation matrix contains undefined values.")
    conflict = np.sum(1.0 - correlation, axis=1)
    information = std * conflict
    total_information = float(information.sum())
    if not np.isfinite(total_information) or np.isclose(total_information, 0.0):
        raise DataValidationError(
            "CRITIC information content sums to zero; indicators do not provide separable information."
        )
    weights = information / total_information

    diagnostics = pd.DataFrame(
        {
            "indicator": indicator_names,
            "source_column": source_columns,
            "minimum": minima,
            "maximum": maxima,
            "normalized_std": std,
            "conflict": conflict,
            "information_content": information,
            "weight": weights,
        }
    )
    for i, name in enumerate(indicator_names):
        diagnostics[f"corr_{name}"] = correlation[:, i]
    return normalized_df, diagnostics, weights


def _cluster_severity(
    severity: np.ndarray, config: AppConfig
) -> tuple[np.ndarray, np.ndarray, float, float]:
    if np.unique(np.round(severity, decimals=14)).size < 3:
        raise DataValidationError("At least 3 distinct H_t values are required for K=3.")
    model = KMeans(
        n_clusters=3,
        random_state=config.kmeans.random_state,
        n_init=config.kmeans.n_init,
        max_iter=config.kmeans.max_iter,
        algorithm="lloyd",
    )
    model.fit(severity.reshape(-1, 1))
    centers = np.sort(model.cluster_centers_.ravel())
    if np.unique(np.round(centers, decimals=14)).size < 3:
        raise DataValidationError("K-means did not produce three distinct cluster centers.")
    tau_1 = float((centers[0] + centers[1]) / 2.0)
    tau_2 = float((centers[1] + centers[2]) / 2.0)
    labels = np.select(
        [severity < tau_1, severity < tau_2],
        [SCENARIO_NAMES[0], SCENARIO_NAMES[1]],
        default=SCENARIO_NAMES[2],
    )
    return labels.astype(str), centers, tau_1, tau_2


def run_data_layer(raw_events: pd.DataFrame, config: AppConfig) -> DataLayerResult:
    """Run cleaning, Min-Max, CRITIC, H_t, K=3 clustering, and scenario estimation."""
    clean, cleaning_log = _clean_events(raw_events, config)
    normalized, diagnostics, weights = _minmax_and_critic(clean, config)
    severity = normalized.to_numpy() @ weights
    labels, centers, tau_1, tau_2 = _cluster_severity(severity, config)

    indicator_names = config.columns.indicator_names
    third_indicator_name = config.columns.third_indicator_name
    events = clean.copy()
    events.columns = ["event_id", *indicator_names]
    events = pd.concat([events, normalized], axis=1)
    events["H_t"] = severity
    events["scenario"] = labels

    statistic = config.scenarios.representative_statistic
    summary_rows: list[dict[str, Any]] = []
    for index, scenario in enumerate(SCENARIO_NAMES):
        subset = events.loc[events["scenario"] == scenario]
        if subset.empty:
            raise DataValidationError(f"K-means produced an empty scenario: {scenario}")
        representative = subset.loc[:, indicator_names].agg(statistic)
        summary_rows.append(
            {
                "scenario": scenario,
                "cluster_center_mu": centers[index],
                "lower_H_bound": np.nan if index == 0 else (tau_1 if index == 1 else tau_2),
                "upper_H_bound": tau_1 if index == 0 else (tau_2 if index == 1 else np.nan),
                "event_count": len(subset),
                "probability": len(subset) / len(events),
                "representative_rainfall": representative["rainfall"],
                "representative_sea_level": representative["sea_level"],
                f"representative_{third_indicator_name}": representative[third_indicator_name],
                "representative_statistic": statistic,
            }
        )
    scenario_summary = pd.DataFrame(summary_rows)

    parameters: list[dict[str, Any]] = [
        {"parameter": "tau_1", "value": tau_1, "detail": "(mu_1 + mu_2) / 2"},
        {"parameter": "tau_2", "value": tau_2, "detail": "(mu_2 + mu_3) / 2"},
        {"parameter": "mu_1", "value": centers[0], "detail": "Moderate center"},
        {"parameter": "mu_2", "value": centers[1], "detail": "Severe center"},
        {"parameter": "mu_3", "value": centers[2], "detail": "Extreme center"},
        {"parameter": "random_state", "value": config.kmeans.random_state, "detail": "K-means seed"},
        {"parameter": "n_init", "value": config.kmeans.n_init, "detail": "K-means initializations"},
        {"parameter": "clean_event_count", "value": len(events), "detail": "N"},
    ]
    parameters.extend(
        {"parameter": f"w_{name}", "value": weights[i], "detail": "CRITIC weight"}
        for i, name in enumerate(indicator_names)
    )

    return DataLayerResult(
        raw_events=raw_events.copy(),
        event_results=events,
        scenario_summary=scenario_summary,
        indicator_diagnostics=diagnostics,
        model_parameters=pd.DataFrame(parameters),
        cleaning_log=cleaning_log,
    )
