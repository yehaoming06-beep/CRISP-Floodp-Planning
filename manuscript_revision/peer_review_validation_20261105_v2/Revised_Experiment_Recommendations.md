# 补充验证后的实验与改稿建议

## Material Passport

日期：2026-11-05（Asia/Shanghai）；结果版本：peer_review_validation_20261105_v2。本文是供作者核对的建议附件，**不是对冻结主稿的修订**。本轮完成执行前独立评估、单独求解、另一求解器核验和来源对照；没有新现场数据，不使用上一轮未采纳草稿结果。

## 结论先行：完成最小补充，暂不扩张实验

已完成8个EV定义规格、24个组件RP规格及8个假设覆盖RP规格；包括枚举在内共500次Gurobi求解，498 OPTIMAL、2 INFEASIBLE。独立SciPy/HiGHS复核500个保存模型，并从原始快照重建416个固定政策EV及其20条最优政策EEV，共936次独立优化；最大主目标差1.3074×10⁻¹¹，保存解的约束/整数域残差均0。全部EV政策集合、选择规则和范围通过。仅这些新规格经过本轮双求解器核验，不能称原有555组全部得到该项新增验证。

数值证据足以建议小幅补充基准定义、组件归因与覆盖限制。无需因本轮基线结果改写冻结主数值，也无需自动重跑555组。把方法结论升级为实用防洪配置，仍需要CI-06的新实证；增加同类压力测试不能替代这一缺口。

## Task 4：23与60究竟在比较什么

本轮逐字段比较原23 `baseline_inputs.json` 与最终 `backend_probability60/inputs.json`，**唯一改变的顶层字段为probabilities**。setup、运行费用与容量、单位需求、benefit权重/分量、α/β、完整b和U均相同；`run_backend.py:28`也只用新频率替换旧参数。证据见 [链条审计](assessment/Scenario_Chain_Audit.json)，核验代码及原文件快照均保留。

前端情景则不是固定类别下只改样本量。60条重新估计Min–Max、CRITIC与聚类，原23中6个标签改变；旧阈值0.247782/0.485191变为0.272564/0.505236。同60条用旧规则投影是43/12/5，完整重拟合才是35/19/6。下表显示同名类别代表值已改变；R/W/S是各自类内均值，不是同步过程。

| 同名类别 | 原23计数 | 新60计数 | 原23代表(R mm/day, W mCD, S m) | 新60代表(R, W, S) |
| --- | ---: | ---: | --- | --- |
| Moderate | 9 | 35 | 57.966667, 2.710000, 0.591111 | 37.171429, 2.515429, 0.363429 |
| Severe | 9 | 19 | 118.811111, 3.010000, 0.704444 | 122.026316, 2.788947, 0.557895 |
| Extreme | 5 | 6 | 220.680000, 3.486000, 1.474000 | 222.316667, 3.390000, 1.321667 |

因此，后端比较实际是“把新分类的条件频率附着到旧的、假设性响应表标签上”的**frequency-only敏感性**。这是明确受控的部分链条检验，但不能把同名标签当成物理状态完全相同，也不能把它称为已完成响应校准的60事件分析；优化仍使用三个类别情景。未建立、也没有证据授权建立实测R/W/S→成本/资源/效益函数。

| 结论类型 | 可用证据及可说范围 | 应避免的升级 |
| --- | --- | --- |
| 后端frequency-only | 固定表下RP/EEV/VSS/EVPI与返回政策对频率的条件依赖；移动基线RP增加18.434167但原政策仍最优、regret=0 | 60条导致更好的实际政策、避免损失增加或新的采购收益 |
| 前端方法验证 | 已有候选框可追踪、原23数值重建、重拟合/旧投影分离、共同59身份潮站对照、聚类计算复核 | 恢复原历史筛选、证明数据无偏、潮站代表性获现场认证 |
| 优化方法实现 | 非前视性、共享库存守恒、完整固定EEV、EV集合、约束和目标重构、双求解器一致 | 新算法优越性、现场效果或普遍模型稳健性 |
| 组件与覆盖 | 指定可行域差异与假设部署规则的机会成本 | 模型分数下降等于性能差、实际受保护居民减少或公平成本 |
| 既有555组 | 作为给定假设下的广泛计算压力测试；其20个返回plan和18个采购量变化是选中解的比较 | 全局唯一政策切换次数、共同稳健方案或抽样置信区间 |

两组频率均条件于各自候选框、可分析记录及分类规则，不估计年发生率、重现期、未来大澳洪水概率或气候趋势。CI-01的新框、pending与历史来源缺口，和CI-06的响应校准缺口应分别保留。

## 作者可以逐项核对的最小修稿

下列候选英文句只供核对后采用；本轮没有写入主稿，也没有更新引用编号、Word或图表。

