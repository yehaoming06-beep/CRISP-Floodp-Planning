> **Current delivery selection (18 November 2026):** the following is the earlier rights audit. The current [delivery report](delivery_20261118/DELIVERY_REPORT.md) supersedes its packaging status. Complete HKO legal notices/conditions and official disclaimers now accompany the numerical subset in [THIRD_PARTY_NOTICES](../THIRD_PARTY_NOTICES.md); raw archives remain excluded. Full numerical logs and unique solution/tie evidence are represented in checked archives, not silently discarded. The new [source access manifest](../data/provenance/source_access.csv) retains 338 verified source records. No blanket license, raw-source release or historical-guard PASS is asserted.

# Data rights, access and evidence status

Checked on **18 November 2026**. This is an evidence and release-status record, not legal clearance. The local source is `/Users/yehaoming/Desktop/climate_Devin`; the original research files and manuscript have not been edited. No repository-wide license has been added, and author-produced computational results have not been assigned a new license.

## Materials and provenance

The native numbered layout is retained because existing research programs use those relative paths.

| Material | Local location | Interpretation |
| --- | --- | --- |
| Original model parameters | `01_Data/CRISP_Master_Data.xlsx`; `01_Data/Evidence/`; `01_Data/Controls/` | Workbook inputs, parameter evidence and historical numerical controls. Operating/benefit coefficients include illustrative assumptions. |
| Original event observations and processed inputs | `01_Data/Events/event_metadata.csv`, `reference_events.csv`, `model_input.csv` | Historical 23-event set; model input has 23 data rows. It is not an exhaustive flood-event register. |
| Raw third-party archives | `01_Data/Sources/Calibration/`, `Census/`, `HKO/`; nested `sources/` directories under `manuscript_revision/` | Saved webpages, PDF reports, source responses, extracts and map data; downloading does not establish redistribution rights. |
| Original spatial inputs | `01_Data/Spatial/` | Census statistics and author-defined sector geometry; population context does not establish exposed or protected population. |
| Final reconstructed event frame | `manuscript_revision/audit/ci01_independent_20261104/Candidate_Event_Inventory.csv`, `Inclusion_Exclusion_Audit.csv`, `evidence/` | 63 cyclone identities in 62 warning groups; 60 included numerical cases and three pending identities. |
| Final processed model inputs | `manuscript_revision/audit/ci01_independent_20261104/analysis/reconstructed_model_input.csv`, `backend_probability_update.json`, `scenarios/reconstructed60_adjudicated/` | Final 60-event fit; scenario counts 35/19/6. The 59-case Shek Pik/Tai O files are a separate matched-station sensitivity. |
| Historical and final numerical outputs | `04_Results/Optimization/`; `manuscript_revision/audit/ci01_independent_20261104/backend_probability60/`, `backend_probability60_replay/` | Original-23 and final-60 runs each contain 555 configuration summaries. Main solver-audit counts differ: 3,875 and 3,888 respectively. |
| Supplemental experiment inputs and results | `manuscript_revision/peer_review_validation_20261105_v2/snapshots/`, `runs/primary/parameters/`, `runs/primary/`, `independent_validation/` | Final v2 supplement evidence: 500 recorded primary solves, including two expected infeasible cases; nine content-addressed parameter records. |

The original 23 and reconstructed 60 have distinct selection histories. `backend_probability61`, the pre-adjudication stage and peer-review v1 are historical artifacts, not the final main analysis. Saved validation PASS records establish their stated computational checks; this organization task does not independently rerun all experiments.

The local source registry `01_Data/Sources/source_registry.json` has 23 parameter/census archive entries. All 23 archived files matched their registered SHA-256 values during this audit. Additional HKO provenance is recorded in CI01 `Official_Source_Manifest.csv` and `PDF_Source_Manifest.csv`. Integrity checks establish neither ownership nor permission.

## Third-party rights matrix

Official terms were checked on 2026-11-18. File-specific conditions and third-party content can override general site notices. No permissions were requested or inferred on the authors' behalf.

