# Verification of CI-01 results integrated into the English manuscript v2

Verification date: 2026-11-05 (Asia/Shanghai). Status: **PASS for the numerical checks below, with explicitly unresolved CI-01 research items. CI-01 is not fully closed.**

## 1. Scope and evidence hierarchy

This verification checks existing data and saved results. It does not run a new optimization experiment, enlarge the experimental design, create empirical coefficients, resolve conflicting observations, or establish the historical selection procedure. New arithmetic was limited to reproducing the published preprocessing calculations and checking cross-file consistency.

The source of final CI-01 results is `audit/ci01_independent_20261104/`, specifically:

- `CI01_Resolution_Report.md`, `Screening_Protocol.md`, `Source_Conflict_Adjudication.md`, `TaiO_Spatial_Sensitivity_Addendum.md`, and `Scenario_Impact_Assessment.md`;
- `Candidate_Event_Inventory.csv`, `Inclusion_Exclusion_Audit.csv`, and `Original23_vs_Reconstructed.csv`;
- `analysis/scenario_impact.json`, `analysis/spatial_impact.json`, the corresponding scenario input/results files, and both label-migration CSVs;
- `backend_probability60/inputs.json`, `summary.csv`, `Original555_vs_Reconstructed.csv`, `solver_audit.csv`, `validation.json`, `solutions/`, `ev_optimal_policies.csv`, `ev_policy_tie_ranges.csv`, and `ev_tie_verification.json`;
- `backend_probability60_replay/summary.csv` and `logs/Final_Verification.json`.

The earlier 61-row stage and `backend_probability61/` remain historical audit artifacts. Their results are not substituted for the final 60-row analysis. The 61-warning-group sensitivity is a separate analysis unit, not the final individual-cyclone sample.

The independently written checker is `audit/ci01_integration_20261105/verify_existing_ci01_results.py`; its machine-readable result and execution output are `existing_results_consistency.json` and `existing_results_consistency.log` in that directory. All checks stated below passed. NumPy 2.3.5 was used for the independent arithmetic; no optimization solver was invoked during this integration check.

## 2. Candidate frame, adjudication, and linkage

| Check | Independently checked result |
| --- | --- |
| Candidate inventory / screening audit / full outer comparison | 63 rows in each, with 63 unique identities |
| HKO local-warning groups | 62 distinct groups |
| Warning-record line references | 203 distinct warning segments |
| Analysis status | 60 INCLUDE; 3 PENDING_DATA; 0 entity exclusions |
| Historical events linked to the reconstruction | All 23 |
| Historical events retained for numerical analysis | All 23; 37 additional analyzable identities |
| Historical R/W/S changes under the new rules | Zero for every variable and every original event |
| Historical anchor-date changes | Five; selected rainfall stations unchanged |
| Rainfall stations among the 60 analyzable identities | R11: 54; HKA: 4; R12: 2 |

The five changed anchors are E011 (2021-10-13 to 2021-10-12), E012 (2022-07-02 to 2022-07-01), E013 (2022-08-25 to 2022-08-24), E019 (2024-11-14 to 2024-11-13), and E022 (2025-09-08 to 2025-09-07). The reported R/W/S vectors remain unchanged despite those shifts. This compatibility does not recover the original decision rules.

The three pending identities remain TC2017_06, TC2021_02_E, and TC2021_02_W. The first has conflicting official W/S values; the latter two share one warning/observation summary whose components cannot be separated. Yagi remains in the 60-row numerical analysis with its unresolved surge-peak date disclosed. Missingness and unresolved attribution have not been reclassified as entity exclusions.

The 203-segment frame establishes completeness only within the stated HKO local-warning definition, not within all Tai O floods or all cyclone-related impacts. Source records, station QC, and original historical selection remain distinct evidentiary questions.

## 3. Scenario arithmetic and independent partition check

For each main dataset, the checker independently calculated Min-Max scaling, population standard deviations (`ddof=0`), Pearson correlations, CRITIC information values, normalized weights, and H scores. It then enumerated every nonempty contiguous three-way partition of the sorted one-dimensional H scores, without calling the existing clustering code. Its minimum-SSE labels agree with every saved event label. Scenario representatives, calculated independently as class-specific variable means, also agree.

