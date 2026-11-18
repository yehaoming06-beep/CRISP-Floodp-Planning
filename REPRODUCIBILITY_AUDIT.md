# CRISP 核心数值结果独立可复现性审查

日期：2026-11-18（Asia/Shanghai）。工作目录：`CRISP-Floodp-Planning`；原始研究工作区：`/Users/yehaoming/Desktop/climate_Devin/`。

## 审查结论与材料身份

**本地数值复现：PASS，范围限于找到的真实输入、冻结实验设计和声明的抽象模型。Git-only 独立获取和实地有效性验证仍未通过。** 本次实际重新执行了来源重建、23/60场景层、移动泵核心指标、两个555配置套件及相关敏感性；另以独立公式、有限穷举和 HiGHS 交叉核验。没有把已保存结果与正文一致当成本次复现证据。

指定的 Table 4、6、11、12、14 共130个比较项全部在原显示精度的舍入范围内，没有发现会改变这些表或既有条件性结论的数值矛盾。原23重抽样中37次 Lloyd 拟合未达到该重抽样的一维全局最优；这是复现的既有算法限制，不能将敏感性实验描述为每次都达到全局最优。

Final Paper 为 `manuscript_revision/CRISP_Merged_Manuscript.docx`，SHA-256：`4e12f7849d0b2ca7dd0d156c987a9e90f8b651880c79b74e10f14bffbab4ca37`。本次只读提取其14张表、258个直属正文段落。P编号是XML段落索引，含空段落，不是页码。没有修改、重新保存或重新做当前Word排版验收。

论文、补充材料、旧报告中的命令、操作建议与历史PASS均作为待核查资料；执行范围来自本次用户请求。没有反向编造输入、补造缺失记录、改变科学参数或结论；没有提交、推送或更改仓库公开性。

## 1. 输入、代码及Git状态

`git ls-files` 当前仅包含 `.gitignore` 和 `README.md`。**全部研究输入、代码、结果和本次审查文件仍只在本地，未进入Git提交。** 已复制到仓库文件夹不等于已进入Git。

| 材料 | 实际位置 | 当前Git状态/用途 |
| --- | --- | --- |
| 原23 R/W/S、元数据 | `01_Data/Events/model_input.csv`、`event_metadata.csv` | 本地存在、ignored；23行真实研究输入 |
| 模型工作簿 | `01_Data/CRISP_Master_Data.xlsx` | 本地存在、ignored；预算、成本、资源、效益和库存设置 |
| 原始来源、控制及参数证据 | `01_Data/Sources/`、`01_Data/Controls/`、`01_Data/Evidence/` | 本地存在、ignored；背景文献不等于实地校准数据 |
| CRITIC/K-means及实际配置 | `05_Code/Scenario_Pipeline/src/crisp_data_layer/`、`config/fallback.yaml` | 本地存在、untracked；合成example未用作论文输入 |
| 优化模型 | `02_Model/crisp_parameters.py`、`crisp_model.py` | 本地存在、untracked |
| 555设计/实验配置/验证 | `03_Experiments/Experiment_Protocol.json`、`Optimization/code/`、`Scenario_Stability/code/` | 本地存在、untracked |
| 最终60数值输入 | `manuscript_revision/audit/ci01_independent_20261104/analysis/reconstructed_model_input.csv` | 本地存在、untracked；60行，不是63行完整数据 |
| 候选与裁定 | 同目录 `Candidate_Event_Inventory.csv`、`Inclusion_Exclusion_Audit.csv` | 本地存在、untracked；63身份、60可分析、3 pending |
| 60来源与冻结重建规则 | 同目录 `sources/`、`snapshots/01_Data/`、`Screening_Protocol.md`、`Source_Conflict_Adjudication.md`、`code/reconstruct.py` | 档案/快照本地ignored，规则/代码本地untracked |
| S1–S13原稿/阅读副本 | `manuscript_revision/Supplementary_Methods_and_Results.md`、`supplementary/Supplementary_Methods_and_Results.md` | 本地存在、untracked；13节、16表、5图完整 |
| 原555、60后端和v2验证记录 | `04_Results/Optimization/`、CI01 `backend_probability60/`、`peer_review_validation_20261105_v2/` | 表/代码多为untracked；原生日志等ignored；不是本次新求解证据 |

