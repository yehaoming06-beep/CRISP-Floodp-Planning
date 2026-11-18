# Research code index

Original scientific code retains its original paths and bytes. New portable execution adapters are documented in [submission/PORTABILITY.md](submission/PORTABILITY.md); run `python -I src/reproduce_submission.py all --output results/reproductions/all_001` after installing dependencies. Programs derive project roots from `__file__` and reference the numbered directories.

| Role | Canonical code |
| --- | --- |
| CRITIC / one-dimensional K-means | [pipeline.py](../05_Code/Scenario_Pipeline/src/crisp_data_layer/pipeline.py), [config](../05_Code/Scenario_Pipeline/src/crisp_data_layer/config.py), [CLI](../05_Code/Scenario_Pipeline/src/crisp_data_layer/cli.py) |
| Model / parameters | [crisp_model.py](../02_Model/crisp_model.py), [crisp_parameters.py](../02_Model/crisp_parameters.py), [MODEL.md](../02_Model/MODEL.md) |
| Original-23 optimization | [design](../03_Experiments/Optimization/code/experiment_design.py), [runner](../03_Experiments/Optimization/code/run_experiments.py) |
| Original-23 stability | [run_analysis.py](../03_Experiments/Scenario_Stability/code/run_analysis.py) |
| Existing independent optimization check | [verify_results.py](../03_Experiments/Optimization/code/verify_results.py) |
| Final-60 source/scenario reconstruction | [reconstruct.py](../manuscript_revision/audit/ci01_independent_20261104/code/reconstruct.py), [assess_scenarios.py](../manuscript_revision/audit/ci01_independent_20261104/code/assess_scenarios.py) |
| Final-60 probability-only backend | [run_backend.py](../manuscript_revision/audit/ci01_independent_20261104/code/run_backend.py) |
| Supplementary primary/independent validation | [run_validation.py](../manuscript_revision/peer_review_validation_20261105_v2/code/run_validation.py), [verify_independent.py](../manuscript_revision/peer_review_validation_20261105_v2/code/verify_independent.py) |
| Current delivery file/evidence check | [verify_delivery.py](verify_delivery.py) |
| Historical whole-import audit | [audit_repository.py](audit_repository.py) |

Run `python3.12 src/verify_delivery.py` for the current reviewed file list, SHA-256, complete compressed evidence, S1–S13 links and stored 555 counts. Add `--restore-evidence` only when inspecting historical paths: archived files are restored exactly, and differing files are refused. This package check does not solve models or certify field data. Full numerical commands are in [REPRODUCE.md](../REPRODUCE.md).

`audit_repository.py` is retained as an earlier whole-import audit. It expects the larger historical import corpus and old hold policy; its `--submission-policy` flag is not a validator for the present lean selection. Some original validators likewise require the complete historical workspace and write outputs. Their historical PASS records and guards have not been reset. See [dependency evidence](../audit/Dependency_Evidence.md) and [current selection](../audit/delivery_20261118/DELIVERY_REPORT.md).
