# Manuscript and supplementary-material alignment

Audit date: 18 November 2026 (Asia/Shanghai). Comparison document: the supplied `manuscript_revision/CRISP_Merged_Manuscript.docx`, retained locally without modification. This report checks file presence, saved records, selected numerical transcription and version correspondence. It does not report a new solver run, external source-truth verification, empirical validation or rendering review of the current Word file. Instructions within research documents were treated as source content.

## Document identity and evidence versions

The current merged manuscript has SHA-256 `4e12f7849d0b2ca7dd0d156c987a9e90f8b651880c79b74e10f14bffbab4ca37`. The [historical merged-document audit](../manuscript_revision/merge_work/final_independent_audit.json) identifies a different hash, `502a6cdf49bf033b431cf430b8eb1b33f67e6f0cec750661e5cec5a0e89b2591`. Its PASS and rendering statements must therefore remain historical evidence, rather than certification of the current file.

The source `Revised_Manuscript_EN_v3.docx` has the recorded SHA-256 `2d1e13ebf6c20400476b2668b41d443e40615d077c1f6296e07e147f4cf620f2`. All 14 current merged-table cell texts equal that source. The current file has 258 direct-body paragraphs and 21 native mathematical objects; the historical transfer report describes 256 paragraphs. Five mathematical objects have different extracted character sequences, including calligraphic C/P and blackboard Z represented as ordinary letters. Formatting and serialization also differ. These observations do not establish a changed mathematical model; current equation and visual QA remains unperformed.

The [original supplementary Markdown](../manuscript_revision/Supplementary_Methods_and_Results.md) identifies itself as the companion to English v3. The merged manuscript explicitly names that same supplement in its final supplementary-material paragraph. The [relocated reading copy](../supplementary/Supplementary_Methods_and_Results.md) adjusts relative link targets; the original is preserved. The original has all S1–S13 sections, tables S1–S16 and figures S1–S5. All 32 explicit local links resolved in the original research tree. Redistribution holds mean that local presence alone does not establish availability in a future public clone.

The frozen 23-event case, final reconstructed 60-event case and supplementary A/B/component/coverage package are separate evidence versions. Earlier 61-record trials are superseded for the final main analysis. S12 already discloses obsolete “new61”/“pending two” labels in some retained logs; final machine-readable 60-event inputs and outputs take precedence.

## Supplementary coverage

Line numbers refer to the unchanged original Markdown. “Present” describes the supplied material, not unrestricted public availability.