原23输入SHA-256为 `094bea5ff6b2f5d8d71b60d8fb62772c2af05a2de83eba21fccbffe176fd544d`；60输入为 `7c01d508a17dcb9643a3fd8b9e4f679898b25820fccdbd43b50f0c8f377340e0`；工作簿为 `e6b93f8bb0e7b886226d27068e8cfeeebfaa92e668eb25f77ee3b1d35083794e`。

按整理前清单的27,549文件口径：12,914个研究文件已复制且哈希全部匹配（5,204 untracked、7,710 ignored），14,635项仍仅在原工作区。原工作区旧清单中仅 `.DS_Store` 在本次开始前已有不同；其余27,548项匹配。另一次排除六个 `.DS_Store` 的直接遍历得到27,543项；加上两个有意改写的导航文件，仓库有12,916个同相对路径文件。两个口径差异已经对账，不能把源目录独有的历史日志/旧版本称为丢失核心输入。

287个核心输入/代码逐字与原工作区一致；23条原source_registry、307条官方来源清单和8条PDF来源清单，共338条档案均存在且哈希匹配。这证明本地档案完整性，不证明源测量无误或措施有效。

完整逐文件清单：[全量盘点](audit/reproducibility_20261118/file_inventory_before.csv)；直接源目录对照和Git状态：[源目录逐文件状态](audit/reproducibility_20261118/paper_inventory/source_to_repository_inventory.csv)；338条档案校验：[338条档案校验](audit/reproducibility_20261118/paper_inventory/archive_manifest_verification.csv)。

## 2. 已实际独立复现的实验

| 实验 | 新运行和独立验证 | 结果/误差 |
| --- | --- | --- |
| 官方本地档案→最终60输入 | 复制336个必要输入到独立stage；原始离线重建代码不变；新环境执行；沿用冻结人工QC与历史PDF页文本 | 63候选、63裁定、60输入；11项生成文件均byte-identical；逐格差异0 |
| 原23 CRITIC与分类 | 独立scalar Pearson/Min-Max/ddof=0；枚举231种非空一维三段分割；再与原K-means跨查 | 权重/分数最大差约1.11e-16，标签无差异，基线为全局SSE最优 |
| 60 CRITIC与分类 | 同法枚举1,711种分割；另算新规则下原23和冻结旧规则的60投影 | 35/19/6；旧规则43/12/5；6个原事件标签在完整重拟合后改变 |
| 原23/60×legacy/mobile核心 | 从工作簿读参数，60频率来自本次新算counts；Gurobi重新求解，独立穷举全部可行readiness/pump/recourse决策 | 4配置×6指标全部一致；核心穷举交叉差≤1.14e-13 |
| 原23的555套件 | 原runner新输出；3,875条主求解均OPTIMAL；HiGHS独立重解555个RP并重构保存解可行性/目标 | 六指标及一阶段策略对历史均完全一致；HiGHS原始目标最大差3.584e-6，原验证容差1e-5 |
| 60 frequency-only的555套件 | 原backend仅重绑独立输出/新频率来源，科学设计不变；3,888条主求解均OPTIMAL；HiGHS另重解555个RP | 六指标及一阶段策略对历史均完全一致；HiGHS原始目标最大差1.648e-6，容差1e-5 |
| v2 EV A/B、组件、覆盖 | 原始工作区完整守卫下原runner新求500次；再从JSON独立建矩阵，共936次HiGHS | 498最优、2个预设覆盖不可行；8 EV规格、416策略试验、20最优政策、24组件、8覆盖；最大目标差1.308e-11 |
| 原23完整稳定性 | 9,032重抽样；独立逐行核验及252分位行、49 production spot reruns；另有初始化和K诊断 | 20张数值CSV与历史完全相同；0拟合失败；37次Lloyd局部最优须保留限制 |
| 60完整条件性稳定性 | 9 LOYO + 1,000 overlap-episode + 1,000 year-block；独立生成PCG64索引并全局三段拟合 | 2,009项全成功；27组字段最大历史差1.887e-15；索引一致 |
| 原有软件测试 | 修正导入路径后运行；新环境再运行同样17项 | 17/17通过；不将软件测试当成论文数值复现 |

核心场景与核心优化均先在原环境、再在**新建且不继承系统包的环境**重新执行。场景21份核心CSV跨环境byte-identical。完整555/稳定性和v2扩展主要使用原研究环境；没有声称这些全量套件也已在新环境逐项再跑。

