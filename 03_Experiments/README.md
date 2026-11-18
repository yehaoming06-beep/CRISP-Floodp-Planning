# Current experiments

Optimization/code contains the current 555-configuration protocol runner, independent HiGHS verification, EV-policy tie audit, result workbook authoring and six figure scripts. Experiment_Protocol.json contains the perturbation design; current fleet inputs are read only from the master workbook.

Scenario_Stability/code contains the 23-event CRITIC/K-means stability analysis. It uses the common event dataset in 01_Data/Events and the common production package in 05_Code/Scenario_Pipeline/src. Only one validated stability result set is retained under 04_Results.

Saved results, comparison fixtures and source archives are different roles. Control files in 01_Data/Controls document numerical regression checks against the pre-cleanup run; they are not additional field observations.
