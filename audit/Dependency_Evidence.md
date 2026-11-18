# CRISP source and dependency audit

Date: 2026-11-18 (Asia/Shanghai). Scope: read-only source/metadata audit, no research script executed, no scientific originals changed. Source root: `/Users/yehaoming/Desktop/climate_Devin`.

## Layout decision

Preserve native `01_Data`, `02_Model`, `03_Experiments`, `04_Results`, `05_Code` and relevant `manuscript_revision` paths at repository root. Top-level `data/`, `src/`, `results/`, `supplementary/` may be navigation indexes rather than duplicate scientific files. This is preferable to moving .py files: sources derive project root through `Path(__file__).resolve().parents` and hard-code numbered paths. Renaming directories requires code edits and invalidates historical hashes. No wrapper is needed for the documented commands.

## Scientific code found

| Role | Canonical source | Observations |
|---|---|---|
| CRITIC / 1D K-means | `05_Code/Scenario_Pipeline/src/crisp_data_layer/pipeline.py` | Package configuration, CSV I/O and CLI alongside; `config/fallback.yaml` is actual 23-event R/W/storm-surge case. `default.yaml` and `examples/sample_events.csv` are explicitly synthetic test/example assets, not substitutes for missing scientific files. |
| Frozen 23-event stability | `03_Experiments/Scenario_Stability/code/run_analysis.py` | Reads `01_Data/Events/model_input.csv` and `event_metadata.csv`; asserts N=23; CRITIC, bootstrap/year-block/subsample/LOYO and exact 1D partition checks. |
| Mobile inventory model | `02_Model/crisp_model.py`, `crisp_parameters.py` | Reads master XLSX and protocol; Gurobi optimization; retains illustrative CU and benefit-score interpretation. |
| Frozen original 555 configurations | `03_Experiments/Optimization/code/run_experiments.py`, `experiment_design.py` | Default new output `04_Results/Reproductions/<run-id>`; refuses existing output directory. This is the original23 workflow, not final60 reconstruction. |
| Original555 independent checks | `03_Experiments/Optimization/code/verify_results.py` | Uses SciPy/HiGHS, checks all555 RP optima, compares against pre-cleanup metrics, writes `independent_verification.json`. |
| EV ties | `03_Experiments/Optimization/code/audit_ev_ties.py` | Enumerates EV optimum policies separately from main solver counts. |
| Final60 reconstruction | `manuscript_revision/audit/ci01_independent_20261104/code/reconstruct.py`, `hko_parse.py` | Offline source reconstruction; needs archived HKO responses, sources/ranges/PDF text/evidence and snapshots. Writes derived outputs. |
| Final60 scenarios | Same code directory: `assess_scenarios.py`, `verify_tides_and_spatial.py` | Uses snapshot pipeline and config, original23 comparison data, final source QC. |
| Final60 555 backend | Same: `run_backend.py`, `audit_backend_ev_ties.py` | Imports models and design from audit snapshots, updates only conditional probabilities; new named output refuses overwrite. |
| Peer-review500 | `manuscript_revision/peer_review_validation_20261105_v2/code/run_validation.py` | Separate 500 calls,498 optimal/2 infeasible expected in saved records; snapshots18 files,419716 bytes; does not rerun frozen555. |
| Peer-review independent500 | Same: `verify_independent.py` | Independent matrices/HiGHS, reads fixed `runs/primary` and writes fixed `independent_validation`. |
| Mapping | `05_Code/build_study_area.py` | shapely,pyproj,reportlab; ancillary study-area artifact. |

Copies in `audit/ci01_integration_20261105/before`, `audit/.../snapshots`, `stages/v1_before_secondary_tide_crosscheck`, and peer-review v1 are historical versions. In particular reconstructed61 and backend_probability61 are not final60. Preserve labels rather than silently promoting them.

## Reproduction limits

