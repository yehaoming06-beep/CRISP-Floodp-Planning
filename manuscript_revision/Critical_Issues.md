# 修订论文证据一致性关键问题

日期：2026-11-04（Asia/Shanghai），修复后复查。**8项CI中5项CLOSED、1项PARTIAL、2项OPEN。** CLOSED仅适用于下表明确界定的问题，不等于整篇实证验证通过。主稿Markdown与Word已同步；模型、23条事件数值、站点、筛选集合和已核准结果均未改动。

真正解决的是E020注释、五条完整原表恢复与替代来源链、Cai错配、231计数和K评价措辞。Gabrel通过作者版章节定位与限制性表述处理，出版版仍未核，维持PARTIAL。候选/排除/锚点/站点替代历史及现实运行/效益校准必须另补新证据，维持OPEN。

| CI | 状态 | 处理类别 | 问题及实际处理 | 实际证据 | 关闭范围或未完成原因 |
| --- | --- | --- | --- | --- | --- |
| CI-01 | OPEN | 作者新证据 | 最初候选母体、入选/排除、锚点及站点替代历史未恢复 | 已检查原稿、现存配置/分析方案、迁移登记、项目树、Git标记和三个实际存在的ZIP；清理备份记录路径不存在。迁移可追踪文件路径，不能证明初筛规程。 | 作者须提供当时的候选/排除登记、锚点定义、四次站点替代决策及真实备份；目前只保留所选23条的条件分析。 |
| CI-02 | CLOSED | 真正解决 | E020共同驱动定义及注释遗漏已修正 | 完整官方Table 3.7.3的表头、Shek Pik行及脚注已读取并留存；主稿§3.2/§4.2/§4.3、Table 3、Appendix A、元数据及生成源均保留东北季风与Man-yi共同作用。 | 关闭范围为标签/定义与引用一致性；0.66 m及所有冻结数值不变，不推断纯台风分量。 |
| CI-03 | CLOSED | 真正解决 | 五个待补原表及六个失效链接的替代证据链已补齐 | E004/E019完整官方HTML；E021/E022/E023完整官方月报PDF，逐项核对Shek Pik、W/S、日期时间、单位/基准及质量脚注；完整PDF通过三路页数检查并核看原页，快照和SHA-256已保存。 | 关闭范围为这五条原表恢复与逐字段核对；不是23条观测无误、初筛无偏、雨站替代规程或现场测量校准的认证。原404链接保留并新增Verified来源。 |
| CI-04 | CLOSED | 真正解决 | Cai→Yang错误映射及生成原因已修正 | O03清空新编号并标记本稿未使用；O09仍唯一映射Yang [6]。生成器改为DOI身份匹配，对无DOI的Maqsood要求首作者签名和完整题名，已对账33条处置和当前20条文献。 | 关闭范围为错配与下游当前记录。旧重复编号及[31]–[40]原始意图仍未知，未猜填，也不把未使用文献判为虚假。 |
| CI-05 | PARTIAL | 限制性处理 | Gabrel具体章节仅取得作者版本，未完成出版版对照 | 已取得2012年7月、2013年5月修订作者全文：§2.2（PDF/印刷p.2）为静态无recourse；§2.3/§2.3.1（p.4）讨论多阶段及adjustable两阶段。正文缩窄为综述覆盖范围并明确版本。 | 出版商全文HTTP403，作者版与2014最终版逐段一致性尚未核；保留PARTIAL。[11]原公式逐式审读也未完成，稿件未宣称已做。 |
| CI-06 | OPEN | 作者新证据 | 效益、成本、真实运行与数据到优化的不确定性传播仍缺实证 | 现存模型和555配置仅支持给定假设下计算；未增加现场数据，未把重采样或求解器一致性当作效益校准。 | 须补真实库存/可达性/有效流量/班组/运输/运行成本、暴露及避免损失关系，并统一经济口径；若变更输入，完整重算受影响链。 |
| CI-07 | CLOSED | 真正解决 | 253→231及生成模板/图说已同步 | 23个有序点有22个内部空隙，非空三段选两个切点，C(22,2)=231。报告两处、build_report.py、plot_figures.py和captions.json均已修正，并写入更正历史。 | 只修文字计数；冻结SSE、分类、9,032行重采样和所有优化结果未改。历史错误值仅在明确标识的更正记录和旧快照中保留。 |
| CI-08 | CLOSED | 真正解决 | K=2评价限定为具体指标，删除笼统优越论 | 冻结k_diagnostics.csv：silhouette K2=0.6613216548>K3=0.5377687423；Davies–Bouldin越小越好，K3=0.5011840382<K2=0.5110220243。主稿§5.1和辅助事项均写明。 | 不宣称K2或K3是真实类别数；三类仍为既定规划离散化。 |

