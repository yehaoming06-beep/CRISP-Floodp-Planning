# Reproduce the reviewed submission

These commands apply after the selected files are committed and pushed. The repository is private: authenticate to GitHub with an account granted access. The old commit currently on GitHub has only two files and cannot run these commands. No local absolute research path is required.

Python 3.12.8/macOS arm64 was tested. Use Python 3.12, network access to install the pinned packages, and Gurobi under its applicable license. `pip` supplies a restricted non-production Gurobi license which passed these fixed small models in the recorded clean test; obtain an appropriate [academic/commercial license](https://support.gurobi.com/hc/en-us/articles/360051597492-How-do-I-resolve-a-Model-too-large-for-size-limited-Gurobi-license-error) if needed. Keep license files, WLS credentials and tokens outside Git. No paid-license credentials are bundled. Other operating systems are not certified.

Read [the HKO source conditions and official disclaimers](THIRD_PARTY_NOTICES.md) first. The included numerical observations are for free-of-charge non-commercial use subject to those terms. No unrestricted code/data license is asserted.

```sh
git clone https://github.com/yehaoming06-beep/CRISP-Floodp-Planning.git CRISP-Floodp-Planning
cd CRISP-Floodp-Planning
python3.12 src/verify_delivery.py
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt -c audit/submission_20261118/clean_freeze.txt
.venv/bin/python -m pip check

# Core 23/60 and both 555-configuration suites in one fresh destination.
.venv/bin/python -I src/reproduce_submission.py all \
  --output results/reproductions/all_001

# 48 core paper cells, in addition to the 82 scenario cells checked above.
.venv/bin/python -I audit/submission_20261118/check_fresh_core_tables.py \
  --core-metrics results/reproductions/all_001/core/core_metrics.csv \
  --output results/reproductions/all_001/paper48

# Existing production-pipeline tests.
PYTHONPATH=05_Code/Scenario_Pipeline/src .venv/bin/python -m pytest -q 05_Code/Scenario_Pipeline/tests 03_Experiments/Optimization/code/test_mobile_model.py
```

Every execution target requires a new destination. To run separately instead of `all`, use:

```sh
.venv/bin/python -I src/reproduce_submission.py core --output results/reproductions/core_001
.venv/bin/python -I src/reproduce_submission.py suite23 --output results/reproductions/suite23_001
.venv/bin/python -I src/reproduce_submission.py suite60 --output results/reproductions/suite60_001
.venv/bin/python -I audit/submission_20261118/check_fresh_core_tables.py \
  --core-metrics results/reproductions/core_001/core/core_metrics.csv \
  --output results/reproductions/core_001/paper48
```

Expected: class counts 9/9/5 and 35/19/6; four core cases checked by enumeration; 555 configurations per suite; 3,875/3,888 primary audit rows all OPTIMAL; independent HiGHS RP and saved-solution checks; 82+48=130 paper comparisons PASS. Inspect the new `execution.json`, `scenarios/scenario_reproduction_summary.json`, `core/core_validation.json`, each suite's `independent_verification.json`, and `paper48/fresh_core_paper_validation.json`. EV/EEV/VSS use the disclosed convention-A tie rule; HiGHS does not independently re-optimize every WS/EV/EEV. The model/experiment settings and scientific conclusions remain unchanged.

To inspect the full saved run and historical solution/tie evidence:

```sh
python3.12 src/verify_delivery.py --restore-evidence
```

Restoration is optional for numerical reruns. It restores exact bytes under ignored historical paths and refuses to replace changed files.

## External-source boundary

No external research data file is needed for the commands above. The six minimal root inputs, final-60 input and adjudication ledger, model/production code, frozen configurations and comparison references are selected into Git. Package installation, GitHub authentication for this private repository and the applicable solver license are external prerequisites.

Rebuilding the historical observations from official source archives is a separate route. [source_access.csv](data/provenance/source_access.csv) gives the official URLs, held paths, exact SHA-256, and source-specific terms for 338 registered source records. Download each item from its stated official source subject to those conditions and compare its SHA-256 with the frozen record. A changed live page is not a substitute for the frozen input. If the exact version has disappeared, seek it from the official publisher or an authorized archive/author access route; no automatic availability guarantee or approved full archive distribution service exists here. DSD/CEDD copied reports/extracts and unreviewed third-party/vendor works are not supplied; commercial use of HKO data needs separate authorization. Census/OSM material has its own attribution/license conditions.

Thus Git-only numerical-input-to-results reproduction is supported. Full official-archive-to-input reconstruction and CI01/v2 whole-workspace guards are not certified from this lean clone. Historical screening gaps, three pending identities, illustrative coefficients, 37 nonglobal Lloyd fits and EV-policy ambiguity remain disclosed in README/S1–S13; this packaging does not repair or change them.
