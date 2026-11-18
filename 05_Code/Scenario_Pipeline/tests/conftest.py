from __future__ import annotations

from pathlib import Path

import pytest

from crisp_data_layer.config import load_config


@pytest.fixture
def default_config():
    return load_config(Path(__file__).parents[1] / "config" / "default.yaml")

