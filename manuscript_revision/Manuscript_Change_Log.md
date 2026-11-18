# 修订历史与当前修复状态

2026-11-04本轮审计修复：CI-02/03/04/07/08 CLOSED，CI-05 PARTIAL，CI-01/06 OPEN。E020共同驱动注释、Cai错配、辅助报告231计数及K指标边界已同步；五条完整官方原表已恢复并核对，Gabrel仅核作者版章节。所有冻结数值不变。当前详细记录见 [Fix_Log.md](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Fix_Log.md) 和 [Remaining_Blockers.md](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Remaining_Blockers.md)。

## 前一轮修订原记录

下列内容按历史保留，反映本轮修复之前的范围，例如“仅核Hato/Mangkhut”“未覆盖253原报告”。这些旧状态已由上述本轮记录和三份当前审计取代，不能作为当前未修事项。

# 英文主稿统一修订记录

修订日期：2026-11-04。依据版本：`mobile_inventory_v2`。新主稿为 `Revised_Manuscript_EN.md`，Word 版由同一主稿生成。此记录描述计算与证据核对，不构成实地校准或投稿就绪认证。

## 文件识别与版本选择

| 类别 | 选定文件 | 使用方式 |
| --- | --- | --- |
| 当前完整英文原稿 | `06_Manuscript/Original_Draft_for_Revision.docx` | 保留作者信息、研究问题和可核验文献，统一重写过时方法及结果 |
| 最新区域小节 | `06_Manuscript/Sections/Study_Area_and_Parameters.docx` | 合并完整普查小区定义、人口和参数证据边界 |
| 官方区域资料 | `01_Data/Spatial/census_units.csv`、`census_units.json`、`zone_summary.json`、`tai_o_census_aligned_zones.geojson`；官方普查 CSV 和 CSDI 存档 | 四个完整小区逐项核对；不进行面积插值 |
| 最新英文模型结果小节 | `06_Manuscript/Sections/Model_and_Results_EN.md` | 用当前实现、工作簿及明细解交叉核对后整合 |
| 主参数与结果工作簿 | `01_Data/CRISP_Master_Data.xlsx`；`04_Results/Optimization/CRISP_Results.xlsx` | 以当前数据和模型单位解释为准，不覆盖工作簿 |
| 六张优化图 | `04_Results/Optimization/figures/fig01_inventory` 至 `fig06_bounds`，各有 PNG/PDF | 原图复制到修订目录，统一为 Figure 2–7；地图为 Figure 1 |
| 当前模型与实验 | `02_Model/crisp_parameters.py`、`crisp_model.py`；`03_Experiments/Optimization/code/` 与 `03_Experiments/Experiment_Protocol.json` | 核对变量、库存、可达性、上界和 EV/EEV 实现 |
| 优化复核记录 | `04_Results/Optimization/模型修改与重跑报告.md`、`validation.json`、`independent_verification.json`、`report_verification.json`、`ev_tie_verification.json` | 采用已完成复核的 555 配置和并列策略结果 |
| 情景实验复核 | `04_Results/Scenario_Stability/完整分析報告.md`、`verification.json`、`reproducibility.json` 与结果表 | 补充 K=2、ARI、37 次非全局 Lloyd 拟合等限制 |
| 参考文献 | 完整原稿末尾 33 个条目，正文部分编号无对应 | 重建 20 条唯一编号文献；逐条处置见审计 CSV |
| 事件与来源表 | `01_Data/Events/event_metadata.csv`、`model_input.csv`、`reference_events.csv`；`01_Data/Sources/source_registry.json` | 逐行复核雨量并生成附录事件来源表；保留潮位核验缺口 |

更完整的定位和核验说明见 `audit/Source_Inventory.md`。版本优先级由项目 README、模型版本、运行来源哈希和复核记录共同确定，未仅按文件修改时间选择。

## 修订执行顺序

按用户要求依次完成：Methodology → Results → Study Area / Data → Discussion → Introduction → Abstract → Conclusion。各阶段正文保存在 `audit/sections/01_...` 至 `07_...`。最终按照论文阅读顺序组装为 Introduction、Related work、Methodology、Study area and data、Results、Discussion、Conclusion。

