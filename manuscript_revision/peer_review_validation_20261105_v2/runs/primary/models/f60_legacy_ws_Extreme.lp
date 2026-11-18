\ Model f60_legacy_ws_Extreme
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize multi-objectives
  benefit: Priority=4 Weight=1 AbsTol=1e-08 RelTol=0
   76.285 deploy_0 + 81.675 deploy_1 + 90.4475 deploy_2 + 62.415 deploy_3
   + 66.825 deploy_4 + 74.0025 deploy_5
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
 capital_HKD: 1e+06 new_pumps <= 0
 operating_budget_Extreme: 3900 deploy_0 + 3300 deploy_1 + 2100 deploy_2
   + 3900 deploy_3 + 3300 deploy_4 + 2100 deploy_5 <= 30000
 labour_capacity_Extreme: 42 deploy_0 + 54 deploy_1 + 68 deploy_2
   + 42 deploy_3 + 54 deploy_4 + 68 deploy_5 <= 400
 equipment_capacity_Extreme: 12 deploy_0 + 8 deploy_1 + 3 deploy_2
   + 12 deploy_3 + 8 deploy_4 + 3 deploy_5 <= 60
 supply_capacity_Extreme: 27 deploy_0 + 45 deploy_1 + 15 deploy_2
   + 27 deploy_3 + 45 deploy_4 + 15 deploy_5 <= 220
 link_Extreme_Tai_O1_Drainage: - 5 ready_0 + deploy_0 <= 0
 link_Extreme_Tai_O1_Barrier: - 4 ready_1 + deploy_1 <= 0
 link_Extreme_Tai_O1_Warning: - 5 ready_2 + deploy_2 <= 0
 link_Extreme_Tai_O2_Drainage: - 5 ready_3 + deploy_3 <= 0
 link_Extreme_Tai_O2_Barrier: - 4 ready_4 + deploy_4 <= 0
 link_Extreme_Tai_O2_Warning: - 5 ready_5 + deploy_5 <= 0
Bounds
 new_pumps = 0
Binaries
 ready_0 ready_1 ready_2 ready_3 ready_4 ready_5
Generals
 deploy_0 deploy_1 deploy_2 deploy_3 deploy_4 deploy_5 new_pumps
End
