# Task 5 — Methodological contribution matrix

審查對象：`Revised_Manuscript_EN_v2.md`，SHA-256 `d245173c74145e3fc64afdf6c6a7f3d5974e092db42c499a74ec8fc668b050d1`。檢索與核驗：2026-11-05；本表為新一輪獨立比對，未使用未採納的 v1 審查交付物。僅新增本目錄文件，未修改主稿、凍結數據或 CI 狀態。

## 判斷

最新版明確不主張「兩階段、移動設備分配或 CRITIC 本身新穎」（§2.3，L53），這個限縮合理；本輪未核驗該主張的版本變更史。但 §2 尚不足以支持方法性貢獻定位：最接近的防洪隨機應急物流、移動泵部署，以及共用臨時擋水設備研究沒有進入逐項比較。現有 Rawls/Turnquist 與 Mete/Zabinsky 引用可支持通用兩階段背景，不能代替這一層對照。

本次有限檢索支持把 CRISP 定位為**透明、可複核的條件方法案例與資料敏感性審計**。它沒有建立新的隨機規劃理論、求解算法、液壓響應模型或現場效益估計。共用庫存與固定所有第一階段決策是正確建模和評價要求；僅在本項目由舊模型修正為可實際計數的泵庫存，不能因而升格為一般方法創新。EV 最優政策集合下的 VSS 範圍、事件母體重建及潮站代理差異，是值得保留並精確證明的具體工作，但此檢索沒有證明它們在全球文獻中首次出現。

## 閱讀範圍與可用性

`P` = 出版商摘要、引言或明示節選；`E` = 出版商被索引的延伸方法/結果片段；`H` = 可取得出版全文 HTML，僅審讀所列相關章節；`A` = 作者版全文 HTML，僅審讀所列章節。**沒有任何一篇因為取得全文而被記成「全文逐式審計完成」。** `U` = 此次取得內容不足以判定。`U` 不代表原文沒有該項。

8 篇均有出版商或作者/機構原始來源支撐；搜尋中的二手索引只用於發現，不承擔方法結論。四篇 Elsevier 直接開啟返回 403；Yosua 頁面直接開啟返回 429。這些失敗沒有被寫成全文取得成功。完整檢索式、來源 URL、取得方式及待核欄見 [檢索台帳](literature/Search_and_Access_Ledger.md) 與 [逐來源範圍](literature/Source_Verification_Ledger.md)。

## 最接近作品逐欄對照

下表為英文短句，便於直接供英文文獻節改寫；所有「差異」均為與**當前 CRISP 公式和實驗**的比較，不聲稱先例已被窮盡。

