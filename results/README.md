# Results and verification index

Saved artifacts remain separated by evidence version. Historical PASS/status fields do not establish a new reproduction.

| Stream | Results | Existing verification |
| --- | --- | --- |
| Frozen original-23 | [555 configurations](../04_Results/Optimization/summary.csv), [3,875 solve records](../04_Results/Optimization/solver_audit.csv), [two baseline JSONs](../04_Results/Optimization/solutions/) and [complete solution archive](evidence/README.md) | [validation](../04_Results/Optimization/validation.json), [independent check](../04_Results/Optimization/independent_verification.json), [EV ties](../04_Results/Optimization/ev_tie_verification.json) |
| Original-23 stability | [tables](../04_Results/Scenario_Stability/tables/), [resampling indices](../04_Results/Scenario_Stability/resample_indices.json) | [verification](../04_Results/Scenario_Stability/verification.json) |
| Final-60 | [analysis](../manuscript_revision/audit/ci01_independent_20261104/analysis/), [555 configurations](../manuscript_revision/audit/ci01_independent_20261104/backend_probability60/summary.csv), [3,888 solve records](../manuscript_revision/audit/ci01_independent_20261104/backend_probability60/solver_audit.csv) | [validation](../manuscript_revision/audit/ci01_independent_20261104/backend_probability60/validation.json) |
| Supplementary v2 | [primary outputs](../manuscript_revision/peer_review_validation_20261105_v2/runs/primary/), [500 solve records](../manuscript_revision/peer_review_validation_20261105_v2/runs/primary/solver_audit.csv), [models](../manuscript_revision/peer_review_validation_20261105_v2/runs/primary/models/) | [primary validation](../manuscript_revision/peer_review_validation_20261105_v2/runs/primary/validation.json), [independent validation](../manuscript_revision/peer_review_validation_20261105_v2/independent_validation/validation.json), [delivery record](../manuscript_revision/peer_review_validation_20261105_v2/Final_Delivery_Verification.json) |
| New repository checks | [repository_audit](repository_audit/) | File hashes, syntax, links, stored counts and Git screening; no new research experiment |

Detailed final-60 replay models/logs and superseded `backend_probability61` outputs remain optional local history. Replay summary/input/validation copies are outside the current Git selection. Intermediate `reconstructed61` labels are historical. [Three checked evidence archives](evidence/README.md) now preserve the full clean run, original frozen solutions, S9 EV ties and supplementary rerun; use `python3.12 src/verify_delivery.py --restore-evidence` from the checkout root for original paths. Other repeated logs/archives remain local.

Two infeasible supplementary cases are intentional `k = 6` controls. Missing objectives must not become zero. Coverage WS/EV/EEV/VSS were not computed. See [paper correspondence](../audit/Manuscript_Alignment.md) and the [organization report](../audit/Repository_Organization_Report.md).

Submission clean-directory rerun evidence is recorded in [clean test](../audit/submission_20261118/CLEAN_REPRODUCTION.md). Newly generated outputs remain distinct from frozen evidence. The actual current Git commit remains incomplete until reviewed candidates are committed.

The authoritative current package check is `python3.12 src/verify_delivery.py`; [delivery report](../audit/delivery_20261118/DELIVERY_REPORT.md) supersedes older packaging inventories. The final selected-tree rerun and summaries are in [selected_tree_test.json](../audit/delivery_20261118/selected_tree_test.json).
