\ Model f60_mobile_A_enum_0_0_ev
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize multi-objectives
  benefit: Priority=4 Weight=1 AbsTol=1e-08 RelTol=0
   75.21433333333334 deploy_0 + 68.495625 deploy_1
   + 75.24183333333335 deploy_2 + 61.539 deploy_3 + 56.041875 deploy_4
   + 61.5615 deploy_5
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
 fix_y_0: ready_0 = 0
 fix_y_1: ready_1 = 0
 fix_y_2: ready_2 = 0
 fix_y_3: ready_3 = 0
 fix_y_4: ready_4 = 0
 fix_y_5: ready_5 = 0
 fix_n: new_pumps = 0
 operating_budget_EV: 2888.333333333333 deploy_0 + 2452.5 deploy_1
   + 1565 deploy_2 + 2888.333333333333 deploy_3 + 2452.5 deploy_4
   + 1565 deploy_5 <= 30000
 labour_capacity_EV: 31.3 deploy_0 + 40.01666666666667 deploy_1
   + 50.15 deploy_2 + 31.3 deploy_3 + 40.01666666666667 deploy_4
   + 50.15 deploy_5 <= 400
 equipment_capacity_EV: 9.033333333333333 deploy_0
   + 5.616666666666667 deploy_1 + 2.416666666666667 deploy_2
   + 9.033333333333333 deploy_3 + 5.616666666666667 deploy_4
   + 2.416666666666667 deploy_5 <= 60
 supply_capacity_EV: 20.16666666666667 deploy_0 + 33.4 deploy_1
   + 11.13333333333333 deploy_2 + 20.16666666666667 deploy_3
   + 33.4 deploy_4 + 11.13333333333333 deploy_5 <= 220
 link_EV_Tai_O1_Drainage: - 6.483333333333334 ready_0 + deploy_0 <= 0
 link_EV_Tai_O1_Barrier: - 6.383333333333334 ready_1 + deploy_1 <= 0
 link_EV_Tai_O1_Warning: - 7.383333333333334 ready_2 + deploy_2 <= 0
 link_EV_Tai_O2_Drainage: - 6.483333333333334 ready_3 + deploy_3 <= 0
 link_EV_Tai_O2_Barrier: - 6.383333333333334 ready_4 + deploy_4 <= 0
 link_EV_Tai_O2_Warning: - 7.383333333333334 ready_5 + deploy_5 <= 0
 shared_EV: deploy_0 + deploy_3 - new_pumps <= 0
Bounds
 new_pumps <= 2
Binaries
 ready_0 ready_1 ready_2 ready_3 ready_4 ready_5
Generals
 deploy_0 deploy_1 deploy_2 deploy_3 deploy_4 deploy_5 new_pumps
End
