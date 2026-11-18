\ Model f60_mobile_ws_Severe
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize multi-objectives
  benefit: Priority=4 Weight=1 AbsTol=1e-08 RelTol=0
   80.3 deploy_0 + 74.25 deploy_1 + 78.65 deploy_2 + 65.7 deploy_3
   + 60.75 deploy_4 + 64.35 deploy_5
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
 operating_budget_Severe: 3100 deploy_0 + 2650 deploy_1 + 1700 deploy_2
   + 3100 deploy_3 + 2650 deploy_4 + 1700 deploy_5 <= 30000
 labour_capacity_Severe: 34 deploy_0 + 43 deploy_1 + 54 deploy_2
   + 34 deploy_3 + 43 deploy_4 + 54 deploy_5 <= 400
 equipment_capacity_Severe: 10 deploy_0 + 6 deploy_1 + 3 deploy_2
   + 10 deploy_3 + 6 deploy_4 + 3 deploy_5 <= 60
 supply_capacity_Severe: 22 deploy_0 + 36 deploy_1 + 12 deploy_2
   + 22 deploy_3 + 36 deploy_4 + 12 deploy_5 <= 220
 link_Severe_Tai_O1_Drainage: - 6 ready_0 + deploy_0 <= 0
 link_Severe_Tai_O1_Barrier: - 6 ready_1 + deploy_1 <= 0
 link_Severe_Tai_O1_Warning: - 7 ready_2 + deploy_2 <= 0
 link_Severe_Tai_O2_Drainage: - 6 ready_3 + deploy_3 <= 0
 link_Severe_Tai_O2_Barrier: - 6 ready_4 + deploy_4 <= 0
 link_Severe_Tai_O2_Warning: - 7 ready_5 + deploy_5 <= 0
 shared_Severe: deploy_0 + deploy_3 - new_pumps <= 0
Bounds
 new_pumps <= 2
Binaries
 ready_0 ready_1 ready_2 ready_3 ready_4 ready_5
Generals
 deploy_0 deploy_1 deploy_2 deploy_3 deploy_4 deploy_5 new_pumps
End