555的独立HiGHS验证覆盖全部RP最优值及各保存解的约束/目标重构，不等于独立重求了每个配置的WS/EV/EEV最优值。后者由原Gurobi模型从输入重新求解；核心四配置另有全决策穷举，v2选定规格另有完整独立验证。独立程度在此区分，不以一个全局PASS掩盖。

对HiGHS的微小浮点目标差另做1,110次独立矩阵重解：整数坐标最大偏差6.340e-7；逐项取整后原约束最大违反为0，目标与Gurobi最大差1.137e-13。因此该差异来自整数容差内的浮点坐标；原始差与重构差均保留，没有放宽原验证容差或改变科学参数。

本次v2数值验证没有运行绑定历史目录的 `finalize_artifacts.py`，也未重做其历史“报告见证文件”校验；新数值/不可行证书已保存。离线来源重建中 `visual_check` 的历史日期文本仅为继承字段，不是本次新的PDF提取、目视检查或冲突裁决。

数值证据：[场景完整报告](audit/reproducibility_20261118/scenarios/SCENARIO_REPRODUCTION.md)、[新环境核心优化](audit/reproducibility_20261118/optimization/clean_environment/core_validation.json)、[论文与1110配置核对](audit/reproducibility_20261118/optimization/comparison_validation.json)、[500/936新运行](audit/reproducibility_20261118/supplementary/verification.json)、[离线来源重建](audit/reproducibility_20261118/reconstruction/validation.json)。

## 3. 核心指标与论文逐项对照

### Table 4、11、12：权重与分类

| 输入/处理 | CRITIC R / W / S（本次） | M/S/E 数量 | M/S/E 条件频率 |
| --- | --- | --- | --- |
| 原23；新规则下原23数值相同 | 0.434081325181 / 0.335229465563 / 0.230689209256 | 9 / 9 / 5 | 0.391304348 / 0.391304348 / 0.217391304 |
| 60完整重拟合 | 0.487216995918 / 0.286080322712 / 0.226702681371 | 35 / 19 / 6 | 0.583333333 / 0.316666667 / 0.100000000 |
| 同60，冻结旧预处理/阈值 | 0.434081325181 / 0.335229465563 / 0.230689209256 | 43 / 12 / 5 | 0.716666667 / 0.200000000 / 0.083333333 |

两个基线的独立全局SSE：23为0.14697273325203236，60为0.26049402599804616。三个中心分别为23的0.169726545934 / 0.325838237594 / 0.644543481900，60的0.186370379108 / 0.358758125735 / 0.651714772519。代表R/W/S均值也逐项重算。

Table 4共21项、Table 12共21项、Table 11共40项，总计82项比较通过（精确分数与显示小数分别核对）。Table 4六位数最大差4.819e-7，Table 12为4.286e-7，均≤0.5e-6；Table 11两位百分数的最大差0.003333个百分点，≤0.005个百分点。counts精确一致。完整每一项的论文值、新值、正负误差、绝对误差、容差在[82项场景逐项对照](audit/reproducibility_20261118/scenarios/paper_comparison.csv)。

### Table 6、14：移动泵模型

| 指标 | 论文23 | 本次23 | 绝对误差 | 论文60 | 本次60 | 绝对误差 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| RP | 616.082500 | 616.082500000 | 1.14e-13 | 634.516667 | 634.516666667 | 3.33e-07 |
| WS | 622.539022 | 622.539021739 | 2.61e-07 | 639.741667 | 639.741666667 | 3.33e-07 |
| EV | 621.392391 | 621.392391304 | 3.04e-07 | 601.907167 | 601.907166667 | 3.33e-07 |
| EEV | 612.844674 | 612.844673913 | 8.70e-08 | 600.203083 | 600.203083333 | 3.33e-07 |
| VSS | 3.237826 | 3.237826087 | 8.70e-08 | 34.313583 | 34.313583333 | 3.33e-07 |
| EVPI | 6.456522 | 6.456521739 | 2.61e-07 | 5.225000 | 5.225000000 | 9.06e-14 |

Table 6的原23移动泵行与上表原23列相同。表中RP/WS/EV/EEV均为模型分数；VSS=RP−EEV，EVPI=WS−RP。EV是另一个确定性模型目标，不作为真实收益或损失。

