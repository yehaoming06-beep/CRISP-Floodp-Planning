# CRISP: stochastic flood-response planning in Tai O

Research materials accompanying **CRISP: An auditable case study of stochastic flood response planning in Tai O**. CRISP combines CRITIC weighting and one-dimensional K-means classification of rainfall, sea-level and storm-surge indicators with two-stage readiness, mobile-pump inventory and deployment models.

**Delivery review, 18 November 2026:** the selected submission tree contains the core 23/60 inputs, code/configuration, both frozen 555 suites, S1–S13 and complete compressed execution evidence. The authoritative file list and four-way classification are in [the delivery report](audit/delivery_20261118/DELIVERY_REPORT.md). Files remain uncommitted; the existing GitHub commit contains only `.gitignore` and `README.md`. A clone of that old commit cannot reproduce the study. No staging, commit, push, tag/release or visibility change has been made.

**HKO data: free-of-charge, non-commercial use subject to the accompanying [complete source conditions and official disclaimers](THIRD_PARTY_NOTICES.md#hong-kong-observatory).** Government/HKO source ownership is acknowledged; research transformations are the authors' responsibility. Read the notices before redistributing the numerical data. This is not a blanket open-data license.

**HKO official website-material disclaimer**

> Disclaimer This website / publication / product / service contains information that is copied or extracted from data made available on the websites of the Hong Kong Observatory (the "Observatory") including https://www.weather.gov.hk , https://www.hko.gov.hk , and the subdomains of "weather.gov.hk" and "hko.gov.hk". The provision of the information copied or extracted from or a link to the Observatory’s websites shall not be constituted as any form of co-operation or affiliation by the Observatory with any person in relation to this website / publication / product / service or any contents herein. Nothing in this website / publication / product / service shall give rise to any representation, warranty or implication that the Observatory agrees with, approves of, recommends or endorses this website / publication / product / service. The Observatory does not have any liability, obligation or responsibility whatsoever for any loss, destruction or damages (including without limitation consequential loss, destruction or damages) howsoever arising from or in respect of your use or misuse of or reliance on or inability to use any contents herein.

**HKO official publication-material disclaimer**

> Disclaimer This publication / website / product / service contains information that is copied or extracted from data made available in the publications of the Hong Kong Observatory (the "Observatory"). The provision of the information copied or extracted from the Observatory's publications shall not be constituted as any form of co-operation or affiliation by the Observatory with any person in relation to this publication / website / product / service or any contents herein. Nothing in this publication, the product or the service shall give rise to any representation, warranty or implication that the Observatory agrees with, approves of, recommends or endorses this publication / website / product / service. The Observatory does not have any liability, obligation or responsibility whatsoever for any loss, destruction or damages (including without limitation consequential loss, destruction or damages) howsoever arising from or in respect of your use or misuse of or reliance on or inability to use any contents herein.

The study supports conditional method validation with illustrative coefficients. Conditional sample proportions are not annual flood probabilities. HKD procurement costs, CU operating expenses and model-score benefits are different quantities. Results do not establish measured damage reduction, protected population or operational effectiveness.

## Materials

| Location | Role |
| --- | --- |
| [01_Data](01_Data/) | Minimal numerical workbook, original-23 inputs and frozen numerical controls; raw archives remain held locally |
| [02_Model](02_Model/) | Unchanged parameter reader and optimization model |
| [03_Experiments](03_Experiments/) | Frozen experiment protocol, original runners and independent verification |
| [04_Results](04_Results/) | Historical original-23 results and stability evidence |
| [05_Code/Scenario_Pipeline](05_Code/Scenario_Pipeline/) | CRITIC/K-means implementation, configuration and existing software tests |
| [src/submission](src/submission/PORTABILITY.md) | Documented portable execution adapters; no new scientific design |
| [supplementary](supplementary/ARCHIVE_INDEX.md) | S1–S13, tables S1–S16, figures S1–S5 and evidence index |
| [manuscript_revision](manuscript_revision/) | Final-60 ledgers/input/results and supplementary v2 historical evidence; Word manuscripts are excluded from Git candidates |
| [audit/reproducibility_20261118](REPRODUCIBILITY_AUDIT.md) | Earlier complete numerical reruns, independent checks, actual logs, inputs and output manifests |
| [audit/submission_20261118](audit/submission_20261118/) | Historical submission checks, supplementary alignment and numerical comparisons |
| [audit/delivery_20261118](audit/delivery_20261118/DELIVERY_REPORT.md) | Current selection, rights/access, safety review and selected-tree test |
| [results/evidence](results/evidence/README.md) | Full byte-preserving execution/solution/EV-tie archives and member SHA-256 |

The comparison manuscript is the unmodified local `manuscript_revision/CRISP_Merged_Manuscript.docx`, SHA-256 `4e12f7849d0b2ca7dd0d156c987a9e90f8b651880c79b74e10f14bffbab4ca37`. Portable scenario checks use its archived table transcription as a comparison reference, never as a fit input. No Word file is required by the commands below.

## Fresh-checkout environment

These commands apply **after the reviewed candidate files have been committed and made available**. The current local HEAD is not that complete tree. Run from the checkout root. Python **3.12.8**, macOS arm64 was tested; other platforms have not been certified. Python, network access for package installation and the applicable solver license are prerequisites.

```sh
git clone https://github.com/yehaoming06-beep/CRISP-Floodp-Planning.git CRISP-Floodp-Planning
cd CRISP-Floodp-Planning
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt -c audit/submission_20261118/clean_freeze.txt
.venv/bin/python -m pip check
```

[requirements.txt](requirements.txt) pins all 15 direct dependencies; the command also constrains the recorded transitive versions. The direct pins agree with the unchanged [research lock](requirements-lock.txt). The complete installed dependency set used in the submission check is in [clean_freeze.txt](audit/submission_20261118/clean_freeze.txt). The environment must not inherit system packages. Windows users should use the equivalent `.venv\Scripts\python.exe` path. A trusted CA bundle may be needed if pip reports certificate errors; keep TLS verification enabled.

The primary runners use **gurobipy 13.0.2**. A usable Gurobi license is required. Pip includes a restricted nonproduction license with model-size limits; an appropriate academic/commercial license is needed if those limits or terms do not cover the run. See [Gurobi's official license explanation](https://support.gurobi.com/hc/en-us/articles/360051597492-How-do-I-resolve-a-Model-too-large-for-size-limited-Gurobi-license-error). Never commit license files or license-service credentials. `scipy.optimize.milp` supplies the independent HiGHS RP check; it does not replace the Gurobi runner for WS/EV/EEV or its EV tie-breaking rules. No complete alternate-solver reproduction route is claimed. Node.js and styled Excel export are not needed for CSV/JSON reproduction; their historical export environment remains incompletely specified.

## Reproduce the 23/60 core results

Use a **new** output directory for each run; existing destinations are refused. The commands do not overwrite frozen results.

```sh
.venv/bin/python -I src/reproduce_submission.py core \
  --output results/reproductions/core_001
```

This reads the original 23-event input, final adjudicated 60-event input and inclusion ledger, recomputes CRITIC/classification with the original production implementation and an independent global one-dimensional partition check, then solves the four core cases (23/60 × legacy/mobile). Core optimization is cross-checked by finite enumeration. The 60 probabilities come from **that run's newly fitted counts**. Workbook coefficients remain fixed.

Expected class counts (Moderate/Severe/Extreme) are **9/9/5** and **35/19/6**. Mobile-pump metrics at six decimals are:

| Input | RP | WS | EV | EEV | VSS | EVPI |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Original 23 | 616.082500 | 622.539022 | 621.392391 | 612.844674 | 3.237826 | 6.456522 |
| Final 60 | 634.516667 | 639.741667 | 601.907167 | 600.203083 | 34.313583 | 5.225000 |

Read `<output>/execution.json`, `scenarios/scenario_reproduction_summary.json`, `core/core_validation.json`, `core/core_metrics.csv` and `core/independent_core_comparison.csv`. Scenario paper comparisons contain 82 cells. Check all 48 Table 6/14 cells against this run's new core results as well (130 paper comparisons overall):

```sh
.venv/bin/python -I audit/submission_20261118/check_fresh_core_tables.py \
  --core-metrics results/reproductions/core_001/core/core_metrics.csv \
  --output results/reproductions/core_001/paper48
```

For the combined `all_001` command below, substitute `all_001` for `core_001` in both paths. [REPRODUCE.md](REPRODUCE.md) gives the complete copyable sequence.

## Run the two frozen 555-configuration suites

```sh
.venv/bin/python -I src/reproduce_submission.py suite23 \
  --output results/reproductions/suite23_001
.venv/bin/python -I src/reproduce_submission.py suite60 \
  --output results/reproductions/suite60_001
```

Or execute both suites and the core checks together:

```sh
.venv/bin/python -I src/reproduce_submission.py all \
  --output results/reproductions/all_001
```

The original-23 runner is unchanged. The final-60 adapter uses fresh scenario counts and the unchanged model/design, updates **only conditional frequencies**, and writes a separate destination. Each suite has 555 configurations: 2 baselines, 21 legacy capacity, 21 mobile capacity, 26 spatial, 8 ablation, 56 OAT, 400 paired perturbation, 9 purchase-limit, 5 existing-stock, 5 price and 2 access configurations. The 200 paired draws retain PCG64 seed `20261103`.

Expected main solver-audit rows are **3,875** (23) and **3,888** (60), all OPTIMAL. The latter includes two original-23 baseline checks and one evaluation of the old policy under new frequencies. Each generated suite has `summary.csv`, `solver_audit.csv`, solutions, logs and `independent_verification.json`. The independent HiGHS checker re-solves all 555 RP objectives per suite and reconstructs saved solution feasibility/objectives; it does not independently re-optimize every WS/EV/EEV. Historical summaries are read for post-solve comparison, not to build scientific inputs.

Primary metrics and first-stage choices should match the frozen suite at `1e-9`; HiGHS raw RP differences use the original `1e-5` tolerance. Earlier integer-coordinate reconstruction explains the small solver floating-point differences without relaxing that tolerance. Read [numerical audit](REPRODUCIBILITY_AUDIT.md) for exact boundaries.

## Supplementary evidence and limits

[S1–S13](supplementary/Supplementary_Methods_and_Results.md) contains 16 tables and five figures. [Submission alignment](audit/submission_20261118/supplementary_alignment.md) checks current manuscript references, configuration counts and numerical tables. The separate v2 record contains 500 primary solves: 498 optimal and two intentionally infeasible coverage controls, plus 936 independent calls. Coverage WS/EV/EEV/VSS were not computed and are not supplied as zeros.

The following remain unresolved:

- Contemporaneous original-23 candidate/exclusion, anchor and station-substitution evidence is incomplete; retrospective reconstruction does not recover historical intent.
- Costs, inventory/access, pump performance, deployment requirements and benefit-to-loss/population mappings lack field calibration.
- `TC2017_06`, `TC2021_02_E` and `TC2021_02_W` remain pending because of conflicting values or inseparable observations. There are 63 identities but only 60 analyzable events.
- The original seeded Lloyd method reached local rather than global optima in 37 resamples. Successful baseline checks do not make every stability fit globally optimal.
- Final-60 mobile EV has four optimal first-stage policies. EEV spans 600.203083–626.497667; the quoted VSS uses the disclosed convention-A tie rule.

The clean route starts from the included numerical inputs. Complete official-archive → input reconstruction still needs held source archives, frozen extraction/QC evidence and an approved distribution/access route. CI01/v2 historical whole-workspace guards require a larger historical corpus; they are retained without resetting or fabricating a PASS. Historical links and absolute paths are provenance, not dependencies of the new entry point. The submission test does not certify new PDF inspection, source adjudication, full stability/v2 clean reruns, current Word visual QA or field validity.

## Evidence, rights and delivery gate

Run `python3.12 src/verify_delivery.py` to verify the selected-file hashes, all three evidence archives and 16,717 member hashes without running a solver. Use `python3.12 src/verify_delivery.py --restore-evidence` to restore the archived execution/solution/tie files at their original paths when reviewing historical reports. Existing different files are never overwritten. The core/all commands do not require restoration.

The current selection is documented in [the delivery report](audit/delivery_20261118/DELIVERY_REPORT.md), [exact file list](audit/delivery_20261118/submission_files.tsv) and [checklist](SUBMISSION_REPOSITORY_CHECKLIST.md). Earlier audit inventories describe larger historical trees; they are not the current Git allowlist. Some historical paths refer to compressed evidence or optional local material. Raw source archives and legacy whole-workspace guards remain outside the Git-only numerical route.

[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) supplies the full applicable HKO legal notices and disclaimers; [rights/access](audit/Data_Rights_and_Access.md) describes other sources. Unconfirmed DSD/CEDD/other copied works, map databases and vendor helpers are excluded. Environments, credentials, response headers/cookies, caches, manuscript drafts/Word originals and newly generated reproduction outputs are excluded. Original local materials and Final Paper have not been deleted or modified. Historical username/workspace paths remain in selected provenance records; they are not execution dependencies or credentials.

The reviewed numerical-input-to-results package can be submitted for commit approval. Commit and push require the user's confirmation, followed by a real fresh clone of that exact commit and the commands in [REPRODUCE.md](REPRODUCE.md) before tagging `v1.0-submission`. A release must clearly state this numerical-input boundary; it must not claim a complete official-archive-to-input clean reproduction or field validation. Keep the existing private visibility. No public release or unrestricted reuse license is authorized by this preparation.