| Dataset | N | CRITIC R / W / S | Moderate / Severe / Extreme | Conditional relative frequencies (%) |
| --- | --- | --- | --- | --- |
| Historical frozen sample | 23 | 0.434081 / 0.335229 / 0.230689 | 9 / 9 / 5 | 39.130435 / 39.130435 / 21.739130 |
| Original identities under the new rules | 23 | 0.434081 / 0.335229 / 0.230689 | 9 / 9 / 5 | 39.130435 / 39.130435 / 21.739130 |
| Final adjudicated reconstruction | 60 | 0.487217 / 0.286080 / 0.226703 | 35 / 19 / 6 | 58.333333 / 31.666667 / 10.000000 |
| Same 59 identities, Shek Pik | 59 | 0.489416 / 0.284729 / 0.225855 | 34 / 19 / 6 | 57.627119 / 32.203390 / 10.169492 |
| Same 59 identities, Tai O | 59 | 0.465760 / 0.314428 / 0.219812 | 41 / 15 / 3 | 69.491525 / 25.423729 / 5.084746 |

The maximum independent CRITIC-weight discrepancy was 1.11 × 10^-16. The exhaustive-partition checks used 231 possible partitions for N=23, 1,711 for N=60, and 1,653 for each N=59 comparison. Independent SSEs were 0.146972733252035, 0.260494025998046, 0.257917504164599, and 0.242598880832136, respectively; discrepancies from saved SSEs were below 10^-12. The fixed K=3 choice is a planning discretization and is not evidence of three natural hazard populations.

| Quantity | Historical 23 | Final 60 |
| --- | --- | --- |
| Minima R / W / S | 13.5 / 2.38 / 0.22 | 0 / 1.71 / 0.06 |
| Min-Max ranges R / W / S | 338.4 / 1.53 / 2.12 | 351.9 / 2.20 / 2.28 |
| H thresholds | 0.247782 / 0.485191 | 0.272564 / 0.505236 |

R has units mm/day; W is m above Chart Datum (mCD); S is m above astronomical tide. H, thresholds, weights, and frequencies are dimensionless. Percentages rounded separately need not sum to exactly 100% at the displayed precision.

The Extreme fraction changes by -11.739130 percentage points. This is a change in sample-conditional composition after reconstruction and refitting; it is neither a decline in annual flood probability nor a climate trend.

The existing `analysis/stability_runs.csv` contains exactly 2,009 valid rows: 1,000 overlap-episode bootstraps, 1,000 year-block bootstraps, and nine leave-one-year-out fits. Recalculation of the saved ARI quantiles agrees with `stability_summary.json`; their respective median projection ARIs are 0.717193, 0.762460, and 0.972553. This check only aggregates retained results; it does not generate new resamples or rerun their fits. Annual warning-group, identity, historical-sample, analyzable, and pending counts were also independently regrouped from the inventory/audit and agree with Appendix C of manuscript v2.

### 3.1 Label migration and refitting

The migration matrix for the original 23 identities was counted directly from `analysis/Original23_Label_Migration.csv`:

| Original class | Refitted Moderate | Refitted Severe | Refitted Extreme |
| --- | --- | --- | --- |
| Moderate | 4 | 5 | 0 |
| Severe | 0 | 8 | 1 |
| Extreme | 0 | 0 | 5 |

Six identities change labels: E001, E004, E005, E013, and E014 move from Moderate to Severe; E010 moves from Severe to Extreme. The independently calculated adjusted Rand index (ARI) is 0.375139560849. Their original R/W/S values did not change. The label changes arise from refitting the preprocessing/weighting/clustering to a different sample.

Projecting all 60 observations through the frozen 23-row preprocessing and thresholds gives 43/12/5, rather than the fully refitted 35/19/6. The independently calculated ARI between these classifications is 0.571450729570. Twenty-five observations fall below at least one old Min-Max lower bound; the projection retains these extrapolations without clipping. Therefore, the reconstruction cannot be described as a denominator-only change.

### 3.2 Representative values

| Final-60 class | H centroid | R mean (mm/day) | W mean (mCD) | S mean (m) |
| --- | --- | --- | --- | --- |
| Moderate | 0.186370 | 37.171429 | 2.515429 | 0.363429 |
| Severe | 0.358758 | 122.026316 | 2.788947 | 0.557895 |
| Extreme | 0.651715 | 222.316667 | 3.390000 | 1.321667 |