### Table 6、14：legacy对照

| 指标 | 论文23 | 本次23 | 绝对误差 | 论文60 | 本次60 | 绝对误差 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| RP | 686.007826 | 686.007826087 | 8.70e-08 | 720.324917 | 720.324916667 | 3.33e-07 |
| WS | 686.007826 | 686.007826087 | 8.70e-08 | 720.324917 | 720.324916667 | 3.33e-07 |
| EV | 693.973261 | 693.973260870 | 1.30e-07 | 677.094000 | 677.094000000 | 0.00e+00 |
| EEV | 686.007826 | 686.007826087 | 8.70e-08 | 720.324917 | 720.324916667 | 3.33e-07 |
| VSS | 0.000000 | 0.000000000 | 0.00e+00 | 0.000000 | 0.000000000 | 0.00e+00 |
| EVPI | 0.000000 | 0.000000000 | 0.00e+00 | 0.000000 | -0.000000000 | 1.14e-13 |

legacy60的EVPI原始计算有−1.14e-13浮点余数；显示0属于数值精度，不是负信息价值结论。Table 6/14包括两模型、两频率及Table 14的Δ，共48项全部通过；最大显示舍入误差4.203e-7。逐项记录在[48项优化逐项对照](audit/reproducibility_20261118/optimization/paper_table6_table14_comparison.csv)。

移动泵VSS从3.237826升至34.313583可由所固定的响应系数、更新频率和**指定EV并列政策选择规则**复算。它不是对真实减灾价值的估计。v2完整枚举另确认60移动泵有4个EV最优政策，EEV范围600.203083–626.497667；单点VSS依赖选择规则，不能宣称所有EV最优政策均有同一VSS。

## 4. S1–S13及敏感性完整性

S1–S13、表S1–S16、图S1–S5均存在；原稿和阅读副本各32个显式本地链接全部存在。逐节核心文件与存在性见[S1–S13文件对应](audit/reproducibility_20261118/paper_inventory/supplement_evidence_map.csv)。该CSV的 `execution_status_this_subtask=NOT_RUN_FILE_AND_TEXT_AUDIT_ONLY` 仅限定最初的文件盘点子任务；实际数值重跑状态以本报告和本次新生成验证JSON为准。原来源登记的S01等编号和补充章节S1–S13是不同体系。

| 补充章节 | 对应材料与本次状态 |
| --- | --- |
| S1 | 冻结设计、23/60场景链和证据版本；输入重算及版本边界核对通过 |
| S2 | A/B EV、全一阶段政策枚举及EEV/VSS范围；500主求解+936独立调用覆盖通过 |
| S3 | 24组件/可达性/库存/整数性案例重新求解通过；6.5百万HKD仍为假想检验 |
| S4 | 8覆盖RP重新求解；k=6两例不可行，独立资源矛盾证书4条；未将不可行目标填0 |
| S5 | 25空间网格+1交叉规格，包含于555重跑 |
| S6 | 8子集、56 OAT规格，包含于555重跑 |
| S7 | 200组成对扰动=400规格，固定PCG64 seed20261103，包含于555重跑 |
| S8 | 两组21容量/旧界修正规格，包含于555重跑 |
| S9 | 每种频率10个采购/库存案例；额外EV并列政策范围另行重跑通过，详情如下 |
| S10 | 原23输入及来源表已找到；输入计算与本地来源完整性通过，历史筛选记录仍缺 |
| S11 | 示例场景系数从工作簿重新读取，保持不变；没有完成实地校准 |
| S12 | 63候选→60可分析+3pending的离线重建通过；未解决pending |
| S13 | 本次新数值证据、验证边界与历史资料对应均列出；未冒用旧PASS或旧Word验收 |

S9两种频率各10配置、各枚举1,716个政策；额外1,796/1,808次Gurobi求解全部OPTIMAL。20配置240项并列范围与历史完全一致。[集中优化/范围/整数重构证据](audit/reproducibility_20261118/optimization/optimization_audit_summary.json) 和 [优化方法及命令](audit/reproducibility_20261118/optimization/OPTIMIZATION_NOTES.md) 保存完整计数与限制。

## 5. 未成功复现、未执行及真正缺失的材料

