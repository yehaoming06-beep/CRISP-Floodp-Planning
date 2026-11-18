# V3 manuscript change log

Prepared 6 November 2026 (Asia/Shanghai). This is a versioned submission candidate for a conditional methods-validation case, not a submitted article or an acceptance assessment. All scientific results integrated here were already present in the frozen v2, the CI-01 reconstruction, or the completed 5 November supplementary review. No new optimization, clustering experiment, field observation or untargeted stress test was added.

## 1 Inputs and source precedence

The revision read both `Revised_Manuscript_EN_v2.md` and `.docx`, including their body, tables, native equations, figures and source links. A read-only comparison confirms the two v2 formats agree on 262 content blocks, 20 tables, seven figures and 18 equation groups represented by 19 native Word math objects. Their SHA-256 values are recorded in [the v2 read-only comparison](v3_audit/v2_word_sync_read_only.json).

The five supplementary inputs are the final files in `peer_review_validation_20261105_v2`: [Peer Review Issues](peer_review_validation_20261105_v2/Peer_Review_Issues.md), [EV Convention Sensitivity](peer_review_validation_20261105_v2/EV_Convention_Sensitivity.md), [Controlled Model Ablation](peer_review_validation_20261105_v2/Controlled_Model_Ablation.md), [Methodological Contribution Matrix](peer_review_validation_20261105_v2/Methodological_Contribution_Matrix.md), and [Revised Experiment Recommendations](peer_review_validation_20261105_v2/Revised_Experiment_Recommendations.md). The unused earlier review-v1 directory and superseded 61-record trial were not adopted as final results.

Prior risk/source evidence includes `Critical_Issues.md`, `Citation_Audit.md`, `Event_Validation_Audit.md`, `Remaining_Research_Risks.md`, the CI-01 resolution and conflict-adjudication reports, original source manifests and the current integration's source-risk record. The 5 November CI-01 status takes precedence over the historical 4 November OPEN entry. **CI-01 remains PARTIALLY RESOLVED / NOT FULLY CLOSED; CI-06 remains OPEN.** CI-05's author-version/final-publication limitation remains PARTIAL. Older files were not retroactively edited.

## 2 Changes responding to the requested tasks

| Request | Final location | Change and evidence boundary |
| --- | --- | --- |
| A: retain A and compare A/B | Main Sections 3.5 and 5.3, Equations 15–19, Table 8; Supplementary S2 | Retains all frozen A results. Defines B from averaged primitive resources. Reports identical baseline optimal policy sets and EEV/VSS ranges for the eight tested specifications, alongside nonidentical fixed-policy EV values. Does not relabel the 555-case A suite as B. |
| A: separate model components | Main Sections 3.8 and 5.4, Table 9; Supplementary S3 | Separates unrestricted stock, replicated stock, shared stock and procurement-integrality domains. Reports finite-stock contractions, the zero pure-sharing optimal-value difference, the distinct-feasible-set witness, and the current procurement-relaxation equivalence proof. All 24 RP specifications and access branches are retained in the supplement. |
| A: minimum geographic coverage | Main Equation 20, Section 5.4, Table 10; Supplementary S4 | Defines an assumed actual-deployment lower bound for each sector/scenario, using heterogeneous abstract units. Reports k = 1/2 opportunity costs and the certified k = 6 infeasibility. No protected population, measured equity or uncomputed coverage EV/EEV/VSS is inferred. |
| A/C: preserve frozen results and class semantics | Main Sections 3.7, 4.2–4.3 and 5.5–5.7; Tables 11–14 | Separates old 23, refitted 60, frozen-rule projection and the two differently constituted 59-record subsets. Retains conditional-frequency interpretation, label migration, changed representatives and unchanged backend coefficients. RP changes are model-score sensitivities, not real mitigation gains. |
| B: closest literature | Main Sections 1, 2 and 6.1, References 27–30; Supplementary S13.2 | Adds Chang et al. (2007), Garrido et al. (2015), Yosua et al. (2025), and Lopane and Dawson (2026). DOI identities and primary-source access/read scopes were checked. Abstract/preview/excerpt and selected published-section access are not described as complete paper audits or human-author reading. |
| B: contribution positioning | Abstract, Introduction, Related Work, Discussion and Conclusion | Positions the work as an auditable conditional case, inventory-constraint expression, scenario-source/spatial-proxy sensitivity and parallel EV-policy analysis. Removes any inference that general two-stage planning, integer procurement, sharing or correct EEV fixing is a first invention. |
| C: focus and consistency | Entire main manuscript and supplementary cross-references | Revises all six requested prose sections; reduces repeated discussion and relocates detailed noncore experiments and appendices. Retains units, pending identities, source conflicts and author-confirmation placeholders. |
| D: submission gate | Final_Submission_Readiness.md and Remaining_Submission_Blockers.md | Separates completed content fixes, remaining author/access/venue actions, recommendations and disclosed limits. No fatal mathematical contradiction was identified within the bounded claim; neither field-free calibration nor numerical PASS alone decides submission suitability. |

