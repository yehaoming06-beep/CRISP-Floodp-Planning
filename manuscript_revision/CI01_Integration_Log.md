# CI-01 Integration Log — English Manuscript v2

Date: 5 November 2026 (Asia/Shanghai).

Status: **INTEGRATED; numerical consistency checks passed; CI-01 remains PARTIALLY RESOLVED / NOT FULLY CLOSED.** Word synchronization and final visual review are recorded in Section 6.

## 1. Authorized scope and preservation

The revision integrates the existing independent retrospective screening evidence into the English method-validation paper. It adds no optimization experiment, empirical calibration, occurrence model or journal-specific formatting. The final 60-record chain is integrated as a separately identified comparison; it does not overwrite the historical 23-event reference or replace illustrative response coefficients.

Before manuscript editing, 969 current project files (108,636,347 bytes) were copied and SHA-256 checked in `audit/ci01_integration_20261105/before/`. This backup covers all files under `01_Data/`, `02_Model/`, `03_Experiments/`, `04_Results/`, `05_Code/`, `06_Manuscript/`, plus the original English Markdown and Word manuscripts. `backup_manifest.json` records every original path, size and hash. The original files remain unchanged. The earlier CI-01 guard's 977-file count concerns its separately defined historical manifest, rather than this integration backup's file population.

All new deliverables are separate files in `manuscript_revision/`:

1. `Revised_Manuscript_EN_v2.md`
2. `Revised_Manuscript_EN_v2.docx`
3. `CI01_Integration_Log.md`
4. `New_Results_Verification.md`
5. `Remaining_Research_Risks.md`

The original manuscript remains available under its original name. The versioned v2 is the integrated manuscript for review. The independent evidence directory, historical logs, frozen model and result workbooks were not edited.

## 2. Required materials read before integration

| Material | Read and use |
| --- | --- |
| Original `Revised_Manuscript_EN.md` and `.docx` | The complete Markdown and Word body/table/equation text were read. Word text was extracted to the integration audit directory; its existing native equations, figures and style conventions guided the synchronized v2 |
| `CI01_Resolution_Report.md` | Final flow, verification boundaries and partial-resolution status |
| `Screening_Protocol.md` | Candidate definition, anchors, whole-window rainfall priority, QC, tide interpretation and retrospective status |
| `Candidate_Event_Inventory.csv` | All 63 candidate rows, identities and warning-source links |
| `Inclusion_Exclusion_Audit.csv` | All 63 candidate dispositions, station/QC fields and pending reasons |
| `Original23_vs_Reconstructed.csv` | All 63 outer-reconciliation rows, including the 23 original identities and unchanged numerical vectors |
| `Scenario_Impact_Assessment.md` | Final-60 scenarios, projection/refit contrast, migration, matched-station analysis, frequency-only backend comparison and limits |
| Official sources and evidence | Official-source/PDF manifests, retained HKO warning and tide records, station-window evidence, conflict cross-check, source-conflict amendment and spatial addendum |
| Recalculation records | Final structured verification, scenario summaries, input packages, 555-case comparison/solutions/audits, replay summary, EV-policy range records, existing stability rows and relevant logs |

The required-CSV read summary, source-review record, extracted original Word text and numerical checks are retained in `audit/ci01_integration_20261105/`. Selected HKO pages were checked online again on 5 November: the warning-database landing page, the 2021 two-depression report, the September 2017 tide table and Yagi's 2024 tide table. The raw storm-surge database was inspected from the retained complete responses; no fresh full-database download or instrument validation is claimed.

## 3. Manuscript changes and evidence mapping

