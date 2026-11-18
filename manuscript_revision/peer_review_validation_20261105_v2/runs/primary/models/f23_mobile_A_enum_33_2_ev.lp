\ Model f23_mobile_A_enum_33_2_ev
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize multi-objectives
  benefit: Priority=4 Weight=1 AbsTol=1e-08 RelTol=0
   76.285 deploy_0 + 71.50597826086957 deploy_1 + 78.13706521739131 deploy_2
   + 62.415 deploy_3 + 58.50489130434783 deploy_4
   + 63.93032608695653 deploy_5
  minimum_procurement: Priority=3 Weight=1 AbsTol=1e-08 RelTol=0
   - new_pumps
  minimum_readiness: Priority=2 Weight=1 AbsTol=1e-08 RelTol=0
   - 8500 ready_0 - 7500 ready_1 - 5500 ready_2 - 8500 ready_3 - 7500 ready_4
   - 5500 ready_5
  minimum_mask: Priority=1 Weight=1 AbsTol=1e-08 RelTol=0
   - ready_0 - 2 ready_1 - 4 ready_2 - 8 ready_3 - 16 ready_4 - 32 ready_5
Subject To
 readiness_budget_CU: 8500 ready_0 + 7500 ready_1 + 5500 ready_2
   + 8500 ready_3 + 7500 ready_4 + 5500 ready_5 <= 20000
 capital_HKD: 1e+06 new_pumps <= 2e+06
 fix_y_0: ready_0 = 1
 fix_y_1: ready_1 = 0
 fix_y_2: ready_2 = 0
 fix_y_3: ready_3 = 0
 fix_y_4: ready_4 = 0
 fix_y_5: ready_5 = 1
 fix_n: new_pumps = 2
 operating_budget_EV: 3078.260869565217 deploy_0
   + 2615.217391304348 deploy_1 + 1669.565217391304 deploy_2
   + 3078.260869565217 deploy_3 + 2615.217391304348 deploy_4
   + 1669.565217391304 deploy_5 <= 30000
 labour_capacity_EV: 33.39130434782609 deploy_0
   + 42.65217391304348 deploy_1 + 53.52173913043478 deploy_2
   + 33.39130434782609 deploy_3 + 42.65217391304348 deploy_4
   + 53.52173913043478 deploy_5 <= 400
 equipment_capacity_EV: 9.652173913043478 deploy_0
   + 6.043478260869565 deploy_1 + 2.608695652173913 deploy_2
   + 9.652173913043478 deploy_3 + 6.043478260869565 deploy_4
   + 2.608695652173913 deploy_5 <= 60
 supply_capacity_EV: 21.52173913043478 deploy_0
   + 35.60869565217391 deploy_1 + 11.8695652173913 deploy_2
   + 21.52173913043478 deploy_3 + 35.60869565217391 deploy_4
   + 11.8695652173913 deploy_5 <= 220
 link_EV_Tai_O1_Drainage: - 6.173913043478262 ready_0 + deploy_0 <= 0
 link_EV_Tai_O1_Barrier: - 5.956521739130435 ready_1 + deploy_1 <= 0
 link_EV_Tai_O1_Warning: - 6.956521739130435 ready_2 + deploy_2 <= 0
 link_EV_Tai_O2_Drainage: - 6.173913043478262 ready_3 + deploy_3 <= 0
 link_EV_Tai_O2_Barrier: - 5.956521739130435 ready_4 + deploy_4 <= 0
 link_EV_Tai_O2_Warning: - 6.956521739130435 ready_5 + deploy_5 <= 0
 shared_EV: deploy_0 + deploy_3 - new_pumps <= 0
Bounds
 new_pumps <= 2
Binaries
 ready_0 ready_1 ready_2 ready_3 ready_4 ready_5
Generals
 deploy_0 deploy_1 deploy_2 deploy_3 deploy_4 deploy_5 new_pumps
End
