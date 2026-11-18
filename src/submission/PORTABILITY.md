# Submission execution adapters

These entry points rerun the frozen experiments. They do not introduce new scientific settings or replace historical provenance guards.

- `scenarios.py` derives from `audit/reproducibility_20261118/scenarios/reproduce_scenarios.py`. It removes optional reads of the original research folder, uses repository-relative paths, refuses an existing output directory, and compares against the archived manuscript table transcription rather than requiring distribution of the Word manuscript. The table reference is only read after fitting; it is not a fit input.
- `suite60.py` derives from `audit/reproducibility_20261118/optimization/run_frequency60_555.py`. The same design, model, solver settings, random seed and loops are retained; new counts and the destination are explicit arguments. Fresh 35/19/6 counts replace conditional frequencies only. Model costs, capacities and benefits stay illustrative and fixed.
- `verify60.py` derives from `audit/reproducibility_20261118/optimization/verify_frequency60.py`. Only destination selection changes; the independent matrix builder is the original `verify_results.py`.
- `../reproduce_submission.py` calls these adapters and the unchanged core and original-23 runners, retaining separate logs and historical comparisons. Outputs must use a new directory inside the checkout.

Original scripts and historical results remain unchanged. Source hashes are in `audit/submission_20261118/adapter_lineage.json`. All scientific source inputs are read from the candidate checkout; no original research workspace is required for these routes. Historical whole-workspace guards for CI01 and v2 still require their full historical corpus and are not reset by these adapters. Source archive reconstruction and full v2 guard reproduction are outside this clean-test claim.

The compared manuscript hash is `4e12f7849d0b2ca7dd0d156c987a9e90f8b651880c79b74e10f14bffbab4ca37`. The manuscript was not edited or redistributed by these scripts.