用户已明确要求完整统一修订；因此在独立目录形成全文新稿。原文件不覆盖。本次没有重新定义实验、调整输入、补造现场参数或生成新优化结果。

## 关键冲突及处理

| 原稿或旧材料表述 | 统一后的处理与位置 |
| --- | --- |
| 基准准备 Drainage + Warning，准备费用 14,000 CU，RP 686.008，VSS/EVPI 均为零 | 该组只保留为 legacy 对照。当前基准准备 Tai O1 的 Barrier + Warning，费用 13,000 CU、购泵 0，RP 616.082500、WS 622.539022、EEV 612.844674、VSS 3.237826、EVPI 6.456522。见 §5.2、Table 6–8 |
| “没有任何测试点同时满足 WS > RP > EEV” | 当前基准已同时严格满足，旧结论删除 |
| “全部资源约束均不紧”及设备利用率近满 | 改为当前 Moderate 物资 220/220 紧约束，劳动利用率 99.00%、99.75%、98.50%；设备最高 63.33% |
| 旧原稿只有二元准备和整数部署 | 增加第一阶段整数购泵 n、HKD 资本约束、逐情景共享库存与不可达区域抽水为零。保留其他准备和资源约束 |
| 泵准备费用可被理解为采购价，设备容量可被理解为泵库存 | 8,500 CU 是假设的地点准备费用；约 HKD 1,000,000 是 2025 年设备采购参考；抽象设备单位与物理库存分别解释 |
| EEV 只描述固定 y | 明确固定全部 y 与 n；原情景内仅重新优化部署 |
| 使用泛化大 M 或冻结旧 U | 统一为按当前运行预算及劳动、设备、物资比值推导的 U。旧 U 和额外可用性上限仅作为显式对照 |
| 旧 21 点结果未区分上界修复和库存扩展 | 五个修正点逐项列于 Table 11，六个准备预算点不受上界修复影响；当前库存模型的另一组 21 点单独说明 |
| 25,000 CU 后 VSS 为旧值约 28.409 | 当前库存网格为 RP 647.308152、所选策略 VSS 34.463478；旧值只属于 legacy 对照 |
| 准备预算、设备、物资结论沿用旧基准 | 用完整当前网格重新表述。当前劳动 600 时 RP 902.652826；legacy 修正值为 963.516304，二者不混用 |
| 较大采购上限的正 VSS 被理解为对所有 EV 最优策略成立 | 补充 10 个规格、1,716 项策略枚举；上限 3/4/6/8/12/20 的 VSS 范围下界均为 0。两泵基准所有审计 EV 最优策略 VSS 均为 3.237826 |
| 六泵为实际采购建议 | 明确是当前假设网格达到 legacy RP 的条件性阈值 |
| 两区泛称“候选地点”，人口或边界不完整 | Tai O1 = 完整 94404S，825 人；Tai O2 = 完整 94401S + 94409 + 94411，2,853 人。排除 94101S 的 682 人，不声称覆盖整个大澳行政区域 |
| 雨量是 maximum rainfall intensity | 改为五日窗口最大日累计雨量；不是最大小时雨强或五日总量 |
| 23 条事件“全部经过来源验证” | 明确雨量 23/23 与本地 RF 归档一致；潮位/增水仅本次直接核实 Hato 和 Mangkhut 两条；保留其他记录和入选母体缺口 |
| 事件频率被当作长期概率 | 改为所选事件的条件频率 9/23、9/23、5/23；不估计年概率、重现期或气候趋势 |
| 预警阈值或 200 人容量暗示已进入优化 | 标为官方背景，未用于当前 Warning 校准、庇护约束或聚类边界 |
| 三类分群或 CRITIC 排序被理解为真实确定结构 | 补充 K=2 silhouette 0.661 > K=3 的 0.538；事件/年份 ARI 中位数 0.5192/0.5085；37/9,032 次 Lloyd 未达全局 SSE；不作因果解释 |
| 情景报告称有 253 种连续三分切点 | 当前代码使用 `combinations(range(1,23),2)`，实际为 C(22,2)=231 个非空三分切点。主稿纠正该文字计数，SSE、9/9/5 和所有模型结果不变；未覆盖原报告 |
| 扰动区间等同置信区间、消融等同现实因果效应 | 统一为参数压力测试分位范围与模型贡献分解；200 项分别优化不构成一项统一稳健政策 |
| 引言中的普遍性空白或方法排他性主张 | 删除未有检索证据的“首次/很少”等主张，承认随机规划和可调整鲁棒模型的既有准备—响应结构 |