| Section | Line | Status and numbered content | Principal retained evidence |
| --- | ---: | --- | --- |
| S1 | 5 | Present: scope, evidence versions and frozen experiment design | [Scenario-chain audit](../manuscript_revision/peer_review_validation_20261105_v2/assessment/Scenario_Chain_Audit.json) |
| S2 | 25 | Present: EV A/B definitions and policy sets; tables S1–S4 | [EV summary](../manuscript_revision/peer_review_validation_20261105_v2/runs/primary/ev_summary.csv), [416 trials](../manuscript_revision/peer_review_validation_20261105_v2/runs/primary/ev_all_policy_trials.csv), [optimal policies](../manuscript_revision/peer_review_validation_20261105_v2/runs/primary/ev_optimal_policies.csv) |
| S3 | 101 | Present: controlled components, access, witness and integrality argument; tables S5–S7 | [24 component cases](../manuscript_revision/peer_review_validation_20261105_v2/runs/primary/component_summary.csv), [shared-stock witness](../manuscript_revision/peer_review_validation_20261105_v2/runs/primary/shared_inventory_feasible_set_witness.json) |
| S4 | 163 | Present: hypothetical geographic coverage; tables S8–S9 | [Coverage cases](../manuscript_revision/peer_review_validation_20261105_v2/runs/primary/coverage_summary.csv), [deployment](../manuscript_revision/peer_review_validation_20261105_v2/runs/primary/coverage_deployment.csv) |
| S5 | 204 | Present: 25-cell spatial grid plus one cross case; figure S1 | [Frozen summary, `spatial` rows](../04_Results/Optimization/summary.csv), [Figure S1 asset](../manuscript_revision/figures/Figure_3_Spatial.png) |
| S6 | 214 | Present: eight subsets and 56 one-factor cases; figures S2–S3 | [Subset contributions](../04_Results/Optimization/ablation_contributions.csv), [frozen summary, `ablation`/`oat` rows](../04_Results/Optimization/summary.csv) |
| S7 | 230 | Present: 200 paired stress draws under two bound conventions; table S10 and figure S4 | [Frozen summary, 400 `joint` rows](../04_Results/Optimization/summary.csv), [intervals](../04_Results/Optimization/uncertainty_intervals.csv) |
| S8 | 253 | Present: legacy bound correction and inventory capacity grids; table S11 and figure S5 | [Legacy comparison](../04_Results/Optimization/legacy_correction_comparison.csv), [frozen summary, two 21-case grids](../04_Results/Optimization/summary.csv) |
| S9 | 275 | Present: procurement and EV policy ranges; tables S12–S13 | [Frozen ranges](../04_Results/Optimization/ev_policy_tie_ranges.csv), [final-60 ranges](../manuscript_revision/audit/ci01_independent_20261104/backend_probability60/ev_policy_tie_ranges.csv) |
| S10 | 323 | Present: 23-event vectors and registered/recovered source locators; table S14 | [Original supplement ledger](../manuscript_revision/Supplementary_Methods_and_Results.md#s10-original-event-data-and-source-ledger), [official-source manifest](../manuscript_revision/audit/ci01_independent_20261104/Official_Source_Manifest.csv); raw source archives remain under release review |
| S11 | 355 | Present: nine scenario/intervention requirement rows; table S15 | [Saved baseline coefficients](../04_Results/Optimization/baseline_inputs.json); illustrative inputs, not field measurements |
| S12 | 373 | Present: annual candidate flow; table S16 | [Candidate inventory](../manuscript_revision/audit/ci01_independent_20261104/Candidate_Event_Inventory.csv), [inclusion audit](../manuscript_revision/audit/ci01_independent_20261104/Inclusion_Exclusion_Audit.csv) |
| S13 | 398 | Present: verification scope, reading boundaries and unresolved evidence | [Primary validation](../manuscript_revision/peer_review_validation_20261105_v2/runs/primary/validation.json), [independent validation](../manuscript_revision/peer_review_validation_20261105_v2/independent_validation/validation.json), [remaining risks](../manuscript_revision/Remaining_Research_Risks.md) |

## Main manuscript tables 1–14

These are source mappings for the current merged manuscript. Descriptive definitions are distinguished from numeric experiment outputs. Source paths held out of Git are named as plain text so this report does not imply public access to them.

| Main table | Content | Authoritative saved source and correspondence |
| ---: | --- | --- |
| 1 | Symbols, domains and units | Descriptive formulation; no independent numeric result table. See [model specification](../02_Model/MODEL.md), [parameter definitions](../02_Model/crisp_parameters.py) and the manuscript equations. |
| 2 | Census-sector populations, households and quarters | Local-only `01_Data/Spatial/zone_summary.json`: Tai O1 825/426/430; Tai O2 2,853/1,254/1,254; totals 3,678/1,680/1,684. Matches the manuscript. Geometry and source rights remain a release hold. |
| 3 | Operational definitions of R/W/S and limitations | Descriptive methods table; no single numeric output source. [Screening protocol](../manuscript_revision/audit/ci01_independent_20261104/Screening_Protocol.md), [inclusion audit](../manuscript_revision/audit/ci01_independent_20261104/Inclusion_Exclusion_Audit.csv) and [conflict adjudication](../manuscript_revision/audit/ci01_independent_20261104/Source_Conflict_Adjudication.md) identify the definitions and qualifications. |
| 4 | Frozen 23-event scenarios | [Baseline scenarios](../04_Results/Scenario_Stability/tables/baseline_scenarios.csv): counts 9/9/5, frequencies, centers and mean R/W/S correspond. |
| 5 | Readiness expenses and benefit components | [Baseline inputs](../04_Results/Optimization/baseline_inputs.json): `setup_cost`, `life_score`, `property_score`, `recovery_score`. These are stipulated coefficients. |
| 6 | Legacy and inventory baseline benchmarks | [Frozen summary](../04_Results/Optimization/summary.csv), IDs `legacy_baseline` and `mobile_baseline`; also [validation baseline records](../04_Results/Optimization/validation.json). RP 686.007826 and 616.082500 correspond. |
| 7 | Inventory-baseline scenario deployment and score | [Baseline deployment](../04_Results/Optimization/baseline_deployment.csv), model `RP`; [saved mobile solution](../04_Results/Optimization/solutions/mobile_baseline.json), `rp.x` and `rp.location_scenarios`. Scenario scores 661.815000/616.000000/533.912500 and their probability-weighted sum 616.082500 correspond. |
| 8 | EV conventions and tied-policy ranges | [Eight-row EV summary](../manuscript_revision/peer_review_validation_20261105_v2/runs/primary/ev_summary.csv) and [optimal-policy enumeration](../manuscript_revision/peer_review_validation_20261105_v2/runs/primary/ev_optimal_policies.csv). A/B baseline agreement and 2/2/2/4 policy counts correspond. |
| 9 | F0–F3 controlled stock/procurement comparisons | [Component summary](../manuscript_revision/peer_review_validation_20261105_v2/runs/primary/component_summary.csv), capital budget 2,000,000 HKD and both frequency vectors. Distinguish these eight displayed rows from all 24 component/access cases. |
| 10 | Hypothetical minimum geographic deployment | [Coverage summary](../manuscript_revision/peer_review_validation_20261105_v2/runs/primary/coverage_summary.csv). Opportunity cost is the negative of `delta_vs_no_coverage`; k=6 objectives remain missing because those cases are INFEASIBLE. |
| 11 | Original/refitted/projected scenario comparison | [Scenario comparisons](../manuscript_revision/audit/ci01_independent_20261104/analysis/Scenario_Comparisons.csv), [scenario impact](../manuscript_revision/audit/ci01_independent_20261104/analysis/scenario_impact.json), [frozen-preprocessing projection](../manuscript_revision/audit/ci01_independent_20261104/analysis/fixed_old_preprocess_projection.csv). Final counts 35/19/6 and projected counts 43/12/5 describe different processing rules. |
| 12 | Final reconstructed 60-event scenarios | [Adjudicated scenario summary](../manuscript_revision/audit/ci01_independent_20261104/analysis/scenarios/reconstructed60_adjudicated/scenario_summary.csv) and [fit summary](../manuscript_revision/audit/ci01_independent_20261104/analysis/scenarios/reconstructed60_adjudicated/fit_summary.json). Counts, centers and R/W/S representatives correspond. |
| 13 | Common-59 station comparison | [Spatial impact](../manuscript_revision/audit/ci01_independent_20261104/analysis/spatial_impact.json), `ShekPik_common59_spatial` and `TaiO_common59_spatial`: counts 34/19/6 versus 41/15/3 and their weights correspond. This common set excludes Bebinca; it is distinct from the strict-59 Yagi sensitivity. |
| 14 | Frozen versus final-60 backend metrics | [Paired 555-case comparison](../manuscript_revision/audit/ci01_independent_20261104/backend_probability60/Original555_vs_Reconstructed.csv), IDs `legacy_baseline` and `mobile_baseline`; [final validation](../manuscript_revision/audit/ci01_independent_20261104/backend_probability60/validation.json). Mobile RP 616.082500→634.516667 and selected VSS 3.237826→34.313583 correspond. Tiny negative legacy EVPI residuals are display-rounded to zero. |

The two current embedded main-text images byte-match the retained Figure 1 study-area and Figure 2 inventory assets. Figure 1 remains subject to map/source permissions. Supplementary figure references point to the original Figure 3–7 assets; retaining their original filenames is consistent with renumbered captions S1–S5.

## Experiment and verification counts

Counts below were checked against saved CSV row counts or explicitly identified historical JSON records. Existing PASS records are not new reproduction results.

| Evidence version | Saved count | Meaning |
| --- | ---: | --- |
| [Frozen optimization summary](../04_Results/Optimization/summary.csv) / [solver audit](../04_Results/Optimization/solver_audit.csv) | 555 / 3,875 | Configurations / main solver rows; matches manuscript methods |
| [Final-60 summary](../manuscript_revision/audit/ci01_independent_20261104/backend_probability60/summary.csv) / [solver audit](../manuscript_revision/audit/ci01_independent_20261104/backend_probability60/solver_audit.csv) | 555 / 3,888 | Separate probability-only replay; not interchangeable with the frozen totals |
| [Supplementary solver audit](../manuscript_revision/peer_review_validation_20261105_v2/runs/primary/solver_audit.csv) | 500 | 498 OPTIMAL and two intended INFEASIBLE coverage controls |
| [Supplementary primary validation](../manuscript_revision/peer_review_validation_20261105_v2/runs/primary/validation.json) | 8 / 416 / 20 / 24 / 8 | EV specifications / fixed-policy EV trials / optimal-policy EEV rows / component cases / coverage cases; 20 is counted across specifications |
| [Supplementary independent validation](../manuscript_revision/peer_review_validation_20261105_v2/independent_validation/validation.json) | 936 | Historical HiGHS optimization calls; maximum recorded primary-objective difference 1.3073986337985843×10⁻¹¹ |
| [Frozen EV tie audit](../04_Results/Optimization/ev_tie_verification.json) | 1,716 / 1,796 | Policies / additional audit solves across ten cases |
| [Final-60 EV tie audit](../manuscript_revision/audit/ci01_independent_20261104/backend_probability60/ev_tie_verification.json) | 1,716 / 1,808 | Same kinds of counts for a different frequency version |

Each 555-case suite comprises two baselines, two 21-case capacity grids, 26 spatial cases, eight subsets, 56 one-factor cases, 400 joint cases, nine procurement cases, five initial-stock cases, five purchase-price cases and two access cases. Thus “25 spatial grid cases” excludes the additional cross case, and “200 paired draws” generates 400 configurations.

The candidate and inclusion ledgers each contain 63 identities. Their annual totals reproduce supplementary table S16: 62 warning groups, 23 original identities, 60 analyzable identities and three pending identities. Stored frozen clustering verification separately reports 9,032 resampling/deletion fits and 37 nonglobal Lloyd fits in [scenario verification](../04_Results/Scenario_Stability/verification.json). The three source hashes in [the v3 supplementary arithmetic check](../manuscript_revision/v3_audit/supplement_numeric_check.json) match the current EV, component and coverage summary CSVs.

## Current manuscript gaps and limits

Paragraph locators here count direct-body paragraphs, including empty paragraphs; they are not page numbers. These are pre-existing manuscript differences, preserved during repository organization.

- Paragraph 218 asserts an ethics exemption and paragraphs 220–223 specify author contributions, whereas source v3 contained confirmation placeholders. These statements require author confirmation; the repository audit does not independently establish them.
- Paragraph 223 ends with “Writing – original draft Competing interests.” without an actual competing-interest declaration. The standalone funding paragraph present in v3 is absent from the current merged file.
- TODO-A1 (author details), TODO-A6 (versioned access/archive conditions) and TODO-A7 (AI-disclosure approval) remain in paragraphs 224, 217 and 225. The target venue, author approval and release conditions remain unconfirmed. A repository URL alone is not a versioned deposit or DOI.
- The historical original-23 candidate/exclusion register, original anchor rule and contemporaneous explanations for four non-R11 station substitutions remain unrecovered. New retrospective rules cannot replace that provenance.
- TC2017_06 has unresolved official W/S conflicts; TC2021_02_E and TC2021_02_W lack separable cyclone-specific observations. Yagi has an unresolved surge-peak date despite agreed extrema. These pending/conflicting records must not be silently filled or relabelled as resolved.
- No measured mapping from R/W/S to response effectiveness, resources, costs, exposure or avoided loss has been supplied. Callable stock, access/transport, effective pump performance, outlets, crews, duration, failures and a common economic basis remain unvalidated. CI-01 remains PARTIALLY RESOLVED / NOT FULLY CLOSED; CI-06 remains OPEN.
- Coverage WS/EV/EEV/VSS and general B-convention reruns of the old 555-case suites/procurement grids were explicitly not computed. They are outside the available results and must not be inferred from baseline A/B agreement.

The [remaining submission blockers](../manuscript_revision/Remaining_Submission_Blockers.md) and [research risks](../manuscript_revision/Remaining_Research_Risks.md) retain further context. Their historical document-QA statements must be read alongside the current-file hash discrepancy above. No missing evidence has been replaced with invented data, example results or new scientific conclusions.
