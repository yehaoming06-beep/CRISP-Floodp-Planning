# 已通过数值指标的归档证据核对

## Material Passport

- 日期：2026-11-18（Asia/Shanghai）。
- mode：archive-evidence-file-validation；verification_status：ANALYZED_EXISTING_EXECUTION_EVIDENCE。
- 输入为仓库内冻结研究资料和既有实际执行输出；本子任务未重新运行科学实验、未改科学参数、未改Final Paper。
- 本文的“通过”表示已核对原实际执行证据及文件完整性；独立clean复现与再分发许可由最终投稿检查另行判定。

## 结论

审计中通过的130个论文比较项全部有可定位的输入、实际执行记录和输出：Table 4/11/12共82项，Table 6/14共48项。逐项值、误差、容差、CSV行号、所属执行组及SHA-256见 [evidence_trace.json](evidence_trace.json)。本次没有发现通过数值指标缺少执行证据。

复核287个核心输入/代码与338条来源档案当前SHA-256，均匹配历史清单；离线重建336个输入源/副本及11项输出哈希均匹配。旧审计总清单16,187项在核对时均存在，缺失0项、哈希变化0项。审计内22个显式本地链接全部存在。后续获授权的新README/入口变更应由submission清单另记，不回写旧manifest。

## 数值与执行证据

| 通过范围 | 本次文件核对 | 输入/执行/输出定位 |
| --- | --- | --- |
| 来源→60输入 | 336输入源/副本匹配；11输出逐字一致；63候选/63裁定/60向量；0差异格 | `../reproducibility_20261118/reconstruction/`：`copied_input_manifest.csv`、`execution_environment.json`、`execution_stdout.log`、`validation.json`、`output_comparison.csv`、`stage/` |
| 23/60场景 | 82项实际CSV行全部PASS且误差≤原容差；23为9/9/5，60为35/19/6；冻结旧规则43/12/5 | `01_Data/Events/model_input.csv`、CI01 `analysis/reconstructed_model_input.csv`；`scenarios/environment.json`、`input_inventory.json`、`paper_comparison.csv`、`scenario_reproduction_summary.json` |
| 跨环境场景 | `clean_environment_crosscheck.json`明确21份核心CSV byte-identical | `scenarios/clean_environment_execution.log`、`clean_environment/environment.json`、两套核心CSV |
| 四核心优化 | 4配置×6指标=24；独立穷举最大差1.137e-13；48论文项全部PASS | 实际工作簿、协议与`02_Model`；`optimization/clean_environment_console.log`、`clean_environment/core_metrics.csv`、`core_validation.json`、`paper_table6_table14_comparison.csv` |
| 原23完整555 | summary实际555行；solver_audit实际3875行均OPTIMAL；3875份原生日志逐tag存在；555 RP独立HiGHS | `optimization/original23_555/manifest_start.json`、`solver_audit.csv`、`logs/`、`summary.csv`、`independent_verification.json` |
| 60 frequency-only完整555 | summary实际555行；solver_audit实际3888行均OPTIMAL；3888份原生日志逐tag存在；555 RP独立HiGHS | `optimization/reconstructed60_555/manifest_start.json`、`solver_audit.csv`、`logs/`、`summary.csv`、`independent_verification.json` |
| 1110历史比较/整数重构 | 1110配置六指标/策略与历史差0；原始HiGHS差3.584e-6/1.648e-6，原1e-5容差；取整最大约束违反0、目标差1.137e-13 | `historical_1110_comparison.csv`、`independent_integer_rounding_rows.csv`、`independent_integer_rounding_validation.json` |
| S9 EV并列范围 | 每频率10配置/1716政策；额外1796/1808求解全部最优；20配置240字段与历史一致 | 两555目录 `ev_tie_verification.json`、`ev_policy_tie_ranges.csv`、`ev_optimal_policies.csv`；`ev_tie_history_comparison.csv` |
| v2 EV A/B、组件、覆盖 | solver_audit实际500行=498最优+2预设不可行；500原生日志逐tag存在；936独立调用；8 EV规格/416政策试验/20最优政策/24组件/8覆盖/4不可行证书 | `supplementary/execution_corrected.json`、`runs/primary/run_manifest.json`、`solver_audit.csv`、`verification.json`、`independent_corrected/` |
| 原23稳定性 | 9032 resample行、252摘要行、400初始化、2000 K-bootstrap、6 K诊断；20历史数值CSV一致；37次局部最优明示 | `scenarios/stability_execution.log`、`stability_verification.log`、`stability/verification.json`、`historical_comparison.json`、`tables/` |
| 60条件稳定性 | 实际2009行=9 LOYO+1000 episode+1000 year；27组比较最大差1.887e-15；索引重生成一致 | `scenarios/stability60_execution.log`、`stability60/verification.json`、`stability_runs.csv`、`fresh_resample_indices.json` |
| 软件测试 | 新环境日志17 passed；原环境17点全部通过 | `software_test_attempts.json`、`software_tests.txt`、`software_tests_fresh.txt`、`environment_final.json` |

