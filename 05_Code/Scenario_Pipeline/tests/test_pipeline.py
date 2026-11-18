from __future__ import annotations

from dataclasses import replace

import numpy as np
import pandas as pd
import pytest

from crisp_data_layer.pipeline import DataValidationError, SCENARIO_NAMES, run_data_layer


def test_pipeline_obeys_frozen_equations(default_config):
    raw = pd.read_csv(default_config.input.path)
    result = run_data_layer(raw, default_config)

    diagnostics = result.indicator_diagnostics.set_index("indicator")
    weights = diagnostics.loc[["rainfall", "sea_level", "flood_depth"], "weight"].to_numpy()
    normalized = result.event_results[["z_rainfall", "z_sea_level", "z_flood_depth"]].to_numpy()
    expected_h = normalized @ weights

    assert weights.sum() == pytest.approx(1.0)
    assert np.all(weights >= 0.0)
    assert result.event_results["H_t"].to_numpy() == pytest.approx(expected_h)
    assert list(result.scenario_summary["scenario"]) == list(SCENARIO_NAMES)
    assert result.scenario_summary["probability"].sum() == pytest.approx(1.0)
    assert result.scenario_summary["event_count"].sum() == len(result.event_results)

    summary = result.scenario_summary.set_index("scenario")
    tau_1, tau_2 = result.thresholds
    assert tau_1 == pytest.approx(
        (summary.loc["Moderate", "cluster_center_mu"] + summary.loc["Severe", "cluster_center_mu"]) / 2
    )
    assert tau_2 == pytest.approx(
        (summary.loc["Severe", "cluster_center_mu"] + summary.loc["Extreme", "cluster_center_mu"]) / 2
    )
    assert (result.event_results.query("scenario == 'Moderate'")["H_t"] < tau_1).all()
    assert (
        (result.event_results.query("scenario == 'Severe'")["H_t"] >= tau_1)
        & (result.event_results.query("scenario == 'Severe'")["H_t"] < tau_2)
    ).all()
    assert (result.event_results.query("scenario == 'Extreme'")["H_t"] >= tau_2).all()


def test_reproducible_with_same_seed(default_config):
    raw = pd.read_csv(default_config.input.path)
    first = run_data_layer(raw, default_config)
    second = run_data_layer(raw, default_config)
    pd.testing.assert_frame_equal(first.event_results, second.event_results)
    pd.testing.assert_frame_equal(first.scenario_summary, second.scenario_summary)


def test_drop_missing_is_logged(default_config):
    raw = pd.read_csv(default_config.input.path)
    raw.loc[0, default_config.columns.rainfall] = np.nan
    result = run_data_layer(raw, default_config)
    log = result.cleaning_log.set_index("metric")["value"]
    assert log["rows_removed_for_missing_indicators"] == 1
    assert log["clean_rows"] == len(raw) - 1


def test_median_imputation_preserves_row(default_config):
    raw = pd.read_csv(default_config.input.path)
    missing_row = 0
    raw.loc[missing_row, default_config.columns.flood_depth] = np.nan
    config = replace(
        default_config,
        cleaning=replace(default_config.cleaning, missing_strategy="median"),
    )
    result = run_data_layer(raw, config)
    expected = raw[default_config.columns.flood_depth].median()
    assert len(result.event_results) == len(raw)
    assert result.event_results.loc[missing_row, "flood_depth"] == pytest.approx(expected)


def test_constant_indicator_is_rejected(default_config):
    raw = pd.read_csv(default_config.input.path)
    raw[default_config.columns.sea_level] = 1.5
    with pytest.raises(DataValidationError, match="constant indicator"):
        run_data_layer(raw, default_config)


def test_duplicate_event_ids_are_rejected(default_config):
    raw = pd.read_csv(default_config.input.path)
    raw.loc[1, default_config.columns.event_id] = raw.loc[0, default_config.columns.event_id]
    with pytest.raises(DataValidationError, match="Duplicate event IDs"):
        run_data_layer(raw, default_config)


def test_third_indicator_name_propagates_to_all_outputs(default_config):
    raw = pd.read_csv(default_config.input.path).rename(
        columns={default_config.columns.third_indicator: "maximum_storm_surge_m"}
    )
    config = replace(
        default_config,
        columns=replace(
            default_config.columns,
            third_indicator="maximum_storm_surge_m",
            third_indicator_name="storm_surge",
        ),
    )
    result = run_data_layer(raw, config)
    assert "storm_surge" in result.event_results
    assert "z_storm_surge" in result.event_results
    assert "representative_storm_surge" in result.scenario_summary
    assert "w_storm_surge" in set(result.model_parameters["parameter"])
    assert "flood_depth" not in result.event_results
    assert "representative_flood_depth" not in result.scenario_summary