## 实际证据与复核记录

- [七条新增/替代官方来源及原URL链](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/Event_Source_Updates.csv)
- [当前23条潮位逐字段状态](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/tide_source_checks_current.json)
- [Gabrel作者版章节与出版版未完成原因](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/Gabrel_Section_Check.json)
- [历史与备份检索](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/history_search.json)
- [主稿逐块修订补丁](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/revision_patch_round1.json)
- [218/231块原样保留报告](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/manuscript.rev1.anchored.md.apply-report.json)

## K=2 ARI及37次非全局Lloyd拟合核对

前次审计从冻结23向量重新计算Min-Max、CRITIC、K=2–6，重建全部9,032条保存重采样的预处理分数与全局一维三段最优SSE，并对保存投射标签重算ARI。没有重新运行完整9,032次Lloyd拟合或所有优化求解器；“50次初始化”的设置来自保留代码/配置，37次由保存Lloyd SSE对本次独立全局SSE比较得到。对照容差为1e-10。

| 方法 | 保存拟合数 | 非全局数 | ARI中位数 | 2.5%–97.5%经验分位 | 实际最小–最大 |
| --- | --- | --- | --- | --- | --- |
| event_bootstrap | 3000 | 14 | 0.5192072757 | 0.3182806869–1.0000000000 | 0.1360531991–1.0000000000 |
| fixed_preprocess | 3000 | 15 | 0.6001008912 | 0.3273085771–1.0000000000 | 0.2114488505–1.0000000000 |
| year_bootstrap | 2000 | 6 | 0.5084949313 | 0.3273085771–1.0000000000 | 0.1236253573–1.0000000000 |
| subsample80 | 1000 | 2 | 0.4979989911 | 0.3273085771–1.0000000000 | 0.2561036043–1.0000000000 |
| leave_one_event | 23 | 0 | 0.3273085771 | 0.3273085771–1.0000000000 | 0.3273085771–1.0000000000 |
| leave_one_year | 9 | 0 | 0.6001008912 | 0.3273085771–0.8471190417 | 0.3273085771–0.8471190417 |

合计：3,000 + 3,000 + 2,000 + 1,000 + 23 + 9 = 9,032；非全局14 + 15 + 6 + 2 + 0 + 0 = **37**。它们是“成功收敛但未达全局SSE最低”的拟合，不能误写成37次求解失败、37个观测错误或37/23。固定预处理控制虽与事件bootstrap共享抽样索引，仍是单独拟合，包含在9,032中。

[§5.1](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:320)报告事件ARI中位0.5192、分位0.3183–1.0000及年份中位0.5085、分位0.3273–1.0000，与本次结果吻合。这里的“range”被明确限定为百分位范围；不能当作全部样本的最小–最大（实际最小分别约0.1361和0.1236）。原报告T05/T06与原始行也一致。全局解ARI对照维持样本敏感的结论，不将初始化误差当作全部不稳定性的解释。

全样本轮廓系数：K=2为**0.6613216548**，K=3为**0.5377687423**，新稿舍入0.661/0.538准确。前500个事件bootstrap在K=2–5之间按轮廓系数择优，K=2/3/4/5分别胜出224/57/51/168次（44.8%/11.4%/10.2%/33.6%）；论文未展开这组数字，但没有把它们反写成支持K=3。更高内部指标不能视为真实K的概率或独立外部验证。

固定原始23事件分数下，保留记录的200个seed、每次n_init=50均ARI=1，与论文一致；这仅是固定样本初始化诊断。前次独立枚举231个三段切分得到SSE=0.1469727332520323、群规模9/9/5。论文§5.1、§3.2及§3.6都将三类作为规划离散化，而未宣称发现三种自然灾害群体，呈现准确。

本次全局SSE与保存exact_sse最大差9.71e-17；重算全局投射ARI最大差5.55e-17；重算保存标签ARI最大差5.55e-17。完整结果见 [独立复算记录](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/evidence_consistency_20261104/independent_recalculation.json)，原始证据是 [9,032行拟合表](/Users/yehaoming/Desktop/climate_Devin/04_Results/Scenario_Stability/tables/resample_runs.csv)、[抽样索引](/Users/yehaoming/Desktop/climate_Devin/04_Results/Scenario_Stability/resample_indices.json)及[保存投射数组](/Users/yehaoming/Desktop/climate_Devin/04_Results/Scenario_Stability/event_projections.npz)。

## 统计置信度与因果证据解释核查

以下是对主稿实际句子的检查，“未发现误解”只覆盖已读到的主文、表格和图说，不把未做的覆盖率研究或因果验证判为通过。