表内`scenarios/`、`optimization/`、`supplementary/`等路径均相对 `audit/reproducibility_20261118/`。完整仓库相对路径及SHA-256在JSON中；每个论文数值格另带CSV准确行号。

## 输入来源与复现边界

核心23输入SHA-256：`094bea5ff6b2f5d8d71b60d8fb62772c2af05a2de83eba21fccbffe176fd544d`；60输入：`7c01d508a17dcb9643a3fd8b9e4f679898b25820fccdbd43b50f0c8f377340e0`；工作簿：`e6b93f8bb0e7b886226d27068e8cfeeebfaa92e668eb25f77ee3b1d35083794e`。60输入由冻结官方档案、筛选协议和QC裁定产生，三个pending身份没有被塞进数值CSV。

555独立HiGHS最优值验证覆盖RP；其他WS/EV/EEV由原Gurobi模型重新求解，并检查保存解目标、约束和EEV一阶段固定。只有四核心模型的全部六指标另有独立穷举证明。不能将这两种独立程度合并成无限定的“全指标独立重求”。

v2的500/936记录来自完整原研究工作区，历史21678文件守卫在该处通过；其原样守卫在精简Git副本不通过。未重置守卫；未运行固定到历史目录的报告finalizer；原执行中的路径序列化失败与修正记录均保留。

新环境复跑已覆盖核心23/60分类、四核心优化及17软件测试；旧审计的完整555/稳定性/v2主要沿用原研究环境。本阶段clean目录测试是否拓展覆盖，以最终submission清单的实际日志为准。

## 可移植性行动项

- `audit/reproducibility_20261118/scenarios/reproduce_scenarios.py`：ORIGINAL绝对路径只作可选原工作区见证，输入仍取ROOT；应在新可移植入口完全避免读取。
- `audit/reproducibility_20261118/optimization/run_frequency60_555.py`：新--run-name可变输出；频率仍从旧scenarios摘要读取。新入口应从本次新生成counts绑定。
- `audit/reproducibility_20261118/optimization/verify_frequency60.py`：OUT固定旧审计结果目录；不能直接声称校验了新结果。
- `audit/reproducibility_20261118/optimization/run_ev_ties60.py`：输出绑定旧审计结果目录；新入口需重绑，不覆盖历史结果。
- `manuscript_revision/peer_review_validation_20261105_v2/code/run_validation.py`：21678历史全工作区守卫不能在精简仓库原样通过；不能初始化/改写旧守卫伪装通过。

这些属于归档入口适配和验证范围问题，不是补造数据的理由。旧执行记录中的绝对路径是历史出处，不能批量替换后冒称原记录。

## 仍未解决的限制

- 原23同期候选/排除登记、原anchor规则版本和四站选择理由未恢复。
- 实地成本、资源、库存、通达性、性能和效益校准不足；model scores不能换算真实损失或保护人口。
- TC2017_06、TC2021_02_E、TC2021_02_W仍pending，只有60条可分析向量。
- 37次Lloyd重抽样局部最优；没有补做全局替换后的敏感性影响实验。
- 60移动泵有4个EV最优策略，EEV范围600.2030833333334–626.4976666666668；单点VSS依赖指定并列选择规则。
- 样式化Excel/Node导出缺manifest/lock，不影响核心CSV/JSON数学复现。
- 本证据检查不构成第三方档案再分发许可、Git已提交或外部干净clone通过的声明。

## 原稿保全

只读核对 `manuscript_revision/CRISP_Merged_Manuscript.docx`：SHA-256 `4e12f7849d0b2ca7dd0d156c987a9e90f8b651880c79b74e10f14bffbab4ca37`，与主审计一致。本子任务仅新增本文及`evidence_trace.json`，没有Commit、Push、修改仓库公开性或覆盖研究原资料。
