# 修订论文全文引用与证据一致性审计

日期：2026-11-04（Asia/Shanghai），本次修复后的当前状态。20条书目、29个展开后的正文引用继续编号闭合；Cai→Yang错配已修正，Gabrel按已取得作者版具体章节缩窄论断并保留PARTIAL。事件来源恢复已补齐五条原表，未将下载失败、未读出版版或历史缺失认定为通过。

本报告保留未改变文献的前次核验范围，本次新增证据单独标明。前次三份报告完整保存于 [修复前快照](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/before/manuscript_revision)。

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

## 核验口径

`META`仅核身份/书目信息；`ABSTRACT/PREVIEW`只支持实际读到的摘要/引言概述；`PRIMARY`表示已读取相应官方正文或具体表行；`LOCAL`表示本地原始格式归档及复算，不等于本次在线回源。`PARTIAL`为部分核实，`UNVERIFIED`为未核实，均不是通过。找不到或打不开不能推定伪造，也不能推定支持。以下“支持”只适用于表中具体论点与取得材料的范围，不表示全文已审读、数据已实测校准或研究结论已验证。

正文位置已按修订后的Markdown一基行号复核；Word P编号为原始`word/document.xml`正文顶层段落的一基序号，包含空段落、不含表格内部段落，不是页码。完整上下文保存在 [29条Markdown引用记录](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/citation_mentions_current.json)、[29条Word引用记录](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/docx_citation_mentions_current.json)。

## 全文引用映射表