## 公式、符号、单位与图表

- 全文采用 s/j/i 的情景—区域—措施索引，y/n 为第一阶段，x 为第二阶段。
- 恢复为可读取的 18 组公式，明确 CRITIC ddof=0、EV 平均系数和平均 U 的保留约定、EV 并列数值容差 10⁻⁶、域与信息价值方向。
- 用 G 表示 recovery component score，λ 表示政策偏好权重，w 表示 CRITIC 权重，避免与事件雨量和资源符号混用。
- 金额分别标为 HKD 和 CU，效益及信息价值均标为 model score，劳动/设备/物资保持抽象单位。800 m³/h 为额定上限，8 h 为加油间隔，未转成响应时长或减损系数。
- 正文图为 Figure 1–7，表为 Table 1–11，附录表为 A1/B1。六张优化图在复制时保持原图内容和原始文件不变。
- Figure 6 的箱线须为最小值—最大值，Table 10 为 2.5%—97.5% 分位；Figure 7 是 legacy 上界修正图，不能当库存模型图。
- 英文术语统一为 readiness、procurement、deployment、shared pump stock、accessibility、conditional scenario frequency、model-score units。Drainage 专指 mobile pumping。

## 文献清理

原稿有重复 [1]–[3]、九条未编号条目，以及正文 [31]–[40] 缺少明确文末对应。修订稿建立了 20 条唯一编号参考文献，保留有主张用途且核验到元数据/摘要或原始材料的来源。没有将旧编号直接猜配到相似作品，也没有把未保留的作品称为虚假文献。

明确修正：Maqsood 等为 2005 年而非 2007 年，补 DOI；Li 等为 2007 年、39(2) 而非 2008 年、40(2)；Chan 等页码为 201–219，而非 201–212。Rawls、Mete 等原文正文涉及的作品使用已核验的出版记录建立完整条目。CRITIC 与稳定性原文及官方数据、算法说明作为方法依据纳入。

`audit/Citation_Verification.csv` 记录每条新文献的来源和核验范围；`audit/Original_Reference_Disposition.csv` 记录原 33 个条目的去留。不把摘要和元数据核验称为全文精读。目标期刊未指定，本稿使用统一数字引文，待选刊后再转换格式。

## 本次独立检查

- 555 项工作簿、CSV、报告 JSON 的 RP/WS/EV/EEV/VSS/EVPI、第一阶段购泵、费用和方案已逐项对齐。
- 555 份保留解中的 RP/EV/EEV/WS 及可行固定基准解已重构目标并检查整数、预算、资源、链接、库存和可达性；EEV 的 y/n 与 EV 一致。
- 六份运行来源哈希与当前主参数、模型、实验程序和方案一致。
- 23 条雨量最大日值、窗口总量及事件日值与归档 RF 数据一致；使用 RF 字段匹配，避免把机场多变量文件中的风向表误作雨量。
- 独立重算 CRITIC、事件分数与 K=3 全局切点，复现 9/9/5 及 SSE 0.146972733252。
- 四个普查单元人口、家庭及居所数与官方归档表一致。
- 原目录文件保持不变，前后哈希记录保存在审计目录。新稿中的 TODO 全部映射到 `Unresolved_Issues.md`。

本次未重新运行 555 项优化求解；HiGHS 最大差 3.58 × 10⁻⁶ 和完整重复运行结果来自已核验记录。本次独立工作是保留解和证据的一致性检查，不宣称新增实测或外部同行评审。DOCX 的最终页数和版面检查结果见 `audit/delivery_checks.json`。
