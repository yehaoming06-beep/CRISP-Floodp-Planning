# Scenario data pipeline

The package under src/crisp_data_layer implements CRITIC weighting and one-dimensional K-means. The fallback configuration reads the common 23-event dataset in 01_Data/Events. Source archives are in 01_Data/Sources; no second data copy or local environment is stored here.

Run tests from the project root:

```sh
PYTHONPATH=05_Code/Scenario_Pipeline/src .venv/bin/python -m pytest -p no:cacheprovider 05_Code/Scenario_Pipeline/tests -q
```

The default.yaml configuration and sample_events.csv are synthetic test/example inputs. The fallback.yaml configuration is the actual R-W-storm-surge case. Storm surge is not Tai O flood depth.