| ID | 正文位置 | 论点与引文编号 | 文献标题 | 作者 | 年份 | DOI | 核验状态 | 是否支持该论点及边界 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C01 | [1 Introduction L23](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:23)；Word P12 | [1] 大澳有已发表的沿海洪水管理挑战研究 | Coastal flood-risk management practice in Tai O, a town in Hong Kong | Chan, F. K. S.; Adekola, O. A.; Ng, C. N.; Mitchell, G.; McDonald, A. T. | 2013 | [10.1017/S1466046613000215](https://doi.org/10.1017/S1466046613000215) | META+ABSTRACT | 支持，限摘要所述地方风险/协调背景 |
| C02 | [1 Introduction L23](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:23)；Word P12 | [2] 官方应急准备与预报水位触发条件相关 | LCQ10: Disaster Preventive Measures of Tai O | Hong Kong Government | 2026 | — 官方网页 | PRIMARY | 支持，官方正文明确 |
| C03 | [1 Introduction L25](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:25)；Word P13 | [3] 灾前预置库址/库存，灾后分配 | Pre-positioning of emergency supplies for disaster response | Rawls, C. G.; Turnquist, M. A. | 2010 | [10.1016/j.trb.2009.08.003](https://doi.org/10.1016/j.trb.2009.08.003) | META+PREVIEW | 支持，出版商摘要及引言 |
| C04 | [1 Introduction L25](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:25)；Word P13 | [4] 医疗物资灾前存储与灾后分配的两阶段结构 | Stochastic optimization of medical supply location and distribution in disaster management | Mete, H. O.; Zabinsky, Z. B. | 2010 | [10.1016/j.ijpe.2009.10.004](https://doi.org/10.1016/j.ijpe.2009.10.004) | META+PREVIEW | 支持，出版商摘要及引言 |
| C05 | [2.1 Physical interventions and response benefits L39](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:39)；Word P20 | [5] LID及管道更换组合在不同降雨条件下优化 | Optimization of green and grey infrastructure for performance enhancement of urban drainage system under future conditions | Ye, C.; Gao, J.; Nachabe, M.; Charkhgard, H.; Zhang, Y.; Zhang, Q. | 2025 | [10.1016/j.jenvman.2025.124518](https://doi.org/10.1016/j.jenvman.2025.124518) | META+ABSTRACT | 支持，摘要/亮点直接对应 |
| C06 | [2.1 Physical interventions and response benefits L39](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:39)；Word P20 | [6] 自然方案的防洪效益及协同效益存在多目标权衡 | Multi-objective optimisation framework for assessment of trade-offs between benefits and co-benefits of nature-based solutions | Yang, S.; Ruangpan, L.; Sanchez Torres, A.; Vojinovic, Z. | 2023 | [10.1007/s11269-023-03470-8](https://doi.org/10.1007/s11269-023-03470-8) | META+PRIMARY_SECTION | 支持，摘要及框架章节 |
| C07 | [2.1 Physical interventions and response benefits L41](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:41)；Word P21 | [7] 欧洲EFAS潜在避免损失效益；不直接校准大澳包级分数 | The monetary benefit of early flood warnings in Europe | Pappenberger, F.; Cloke, H. L.; Parker, D. J.; Wetterhall, F.; Richardson, D. S.; Thielen, J. | 2015 | [10.1016/j.envsci.2015.04.016](https://doi.org/10.1016/j.envsci.2015.04.016) | META+ABSTRACT | 支持前半；后半为本研究适用边界，不可从欧洲效益迁移本地系数 |
| C08 | [2.1 Physical interventions and response benefits L41](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:41)；Word P21 | [1] 地方协调相关，但没有提供本模型系数校准 | Coastal flood-risk management practice in Tai O, a town in Hong Kong | Chan, F. K. S.; Adekola, O. A.; Ng, C. N.; Mitchell, G.; McDonald, A. T. | 2013 | [10.1017/S1466046613000215](https://doi.org/10.1017/S1466046613000215) | META+ABSTRACT | 部分支持：地方协调有摘要依据；未全文穷尽核查其不含任何系数 |
| C09 | [2.1 Physical interventions and response benefits L41](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:41)；Word P21 | [2] 官方响应安排支持协调背景，不提供本模型假设系数 | LCQ10: Disaster Preventive Measures of Tai O | Hong Kong Government | 2026 | — 官方网页 | PRIMARY | 支持，官方安排可定位；本地系数另明确为假设 |
| C10 | [2.2 Sequential decisions and uncertainty L45](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:45)；Word P23 | [8] 水资源分配结合区间、模糊和随机表示 | An interval-parameter fuzzy two-stage stochastic program for water resources management under uncertainty | Maqsood, I.; Huang, G. H.; Yeomans, J. S. | 2005 | [10.1016/j.ejor.2003.08.068](https://doi.org/10.1016/j.ejor.2003.08.068) | PUBLISHER_META+ABSTRACT | 支持，摘要直接对应 |
| C11 | [2.2 Sequential decisions and uncertainty L45](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:45)；Word P23 | [9] 混合区间/模糊两阶段整数防洪分洪规划 | Mixed interval–fuzzy two-stage integer programming and its application to flood-diversion planning | Li, Y. P.; Huang, G. H.; Nie, S. L. | 2007 | [10.1080/03052150601044831](https://doi.org/10.1080/03052150601044831) | META+ABSTRACT | 支持，题名与摘要直接对应 |
| C12 | [2.2 Sequential decisions and uncertainty L45](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:45)；Word P23 | [3] 不确定需求和交通网络条件下预置及配送 | Pre-positioning of emergency supplies for disaster response | Rawls, C. G.; Turnquist, M. A. | 2010 | [10.1016/j.trb.2009.08.003](https://doi.org/10.1016/j.trb.2009.08.003) | META+PREVIEW | 支持，摘要及引言直接对应 |
| C13 | [2.2 Sequential decisions and uncertainty L45](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:45)；Word P23 | [4] 医疗存储与情景配送相联 | Stochastic optimization of medical supply location and distribution in disaster management | Mete, H. O.; Zabinsky, Z. B. | 2010 | [10.1016/j.ijpe.2009.10.004](https://doi.org/10.1016/j.ijpe.2009.10.004) | META+PREVIEW | 支持，摘要直接对应 |
| C14 | [2.2 Sequential decisions and uncertainty L47](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:47)；Word P24 | [10] 作者版综述覆盖静态与多阶段决策，并列明版本核验边界 | Recent advances in robust optimization: An overview | Gabrel, V.; Murat, C.; Thiele, A. | 2014 | [10.1016/j.ejor.2013.09.036](https://doi.org/10.1016/j.ejor.2013.09.036) | AUTHOR_VERSION_SECTIONS / PUBLISHED_TEXT_PARTIAL | 限制性支持：已读2013年5月修订作者版§2.2 p.2及§2.3.1 p.4；正文缩窄并明确版本。2014出版版未取得，PARTIAL。 |
| C15 | [2.3 Hazard classification and evidence strength L51](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:51)；Word P26 | [11] CRITIC由对比与准则相关性产生数据权重 | Determining objective weights in multiple criteria problems: The CRITIC method | Diakoulaki, D.; Mavrotas, G.; Papayannakis, L. | 1995 | [10.1016/0305-0548(94)00059-H](https://doi.org/10.1016/0305-0548(94)00059-H) | META+ABSTRACT | 支持方法概述；不是偏好或因果权重的实证估计 |
| C16 | [2.3 Hazard classification and evidence strength L51](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:51)；Word P26 | [12] 重采样能揭示群成员敏感性，稳定不保证物理类型有效 | Cluster-wise assessment of cluster stability | Hennig, C. | 2007 | [10.1016/j.csda.2006.11.025](https://doi.org/10.1016/j.csda.2006.11.025) | META+PREVIEW | 支持，摘要及引言对应 |
| C17 | [3.2 Hazard normalization and classification L81](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:81)；Word P38 | [11] CRITIC反映样本变异及相关，不等于偏好/因果贡献 | Determining objective weights in multiple criteria problems: The CRITIC method | Diakoulaki, D.; Mavrotas, G.; Papayannakis, L. | 1995 | [10.1016/0305-0548(94)00059-H](https://doi.org/10.1016/0305-0548(94)00059-H) | META+ABSTRACT | 支持方法概述；公式逐式原文核验未完成，本地实现已复算 |
| C18 | [3.2 Hazard normalization and classification L83](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:83)；Word P39 | [13] K=3、k-means++、42、50次初始化、300迭代、Lloyd | KMeans | scikit-learn developers | n.d. | — 软件文档 | OFFICIAL_DOC+LOCAL_CODE | 支持，官方参数含义与本地设置吻合；运行设置依本地文件而非文档替作者背书 |
| C19 | [3.6 Experiment design and computational checks L230](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:230)；Word P88 | [14] ARI度量与基线分区的一致性 | adjusted_rand_score | scikit-learn developers | n.d. | — 软件文档 | OFFICIAL_DOC+LOCAL_RECALC | 支持，定义及本次逐行复算对应 |
| C20 | [3.6 Experiment design and computational checks L230](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:230)；Word P88 | [12] 借鉴重抽样诊断，且本项目Jaccard不同于最相似群统计 | Cluster-wise assessment of cluster stability | Hennig, C. | 2007 | [10.1016/j.csda.2006.11.025](https://doi.org/10.1016/j.csda.2006.11.025) | META+PREVIEW | 支持，区别已准确披露 |
| C21 | [4.1 Census-aligned research sectors L238](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:238)；Word P92 | [15] 四个完整普查小单元定义研究域 | 2021 Population Census (Statistics and Boundaries of Small Subunit Groups), SSUG_21C | Census and Statistics Department | n.d.; 数据年度2021 | — 官方数据集 | LOCAL_PRIMARY+PROVENANCE | 支持官方单元来源；两区组合和不裁剪是作者操作，不是官方行政分区 |
| C22 | [4.1 Census-aligned research sectors L254](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:254)；Word P98 | [15] 图1普查界线、2021人口及2026-11-04获取记录 | 2021 Population Census (Statistics and Boundaries of Small Subunit Groups), SSUG_21C | Census and Statistics Department | n.d.; 数据年度2021 | — 官方数据集 | LOCAL_PRIMARY+PROVENANCE | 支持，留存服务/几何来源登记及人口对账；未完成地理制图质量全面复核 |
| C23 | [4.1 Census-aligned research sectors L254](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:254)；Word P98 | [16] 背景岸线/建筑来自OSM、ODbL、2026-11-03提取 | Contextual coastline and building data for Tai O, extract dated 3 November 2026 | OpenStreetMap contributors | 2026 | — 地理数据 | LOCAL_PRIMARY+OFFICIAL_LICENSE | 支持，档案属性及获取登记相符 |
| C24 | [4.1 Census-aligned research sectors L254](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:254)；Word P98 | [17] 普查数据使用需依CSDI条款署名 | Terms and Conditions of Use | Common Spatial Data Infrastructure Portal | n.d. | — 官方条款 | PRIMARY | 支持，官方条款明确 |
| C25 | [4.2 Event inventory and observable screening rules L264](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:264)；Word P103 | [18] 19 R11、3 HKA、1 R12及年度事件计数 | Daily meteorological records at R11, HKA and R12, 2017–2025 | Hong Kong Observatory | n.d.; 数据年度2017–2025 | — 官方站点数据 | LOCAL_RF_23 / LIVE_INCOMPLETE | 支持本地台账；雨量归档一致性通过，完整在线回源和替代机制未核 |
| C26 | [4.2 Event inventory and observable screening rules L274](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:274)；Word P106 | [19] 海图基准潮位与天文潮以上增水有别，非淹没深度 | Tropical cyclone reports and event tables of maximum sea level and maximum storm surge, 2017–2025 | Hong Kong Observatory | n.d.; 事件年度2017–2025 | — 官方事件表 | PRIMARY_TABLES / JOINT_RISE_QUALIFIED | 支持量纲区分；E020共同驱动脚注已进入正文和元数据，不作纯台风分量推断。 |
| C27 | [4.3 Source checks and scenario inputs L280](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:280)；Word P109 | [19] 前次18张原表及本次补齐五条完整来源，字段相符且保留E020定义 | Tropical cyclone reports and event tables of maximum sea level and maximum storm surge, 2017–2025 | Hong Kong Observatory | n.d.; 事件年度2017–2025 | — 官方事件表 | PRIMARY_COMPLETE_RECOVERY_5 / PRIOR_DIRECT_18 | 支持限定的原表核对：五条完整快照、站点/值/时间/单位/质量检查见新来源台账；不支持初筛无偏或现场校准。 |
| C28 | [4.4 Illustrative intervention inputs and official equipment reference L306](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:306)；Word P118 | [20] 2025-08-12泵价约100万港元、最高800m³/h、约8小时加油 | Drainage Services Department procures additional pumping robots to respond to flooding [translated title] | Hong Kong Government | 2025 | — 官方新闻 | LOCAL_PRIMARY+OFFICIAL_INDEX | 支持官方报道事实；不支持有效流量、调用库存或本地效益校准 |
| C29 | [4.4 Illustrative intervention inputs and official equipment reference L310](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Revised_Manuscript_EN.md:310)；Word P120 | [2] 3.0 mCD/24h部分启动、3.3 mCD/数小时完全启动、约200人 | LCQ10: Disaster Preventive Measures of Tai O | Hong Kong Government | 2026 | — 官方网页 | PRIMARY | 支持；系背景条件，未作为本模型约束或效益参数 |

## 逐文献核验凭据与读取深度

Crossref公开元数据成功返回10篇；[8]接口返回429，保留失败状态，改由已经取得的出版商记录核对，未绕过接口限流。元数据不证明语义支持。该接口未返回更新关系也不能代替完整撤稿核查，本次不宣称完成了撤稿数据库筛查。

| 编号 | 凭据 | 本次实际核实范围 |
| --- | --- | --- |
| [1] | [出版商/官方记录](https://www.cambridge.org/core/journals/environmental-practice/article/abs/research-article-coastal-floodrisk-management-practice-in-tai-o-a-town-in-hong-kong/FD5FAF127B7EA447F1945F76EB79D5EA) | Cambridge题名、五位作者、摘要、15(3):201–219；Crossref同一DOI相符。未审读付费全文。 |
| [2] | [出版商/官方记录](https://www.info.gov.hk/gia/general/202605/06/P2026050600345.htm) | 官方答复正文及本地S03；3.0/3.3 mCD、24小时/数小时及约200人可定位。 |
| [3] | [出版商/官方记录](https://www.sciencedirect.com/science/article/pii/S0191261509001118) | Crossref题名、作者、2010、44(4):521–534相符；出版商检索到摘要与引言的两阶段库存/分配描述；直开403，未审读全文。 |
| [4] | [出版商/官方记录](https://www.sciencedirect.com/science/article/pii/S0925527309003582) | Crossref及出版商摘要/引言相符；预先存储及灾后医疗供应分配可核。直开403，未审读全文。 |
| [5] | [出版商/官方记录](https://www.sciencedirect.com/science/article/abs/pii/S0301479725004943) | Crossref六位作者及376:124518相符；出版商摘要明确LID、管道更换、六个降雨情景。未审读全文。 |
| [6] | [出版商/官方记录](https://link.springer.com/article/10.1007/s11269-023-03470-8) | Springer开放文章摘要及框架章节；Crossref同一四位作者及37:2325–2345相符。出版商规范引文将第三作者写作Torres, A. S.；属于姓名拆分规范差异。 |
| [7] | [出版商/官方记录](https://repository.mdx.ac.uk/item/856z2) | 作者机构Middlesex存储库及出版商摘要；Crossref六位作者、51:278–291相符。只核EFAS背景及潜在避免损失概述。 |
| [8] | [出版商/官方记录](https://www.sciencedirect.com/science/article/abs/pii/S0377221704002929) | 出版商记录明确2005-11-16、167(1):208–225及三位作者；摘要确认区间/模糊/随机结合。Crossref本次429，未重试，不能称该接口核验通过。 |
| [9] | [出版商/官方记录](https://www.tandfonline.com/doi/abs/10.1080/03052150601044831?medium=article) | Crossref与出版商期刊记录相符：39(2)、2007、163–183；网页另列2010在线日期，不替换卷期年2007。未审读全文。 |
| [10] | [作者版原始PDF](https://optimization-online.org/wp-content/uploads/2012/07/3537.pdf)；[章节记录](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/Gabrel_Section_Check.json) | 2013年5月修订作者版§2.2 PDF/印刷p.2、§2.3/§2.3.1 p.4已读并核看原页。全文PDF完整性PASS不等于全文所有技术结论已审读。出版商全文403，最终版未对照；PARTIAL。 |
| [11] | [出版商/官方记录](https://www.sciencedirect.com/science/article/abs/pii/030505489400059H) | Crossref及出版商摘要确认对比强度/准则冲突的方法依据；本文采用的逐式实现另有本地独立复算。未完成原论文公式逐式审读。 |
| [12] | [出版商/官方记录](https://www.sciencedirect.com/science/article/pii/S0167947306004622) | Crossref、出版商摘要/引言确认bootstrap、最相似群Jaccard及稳定不等于有效；未将该方法等同于本项目的排序对齐Jaccard。 |
| [13] | [出版商/官方记录](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html) | 官方1.9.1文档及本地代码：k-means++、n_init=50、seed=42、max_iter=300、algorithm=lloyd；多初始化不保证全局最优。 |
| [14] | [出版商/官方记录](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_rand_score.html) | 官方文档定义机会校正的两分区一致性；本次逐条重算已存投射标签ARI，非真实洪水标签准确率。 |
| [15] | [本地原始材料](/Users/yehaoming/Desktop/climate_Devin/01_Data/Sources/Census/census_service.json)；[普查CSV](/Users/yehaoming/Desktop/climate_Devin/01_Data/Spatial/census_ssg_2021_utf8.csv) | 动态门户只返回网页壳；本地CSDI服务/图层/几何SHA与来源登记相符，四单元人口、住户、屋宇与保留普查CSV逐项相符。两区组合是作者定义。 |
| [16] | [本地原始材料](/Users/yehaoming/Desktop/climate_Devin/01_Data/Sources/Calibration/S20.osm) | S20.osm、原始署名/ODbL属性、2026-11-03获取登记及SHA相符；官方版权页可读。不能据此认证建筑暴露或现状测绘精度。 |
| [17] | [本地原始材料](/Users/yehaoming/Desktop/climate_Devin/06_Manuscript/Sections/Study_Area_and_Parameters.docx) | 官方条款要求注明政府、CSDI及有关机构来源；本次只核引用依据，不作完整法律合规结论。 |
| [18] | [逐日RF复算](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/evidence_consistency_20261104/rainfall_recalculation.json) | 23条按RF块和±2日窗口独立复算相符；19条R11、3条HKA、1条R12。未重新在线下载全部站年资料；站点替代规则未证实。 |
| [19] | [当前23条潮位核验记录](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/tide_source_checks_current.json)；[恢复来源台账](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/Event_Source_Updates.csv) | 前次18条直接原表，加本次五条完整来源（E004/E019 HTML；E021/E022/E023完整PDF及原页）；数值均相符。E020以共同驱动定义保留。仅关闭来源恢复与逐字段核对，不认证筛选历史或现场效度。 |
| [20] | [出版商/官方记录](https://www.news.gov.hk/chi/2025/08/20250812/20250812_155549_205.html)；[S05正文](/Users/yehaoming/Desktop/climate_Devin/01_Data/Sources/Calibration/S05.txt:114) | S05原始网页哈希匹配，正文可定位约HKD100万/台、最高800m³/h、约8小时加油；官方检索文字吻合。实时直开超时，不声称现场性能校准。 |

元数据查询结果及失败记录：[公开来源获取日志](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/evidence_consistency_20261104/primary_fetch_log.json)。本次来源哈希与数值核对：[独立复算记录](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/evidence_consistency_20261104/independent_recalculation.json)。不沿用先前CSV中的“checked”作为本次通过依据。

## 旧稿[1] [2] [3]重号

直接读取旧稿438个正文顶层段落，References后有33条书目记录；P394是“上面是robust optimization 的文献”的编辑注，不计作第34条文献。33条中印刷编号只覆盖[1]–[11]和[21]–[30]，其中[1]、[2]、[3]各出现两次；另有9条未编号。按相同作品身份识别，Wu条目还在有编号与无编号位置重复，故有33个条目、32个可区分作品。不能把33个条目顺序当作编号[1]–[33]。

| 旧印刷编号 | 第一处 | 第二处 | 审计结论 |
| --- | --- | --- | --- |
| [1] | P391 Gabrel/Murat/Thiele (2014)，DOI 10.1016/j.ejor.2013.09.036 | P398 Ouazad/Kahn (2025)，DOI 10.3386/w33333 | 不同作品重号；旧正文仅写[1]时不足唯一定位。新稿[10]仅保留Gabrel。 |
| [2] | P392 Wu/Zou/Kang (2026) | P399 Ward等 (2017)，DOI 10.1038/nclimate3350 | 不同作品重号；Wu又在P412无编号重复。新稿[2]是政府答复，不能继承旧含义。 |
| [3] | P393 Cai等 (2025)，DOI 10.1016/j.fmre.2024.05.005 | P400 Maqsood/Huang/Yeomans（旧写2007） | 不同作品重号；Maqsood在新稿[8]改为2005。Cai并非新稿[6]。 |

## 9条未编号文献逐项处置

以下U01–U09是本审计的临时行标识，绝非替作者补成旧[12]–[20]。这些作品在修订稿中均未作为参考条目使用，“已删除/未使用”不等于书目核实或论点核实通过。

| 行ID/旧稿段落 | 题名 | 作者/年 | DOI与来源 | 核验状态及新稿处置 |
| --- | --- | --- | --- | --- |
| U01/P410 | A Multi-Objective Dynamic Resource Allocation Model for Search and Rescue and First Aid Tasks in Disaster Response by Employing Volunteers | Kapukaya, E. N.; Satoglu, S. I. (2025) | [10.3390/logistics9010041](https://www.mdpi.com/2305-6290/9/1/41) | 出版商作者、2025、Logistics 9(1):41及摘要相符；仅核身份和概述。 新稿未使用，旧编号映射未恢复。 |
| U02/P412 | Multi-stage robust and multi-role integrated allocation of emergency resources for hazard-induced disasters | Wu, X.; Zou, K.; Kang, W. (2026) | [10.1038/s41598-026-48199-7](https://www.nature.com/articles/s41598-026-48199-7) | 出版商2026-05-02、Scientific Reports 16:20513、三位作者及摘要相符；与P392同一作品重复。 新稿未使用，旧编号映射未恢复。 |
| U03/P414 | Evolve-DGN: An Evolving Dynamic Graph Network for Adaptive and Equitable Resource Allocation in Disaster Response | Kumar, S. (2025) | [10.1609/aaaiss.v7i1.36865](https://ojs.aaai.org/index.php/AAAI-SS/article/view/36865) | AAAI原始会议记录：2025-11-23、7(1):42–49、作者Sachin Kumar；身份相符，未核全部实验结论。 新稿未使用，旧编号映射未恢复。 |
| U04/P416 | A seismic-risk-based bi-objective stochastic optimization framework for the pre-disaster allocation of earthquake search and rescue units | Aydın, N. S. (2024) | [10.53391/mmnsa.1517843](https://dergipark.org.tr/en/pub/mmnsa/article/1517843) | 期刊原始记录：2024-09-30、4(3):370–394；身份和摘要相符。 新稿未使用，旧编号映射未恢复。 |
| U05/P418 | Pre- and Post-Disaster Allocation Strategies of Relief Items in the Presence of Resilience | Zhang, F.; Liu, Y.; Yun, H.; Cao, C.; Liu, X. (2025) | [10.3390/systems13080704](https://www.mdpi.com/2079-8954/13/8/704) | 出版商题名、Systems 13(8):704、2025及摘要核实；未逐一核完全部作者身份。 新稿未使用，旧编号映射未恢复。 |
| U06/P420 | Research on Allocation of Emergency Supplies and Vehicles Based on Multi-Period Demand and Supply | Qu, Y.; Yuan, X. (2026) | [10.2991/978-94-6239-652-4_20](https://www.atlantis-press.com/proceedings/emis-26/126022985) | 官方会议记录恢复完整题名：Yunchao Qu/Xinxing Yuan，2026-04-19、193–207；旧条目在“and.”处被截断，且只写起始页193，需补全。 新稿未使用，旧编号映射未恢复。 |
| U07/P422 | RADAR: Resource Allocation for Disaster Resilience in Senior Health Care | Kenne, M. M. et al. (2025) | [10.1145/3748636.3764164](https://dl.acm.org/doi/10.1145/3748636.3764164) | UNVERIFIED：出版商直开403，检索未取得足够原始记录；DOI仅为旧稿所载，未核实元数据或支持性，不能判不存在。 新稿未使用，旧编号映射未恢复。 |
| U08/P424 | Dynamic resource allocation for humanitarian relief chain coordination integrated with volunteers | Kapukaya, E. N. (2025) | [— 旧稿未列，未核实](https://polen.itu.edu.tr/server/api/core/bitstreams/80b534cd-e49b-4036-a56c-784d4cbd19f5/content) | UNVERIFIED：原学校存储链接本工具不可达，未取得可核正文/学位记录；不能将同名作者期刊文替代这项学位作品。 新稿未使用，旧编号映射未恢复。 |
| U09/P426 | An Optimization Model for Efficient Relocation of Hazardous Materials and Valuable Assets During Natural Disaster Warning Periods | Al Kalbani, A.; Gultekin, H.; Al Hinai, N. (2026) | [10.3390/logistics10020050](https://www.mdpi.com/2305-6290/10/2/50) | 出版商题名、三位作者、Logistics 10(2):50、摘要核实；这是确定性MILP概述，不能自动当两阶段随机规划证据。 新稿未使用，旧编号映射未恢复。 |

## 旧正文[31]–[40]映射检查

十个编号在旧正文P56/P58/P59出现，但References没有同号条目。不能按文末第31–33个物理条目猜配；那几行是互不相同的基础设施综述条目。除明确列出的新文献候选外，下表未猜填题名、年份或DOI。

| 旧编号 | 旧正文位置 | 署名/论点 | 身份与支持性状态 |
| --- | --- | --- | --- |
| [31] | P56 | Grass and Fischer：先决策后补救的两阶段结构 | 无唯一文末条目；题名、年、DOI未核。新稿改用已核[3,4]支持相关概述。 |
| [32] | P58 | Rawls and Turnquist：灾前设施/库存，灾后配送 | 可与新稿[3]的具体已核作品形成强候选对应；旧稿未列题名/DOI，仍不能断言恢复了原意。 |
| [33] | P58 | Mete and Zabinsky：医疗存储及情景配送 | 可与新稿[4]形成强候选对应；旧稿原编号意图未得到作者原始文献库确认。 |
| [34] | P58 | He and Zhuang：灾前准备与灾后救助支出权衡 | 无唯一文末条目；新稿删除该具体综述，身份及支持性未核。 |
| [35] | P58 | Alem et al.：预算、采购、车队、提前期与风险 | 无唯一文末条目；新稿删除，身份及支持性未核。 |
| [36] | P58 | Moreno et al.：设施、多趟运输、需求/路径不确定与剥夺成本 | 无唯一文末条目；新稿删除，身份及支持性未核。 |
| [37] | P59 | Zhang and Alipour：灾前桥梁减灾与洪后网络恢复 | 无唯一文末条目；新稿删除，身份及支持性未核。 |
| [38] | P59 | Wang et al.：台风路径不确定的多阶段能源系统 | 无唯一文末条目；作者名无法唯一识别作品，新稿删除。 |
| [39] | P59 | Wang et al.：第三阶段横向转运应急物流 | 无唯一文末条目；不能与[38]作者同姓合并，新稿删除。 |
| [40] | P59 | Liu et al.：随机/鲁棒混合的分布式能源资源配置 | 无唯一文末条目；新稿删除，身份及支持性未核。 |

## 33条旧书目与处置表对账

以下按原始文件物理顺序O01–O33编号。前次审计发现8个非空映射中O03 Cai错配为新[6] Yang；本次已清空O03新编号并记为本稿未使用，O09继续映射Yang [6]。修正后33条处置中7个非空映射均按作品身份对账；生成器改用DOI匹配，对无DOI的Maqsood同时要求首作者签名及题名。历史错误记录留在before快照及前次审计目录，不能作为当前映射。旧重复[3]的原始意图和旧[31]–[40]仍未恢复。

| 旧条目ID/段落 | 原文书目记录 | 既有CSV新编号 | 本次结论 |
| --- | --- | --- | --- |
| O01/P391 | [1] V. Gabrel, C. Murat, and A. Thiele, “Recent advances in robust optimization: An overview,” European Journal of Operational Research, vol. 235, no. 3, pp. 471–483, 2014, https://doi.org/10.1016/j.ejor.2013.09.036 | 10 | 作品身份匹配；正文相关概述见新引用映射 |
| O02/P392 | [2] Wu, X., Zou, K. & Kang, W. Multi-stage robust and multi-role integrated allocation of emergency resources for hazard-induced disasters. Sci. Rep. https://www.nature.com/articles/s41598-026-48199-7 (2026). | 未映射 | 未使用；本次未完成单独书目及语义核验 |
| O03/P393 | [3] J. Cai, Y. Wei, J. Yang, C. Ji, M. Liu, W. Fang, Z. Ma, and J. Bi, "A two-stage robust decision-making framework (2S-RDM) for flood risk adaptation under deep uncertainty," Fundamental Research, vol. 5, no. 4, pp. 1771-1780, 2025. https://doi.org/10.1016/j.fmre.2024.05.005 | 未映射 | 已修正：本稿未使用Cai；与Yang [6]不是同一作品。旧[3]原意仍未恢复。 |
| O04/P398 | [1] Ouazad, A., & Kahn, M. E. (2025). Time consistent infrastructure investments: Optimal flood protection policies in spatial equilibrium. NBER Working Paper No.33333. National Bureau of Economic Research. https://doi.org/10.3386/w33333. | 未映射 | 未使用；本次未完成单独书目及语义核验 |
| O05/P399 | [2] Ward, P. J., Jongman, B., Aerts, J. C. J. H., Bates, P. D., Botzen, W. J. W., Diaz Loaiza, A., Hallegatte, S., Kind, J. M., Kwadijk, J., Scussolini, P., & Winsemius, H. C. (2017). A global framework for future costs and benefits of river-flood protection in urban areas. Nature Climate Change, 7, 642–646. https://doi.org/10.1038/nclimate3350. | 未映射 | 未使用；本次未完成单独书目及语义核验 |
| O06/P400 | [3] Maqsood, I., Huang, G. H., & Yeomans, J. S. (2007). An interval-parameter fuzzy two-stage stochastic program for water resources management under uncertainty. European Journal of Operational Research, 167, 208–225. | 8 | 作品身份匹配；2007→2005已核 |
| O07/P401 | [4] Li, Y. P., Huang, G. H., & Nie, S. L. (2008). Mixed interval-fuzzy two-stage integer programming and its application to flood-diversion planning. Engineering Optimization, 40(2), 163–183. https://doi.org/10.1080/03052150601044831. | 9 | 作品身份匹配；2008/40→2007/39已核 |
| O08/P402 | [5] Ye, C., Gao, J., Nachabe, M., Charkhgard, H., Zhang, Y., & Zhang, Q. (2025). Optimization of green and grey infrastructure for performance enhancement of urban drainage system under future conditions. Journal of Environmental Management, 376, 124518. https://doi.org/10.1016/j.jenvman.2025.124518. | 5 | 作品身份匹配；正文相关概述见新引用映射 |
| O09/P403 | [6] Yang, S., Ruangpan, L., Sanchez Torres, A., & Vojinovic, Z. (2023). Multi-objective optimisation framework for assessment of trade-offs between benefits and co-benefits of nature-based solutions. Water Resources Management, 37, 2325–2345. https://doi.org/10.1007/s11269-023-03470-8. | 6 | 作品身份匹配；正文相关概述见新引用映射 |
| O10/P404 | [7] Lopane, F. D., & Dawson, R. J. (2026). Optimisation of temporary and demountable flood protection for infrastructure resilience. Journal of Flood Risk Management. https://doi.org/10.1111/jfr3.70182. | 未映射 | 未使用；本次未完成单独书目及语义核验 |
| O11/P405 | [8] Pappenberger, F., Cloke, H. L., Parker, D. J., Wetterhall, F., Richardson, D. S., & Thielen, J. (2015). The monetary benefit of early flood warnings in Europe. Environmental Science & Policy, 51, 278–291. https://doi.org/10.1016/j.envsci.2015.04.016. | 7 | 作品身份匹配；正文相关概述见新引用映射 |
| O12/P406 | [9] Singh, M., & Cai, X. (2023). Coastal flooding hazard, exposure, and readiness of buildings in Hong Kong in 2080–2100, and the implications for real estate management. ISPRS International Journal of Geo-Information, 12(3), 86. https://doi.org/10.3390/ijgi12030086. | 未映射 | 未使用；本次未完成单独书目及语义核验 |
| O13/P407 | [10] Chan, F. K. S., Adekola, O. A., Ng, C. N., Mitchell, G., & McDonald, A. T. (2013). Coastal flood-risk management practice in Tai O, a town in Hong Kong.ΩEnvironmental Practice, 15(3), 201–212. https://doi.org/10.1017/S1466046613000215 | 1 | 作品身份匹配；201–212→201–219已核 |
| O14/P408 | [11] Ma, S., Chen, B. & Wang, Z. Resilience Enhancement Strategy for Distribution Systems Under Extreme Weather Events. IEEE Trans. Smart Grid 9, 1442–1451 (2018). | 未映射 | 未使用；本次未完成单独书目及语义核验 |
| O15/P410 | Kapukaya, E. N. & Satoglu, S. I. A Multi-Objective Dynamic Resource Allocation Model for Search and Rescue and First Aid Tasks in Disaster Response by Employing Volunteers. Logistics 9, 41 (2025). | 未映射 | 未使用；身份核验见U表，不代表已支持旧论点 |
| O16/P412 | Wu, X., Zou, K. & Kang, W. Multi-stage robust and multi-role integrated allocation of emergency resources for hazard-induced disasters. Sci. Rep. https://www.nature.com/articles/s41598-026-48199-7 (2026). | 未映射 | 未使用；身份核验见U表，不代表已支持旧论点 |
| O17/P414 | Kumar, S. Evolve-DGN: An Evolving Dynamic Graph Network for Adaptive and Equitable Resource Allocation in Disaster Response. in Proceedings of the AAAI Symposium Series vol. 7 42–49 (2025). | 未映射 | 未使用；身份核验见U表，不代表已支持旧论点 |
| O18/P416 | Aydın, N. S. A seismic-risk-based bi-objective stochastic optimization framework for the pre-disaster allocation of earthquake search and rescue units. Math. Model. Numer. Simul. Appl. 4, 370–394 (2024). | 未映射 | 未使用；身份核验见U表，不代表已支持旧论点 |
| O19/P418 | Zhang, F., Liu, Y., Yun, H., Cao, C. & Liu, X. Pre- and Post-Disaster Allocation Strategies of Relief Items in the Presence of Resilience. Systems 13, 704 (2025). | 未映射 | 未使用；身份核验见U表，不代表已支持旧论点 |
| O20/P420 | Qu, Y. & Yuan, X. Research on Allocation of Emergency Supplies and. in Proceedings of the 2026 5th International Conference on Engineering Management and Information Science (EMIS 2026) 193 (Springer Nature, 2026). | 未映射 | 未使用；身份核验见U表，不代表已支持旧论点 |
| O21/P422 | Kenne, M. M. et al. RADAR: Resource Allocation for Disaster Resilience in Senior Health Care. in Proceedings of the 33rd ACM International Conference on Advances in Geographic Information Systems 959–972 (ACM, The Graduate Hotel Minneapolis Minneapolis MN USA, 2025). doi:10.1145/3748636.3764164. | 未映射 | 未使用；身份核验见U表，不代表已支持旧论点 |
| O22/P424 | Kapukaya, E. N. Dynamic resource allocation for humanitarian relief chain coordination integrated with volunteers. https://polen.itu.edu.tr/server/api/core/bitstreams/80b534cd-e49b-4036-a56c-784d4cbd19f5/content (2025). | 未映射 | 未使用；身份核验见U表，不代表已支持旧论点 |
| O23/P426 | Al Kalbani, A., Gultekin, H. & Al Hinai, N. An Optimization Model for Efficient Relocation of Hazardous Materials and Valuable Assets During Natural Disaster Warning Periods. Logistics 10, 50 (2026). | 未映射 | 未使用；身份核验见U表，不代表已支持旧论点 |
| O24/P428 | [21] Wassmer, D., Merz, B., & Marwan, N. (2024). Resilience of transportation infrastructure networks to road failures. | 未映射 | 未使用；本次未完成单独书目及语义核验 |
| O25/P429 | [22] Martín, B., et al. (2021). Assessing road network resilience: An accessibility comparative analysis. | 未映射 | 未使用；本次未完成单独书目及语义核验 |
| O26/P430 | [23] Tariverdi, M., et al. (2023). Measuring accessibility to public services and infrastructure criticality for disasters risk management. | 未映射 | 未使用；本次未完成单独书目及语义核验 |
| O27/P431 | [24] Watson, M., & Ahn, S. (2022). A systematic review: To increase transportation infrastructure resilience to flooding events. | 未映射 | 未使用；本次未完成单独书目及语义核验 |
| O28/P432 | [25] Lang, Y., et al. (2024). Resilience assessment and enhancement strategies for urban transportation infrastructure to cope with extreme rainfalls. | 未映射 | 未使用；本次未完成单独书目及语义核验 |
| O29/P433 | [26] Gupta, S., Robinson, C., & Dilkina, B. (2018). Infrastructure resilience for climate adaptation. | 未映射 | 未使用；本次未完成单独书目及语义核验 |
| O30/P434 | [27] Blagojević, N., et al. (2023). Quantifying disaster resilience of a community with interdependent civil infrastructure systems. | 未映射 | 未使用；本次未完成单独书目及语义核验 |
| O31/P435 | [28] Oikonomou, K., et al. (2021). Resilience of interdependent water and power systems: A literature review and conceptual modeling framework. | 未映射 | 未使用；本次未完成单独书目及语义核验 |
| O32/P436 | [29] Sathurshan, M., et al. (2022). Resilience of critical infrastructure systems: A systematic literature review of measurement frameworks. | 未映射 | 未使用；本次未完成单独书目及语义核验 |
| O33/P437 | [30] Sänger, N., Heinzel, C., & Sandholz, S. (2021). Advancing resilience of critical health infrastructures to cascading impacts of water supply outages—Insights from a systematic literature review. | 未映射 | 未使用；本次未完成单独书目及语义核验 |

## 仍须完成的证据工作

1. CI-05保持PARTIAL：补2014出版版相关章节并与作者版对照；不能把取得作者版或出版商403写成最终版核验通过。[11]没有完成原公式逐式审读。
2. CI-01保持OPEN：作者须提供真实候选/排除登记、锚点定义及站点替代记录。旧[31]–[40]原始引用意图、U07/U08身份不足只在作者恢复相应论述时补证，不猜配。
3. CI-06保持OPEN：运行与效益参数仍需现场校准。23对官方表格相符不能代替这些新证据。
4. 当前29个正文引用位置与20条书目编号闭合，只证明当前引用记录一致；其余文献保留前次实际读取深度，不升级为全部全文审读。
