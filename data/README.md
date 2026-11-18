# Data and model-input index

Scientific files retain their original paths so unchanged programs and historical hashes remain interpretable. Local presence is not redistribution clearance.

| Material | Canonical location | Version/use |
| --- | --- | --- |
| Master workbook | [CRISP_Master_Data.xlsx](../01_Data/CRISP_Master_Data.xlsx) | Assumptions, budgets, resource requirements and pump settings; submission candidate |
| Hazard input | [model_input.csv](../01_Data/Events/model_input.csv), [metadata](../01_Data/Events/event_metadata.csv) | Frozen 23-event reference |
| Controls/evidence | [Controls](../01_Data/Controls/); `01_Data/Evidence/` held locally | Numerical reference and parameter provenance |
| Source provenance | [parameter registry](provenance/parameter_sources.json), [access/SHA manifest](provenance/source_access.csv) | 23 parameter + 307 official + 8 PDF records; raw source works remain held locally |
| Final candidate frame | [inventory](../manuscript_revision/audit/ci01_independent_20261104/Candidate_Event_Inventory.csv), [inclusion audit](../manuscript_revision/audit/ci01_independent_20261104/Inclusion_Exclusion_Audit.csv) | 63 identities, 60 analyzable, three pending |
| Final numerical input | [reconstructed_model_input.csv](../manuscript_revision/audit/ci01_independent_20261104/analysis/reconstructed_model_input.csv) | 60-case adjudicated input |
| Final classification | [reconstructed60_adjudicated](../manuscript_revision/audit/ci01_independent_20261104/analysis/scenarios/reconstructed60_adjudicated/) | CRITIC, clustering, class representatives |
| Backend parameters | [inputs.json](../manuscript_revision/audit/ci01_independent_20261104/backend_probability60/inputs.json) | Original coefficients with final conditional frequencies |
| Supplementary parameters | [content-addressed inputs](../manuscript_revision/peer_review_validation_20261105_v2/runs/primary/parameters/) | Per-solve parameter IDs resolve here |
| Spatial context | `01_Data/Spatial/` (held locally) | Census context and author-aligned sectors; excluded from candidates |

Six minimal numerical inputs in `01_Data` are now explicit Git candidates: the workbook, model_input.csv, event_metadata.csv and three numerical Controls. Raw source archives, snapshot source works and map material remain held locally. The final-60 numerical input and ledgers are also candidates. The portable core/two-555 route uses this selected numerical subset; official-archive reconstruction still needs a rights-cleared archive/access route. No unrestricted data license is asserted. See the final submission checklist; nothing has yet been committed.

See [rights/access](../audit/Data_Rights_and_Access.md), [import checksums](../audit/import_manifest.csv) and [official URLs, held paths and SHA-256](provenance/source_access.csv). Historical selection records, three unresolved cyclone observations and field response calibration remain absent or unresolved; no examples fill these gaps.

Complete HKO rights notices, applicable conditions and official disclaimers accompany this numerical subset in [THIRD_PARTY_NOTICES](../THIRD_PARTY_NOTICES.md). The v2 snapshot also retains the exact root workbook for its parameter reader; it does not make the historical full-workspace guard portable.