| Source and material | Observed terms and official evidence | Required action before release |
| --- | --- | --- |
| HKO observations, event tables, webpages and publications | [Website notice](https://www.hko.gov.hk/en/readme/readme.htm), [website noncommercial conditions](https://www.hko.gov.hk/en/appweb/applink.htm) and [publication noncommercial conditions](https://www.hko.gov.hk/en/publica/non-commercialuse.htm) impose attribution, accurate reproduction, reproduced notices/conditions and a prominent disclaimer; commercial use requires prior authorization. | Assess the intended distribution and package all applicable notices. This assessment also covers extracted numeric inputs, derived tables and the supplementary document; omission of raw PDFs alone does not settle it. |
| DATA.GOV.HK datasets | [Terms](https://data.gov.hk/en/terms-and-conditions) permit redistribution with source and rights attribution and compliance; linked external sites retain their own terms. | Map each dataset to its actual delivery source and conditions. Portal availability does not license every linked report. |
| Census statistical information | [C&SD notice](https://www.censtatd.gov.hk/en/page_31.html) permits specified statistical reuse with source/Government ownership acknowledgements and clearly marked modifications; maps and other listed media are excluded. | Attribute statistical extracts and label transformations. Check mixed-media reports and geographic material separately. |
| Census spatial service data | [CSDI terms](https://static.csdi.gov.hk/csdi-webpage/doc/TNC) permit redistribution subject to Government, relevant organization and CSDI attribution and other conditions. | Confirm exact dataset scope, retain required attribution and check additional source-specific restrictions. |
| DSD reports and archived webpages | [DSD notice](https://www.dsd.gov.hk/EN/HTML/224.html) grants personal/internal-use permission subject to conditions; uses outside that permission require authorization. | Keep complete copied works and extracts local pending an adequate redistribution basis. Citation and source links may identify their provenance. |
| CEDD coastal-hazard report, `Calibration/S12.pdf` and extracted pages | [CEDD notice](https://www.cedd.gov.hk/eng/notices/index.html) permits local storage for personal/noncommercial internal use; public redistribution is restricted absent authorization. | Retain the full report/extract archive locally; do not treat a publicly accessible download as public redistribution clearance. |
| OpenStreetMap extract `Calibration/S20.osm` and derived databases | [OSM copyright and license](https://www.openstreetmap.org/copyright) specifies ODbL, attribution and share-alike requirements for distributed altered databases. | Determine whether the distributed artifact contains or derives from OSM data and satisfy the corresponding conditions. Do not apply a new blanket code license to it. |
| Boston guidance `Calibration/S15.pdf`, JRC archived page and other copied works | No file-specific redistribution grant has been established in this audit. | Retain full copies/extracts locally pending review; preserve bibliographic URLs and checksums. |
| Vendored PDF-audit helpers | CI01 `code/vendor/` contains third-party helper code; redistribution terms have not been established here. | Keep local pending provenance and license review. |

## Local access versus Git candidates

The local working copy retains native `01_Data/`, nested `**/snapshots/01_Data/`, all `Sources/` and `sources/` trees, native `.log` files, ZIP archives, DOCX manuscripts, study-area maps and `code/vendor/`. These categories are excluded by `.gitignore` for this review. They remain available locally and in the untouched original folder; they will not be supplied by an ordinary Git clone unless an explicitly approved access arrangement is later made. Do not force-add them.

Machine-readable CSV/JSON audit summaries, numerical results and provenance manifests remain **review candidates**, not cleared releases. Some carry source-derived values, machine paths or metadata. Native text solver logs are held locally; JSON verification records in directories named `logs/` can remain candidates. Author-produced calculations do not automatically change the rights in source datasets. The supplementary Markdown is preserved, but its distribution also needs the source-attribution and conditions assessment above.

A public archive, DOI, unrestricted dataset release or license-free computational reproduction has not been established. Gurobi-dependent reruns require a suitable solver license. Some source-integrity checks require locally held archives, snapshot inputs or original paths and cannot be represented as passing in a fresh clone that lacks them.

## Missing files versus unresolved evidence

Core supplied material was found: the merged manuscript, S1–S13 Markdown, model/pipeline code, original and reconstructed inputs, numerical outputs and validation records. Files excluded from Git for rights/access review are **held locally**, not missing research files. Exact inclusion and exclusion records belong to the repository inventory and import manifest.

The following evidence remains unresolved or unrecovered, as documented in `manuscript_revision/Remaining_Research_Risks.md` and `Remaining_Submission_Blockers.md`:

- Contemporaneous historical selection/exclusion and event-anchor records, including original reasons for four station substitutions, have not been recovered.
- Three cyclone identities remain pending because of conflicting observations or inseparable attribution. Yagi peak chronology remains conflicted despite numerical extrema inclusion.
- Field-supported inventory/access, pump performance and deployment requirements, costs, exposure and intervention-to-loss relationships are not supplied as a calibrated decision chain.
- Author-approved distribution arrangements and any required third-party permissions remain unconfirmed.

These gaps must stay explicit. No fabricated input, replacement example, invented experiment or unsupported claim of full reproducibility resolves them.

## Submission-stage update, 18 November 2026

The earlier local-hold disposition above remains the historical organization record. The submission preparation now selects six minimal numerical inputs as Git candidates, with no raw-source release or blanket license: the master workbook, model_input.csv, event_metadata.csv, capacity_bound_reference.json, pre_cleanup_metrics.json and pre_cleanup_report_verification.json. Authors must resolve the applicable distribution basis and HKO conditions/notices before publication. Actual numerical audit logs are candidates after sensitive-pattern screening; response headers, including the network_probe_headers.txt exception, remain excluded. No files were force-added, committed or published. See `THIRD_PARTY_NOTICES.md`, `SUBMISSION_REPOSITORY_CHECKLIST.md` and `audit/submission_20261118/repository_hygiene.md` for current dispositions.
