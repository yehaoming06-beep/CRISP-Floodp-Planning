# Complete execution evidence

Three deterministic tar.gz archives preserve 16,717 original files (200,530,950 uncompressed bytes), with original paths and SHA-256 per member. They contain author-produced numerical execution evidence, not raw third-party source archives. Compression changes storage only; no scientific output byte was edited.

- `clean_run_20261118.tar.gz`: all 8,964 files from the final independent-directory core/23/60 run, including solutions, solver logs and independent verification.
- `frozen_solutions_and_ev_ties_20261118.tar.gz`: 1,112 original frozen solution files plus 3,604 S9 EV-tie evidence files. Two baseline solutions per frozen suite also remain directly accessible for the supplementary readers.
- `supplementary_rerun_20261118.tar.gz`: all 3,037 files of the earlier supplementary rerun, including corrected independent verification and honest failed-attempt records.

The archive-level SHA/size index is [evidence_archives.json](../../audit/delivery_20261118/evidence_archives.json); each archive has a `.members.json` sidecar. `python3.12 src/verify_delivery.py` validates all archives and every member without extracting. `python3.12 src/verify_delivery.py --restore-evidence` restores original paths, skips identical existing files and refuses changed ones. Run these commands from the repository root. Restoration is not needed for the core/all numerical route.

Earlier repeated 555 log/solution copies and workspace snapshots remain local optional audit materials. Summaries, solver-audit tables, independent checks and unique original/S9/clean evidence remain represented in the selected package. Current selection is governed by [the delivery report](../../audit/delivery_20261118/DELIVERY_REPORT.md), not older file inventories.
