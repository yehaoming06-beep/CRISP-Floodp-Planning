from __future__ import annotations

from pathlib import Path

import pytest

from crisp_data_layer.config import ConfigurationError, load_config


def test_paths_are_resolved_relative_to_config(default_config):
    assert default_config.input.path.is_absolute()
    assert default_config.input.path.name == "sample_events.csv"
    assert default_config.output.directory.is_absolute()


def test_k_is_frozen_at_three(tmp_path: Path):
    config = tmp_path / "bad.yaml"
    config.write_text(
        """
input: {path: events.csv}
columns: {event_id: id, rainfall: r, sea_level: w, flood_depth: f}
kmeans: {k: 4}
output: {directory: out, excel_filename: result.xlsx}
""",
        encoding="utf-8",
    )
    with pytest.raises(ConfigurationError, match="fixes kmeans.k at 3"):
        load_config(config)


def test_storm_surge_can_be_named_as_third_indicator(tmp_path: Path):
    events = tmp_path / "events.csv"
    events.write_text("id,r,w,s\nE1,1,2,3\n", encoding="utf-8")
    config = tmp_path / "fallback.yaml"
    config.write_text(
        """
input: {path: events.csv}
columns: {event_id: id, rainfall: r, sea_level: w, storm_surge: s}
output: {directory: out, excel_filename: result.xlsx}
""",
        encoding="utf-8",
    )
    loaded = load_config(config)
    assert loaded.columns.indicator_names == ("rainfall", "sea_level", "storm_surge")
    assert loaded.columns.indicator_columns == ("r", "w", "s")