| ID / primary source / read scope | Decision variables and objective | Constraints verified in accessed material | Uncertainty / scenarios | Validation and limit | CRISP difference supported by this comparison |
| --- | --- | --- | --- | --- | --- |
| L01 Chang, Tseng & Chen (2007), [publisher preview](https://www.sciencedirect.com/science/article/pii/S1366554507000178), **P** | Rescue-organisation structure, storehouse locations, resource allocations and distributions; expected performance across scenarios. | Capacity restrictions stated; exact equations, integrality and stage assignment **U**. | Two stochastic models; stochastic rescue demand; GIS flood-potential maps estimate demand locations and equipment quantities. | SAA and real planning example reported; independent data validation **U**. | Direct flood-logistics precedent missing from §2. CRISP uses two fixed sectors, readiness binaries and integer pump procurement, with illustrative response scores rather than a verified hazard-to-equipment-demand mapping. |
| L02 Garrido, Lamas & Pino (2015), [institutional abstract](https://pure.uai.cl/es/publications/a-stochastic-programming-approach-for-floods-emergency-logistics/), [publisher snippets](https://www.sciencedirect.com/science/article/pii/S1366554514002087), **P** | Emergency inventories and vehicle availability; cost/time considerations. Exact decision domains and stage mapping **U**. | Demand satisfaction with a specified probability; detailed probabilistic constraints **U**. | Spatio-temporal stochastic flood occurrence; zones and discrete periods. | SAA; illustrative six-zone/four-period example and sensitivity analysis in snippets. | Stronger domain match than general water allocation. CRISP has one response period and three mutually exclusive severity classes; it lacks vehicle availability, travel-time and service-probability modelling. |
| L03 Rawls & Turnquist (2010), [publisher](https://www.sciencedirect.com/science/article/pii/S0191261509001118), **P** | First-stage facility locations/sizes and multi-item stocks; second-stage distribution. | Survival of stock and network availability represented; complete constraint system **U**. | Discrete scenarios with probabilities for demand, stock survival and network conditions. | Lagrangian L-shaped heuristic compared with extensive-form CPLEX in a Gulf Coast case; section previews only. | CRISP's procurement and shared stock belong to an established preparedness/recourse structure. Its specific addition is auditable pump units and readiness/benchmark accounting within a much smaller illustrative case. |
| L04 Mete & Zabinsky (2010), [publisher](https://www.sciencedirect.com/science/article/pii/S0925527309003582), **P** | First-stage warehouse selection/inventory; aggregated scenario deliveries; separate MIP converts deliveries to vehicle assignments/routes. | Warehouse, transport and demand estimates discussed; complete capacity/domain equations **U**. | Earthquake scenarios; updated road, demand and supply information can revise response routes. | Seattle case and linked visual simulation reported; no independent replication here. | CRISP explicitly counts pumps and combines pumping, barriers and warning packages, but has no routing or transport submodel. Proper first-stage inventory fixing is not a new two-stage concept. |
| L05 Yosua et al. (2025), [publisher](https://www.mdpi.com/2311-5521/10/5/119), **E** | Pump placement, number, discharge capacity and operating configuration selected through hydraulic criteria; no formal two-stage MILP verified. | Road width/accessibility, channel deficit, head losses, inlet/outlet conditions, depth/duration criteria. | Deployment configurations and hydraulic conditions; probability-weighted recourse formulation **U**. | HEC-RAS placement/configuration simulations reported; selected method/results excerpts, figures not independently inspected. | Mobile pumping optimisation already exists. CRISP supplies an integer stock/readiness model and EV-policy comparisons; it does not supply this predecessor's explicit physical pump-response evaluation. |
| L06 Shehadeh & Tucker (2022), [author v3](https://arxiv.org/html/2012.05387v3), [publication identity](https://www.sciencedirect.com/science/article/pii/S0968090X22002856), **A** | Binary warehouse opening and continuous prepositioned inventory; recourse procurement, flows, unused stock and shortage. | Storage capacity, flow conservation, procurement limits and damaged arc capacity; §4 (1b), (2b–e). | SP plus mean/range DRO and trade-off models; disaster level/location, demand, surviving stock and capacities. | SAA/decomposition; hurricane/earthquake cases; §8.1.2 fixes all first-stage decisions in out-of-sample recourse evaluation. | CRISP's frequency-only replay is narrower than distribution-misspecification evaluation. Its integer equipment and EV-tie range are specific case features; author-v3 findings are not certified against final publisher text. |
| L07 Liang et al. (2025), [published HTML](https://nhess.copernicus.org/articles/25/3545/2025/), **H** | Warehouse–shelter service indicators, kit quantities and satisfaction rates; transportation cost and maximum unmet-rate objectives. | Inventory, shelter capacity and flood-dependent road/facility availability; §2.2–2.4. Vehicle numbers assumed unlimited. | Separate coastal-flood/scarcity cases; no common nonanticipative first-stage procurement found in inspected formulation. | GIS network/demand analysis, Shanghai cases and demand sensitivity; algorithmic optimisation, not field effectiveness verification. | CRISP enforces common pre-event decisions; Liang links flood maps to affected people, demand and usable routes. CRISP currently lacks that physical exposure-to-resource chain and equity objective. |
| L08 Lopane & Dawson (2026), [published HTML](https://onlinelibrary.wiley.com/doi/full/10.1111/jfr3.70182), **H** | Warehouse presence/location and resource storage plans; deployment-time/cost Pareto objectives; GA/NSGA-II. | Feasible land/road locations, resource availability, asset coverage/prioritisation; §2.2–2.4, §3.2. | Eight assumption scenarios on costs, lorries and priorities; not demonstrated as a probability-weighted two-stage recourse model. | Humber infrastructure case, convergence rule and cross-scenario sensitivity; global optimality not independently proved here. | Shared temporary equipment and capital/operating costs have direct precedent. CRISP instead models conditional stochastic readiness/procurement and information values, without spatial warehouse siting or deployment times. |

## CRISP 貢獻分解：哪些已成立、哪些仍需補強

| 主張/部件（主稿位置） | 可辨認性 | 對本稿可成立的最小表述 | 尚缺證據或比較 |
| --- | --- | --- | --- |
| 兩階段預備—部署（§1 L25；§3.1） | 已知結構；L03、L04、L06。L01/L02只作已核實的防洪隨機規劃先例，其確切階段歸屬仍為U | 在大澳條件案例採用既有兩階段規劃 | 不宜稱新方法；補直接防洪先例而非僅泛水資源模型 |
| 共用泵與整數採購（§3.3–3.4，Eq.12–13） | 本項目有實質可計數修正；不是已證明的文獻空缺 | 在既定案例將 Drainage 部署與同時可用泵數連結 | 真實可調用庫存、車輛/通道、有效泵流量、出口與班組校準；此表不關閉 CI-06 |
| EEV 固定全部第一階段變數（§3.5，Eq.16） | 正確評估要求；L06有明確固定先決策的實例 | 當前評估紀律要求 EEV 固定預備與採購，再在各情景求解部署 | 不能據此宣稱全領域新穎；應清楚說明當前固定政策的評估規則，不推定未展示的舊版本曾違反該規則 |
| EV 最優政策集合與 VSS 範圍（Eq.18） | 可重現的精細報告特點；全球優先性未核實 | 在有限一階段政策集合枚舉 EEV/VSS 的最小—最大值 | 對容差、枚舉完備性、平均 linking-bound 定義的穩健性；另需針對 tie-aware VSS 文獻檢索，不能由本次查無推定首次 |
| 23→60、共同59身分潮站、frequency-only replay（§3.7） | 可辨認的資料來源與代理敏感性工作 | 分離事件框、前處理重估、潮站選擇與條件頻率對模型比較的影響 | 未恢復原始歷史篩選；頻率替換仍固定資源/成本/效益，未驗證完整 hazard-to-decision 鏈；CI-01不自動關閉 |
| CRITIC + K-means | 通用組件組合；稿件已限縮 | 可重現的條件情景離散化 | 不由內部分群指標推定真實危害類型；不能宣稱由分類校準了泵效益 |
| 既有555設定與目標重建（主稿所報） | 既有實作驗證與可複核性設計 | 主稿報告既有設定下的數值檢查；本表未重新核驗全部555設定 | 本輪局部重算不能擴張為全部555設定均經本輪雙求解器驗證；亦不等於外部效度或液壓效益 |
| 本輪局部基線、組件及覆蓋測試的雙求解器比較 | 本輪最小獨立數值核驗，範圍以實驗報告為準 | 僅對本輪實際執行並核對的案例判定求解器一致性、可行性與目標重建 | 核驗結果須由本輪實驗報告確認；取得 PASS 前不宣稱通過，也不外推至未重算的555設定或實際減災效益 |

「沒有在某篇摘要/節選中看到」不足以證明該篇沒有同類庫存式、EV-tie 處理或敏感性設計。相對缺失的結論僅在已核公式/方法範圍內成立，其餘保留 U。

## 最小修改與驗證要求

1. §2.2加入 L01、L02，明說防洪物資需求與運輸資源早已有隨機規劃先例。§2.1加入 L05及L08，區分物理移動泵響應、臨時設備空間物流與本稿的抽象分數規劃。L06與L07可作近年不確定分布/物理需求鏈的對照，不必八篇一律擴寫。
2. 貢獻段保留「可審計的案例與敏感性設計」，刪除任何將正確庫存計數、非前視性或 EEV 全部固定視為獨創理論的暗示。若主張 EV-tie range 或資料審計程序是方法創新，需獨立檢索該部件及說明可泛化的增益；此表尚未完成那一項。
3. 最小數值比較應先比較同一可行集上的簡單可行政策（如無泵、固定泵庫存與固定預備組合）及當前 RP/EV 政策；報告可行性、EEV/VSS、採購與受益分布。不同研究的分數、案例規模、求解速度或減災百分比不能直接當作排名。
4. 如需超出條件案例的應用性結論，至少為一個代表性地點驗證有效泵流量/水位/時間/班組/可達性，建立從危害或曝露到資源需求及效益的明示關係，再重算。這是 CI-06 的新證據需求，增加文獻不會替代它。

本次判定不認定參考文獻造假，不因付費牆或限流排除作品；不核准「first」「only」「no prior work」等絕對優先性表述。依 ARS E5，本次檢索只能支撐有日期與來源界限的比較；任何全球首創結論仍為 **UNRESOLVED**。最新版未直接作絕對首次宣稱，故此處是審查邊界，非新增虛構違規。