## 3 Content relocation and identifiers

| Frozen v2 item | V3 destination |
| --- | --- |
| Table 1 notation; Tables 2–5 census, sources and inputs; Tables 6–7 frozen baseline/deployment | Main Tables 1–7, with their table rows unchanged |
| Table 8 resource use | Main Section 5.2 compact resource-use paragraph; original full table remains in unchanged v2/evidence |
| Tables 9 and 17 procurement/policy ranges | Supplementary Tables S12 and S13, Section S9 |
| Sections 5.4–5.7; Figures 3–7 | Supplementary Sections S5–S8, Figures S1–S5; unchanged image files reused |
| Table 10 joint perturbation quantiles; Table 11 legacy bound correction | Supplementary Tables S10 and S11 |
| Tables 12–13 refitting and representatives | Main Tables 11–12 |
| Table 14 label migration | Main Section 5.5 narrative retaining all migration counts and identities; source CSV retained |
| Tables 15–16 station/frequency comparisons | Main Tables 13–14 |
| Appendices A, B and C | Supplementary Sections S10, S11 and S12, Tables S14–S16 |
| Original Section 3.6 detailed experimental design | Supplementary S1.1, with condensed scope retained in main Section 3.6 |

Equations 1–14 retain their scientific definitions. Equation 15 names the retained A convention; Equation 16 adds B. Former Equations 16–18 become 17–19, and Equation 20 defines hypothetical geographic deployment. The final Word document contains editable native equations. During visual QA, the Word builder's unbraced-argument handling was corrected so that the A/B superscript and sector/intervention subscript attach separately to U; barred means also retain their correct index placement. This changes rendering, not model inputs, formulas or scientific results. Two long table headers were shortened to prevent midword wrapping.

## 4 Verification performed in this revision

- Read-only table/source comparison confirms 11 retained main tables and seven relocated tables have exactly the same rows as their corresponding v2 tables. New EV, component and coverage table entries were checked against the completed review's CSVs, including signed opportunity costs and undefined objectives for infeasible cases. See [candidate validation](v3_audit/candidate_validation.json) and [independent main/supplement review](v3_audit/independent_main_supplement_review.json).
- The final Word/Markdown comparison matches all 232 prose/table blocks, 14 tables, two figures and figure descriptions. Equation groups 1–20 correspond to 21 native math objects because the two policy-range expressions share one number. References 1–30 all have body citations, with 61 expanded mentions and no undefined/orphan reference. See [Word synchronization](v3_audit/word_sync_verification.json).
- The Word candidate was rendered to 23 pages and every page visually inspected. Corrections were re-rendered and the five changed pages reinspected; the remaining 18 final page images match their previously approved images byte for byte. Final page-level evidence is in [visual QA](v3_audit/visual_qa_final.json). Internal render PDFs/PNGs are QA artifacts, not additional deliverables.
- SHA-256 comparison covers 27,324 pre-existing files, excluding task outputs and transient/system metadata as defined in the manifest. No recorded file changed. This includes v2, frozen model inputs, old experiments, results and figure files. See [before manifest](v3_audit/frozen_manifest_before.json) and [candidate validation](v3_audit/candidate_validation.json). This guard has a different file population from earlier 977/969/21,678-file guards and does not replace their definitions.

Whitespace-delimited counts, including tables and references, decrease from 14,429 in v2 to 11,750 in the v3 main file (18.6%). These are comparison counts, not a target journal's word-limit calculation. The supplementary file retains the relocated details.

## 5 Remaining decisions

Names and existing affiliations are retained without inventing a corresponding author or CRediT roles. TODO-A1–A7 remain for actual author details, ethics, contributions, interests, funding, archival access and AI disclosure. The authors must select a venue and meet its real article-type, access and packaging requirements. No repository DOI, human approval, ethics exemption, funding denial or competing-interest denial was fabricated.

The final files are submission candidates, not a claim of journal acceptability. CI-01 and CI-06 remain at their disclosed statuses. Their evidence limits block stronger historical-completeness, empirical-effect and operational-policy claims; no unmeasured coefficients or additional experiments have been inserted to make those limits appear resolved.