- Do not advertise every saved validation as an executable read-only check. `verify_results.py`, scenario verifier, CI01 `verify_delivery.py`, v2 `verify_delivery.py`, `verify_independent.py`, `finalize_artifacts.py` and scenario-chain audit write report or derived files. Run in an isolated complete copy if author chooses to repeat them.
- v2 `run_validation.py` reads `frozen_manifest_before.json` at line161; lines264–266 hash all21678 originals relative to project root and assert no missing/changed originals even with a new `--output`. v2 `verify_delivery.py` does the same at lines77–80. A selected export missing original copyrighted sources or legacy material cannot pass this whole-workspace guard unchanged. Record this portability limit explicitly.
- CI01 `verify_delivery.py` lines20–22 checks977 original paths and snapshot hashes; snapshots contain977 files/108745241 bytes. It also reruns three derivation scripts and checks saved backend/replay, PDFs, source freezes. A reduced package must report missing guarded files, not call this guard passed.
- Baseline optimization verifier needs `01_Data/Controls/pre_cleanup_metrics.json`; hashes in run manifests require byte-identical master data, model, protocol and runner source.
- XLSX formatting requires Node.js plus `@oai/artifact-tool` (`export_workbook.mjs` and `build_workbook.mjs`). No Node package manifest/lock was found. The CLI supports `--no-excel` for scientific CSV outputs; Python requirements alone do not reproduce styled workbooks.
- Gurobi requires a usable license. License availability was not tested, no solver was invoked.
- Existing `复现当前实验.command` expects `.venv/bin/python`, is macOS/zsh-specific, and runs original23 baseline workflow, not final60/peer-review500.

## Dependencies, exact evidence

Source `requirements-lock.txt` contains15 pins. All pins match installed package metadata:14 in `.venv/lib/python3.12/site-packages`, gurobipy in inherited system packages at `/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/gurobipy-13.0.2.dist-info`. `.venv/pyvenv.cfg` records Python3.12.8 and `include-system-site-packages=true`; this environment is not isolated.

The [machine-readable dependency comparison](dependency_evidence.csv) records each pin, import name, observed metadata version and evidence class. All 15 versions match; fresh installation remains untested.

Archived CI01 `logs/exact_environment_versions.json` corroborates Python3.12.8 and9 computational/audit packages. v2 `environment_versions.json` corroborates Python3.12.8,gurobipy,numpy,scipy,openpyxl. These are historical/local evidence, not a verified fresh installation.

| Distribution | Recorded pin | Import evidence |
|---|---|---|
| gurobipy |13.0.2| model,peer-review primary |
| numpy |2.5.4| pipelines,design,validation |
| pandas |2.3.3| pipelines,scenario analyses |
| scipy |1.18.1| HiGHS MILP,Spearman |
| scikit-learn |1.9.1| sklearn KMeans and metrics |
| matplotlib |3.11.2| figures |
| openpyxl |3.1.5| master XLSX inputs |
| PyYAML |6.0.3| config (`yaml`) |
| pytest |8.4.2| existing pipeline tests |
| threadpoolctl |3.7.0| scenario computation |
| shapely |2.2.0| study-area geometry |
| pyproj |3.8.0| study-area projections |
| pypdf |6.15.0| archived source PDF extraction |
| reportlab |4.5.1| study-area PDF |
| Markdown |3.11.2| scenario HTML report (`markdown`) |

`unittest`, pathlib,json,csv,hashlib,etc. are standard-library modules and do not belong in pip requirements. Existing tests were read but not executed. All selected canonical Python sources parsed successfully with AST during import audit.

## Commands supported by source, not executed

Use a new output directory and isolated copy with required data. These commands do not by themselves prove manuscript-wide reproducibility:

```sh
python 03_Experiments/Optimization/code/run_experiments.py --run-id reproduction_001
python 03_Experiments/Optimization/code/verify_results.py 04_Results/Reproductions/reproduction_001
python 03_Experiments/Scenario_Stability/code/run_analysis.py --output 04_Results/Reproductions/scenario_stability_001
python 03_Experiments/Scenario_Stability/code/verify_results.py --output 04_Results/Reproductions/scenario_stability_001
python manuscript_revision/audit/ci01_independent_20261104/code/run_backend.py --run-name backend_probability60_reproduction_001
```

For final60 derivations and peer-review500, retain native snapshots and record that whole-workspace hash guards require the full original corpus. Do not use `--initialize` on archived evidence; it captures current source state rather than validating the historical guard. Do not run fixed-output finalizers over archived originals.