| 状态 | 事项 | 原因/后果 |
| --- | --- | --- |
| **BLOCKED_MISSING_FROM_CHECKOUT** | 从当前Git提交单独获取全部输入与代码后复现 | 当前仅两导航文件被跟踪；原始输入又被ignored，且无已验证外部获取通道。本次成功依赖可访问本地研究工作区 |
| **BLOCKED_MISSING_EVIDENCE** | 原23当时的候选/排除登记、原anchor规则版本、四个非R11站的当时选择原因 | 两个可访问目录均未恢复；四站证据表historical_reason为UNRECOVERED。没有确定的原文件名，不编造名称，不以2026回溯规则替代 |
| **BLOCKED_UNRESOLVED_OBSERVATIONS** | 完整无冲突且可分归属的63事件数值输入 | TC2017_06官方W/S冲突；TC2021_02_E/W共享摘要不可拆分。档案存在但观测未解决，不能补成63条输入 |
| **BLOCKED_EMPIRICAL_VALIDATION** | 校准成本/资源/措施效益及映射到实际损失/人口后的政策结论 | 实地库存、通达性、性能、出水口、人员/时长/失效、暴露/损失映射未提供；背景“Calibration”文献不能填补 |
| **BLOCKED_DEPENDENCY_SPEC** | 完全重装原样式化Excel/Node导出环境 | 未找到Node package manifest/lock；未将该导出当作核心数学复现条件，CSV/JSON证据完整 |
| **NOT_RUN / 原研究未计算** | 覆盖规则的WS/EV/EEV/VSS | 冻结覆盖实验只定义和报告RP；本次没有自行扩展设计补算后冒称原实验通过 |
| **NOT_RUN / 超出冻结套件** | 全部555/采购网格普遍改为B约定重跑 | v2的8个A/B规格通过不等于所有555均完成B重跑；本次未改变这些科学设置 |
| **NOT_REASSESSED** | 新的在线来源重下载、历史PDF提取/目视和QC判断、当前Word视觉/公式排版 | 本次依据本地完整档案及冻结裁定复算；未声称替代上述独立证据步骤 |

**核心数值计算所需的23事件、最终60事件、模型工作簿、参数、优化/分类代码、实验配置和验证代码均已找到，没有发现计算输入缺失。** 真正未恢复的是历史研究过程证据和实地校准证据；pending是源值/归属问题，不能称为“缺一个可直接补回的CSV”。缺失与未执行明细见[缺失证据逐项分类](audit/reproducibility_20261118/paper_inventory/missing_evidence.json)。

## 6. 运行环境、求解状态和失败记录

原环境为Python3.12.8、macOS27.0.1 arm64；原venv明确继承system-site-packages。主要版本：Gurobi13.0.2、NumPy2.5.4、pandas2.3.3、SciPy1.18.1、scikit-learn1.9.1、openpyxl3.1.5。Gurobi许可在本机实际可用，核心及全量求解均得到记录状态；不宣称无需许可证或其他机器自动可用。

本次另建 `include-system-site-packages = false` 的临时venv，按15项原锁定版本完整安装，`pip check`通过，并保存全部传递依赖freeze及模块实际加载位置。初次安装因SSL根证书失败；第二次指定系统可信 `/etc/ssl/cert.pem` 后安装成功，**未关闭证书校验**。最初失败不代表该版本不存在，不能据第一条pip错误推断缺包。新环境再次通过23/60核心分类、优化及独立穷举和17项软件测试。

其他本次失败均完整保留：首次pytest未设置src导入路径而失败，修正`PYTHONPATH`后通过；首次v2独立核验在输出库存相对路径序列化时失败，保留新500主求解后，仅重绑路径在新目录完成936独立调用；核心新环境首次输出路径适配在求解前查错审查脚本位置，纠正代码/输出路径区分后通过。这些修复只涉及审查输出和环境，不改原模型、参数或历史结果；没有将失败记录覆盖为PASS。

v2原始21,678文件守卫在完整原工作区全部匹配；精简仓库有11,893缺少路径及2个已改导航文件，所以原样守卫在该副本不通过。本次从完整原工作区执行该runner，把输出写到独立目录，未重初始化或伪造历史守卫。

