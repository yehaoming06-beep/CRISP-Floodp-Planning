# Current CRISP model

`crisp_parameters.py` reads the illustrative CU/score block of `01_Data/CRISP_Master_Data.xlsx`. `crisp_model.py` reads its Mobile_Pump and Study_Area sheets and implements the current two-stage model.

For each zone z and intervention i, y[z,i] is binary readiness. Integer n denotes new pump procurement; N0 is explicitly assumed existing available stock. Ccap*n ≤ Kcap is a separate HKD procurement constraint. Scenario-indexed integer x[s,z,Drainage] is assumed to denote simultaneous pump assignments, with sum_z x[s,z,Drainage] ≤ N0+n in each mutually exclusive scenario. Inaccessible-zone pump assignments are zero. The readiness link and four original scenario resource constraints remain.

Resource-derived U[s,z,i] is recomputed from the current cost and capacity ratios. It is distinct from physical pump inventory. EEV fixes both y and n from EV. The model maximizes the inherited expected score; among primary optima it minimizes n, readiness cost and the binary readiness encoding. Larger-budget EV policy ties are separately enumerated.

HKD procurement cost, illustrative CU readiness/operation cost and benefit-score outcomes have separate meanings. The per-pump interpretation of inherited Drainage resource/score coefficients remains an assumption. No effective discharge, avoided-loss function or cross-sector heavy-equipment access has been field-calibrated. Census population is contextual and does not change beta automatically.