| Location | Integrated change | Supporting records and claim limit |
| --- | --- | --- |
| Abstract | Reports 63/60/3, 9/9/5 versus 35/19/6, matched-59 contrast, frequency-only baseline values and EV range | Final scenario/backend files; states method sensitivity rather than measured policy gains |
| Introduction and contributions | Frames event selection, spatial proxy and conditional-frequency dependence as explicit method-validation questions | Does not assert recovered historical rules, comprehensive Tai O flood coverage or empirical response calibration |
| Methodology 3.2 and Eq. (5) | Distinguishes historical 23 from the new retrospective frame; defines highest-signal first-date anchor, R11→HKA→R12, five-day whole-station QC and Shek Pik extrema; uses dataset-specific denominator T | Protocol v1.0, disclosed conflict interpretation v1.1 and spatial addendum; no prospective preregistration or blinded-team claim |
| Methodology 3.7 | Separates unchanged-identity reconstruction, frozen projection, full refitting, common-identity station sensitivity and frequency-only backend replay | No empirical R/W/S→resource/cost/benefit mapping is introduced |
| Data 4.2–4.3 | Explains 203 segments, 62 warning groups, 63 identities, 60 analyzable, three pending, zero entity exclusions; records five shifted anchors with unchanged vectors | Candidate/audit/reconciliation CSVs; names all pending identities and Yagi's unresolved surge-peak date |
| Results 5.1–5.7 | Retains frozen-sample numerical results and labels their frequency basis | Existing computational reference remains traceable; the old 3,875-solve suite is distinguished from the new 3,888-row audit |
| Results 5.8, Tables 12–14 | Adds CRITIC/count/frequency comparison, representative values, frozen projection and the original-identity migration matrix | Existing numerical outputs independently recalculated; labels reflect refitting rather than changes in old observations |
| Results 5.9, Table 15 | Adds Tai O versus Shek Pik on the same 59 identities | Bebinca's Tai O missingness retained; this identity set differs from the strict 59-record sensitivity omitting Yagi |
| Results 5.10, Table 16 | Adds paired baseline metrics from the existing 555-case frequency-only comparison | Saved parameter/configuration packages checked case by case; hypothetical probability perturbations remain applied and renormalized |
| Results 5.11, Table 17 | Reports EV policy counts and EEV/VSS ranges for nine inventory limits; describes the tenth, legacy case | Exhaustive first-stage tie audit covers ten cases, not all 555 configurations |
| Discussion 6.3–6.5 | Analyzes sample composition, refitting, spatial proxies, illustrative coefficients, source conflicts and limits on operational inference | Original screening history, three pending identities, Yagi timing and calibration gaps remain open |
| Conclusion | Replaces broad main-result language with evidence-qualified method-validation conclusions | Sample fractions remain conditional; no annual/future flood probability, avoided-loss or procurement recommendation |
| References and Appendix A | Adds official references 21–26 and qualifies numerical corroboration versus timing/instrument accuracy | Preserves old registered URLs, original anchors and Yagi's unresolved peak date |
| Appendix C, Table C1 | Adds annual candidate flow, final-versus-superseded version identification and provenance | Does not treat the earlier 61-record trial as the final individual-cyclone sample |

The full text diff and the scripted change list are `manuscript_v2.diff` and `integration_changes.json` in the integration audit directory. The preserved equations remain numbered (1)–(18). The only model-equation change is replacing the fixed sample denominator 23 with T in Eq. (5); the optimization formulation and coefficients are preserved.

## 4. Supported numerical conclusions

| Check | Verified result |
| --- | --- |
| Original identities under new rules | All 23 R/W/S vectors and selected stations unchanged; five anchors shift one day earlier |
| CRITIC R/W/S | Original: 0.434081/0.335229/0.230689; final 60: 0.487217/0.286080/0.226703 |
| M/S/E counts | 9/9/5 versus 35/19/6; frozen-rule projection of the 60 gives 43/12/5 |
| Old-label migration | Six of 23; ARI 0.375140 |
| Same-59 tide-station comparison | Shek Pik 34/19/6 versus Tai O 41/15/3; ten label changes; ARI 0.575573 |
| Mobile RP, frequency-only | 616.082500 to 634.516667 model-score units; original first-stage RP policy remains feasible and optimal, regret zero |
| Final mobile EV tie range | Four EV-optimal policies; EEV 600.203083–626.497667; VSS 8.019000–34.313583 |
| 555-case isolation | Only base probabilities differ in every paired saved parameter package; configurations/fleet assumptions and all other coefficients match |
| Replay | The two saved 555-row summaries are byte-identical; existing new solver audit contains 3,888 OPTIMAL rows |
| Existing stability diagnostics | 2,009 existing rows independently aggregated; year/episode/leave-year statistics agree with saved summaries |

