# Submission adapter review

Review date: 18 November 2026 (Asia/Shanghai). **PASS for unchanged scientific settings, portable input/output routing and corrected failure propagation.** This is a read-only code/evidence review. The reviewer did not run new scientific experiments, alter original scripts, or change the manuscript.

## Scope and lineage

Reviewed `src/reproduce_submission.py` and `src/submission/{scenarios,suite60,verify60}.py` against the three originals named in `adapter_lineage.json`. All three original-script SHA-256 hashes match that lineage record. Unified source diffs and syntax-tree comparisons show:

- `scenarios.py`: repository-root calculation changes with its new location; the original-workspace witness read is removed; output must be new; comparisons use retained Word table transcription; a non-PASS result now raises an error. `raw_input`, `independent_fit`, `dump` and `sha` retain identical syntax trees to the original. The `git_status` helper now returns `prospective_git_tree_export` when `.git` is absent and captures Git stderr; this changes provenance labeling/log noise only, not scientific calculations. CRITIC arithmetic, exhaustive one-dimensional partitions, KMeans cross-check, seeds, initialization count, stopping conditions, representative means and numerical tolerances are unchanged.
- `suite60.py`: new counts and output arguments replace fixed audit-directory inputs. All 13 `for` loop syntax trees are identical to the source script, including every capacity, spatial, subset, OAT, paired-draw, procurement, existing-stock, price and access case. The unchanged model/design/settings loader is used. The only model-field replacement remains `replace(old, probabilities=...)`; no cost, capacity, stock, benefit, resource bound, response coefficient, EV convention or solver setting is changed.
- `verify60.py`: only repository-root and output-directory routing/arguments change. The original independent matrix checker is imported from `03_Experiments/Optimization/code/verify_results.py`. HiGHS RP objective checks, saved-solution constraint/objective reconstruction, fixed EEV first-stage checks and historical comparisons retain their source logic and tolerance.
- The new orchestrator calls the unchanged core and 23-event runners plus these 60-event adapters. It creates a new destination, clears inherited Python module-location overrides, records subprocess logs/status and compares results only after solving. The Gurobi license and dependencies remain explicit environment requirements; the code does not supply or embed a license.

## Fresh scenario counts and comparison references

The orchestrator runs `scenarios.py` before `core`, `suite60` or `all`. Scenario construction reads the actual frozen23 and reconstructed60 numerical input files, cross-checks reconstructed60 values against all eligible rows in the inclusion ledger, fits each dataset and emits a new `scenario_reproduction_summary.json` inside the selected output directory.

The 60-event adapter reads `fits.reconstructed60.counts` from that new output, requires PASS and total N=60, divides counts by 60 in Moderate/Severe/Extreme order, records the new counts file and its SHA, and replaces only probabilities. Its pending count is also taken from that same newly generated summary. There is **no read of the historical `analysis/backend_probability_update.json` or a saved audit scenario summary on this route**. The core runner likewise receives the newly generated counts file.

The archived `paper_tables_4_11_12.json` was independently re-extracted from the current local Word XML during this review and is exactly cell-text identical for Tables 4, 11 and 12. Its values are loaded after independent fitting and production cross-checks; they are comparison references and are not fit/model parameters. Historical 23/60 summary CSVs are used for validation/comparison after solves rather than as coefficients.

## Candidate-tree dependency check

The tested candidate manifest contains all reviewed entry points, the master workbook, 23-event input and metadata, reconstructed60 input, inclusion ledger, Candidate_Event_Inventory.csv, scenario config and every Python file in `crisp_data_layer`, model and parameter modules, experiment protocol and design, both unchanged 23-event runner/verifier, core runner and independent enumeration, both historical summary references, and both control references needed by the 23-event runner/verifier:

- `01_Data/Controls/capacity_bound_reference.json`
- `01_Data/Controls/pre_cleanup_metrics.json`

No checked direct or package dependency was absent from the candidate manifest. At the initial read, their source hashes matched current files. Later failure-propagation fixes and the no-`.git` provenance-label change intentionally changed the orchestrator and scenario adapter: the final candidate/export hashes and clean-run record must refer to those corrected versions, rather than retaining the earlier candidate hashes. Final clean-test status belongs to the root submission checklist; this code review alone is not a committed-clone PASS. The current committed repository initially contained only `.gitignore` and `README.md`, so its clone lacks the research inputs until the author commits the proposed tree.

## Finding corrected during review

The initial scenario adapter wrote a FAIL status but returned process exit code zero. The orchestrator's core branch could therefore continue and later label the overall run PASS, because the original core runner does not itself test the status field. This was reported to the root agent. The corrected scenario adapter raises `RuntimeError` for non-PASS after saving its evidence; the corrected orchestrator independently requires the counts summary to contain PASS before any dependent core/suite execution. The correction is failure reporting and does not change any scientific setting or numerical calculation.

No other actionable implementation defect was found in the reviewed diff. The unchanged verifier scope remains independent RP optimization plus saved-solution checks; it is not a claim that every WS/EV/EEV optimum in all 555 cases was independently reoptimized with HiGHS.

## Reviewed current hashes

| File | SHA-256 |
| --- | --- |
| `src/reproduce_submission.py` | `0568e13fa413b187cf871d47ac2216fdd7bb492aa36e39c192276457ce274479` |
| `src/submission/scenarios.py` | `8a3ef57ca20df9260052bfbe8e75177e4262dfedae74d34d2dc1c602b7a7934a` |
| `src/submission/suite60.py` | `2cf3cc2db88e365e120fa890c4efa4ea00adbbe98e5a68b3d1f7c81cc7b48186` |
| `src/submission/verify60.py` | `7d4894cfe3ec54b2b1ff18e40bc9689c9adef1eb653fe26dbc7bba7830b1d795` |

Original lineage hashes are retained in `adapter_lineage.json`; no historical guard was reset. Historical screening gaps, field-calibration limits, three pending identities, nonglobal Lloyd fits and EV tie/range issues remain unchanged and are not resolved by these adapters. Source-archive reconstruction and full historical v2 corpus guards remain outside the portable core/two-suite route.