These are variable-wise class means, not synchronized observed hydrographs. W and S need not peak simultaneously. They do not quantify flood depth or empirically calibrated resource requirements.

## 4. Spatial sensitivity on matched identities

The two N=59 input files have exactly the same identity set and identical rainfall values. Only the fixed tide-station representation differs. Bebinca 2018 is absent from this paired comparison because its Tai O record is unavailable; the three main pending identities are also unavailable for the comparison. This paired N=59 sample is different from the separate N=59 sensitivity that omits Yagi's source-time conflict.

Ten of the matched 59 labels change between Shek Pik and Tai O. The independently calculated ARI is 0.575572848266. The maximum absolute paired station differences are 0.18 m for W and 0.55 m for S. The smaller Tai O Extreme count is a refitted classification result; it does not prove a lower physical flood risk or validate either station's calibration. Tai O sea level is not ground-referenced inundation depth.

## 5. Frequency-only backend sensitivity

All 555 saved new parameter packages were compared with their corresponding frozen solutions. In every case, the only changed parameter key was `probabilities`; each saved configuration and fleet specification was identical. The new base frequency vector is 35/60, 19/60, and 6/60. Configurations prescribing probability perturbations apply the same frozen multipliers to their respective base frequency vectors and renormalize; their final probabilities therefore need not equal the unperturbed base vector. No revised R/W/S representative was transmitted through a new empirical resource, cost, or benefit function.

The 555-row summary and comparison CSV agree for all six metrics and all deltas. All 3,888 saved solver-audit rows report OPTIMAL and a passed validation flag. The summary rows satisfy WS ≥ RP ≥ EEV, VSS = RP - EEV, and EVPI = WS - RP to 10^-6. The small negative numerical residual (-1.14 × 10^-13) in legacy EVPI is displayed as zero at six decimals.

The completed 555-row replay summary is byte-identical to the first summary: SHA-256 `fecf0ca2681ded84890957794f0db058a9589966ae6d6b92c0a0bada91695162`. This integration step verified that equality and inspected the saved audits; it did not rerun the optimizations. The prior final verification records 102 identical offline preprocessing/evidence outputs and 977 unchanged frozen files. These historical checks do not establish measurement accuracy or sampling validity.

| Baseline | Metric | Original 23 | Final 60 | New minus old |
| --- | --- | --- | --- | --- |
| Legacy | RP | 686.007826 | 720.324917 | 34.317091 |
| Legacy | WS | 686.007826 | 720.324917 | 34.317091 |
| Legacy | EV | 693.973261 | 677.094000 | -16.879261 |
| Legacy | EEV | 686.007826 | 720.324917 | 34.317091 |
| Legacy | VSS | 0.000000 | 0.000000 | 0.000000 |
| Legacy | EVPI | 0.000000 | 0.000000 | 0.000000 |
| Mobile-pump | RP | 616.082500 | 634.516667 | 18.434167 |
| Mobile-pump | WS | 622.539022 | 639.741667 | 17.202645 |
| Mobile-pump | EV | 621.392391 | 601.907167 | -19.485225 |
| Mobile-pump | EEV | 612.844674 | 600.203083 | -12.641591 |
| Mobile-pump | VSS | 3.237826 | 34.313583 | 31.075757 |
| Mobile-pump | EVPI | 6.456522 | 5.225000 | -1.231522 |

All objective values above are illustrative benefit scores. They are not observed avoided losses, annual welfare, or HKD benefits. EV is the deterministic expected-parameter objective and is not directly comparable as a stochastic policy value. EEV evaluates the complete EV first-stage policy under the scenarios. VSS and EVPI are conditional model information values, not measured effects of implementing a policy.

The historical mobile RP policy remains feasible under the reconstructed frequency input, with value 634.516667 and regret zero. The RP policy returned in both versions purchases no new pump. The returned EV policy purchases two pumps under the old input and one under the new input. Across the 555 returned RP solutions, 20 preparation-plan strings and 18 purchase counts differ. These are differences between returned optimal solutions and do not establish uniqueness of the optimal policy.

### 5.1 EV-optimal policy ranges

The 10-case tie audit enumerated 1,716 feasible first-stage policies and recorded 1,808 optimal solves. The existing policy CSV was independently regrouped by case; counts and minimum/maximum EEV and VSS agree with the saved range table.

