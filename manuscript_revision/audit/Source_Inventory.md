# Source inventory and evidence precedence

Audit date: 4 November 2026. The complete manuscript source is `06_Manuscript/Original_Draft_for_Revision.docx`. Its 438 paragraphs and nine tables were extracted read-only for revision. The latest regional replacement is `06_Manuscript/Sections/Study_Area_and_Parameters.docx`, with 32 paragraphs and one table. The latest model-and-results merge source is `06_Manuscript/Sections/Model_and_Results_EN.md`.

The project README identifies `01_Data/CRISP_Master_Data.xlsx` as the single current input workbook and `04_Results/Optimization/CRISP_Results.xlsx` as the current result workbook. Model version `mobile_inventory_v2`, the 4 November run manifest and its source hashes agree with the current code. The result workbook contains six sheets: 结果概览, 全部配置, 上界修正, 库存与并列解, 基准部署 and 假设与来源. Its 555 configuration rows agree with `summary.csv`, `report_data.json` and the retained `solutions/` JSON files.

The master workbook contains Scenario, Intervention_Params, Benefit_Params, Baseline_Settings, Mobile_Pump, Study_Area, Evidence and Input_Guide. Its separation of HKD, CU, physical stock, demographic context and missing field inputs governs the manuscript. Missing physical parameters are not replaced by zero.

## Current model and experimental evidence

- `02_Model/crisp_parameters.py`: coefficient reading and resource-derived bounds.
- `02_Model/crisp_model.py`: readiness, procurement, shared stock, access, recourse, EV averaging, complete first-stage fixing and secondary selection rules.
- `03_Experiments/Optimization/code/experiment_design.py` and `run_experiments.py`: 555-configuration design.
- `03_Experiments/Optimization/code/audit_ev_ties.py`: EV-policy enumeration, including the 10⁻⁶ objective comparison tolerance.
- `04_Results/Optimization/模型修改与重跑报告.md`: integrated interpretation and calibration limits.
- `validation.json`, `independent_verification.json`, `report_verification.json` and `ev_tie_verification.json`: previously completed computational checks, with no field-validation claim.
- `solutions/*.json`, `ev_optimal_policies.csv`, `ev_policy_tie_ranges.csv`, `uncertainty_intervals.csv`, `plan_frequencies.csv`, `ablation_contributions.csv` and `legacy_correction_comparison.csv`: detailed numerical evidence.
- `manifest_start.json`, `Run_Sources.zip`, `Solver_Logs.zip`: run provenance and logs. Legacy controls in `01_Data/Controls` are regression references, not observations.

## Study sectors and sources

`01_Data/Spatial/census_units.csv`, `census_units.json`, `zone_summary.json` and `tai_o_census_aligned_zones.geojson` define complete census-unit sectors. Official CSDI metadata and geometry are under `01_Data/Sources/Census/`. `census_ssg_2021_utf8.csv` and archived `Calibration/SSUG_21C.csv` preserve the statistical records. The map is `04_Results/Study_Area/Tai_O_Zones.png` and `.pdf`.

Tai O1 = 94404S, 825 residents. Tai O2 = 94401S + 94409 + 94411, 2,853 residents. Counts describe 2021 resident population. Four-unit aggregation contains 3,678 residents, 1,680 domestic households and 1,684 occupied quarters. Rural unit 94101S is excluded in its entirety. No clipping or population interpolation is introduced.

`01_Data/Sources/source_registry.json` is the parameter/official-source register. The Evidence sheet contains 24 numeric evidence entries with adoption limits; these are not all adopted as model coefficients. Twenty calibration sources and census source entries are archived locally. The approximate pump purchase price is supported by the 12 August 2025 government equipment report. Reported maximum discharge and refuelling interval remain metadata.

## Events and scenario checks

`01_Data/Events/event_metadata.csv` supplies 23 row-level source records; `model_input.csv` contains the frozen three-indicator vectors; `reference_events.csv`, `reference_indicators.csv` and `reference_scenarios.csv` supply computational controls. Two publication XLSX tables are retained but contain outdated rainfall wording. Their original labels are not adopted in the revised manuscript.

Rainfall archives are in `01_Data/Sources/HKO/r11_daily/`. All 23 selected records agree after RF extraction. The selected inventory's initial sampling frame is not available. The preceding evidence-consistency audit directly read 18 official tide tables. The 4 November follow-up recovered complete official sources for E004, E019, E021, E022 and E023 and checked the station, W/S values, peak dates/times, units and visible quality notes. E020 retains the combined northeast-monsoon and Man-yi rise. The six original E018–E023 tide URLs remain preserved, with verified official alternatives added to Appendix A. Complete recovery snapshots, PDF page locators and SHA-256 records are in audit/fixes_20261104. A source-table match does not validate the sampling frame, station-substitution history or field calibration.

Scenario stability evidence comes from `04_Results/Scenario_Stability/完整分析報告.md`, its tables, `baseline_audit.json`, `verification.json`, `reproducibility.json` and saved resampling outputs. The current optimization revision does not alter these event inputs or propagate their bootstrap draws into optimization.

## Figure mapping

| Revised figure | Existing source stem | Use |
| --- | --- | --- |
| Figure 1 | `04_Results/Study_Area/Tai_O_Zones` | Census-aligned map |
| Figure 2 | `04_Results/Optimization/figures/fig01_inventory` | Procurement and EV policy ranges |
| Figure 3 | `04_Results/Optimization/figures/fig02_spatial` | 25-cell spatial grid |
| Figure 4 | `04_Results/Optimization/figures/fig03_ablation` | Eight intervention subsets |
| Figure 5 | `04_Results/Optimization/figures/fig04_oat` | One-factor endpoints |
| Figure 6 | `04_Results/Optimization/figures/fig05_uncertainty` | Paired parameter draws |
| Figure 7 | `04_Results/Optimization/figures/fig06_bounds` | Legacy bound correction |

PNG and vector PDF files are copied without changing their content. The map and all six plots were visually inspected. Figure numbering, captions and scope are unified in the new manuscript, while the original assets remain untouched.

## Revision-local audit records

`source_manifest_before.json` records SHA-256 and byte counts for 972 original project files, excluding runtime/cache directories. `evidence_verification.json` records the current arithmetic and source checks. `Citation_Verification.csv` records the 20 revised sources and their verification depth. `Original_Reference_Disposition.csv` records all 33 original reference entries. The final manuscript and DOCX content/visual checks are recorded in `delivery_checks.json`. No archive or source document is overwritten.

## Follow-up revision on 4 November 2026

CI-02/03/04/07/08 CLOSED within their stated scopes; CI-05 PARTIAL (Gabrel author-version sections read, final publisher text unavailable); CI-01/06 OPEN. See Fix_Log.md, Remaining_Blockers.md and audit/fixes_20261104/consistency_validation.json. The original 23 numerical vectors, model, workbooks and experiment results are unchanged. event_metadata.csv differs only in E020 data_quality_note.