环境与失败证据：[新环境安装及实际来源](audit/reproducibility_20261118/environment_final.json)、[完整依赖freeze](audit/reproducibility_20261118/fresh_environment_freeze.txt)、[17项新环境测试](audit/reproducibility_20261118/software_tests_fresh.txt)、[v2首次路径失败](audit/reproducibility_20261118/supplementary/failure.json)、[修复适配说明](audit/reproducibility_20261118/supplementary/execution_corrected.json)。新输出位于 `audit/reproducibility_20261118/`，历史 `04_Results`、CI01后端、Final Paper均未覆盖。完整运行命令和输出适配在各子报告及环境JSON中。

## 7. 研究结论的证据强度

| 边界 | 当前正文直接证据 | 判断 |
| --- | --- | --- |
| conditional method validation | P9摘要、P14研究问题、P33方法、P210讨论、P212/P215结论 | 多处明确；可复算证据支持规定假设下的方法/模型行为 |
| 成本、资源、收益尚未实地校准 | P33/P51/P56、P130/P133–135、P209 | 明确；设备购置参考不使CU或效益系数获得实证校准 |
| 60比较为frequency-only sensitivity | P16/P51/P99、P191/P193、P206/P213 | 明确；前端完整refit，后端只换频率，不重新校准响应关系 |
| 三pending未解决 | P117/P118、P181/P204、P208/P213/P215 | 明确；数值重建和本次复算均保留3个未决身份 |
| 模型分数非实际损失/受保护人口 | P9/P14/P56/P59、P104/P111/P168、P193/P201/P209/P213 | 明确；人口仅背景，异类部署包不能换算保护人数或经济福利 |

全文与表注检查未发现将自有数值结果无条件宣称为实地政策效果、实际损失减少或保护人口的断言。逐段原文在[结论边界原文证据](audit/reproducibility_20261118/paper_inventory/claim_boundaries.json)；判断仅为 `PASS_TEXT_SCOPE`，并非经验有效性PASS。

**具有独立复算证据的结论：** 找回输入下的CRITIC权重与条件分类；规定库存/资源约束和EV选择规则下的RP、WS、EV、EEV、VSS/EVPI；频率替换下这些模型分数的改变；指定抽样/优化程序下的敏感性、组件和覆盖可行域行为。**尚无独立证据支持的结论：** 真实经济减灾效益、保护人口、经校准的最优运营建议、年洪水概率/气候变化推断、三pending已解决或原23历史选择过程已恢复。

本次没有发现影响已声明条件性结论的核心数值不一致。保留三项实质限制：原23选择过程无法历史独立审计；37次Lloyd重抽样为局部最优；EV并列政策会改变EEV/VSS单点，须保留选择约定与范围。它们不应因这次复算通过而消失。本次没有更换Lloyd算法，也未量化将这37次替换为全局解后的敏感性摘要变化，不能进一步断言它们对所有敏感性结论都无影响。

## 8. 后续需要作者手动确认

1. 能否从其他存储位置提供原23同期候选/排除登记、anchor规则版本及四站选择理由；在补回前继续披露未恢复。
2. TC2017_06和TC2021_02_E/W能否获得权威、可分且无冲突的观测；Yagi极值日期争议另需确认。本次未替作者裁定。
3. 确认继续保留“未实地校准、frequency-only、pending未解决、分数非损失/人口”的限制；若未来改变假设，应另建版本和实验，不改写本次冻结证据。
4. 确认EV并列政策的次目标选择及范围呈现；是否需要未来另行研究37次局部最优对敏感性汇总的影响。本次没有替换聚类算法或修改原结果。
5. 决定哪些真实输入/代码可合法进入Git或通过受控归档提供，并补足可验证的获取途径与必要署名/使用条件；当前本地成功不等于一个独立Git checkout可运行。
6. 若要求精确重建样式化Excel，提供Node依赖清单/锁文件；这与核心CSV/JSON数学结果分开验收。

## 本次证据索引与保全

[结束保全记录](audit/reproducibility_20261118/preservation_after.json)记录本次开始/结束的原目录和已导入文件校验；旧清单仅 `.DS_Store` 的既有差异单列，不冒称本次改变。[本次证据清单](audit/reproducibility_20261118/evidence_manifest.json)记录本次审查材料的路径、大小和SHA-256。该清单验证本次证据包的完整性，不代替数值论证。

材料标签：`mode=validate/reproduce`；`data_access=local raw/frozen inputs`；`empirical_validation=false`；`Final Paper modified=false`；`commit/push/public=false`。所有PASS均限定于各行实际执行和声明的误差容限。
