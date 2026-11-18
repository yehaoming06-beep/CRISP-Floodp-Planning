\ Model f23_budget6500000_A2_access_O2_only
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize multi-objectives
  benefit: Priority=4 Weight=1 AbsTol=1e-08 RelTol=0
   28.27956521739131 deploy_0 + 24.69619565217392 deploy_1
   + 27.69847826086957 deploy_2 + 23.13782608695652 deploy_3
   + 20.20597826086957 deploy_4 + 22.66239130434783 deploy_5
   + 31.42173913043479 deploy_6 + 29.05434782608696 deploy_7
   + 30.77608695652174 deploy_8 + 25.70869565217392 deploy_9
   + 23.77173913043478 deploy_10 + 25.1804347826087 deploy_11
   + 16.58369565217391 deploy_12 + 17.7554347826087 deploy_13
   + 19.6625 deploy_14 + 13.56847826086956 deploy_15
   + 14.52717391304348 deploy_16 + 16.0875 deploy_17
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
 capital_HKD: 1e+06 new_pumps <= 6.5e+06
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
 shared_Moderate: deploy_0 + deploy_3 - new_pumps <= 0
 access_Moderate_Tai_O1: deploy_0 = 0
 operating_budget_Severe: 3100 deploy_6 + 2650 deploy_7 + 1700 deploy_8
   + 3100 deploy_9 + 2650 deploy_10 + 1700 deploy_11 <= 30000
 labour_capacity_Severe: 34 deploy_6 + 43 deploy_7 + 54 deploy_8
   + 34 deploy_9 + 43 deploy_10 + 54 deploy_11 <= 400
 equipment_capacity_Severe: 10 deploy_6 + 6 deploy_7 + 3 deploy_8
   + 10 deploy_9 + 6 deploy_10 + 3 deploy_11 <= 60
 supply_capacity_Severe: 22 deploy_6 + 36 deploy_7 + 12 deploy_8
   + 22 deploy_9 + 36 deploy_10 + 12 deploy_11 <= 220
 link_Severe_Tai_O1_Drainage: - 6 ready_0 + deploy_6 <= 0
 link_Severe_Tai_O1_Barrier: - 6 ready_1 + deploy_7 <= 0
 link_Severe_Tai_O1_Warning: - 7 ready_2 + deploy_8 <= 0
 link_Severe_Tai_O2_Drainage: - 6 ready_3 + deploy_9 <= 0
 link_Severe_Tai_O2_Barrier: - 6 ready_4 + deploy_10 <= 0
 link_Severe_Tai_O2_Warning: - 7 ready_5 + deploy_11 <= 0
 shared_Severe: deploy_6 + deploy_9 - new_pumps <= 0
 access_Severe_Tai_O1: deploy_6 = 0
 operating_budget_Extreme: 3900 deploy_12 + 3300 deploy_13 + 2100 deploy_14
   + 3900 deploy_15 + 3300 deploy_16 + 2100 deploy_17 <= 30000
 labour_capacity_Extreme: 42 deploy_12 + 54 deploy_13 + 68 deploy_14
   + 42 deploy_15 + 54 deploy_16 + 68 deploy_17 <= 400
 equipment_capacity_Extreme: 12 deploy_12 + 8 deploy_13 + 3 deploy_14
   + 12 deploy_15 + 8 deploy_16 + 3 deploy_17 <= 60
 supply_capacity_Extreme: 27 deploy_12 + 45 deploy_13 + 15 deploy_14
   + 27 deploy_15 + 45 deploy_16 + 15 deploy_17 <= 220
 link_Extreme_Tai_O1_Drainage: - 5 ready_0 + deploy_12 <= 0
 link_Extreme_Tai_O1_Barrier: - 4 ready_1 + deploy_13 <= 0
 link_Extreme_Tai_O1_Warning: - 5 ready_2 + deploy_14 <= 0
 link_Extreme_Tai_O2_Drainage: - 5 ready_3 + deploy_15 <= 0
 link_Extreme_Tai_O2_Barrier: - 4 ready_4 + deploy_16 <= 0
 link_Extreme_Tai_O2_Warning: - 5 ready_5 + deploy_17 <= 0
 shared_Extreme: deploy_12 + deploy_15 - new_pumps <= 0
 access_Extreme_Tai_O1: deploy_12 = 0
Bounds
 new_pumps <= 6
Binaries
 ready_0 ready_1 ready_2 ready_3 ready_4 ready_5
Generals
 deploy_0 deploy_1 deploy_2 deploy_3 deploy_4 deploy_5 deploy_6 deploy_7
 deploy_8 deploy_9 deploy_10 deploy_11 deploy_12 deploy_13 deploy_14
 deploy_15 deploy_16 deploy_17 new_pumps
End