| Purchase limit / case | RP | Number of EV-optimal policies | EEV range among EV optima | VSS range among EV optima |
| --- | --- | --- | --- | --- |
| Legacy baseline | 720.324917 | 2 | 720.324917–720.324917 | 0.000000–0.000000 |
| 0 | 634.516667 | 2 | 634.516667–634.516667 | 0.000000–0.000000 |
| 1 | 634.516667 | 2 | 600.203083–600.203083 | 34.313583–34.313583 |
| 2 (mobile baseline) | 634.516667 | 4 | 600.203083–626.497667 | 8.019000–34.313583 |
| 3 | 675.389917 | 2 | 675.389917–675.389917 | 0.000000–0.000000 |
| 4 | 676.778667 | 4 | 675.389917–676.778667 | 0.000000–1.388750 |
| 6 | 720.324917 | 8 | 675.389917–720.324917 | 0.000000–44.935000 |
| 8 | 720.324917 | 12 | 675.389917–720.324917 | 0.000000–44.935000 |
| 12 | 720.324917 | 20 | 675.389917–720.324917 | 0.000000–44.935000 |
| 20 | 720.324917 | 36 | 675.389917–720.324917 | 0.000000–44.935000 |

For the mobile baseline, four EV-optimal policies have the same EV objective (601.907167). They combine the preparation set Tai O1/Drainage plus Tai O1/Warning, optionally adding Tai O2/Warning, with either one or two new pumps. One-pump policies yield EEV 600.203083; two-pump policies yield EEV 626.497667. The reported selected-policy VSS 34.313583 is thus one admissible value, while the tie-aware range is 8.019000–34.313583. The 10-case audit must not be described as an exhaustive tie audit of all 555 cases.

## 6. Version discrepancy retained in the audit

`logs/final_backend_run.log` contains obsolete labels `original23_policy_new61_*` and a remaining-items sentence referring to two pending attributions. The actual probabilities and reported objectives in that log are those of the final 60-row calculation. `backend_probability60/inputs.json`, `validation.json`, the row-level CSVs, and `logs/Final_Verification.json` explicitly identify N=60 and three pending identities. These final structured files control the manuscript integration. The old log text is retained as provenance and is not silently edited or cited as evidence of N=61 being the final sample.

## 7. Interpretation and retained limits

Passing this check supports exact numerical reporting of the specified retrospective reconstruction and frequency-only sensitivity. It does not establish that the historical 23-event selection was unbiased, that its historical rules have been recovered, that the broader Tai O flood population is complete, that station measurements are calibrated, or that R/W/S has an empirical mapping to resource requirements and policy benefits. The three pending identities, Yagi peak-time conflict, station representativeness, overlapping-event dependence, and annual-probability limitations remain research risks. Sample fractions based on 23 or 60 events are conditional relative frequencies and must never be presented as annual occurrence probabilities or future flood probabilities.

## 8. Manuscript v2 numerical and interpretation review

The integration review read Results Sections 5.8–5.11 and Appendix C against the checked source outputs. Tables 12–17 match the source values at their displayed precision: event-frame comparison, class representatives, original-identity migration, matched-station sensitivity, baseline objective changes, and EV-policy ranges. The reviewed prose correctly distinguishes the two different N=59 identity sets, the 61-unit shared-warning sensitivity, the 60-identity main analysis, and the superseded 61-record trial. Table 17's selected EEV is indeed the lower endpoint for every listed instance; the text confines that result to these audited secondary-choice outcomes.

The annual Appendix C counts agree with independent regrouping of the candidate inventory and audit. The three unresolved identities and Yagi's conflicting peak date remain visible. The main frequency-replay description explicitly retains the existing probability-perturbation multipliers and renormalization, matching the distinction between a changed base frequency vector and configuration-specific probabilities.

A comparison of old and v2 Results Sections 5.1–5.7 found that the original numerical prose and tables were retained. Changes within those sections are descriptive heading changes and figure-source additions that identify the frozen 23-event frequency basis. The added sections are presented as separate conditional validation results rather than silent replacements of those frozen values. No numerical discrepancy remained after this review. This records a content/arithmetic review of the Markdown manuscript; Word synchronization and rendered-page checks are documented separately in the integration log.