| 对象/正文位置 | 实际证据及本次复算 | 当前表述是否误解 | 仍不支持的推论 |
| --- | --- | --- | --- |
| 重采样分位数 [§5.1](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:322)、[§6.3](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:475) | 事件/年份95%经验分位与原始拟合行一致；抽样单位是23事件或9年份，ARI比较共同23行基线。 | 未发现。稿件明确没有证明未来频率置信区间的覆盖率。 | 不能称95%真实类别准确率/总体覆盖率；B=3000不会增加独立观测数。 |
| 模型参数扰动 [§3.6](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:228)、[§5.6](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:427) | PCG64 seed20261103、独立U(0.8,1.2)原始乘子、200对、概率/偏好权重之后归一化；保存乘子200对一致、均在设计范围，已用种子重建核对。 | 未发现。已称hypothetical stress tests，不是拟合参数分布或实测效益置信区间。 | 不能称±20%为实测95%参数区间；归一化后的概率不必各自仍在原始±20%比例；分别求最优不构成共同稳健策略。 |
| Table 10与Figure 6 [表10](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:416)、[图6说明](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:431) | 表为2.5/50/97.5分位；6个论文显示行与保存200点复算一致，全部10个存储分位行最大数值差约3.6e-15。图6已查看，须的min/max含义与生成代码、图说一致。 | 未发现。图说区别须与表分位；主文明确均非实测效益置信区间。 | 图中须不能误读为95%区间；本次没有重新检验任何总体覆盖率。 |
| CRITIC [§2.3](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:51)、[§3.2](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:81) | 权重0.4340813252/0.3352294656/0.2306892093；事件bootstrap雨量权重居首0.892，源于所选样本变异/相关。 | 未发现。明确不是偏好权重或因果灾害贡献。 | 不能写雨量解释43.4%真实损失、89.2%置信度证明主因；与0.5/0.3/0.2效益偏好权重须分开。 |
| 消融/Shapley [§5.5](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:400)、[§6.2](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:469) | 由保存的八个再优化子集值独立计算Shapley=72.6388587/207.0833696/336.3602717，加和616.0825；留一损失0/3.2378261/144.6798913。 | 未发现。明确是规定模型价值函数贡献，而非现实因果效果或救人数。 | 不能称Warning是已实证最有效干预；约束、交互缺省及给定系数决定排序。Drainage留一损失0也不表示无现实价值。 |
| EV最优政策范围 [§3.5](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:218)、[图2说明](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:382) | 主文将同一EV目标并列政策产生的VSS区间与二次选择规则区分。 | 未发现。明确policy range，不是statistical interval。 | 不能把政策并列性区间当抽样不确定性或采购收益的置信区间。 |

### 参数分位与消融复算数值

| 设计 | 指标 | 有效数 | 2.5% | 中位数 | 97.5% |
| --- | --- | --- | --- | --- | --- |
| derived | rp | 200 | 469.792548 | 628.805630 | 811.543295 |
| derived | vss | 200 | 0.000000 | 0.000000 | 31.948876 |
| derived | evpi | 200 | 0.000000 | 0.000000 | 7.109179 |
| derived | regret | 200 | 0.000000 | 15.182290 | 73.980971 |
| availability | rp | 200 | 465.300577 | 624.199544 | 811.515040 |
| availability | vss | 200 | 0.000000 | 0.000000 | 38.005348 |
| availability | evpi | 200 | 0.000000 | 0.000000 | 7.881676 |
| availability | regret | 200 | 0.000000 | 17.654210 | 78.288377 |

两个设计的固定基准策略均200/200可行，故这些后悔值没有将不可行样本补0；代码仍把潜在不可行比较保留为缺失。VSS近零的浮点残差不构成负的实质信息价值。[分位数与Shapley生成程序](/Users/yehaoming/Desktop/climate_Devin/03_Experiments/Optimization/code/build_report.py)及[参数扰动设计](/Users/yehaoming/Desktop/climate_Devin/03_Experiments/Optimization/code/experiment_design.py)已检查；本次不重新运行555项优化求解。

## 本次验证范围

前节保留的是前次独立数值复算记录，本次未重新执行9,032次聚类拟合或555项优化。当前冻结输入、模型/配置、结果和图像以修复前后哈希对账；主稿全部数值表、方程和图像与修复前保持一致，新增指标比较来自冻结k_diagnostics.csv。完整复核结果见 [当前交付一致性记录](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/consistency_validation.json)。

具体修复和未完成事项分别见 [Fix_Log.md](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Fix_Log.md) 与 [Remaining_Blockers.md](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Remaining_Blockers.md)。前次报告在before目录完整保留；本报告取代其当前状态结论。