| 位置 | 建议 | 充分证据/限制 |
| --- | --- | --- |
| §3.5后或补充材料 | 保留A的定义，补B公式及基线相同、定义不等价的结果 | 8规格、完整416固定政策枚举；不能扩展到555所有配置 |
| §3.6/§5.1 | 区分bundled legacy/mobile比较、措施子集消融与本轮组件消融 | 24个同输入RP；共享纯增量为零也必须披露 |
| §6.2后 | 增加明确hypothetical minimum geographic deployment | k=1可行、分数机会成本及k=6不可行；只RP、非人数 |
| §5.10/§6.3 | 保留并突出refitted-label semantics与未重校准响应表 | 唯一频率字段变化、代表值/阈值/迁移证据；不修改实测R/W/S |
| §2.1/§2.2及贡献段 | 由作者核对后补Chang、Garrido、Yosua、Lopane/Dawson等直接比较，定位条件案例和透明性 | [文献矩阵](Methodological_Contribution_Matrix.md)标明取得深度；不称全文逐式核验或首次证明 |

**EV候选句：** “For the two baseline formulations under both conditional frequency vectors, averaging scenario-derived bounds and recomputing bounds from averaged primitive resource data yield the same primary-optimal EV policy sets and EEV/VSS ranges. Under the 23-event frequencies, however, fixed-policy EV values differ for 6 of 26 legacy and 35 of 78 inventory policies; this baseline agreement does not establish general equivalence of the conventions.”

**组件候选句：** “Controlled comparisons retain identical benefit and resource inputs. The score difference from an unrestricted-stock relaxation reflects the smaller feasible set with finite pump stock; the per-location and shared-stock formulations have the same optimal RP values in these instances despite different feasible sets. Relaxing procurement integrality alone has zero primary-objective effect because deployments remain integer.”

**覆盖候选句：** “In a hypothetical minimum geographic deployment comparison requiring at least one abstract intervention unit in each sector in every scenario, RP decreases by 14.206739 and 13.680333 score units under the 23- and 60-event frequencies, respectively. These changes quantify the model opportunity cost of the assumed deployment rule and do not measure protected population.”

**23/60候选句：** “Because refitting changes class membership and representative indicators while the response coefficients remain unchanged, the backend replay is a frequency-only sensitivity attached to scenario labels, rather than a fully recalibrated observation-to-decision model.”

上述建议不要求更换正文全部结果。作者若选择B作为今后主报告定义，必须另存新结果版本，并重算希望纳入正文的全部受影响EV、EEV、VSS和政策范围；本轮基线一致不能授权把原555结果统一改名为B。

## 后续实验何时才有必要

1. **若只维持条件方法案例：** 本轮证据已满足所提最小补充，不再追加随机压力测试或重新聚类来制造稳健性叙事。作者核对本目录、原文取得范围和贡献定位后，再决定是否将小表放补充材料。
2. **若要声称完整危害到决策验证：** 先取得可调用库存、通道/运输、有效流量/扬程/出口、时长/班组、真实需求/暴露及成本和避免损失证据；明确单位、价格年份和机制，再版本化校准、拟合外验证及受影响全链重算。没有这些数据，本轮不指定虚构函数形式。
3. **若要主张方法首创或优于最近邻方法：** 先取得并逐式审查最近邻全文、定义可比问题和同一评价标准；特别检索tie-aware EV/VSS的直接先例。不能比较不同研究的score、规模或物理效益百分比来建立排名。
4. **若要实证地理公平：** 先定义服务、暴露、人群异质性、重复保护及可测结果，验证所选指标后再研究覆盖；本轮k包对照不填补这些内容。

## 版本、结果与复核入口

- [执行前评估](assessment/Decision_Before_Execution.md) 和 [独立预审](assessment/Independent_Pre_Execution_Review.md)：先评估再运行的证据。
- [运行清单](runs/primary/run_manifest.json)、[环境](environment_versions.json)、[代码](code/run_validation.py)、[参数/模型/日志/解](runs/primary)：500次求解的完整证据。
- [独立核验](independent_validation/verification.json) 和 [独立实现](code/verify_independent.py)：936次HiGHS计算与证据检查；代码初始版和最终版均保留。
- [冻结清单](frozen_manifest_before.json) 和 [求解后守卫](runs/primary/frozen_guard.json)：涵盖21,678个既有科学源文件，无变化；排除本轮目录、未采纳v1、环境缓存及系统元数据。最终交付另行再核对。
- [复现与交付说明](README.md)：完整运行命令、目录、拒绝覆盖规则及证据边界。

**状态不变：CI-01 = PARTIALLY RESOLVED / NOT FULLY CLOSED；CI-06 = OPEN。** 旧11月4日台账的CI-01 OPEN与11月5日最新风险状态按日期解释，本轮不覆盖任何旧台账。
