\ Model f60_legacy_ws_Moderate
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize multi-objectives
  benefit: Priority=4 Weight=1 AbsTol=1e-08 RelTol=0
   72.27 deploy_0 + 63.1125 deploy_1 + 70.785 deploy_2 + 59.13 deploy_3
   + 51.6375 deploy_4 + 57.915 deploy_5
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
 operating_budget_Moderate: 2600 deploy_0 + 2200 deploy_1 + 1400 deploy_2
   + 2600 deploy_3 + 2200 deploy_4 + 1400 deploy_5 <= 30000
 labour_capacity_Moderate: 28 deploy_0 + 36 deploy_1 + 45 deploy_2
   + 28 deploy_3 + 36 deploy_4 + 45 deploy_5 <= 400
 equipment_capacity_Moderate: 8 deploy_0 + 5 deploy_1 + 2 deploy_2
   + 8 deploy_3 + 5 deploy_4 + 2 deploy_5 <= 60
 supply_capacity_Moderate: 18 deploy_0 + 30 deploy_1 + 10 deploy_2
   + 18 deploy_3 + 30 deploy_4 + 10 deploy_5 <= 220
 link_Moderate_Tai_O1_Drainage: - 7 ready_0 + deploy_0 <= 0
 link_Moderate_Tai_O1_Barrier: - 7 ready_1 + deploy_1 <= 0
 link_Moderate_Tai_O1_Warning: - 8 ready_2 + deploy_2 <= 0
 link_Moderate_Tai_O2_Drainage: - 7 ready_3 + deploy_3 <= 0
 link_Moderate_Tai_O2_Barrier: - 7 ready_4 + deploy_4 <= 0
 link_Moderate_Tai_O2_Warning: - 8 ready_5 + deploy_5 <= 0
Bounds
 new_pumps = 0
Binaries
 ready_0 ready_1 ready_2 ready_3 ready_4 ready_5
Generals
 deploy_0 deploy_1 deploy_2 deploy_3 deploy_4 deploy_5 new_pumps
End