`New_Results_Verification.md` states the arithmetic methods, exact source paths, tolerances and full tables. No optimization solver or new resampling experiment was run during integration. Recomputing CRITIC, exact sorted partitions, ARI, row counts and saved-result aggregates was limited to consistency verification.

The increase in the mobile RP score is a change in conditional weighting of illustrative scenario scores. It is not an observed gain from a new policy; the original RP policy has zero regret under the new base frequencies. EV is an averaged-scenario objective; EEV evaluates a complete first-stage policy under the scenarios. VSS and EVPI remain model information values. The one-policy VSS 34.313583 is reported together with the audited 8.019000–34.313583 range.

## 5. Version discrepancy and unresolved research issues

`logs/final_backend_run.log` retains obsolete `new61` field names and a sentence referring to two pending attributions. The final numerical inputs are the 60-event vector. Final `backend_probability60/inputs.json`, `validation.json`, the paired CSVs, the EV-policy tables and `logs/Final_Verification.json` control the integration: **60 analyzable identities, three pending**. The earlier 61-record trial and its output directory remain preserved, without alteration of the original log text.

The 61-observation warning-group sensitivity is separately identified as a change in analysis unit. It is not the superseded trial and does not resolve the two shared-summary cyclone identities. The strict 59-record conflict sensitivity omits Yagi; the spatial common-59 comparison omits Bebinca instead. These similarly sized datasets are not conflated.

CI-01 is not marked closed. `Remaining_Research_Risks.md` retains the historical screening gap, bounded frame, post-data retrospective choices, three pending identities, Yagi timing, mixed drivers, spatial/datum representativeness, sample dependence, annual/future-probability restrictions, uncalibrated coefficient mapping and model simplifications. Official numerical corroboration does not prove instrument calibration. The revised manuscript makes no field-measured or causal policy-benefit claim.

## 6. Markdown/Word synchronization and delivery checks

The v2 Word file is generated from the final v2 Markdown using a separate, v2-only builder. It preserves the original general document style rather than applying a journal template. All seven figures are retained. New tables are numbered 12–17, with annual flow in Table C1; the pre-existing Tables 1–11, A1 and B1 retain their identifiers. Units and sources are stated with the new tables.

The synchronized structure contains 20 tables, seven embedded figures, 18 numbered equation groups and 19 native Word math objects (Eq. 18 spans two objects). There are 262 body/table blocks, checked individually against the Markdown. Native math is retained, rather than replacing equations with pictures. The final Word rendering is 30 pages.

Final visual review: **PASS**. All 30 rendered pages were inspected individually. New CRITIC-weight tables, the migration matrix, the baseline metric comparison and the long EV-range table are legible, with no clipping, overlapping text, missing content or malformed table rows. Table C1 uses the caption style. Two pages retain reasonable lower-page whitespace because a pre-existing figure/caption group moves together to the next page; this is a pagination consequence, not missing content. `word_sync_verification.json`, `word_render_qa.json` and `Word_Render_QA.md` retain the synchronization results and page-level review record. The Word build records the exact final Markdown hash.

The final delivery audit checks output existence, numbering, source references, preserved-original hashes and Markdown/Word synchronization. Its machine-readable records, builder and rendering QA are kept under `audit/ci01_integration_20261105/`. Deliverable hashes are recorded in a separate `delivery_manifest.json`, avoiding a circular hash inside this log.

No publication, external submission, repository deposit or journal-format conversion was performed.
