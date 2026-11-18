# Supplementary archive alignment check

Date: 18 November 2026 (Asia/Shanghai). Status: **PASS for archival presence, references, saved-record counts and checked numerical transcription**. This check ran no optimization, clustering, resampling, new scientific experiment or manuscript edit.

## Files and checks

The retained reading copy contains S1–S13, Tables S1–S16, Figures S1–S5 and four supplementary equation labels. All 32 explicit local link destinations exist; all five image destinations are present. Removing link destinations makes the reading copy byte-for-byte text-identical to the original supplementary Markdown. No scientific text, number, caption, historical statement or source manuscript was changed.

The current merged manuscript explicitly names `Supplementary_Methods_and_Results.md` at direct-body paragraph 258. All explicit S references in the Word body resolve to retained supplement headings. Paragraphs 94, 140, 188 and 194 agree with the saved experiment/solver counts below. Direct-body paragraph numbers are XML locators, not page numbers.

A total of **98 structural/count/reference checks and 768 numeric comparisons passed**: 672 comparisons in the numerical Supplementary Tables and 96 in main Word Tables 8, 9, 10 and 14 against their shared source evidence. Table S5 is a descriptive switch table and was checked separately for its six component labels; its prose is not misrepresented as a numerical experiment. Decimal values are compared within half a unit at their printed precision; integer counts are exact to floating tolerance. Repeated specification/sector cells are counted as separate comparisons. This is a transcription/evidence check; actual rerun status remains in `REPRODUCIBILITY_AUDIT.md` and its execution evidence.

The auditable outputs are:

- [Machine-readable section, source-hash and reference index](supplementary_index.json).
- [All numeric comparisons](supplementary_numeric_comparisons.csv).
- [Read-only checking script](check_supplementary.py); executed against the local research tree with `python3 audit/submission_20261118/check_supplementary.py`. It requires the unchanged local Word manuscript and linked source evidence. The Word manuscript is excluded from the candidate submission tree, so this is a local manuscript/supplement alignment check, not a candidate-clone test; its saved comparison records preserve the checked values and source hashes.

## Supplementary sections

Line numbers refer to `supplementary/Supplementary_Methods_and_Results.md`.

| Section | Retained heading | Line |
| --- | --- | ---: |
| S1 | Scope and evidence versions | 5 |
| S2 | EV conventions and complete baseline policy comparisons | 25 |
| S3 | Controlled model components | 101 |
| S4 | Hypothetical minimum geographic coverage | 163 |
| S5 | Frozen spatial heterogeneity | 204 |
| S6 | Frozen intervention subsets and one factor perturbations | 214 |
| S7 | Frozen joint parameter stress tests | 230 |
| S8 | Frozen legacy bounds and capacity grids | 253 |
| S9 | Detailed procurement and inventory sensitivity | 275 |
| S10 | Original event data and source ledger | 323 |
| S11 | Scenario dependent illustrative requirements | 355 |
| S12 | Reconstructed local warning frame and provenance | 373 |
| S13 | Verification scope and source-reading boundaries | 398 |

## Experiment counts checked against retained records

| Package | Configurations or specifications | Solver/evaluation records |
| --- | ---: | --- |
| Frozen 23-event suite | 555 | 3,875 main rows, all OPTIMAL |
| Reconstructed 60-frequency suite | 555 | 3,888 main rows, all OPTIMAL |
| Targeted A/B baseline comparison | 8 | 416 fixed-policy EV trials; 20 optimal-policy EEV rows counted across specifications |
| Controlled components/access | 24 | RP only |
| Hypothetical coverage | 8 | Six OPTIMAL, two intentional INFEASIBLE; no infeasible objective filled with zero |
| Entire targeted supplementary package | 500 primary solves | 498 OPTIMAL + 2 intended INFEASIBLE |
| Retained independent supplementary verification | 936 calls | Maximum primary-objective error 1.3073986337985843e-11 |

Both 555 suites have the same configuration breakdown: two baselines, two 21-case capacity grids, 26 spatial cases (25 grid + one cross), eight subsets, 56 one-factor cases, 400 joint cases (200 paired draws), nine procurement limits, five initial-stock cases, five purchase-price cases and two access cases. Summing the configurations gives 555. The 63-candidate ledger and inclusion audit reproduce Table S16: 62 warning groups, 23 original identities, 60 analyzable identities and three pending. Earlier 61-record trials remain superseded.

## Integrity and remaining limits

- Current merged Word SHA-256: `4e12f7849d0b2ca7dd0d156c987a9e90f8b651880c79b74e10f14bffbab4ca37`. It differs from the hash certified by the historical merged-document rendering audit; that historical QA is not current Word visual QA. The Word file was read only and was not modified.
- Original supplement SHA-256: `b5913966d2061b1e681ee72ffb553fc348a4088b9fedc8730c3d11abf7113641`. Reading-copy SHA-256: `a8212932368491f729ec791e077aa804ab71fb42bbf301d39cc9b5f9142a9267`. Their only content difference is relative link destinations.
- No supplementary section, table, figure or checked numeric result was found missing or inconsistent. This does not certify author approval, current declarations, third-party redistribution rights, publication or a versioned deposit.
- Historical original-23 screening/anchor/station-selection evidence remains unrecovered; this archival check supplies none of those missing records.
- There is no field-calibrated R/W/S-to-effectiveness/resource/cost mapping. Illustrative scores and CU are not measured avoided losses or monetary benefits; HKD procurement remains separate.
- The three pending identities remain TC2017_06, TC2021_02_E and TC2021_02_W. Yagi remains extrema-only with its unresolved peak-date conflict.
- The 37 nonglobal Lloyd fits among 9,032 historical resampling/deletion fits remain a disclosed limitation. No algorithm or saved fit was replaced.
- The four 60-event mobile EV optima retain VSS 8.019000–34.313583. Selection rules and ranges remain necessary; no unique primary-optimal policy is asserted.
- All 555/procurement suites retain convention A. Baseline A/B agreement does not establish general equivalence; component/coverage variants report RP only.
- This report verifies local destinations and source hashes. Whether all are selected into the submission Git tree and legally redistributable is a separate release check; local existence is not a public-clone claim. No file was committed or pushed.

The broader unchanged manuscript issues and historical/source boundaries are retained in [the manuscript alignment audit](../Manuscript_Alignment.md). No missing evidence was replaced with invented data.
