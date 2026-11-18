# 23条事件数据核验与入选追溯审计

日期：2026-11-04（Asia/Shanghai），修复后状态。**五条此前仅索引部分核实的潮位记录，现已取得完整官方来源并逐字段核对相符。** 前次18张直接原表与本次五条恢复来源合计覆盖23对W/S；E020仍是有明确共同驱动限定的增水，不能当作纯台风分量。该覆盖只证明来源表格与冻结输入一致，不代表样本无偏、仪器校准、雨站替代程序或大澳淹水深度验证。

冻结输入、事件日期/站点、五日雨窗、筛选集合和所有数值未变；元数据仅在E020的data_quality_note追加语义注释。23条雨量仍沿用前次本地RF归档复算范围，本次没有重新在线下载全部雨量来源。

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

## 来源恢复及完整性证据

E004/E019完整官方HTML含表头、全部站行及表后区域，现已直接取得；原浏览工具的Cache miss保留为失败历史，不改写为本次失败。三条2025记录的原informtc链接本次仍为404。两份官方月报初次整文件下载中断，本次按服务器支持的HTTP 206分段续传：161段均核对Content-Range、长度和同一Last-Modified，按字节顺序组成完整17,550,025及24,443,418字节PDF；三路页数分别一致为87和136，无解析修复警告。随后读取并核看完整原页和质量脚注，才将这五条升级。

| 事件 | 原表定位（含事件名） | PDF页 | 印刷页 | 快照 | SHA-256 | 质量注释检查 |
| --- | --- | --- | --- | --- | --- | --- |
| E004 | Table 3.4.4, Pakhar, Shek Pik | HTML完整表 | — | [完整快照](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/sources/E004_table344.html) | 4cde7bab5a25388f319a1a200829a7deb2ef56087e3a6071157e813144917788 | No table-specific quality footnote or incomplete-data marker is present in the complete HTML table. |
| E019 | Table 3.6.4, Toraji, Shek Pik | HTML完整表 | — | [完整快照](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/sources/E019_table364.html) | 9f255f1ff743602609d7958995529f57f80e46b74c524eedb85167be7a751ae1 | No table-specific quality footnote or incomplete-data marker is present in the complete HTML table. |
| E021 | July 2025 Monthly Weather Summary, Table 2.3.5, Wipha | 45 | 42 | [完整快照](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/sources/HKO_MWS202507.pdf) | 42f598310745d9ffa56c5f6a01a90f8e995d165b7cc9f3688a9394b134d7ab44 | Complete page visually checked; Shek Pik has no bracketed or incomplete-data marker. No tide-table-specific quality note is present. |
| E022 | September 2025 Monthly Weather Summary, Table 2.2.4, Tapah | 32 | 29 | [完整快照](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/sources/HKO_MWS202509.pdf) | 3b4e66b57b4387b723863ea6cf7936a7bf594bb2b7185d2e3b85b561f50a592b | Complete page visually checked; Shek Pik has no bracketed or incomplete-data marker. The bracketed-data note is above this tide table and belongs to the preceding rainfall table. |
| E023 | September 2025 Monthly Weather Summary, Table 2.2.5, Ragasa | 71 | 68 | [完整快照](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/sources/HKO_MWS202509.pdf) | 3b4e66b57b4387b723863ea6cf7936a7bf594bb2b7185d2e3b85b561f50a592b | Complete page visually checked; Shek Pik has no bracketed or incomplete-data marker. The bracketed-data note is above this tide table and belongs to the preceding rainfall table. Waglan Island is explicitly unavailable; this does not apply to Shek Pik. |

九月月报重复使用Table 2.2.4编号（Tapah与Mitag），本台账以事件名和PDF页共同定位，未误用Mitag表。九月两页的方括号注释在前一张雨量表下方，只适用于相应雨量数据；Ragasa的无资料说明指Waglan Island，不能移给Shek Pik。五条目标Shek Pik行均无不完整数据标记；这不等于证明传感器没有测量误差。月报PDF第2页明确时间为UTC+8。E004/E019 HTML未写独立时区行，按原表抄录日期时间且不转换，不额外推断时区。

[逐次下载及失败记录](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/retrieval_log.json)；[分段完整性记录](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/range_download_log.json)；[原页文本提取](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/monthly_table_extraction.json)；[原URL与替代证据链](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/Event_Source_Updates.csv)。

## 23条逐事件当前登记

L表示前次本地雨量RF归档复算相符；D表示前次直接官方原表记录；D+表示本次完整来源逐字段核对；J表示共同驱动定义已经准确限定。各极值不要求同时发生。

| ID及台账锚点 | 事件 | 雨站 | R mm/日及状态 | W mCD及峰值日期时间 | S m及峰值日期时间 | 潮位/增水状态 | 来源 | 质量及含义 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E001 2017-06-12 | Severe Tropical Storm Merbok | R11 | 117.0；L | 2.57；2017-06-12 10:06 | 0.28；2017-06-12 10:09 | D：前次直接原表相符 | [Table 3.1.4, Shek Pik](https://www.hko.gov.hk/en/publica/tc/tc2017/table314.html) | Shek Pik行未标不完整 |
| E002 2017-07-23 | Tropical Storm Roke | R11 | 13.5；L | 2.75；2017-07-23 08:04 | 0.22；2017-07-23 08:03 | D：前次直接原表相符 | [Table 3.2.3, Shek Pik](https://www.hko.gov.hk/en/publica/tc/tc2017/table323.html) | Shek Pik行未标不完整 |
| E003 2017-08-23 | Super Typhoon Hato | R11 | 86.0；L | 3.91；2017-08-23 11:30 | 1.54；2017-08-23 11:32 | D：前次直接原表相符 | [Table 3.3.4, Shek Pik](https://www.hko.gov.hk/en/publica/tc/tc2017/table334.html) | 不完整标记属于其他站，Shek Pik无此标记 |
| E004 2017-08-27 | Severe Tropical Storm Pakhar | HKA | 136.2；L | 2.38；2017-08-27 12:22 | 0.67；2017-08-27 06:52 | D+：完整来源相符 | [Table 3.4.4, Pakhar, Shek Pik](https://www.hko.gov.hk/en/publica/tc/files/TC2017.pdf)；[本次快照](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/sources/E004_table344.html) | No table-specific quality footnote or incomplete-data marker is present in the complete HTML table. |
| E005 2017-10-15 | Severe Typhoon Khanun | R11 | 45.0；L | 2.88；2017-10-15 19:02 | 1.04；2017-10-15 19:04 | D：前次直接原表相符 | [Table 3.7.4, Shek Pik](https://www.hko.gov.hk/en/publica/tc/tc2017/table374.html) | Shek Pik行未标不完整 |
| E006 2018-09-16 | Super Typhoon Mangkhut | R11 | 277.5；L | 3.89；2018-09-16 14:16 | 2.34；2018-09-16 14:16 | D：前次直接原表相符 | [Table 3.5.5, Shek Pik](https://www.hko.gov.hk/en/publica/tc/tc2018/table355.html) | 不完整标记属于其他站，Shek Pik无此标记 |
| E007 2019-07-31 | Tropical Storm Wipha | HKA | 104.8；L | 3.20；2019-08-01 09:30 | 0.64；2019-08-01 09:29 | D：前次直接原表相符 | [Table 3.2.4, Shek Pik](https://www.hko.gov.hk/en/publica/tc/tc2019/table324.html) | Shek Pik行未标不完整；潮位日期比事件锚点晚一天 |
| E008 2020-08-19 | Typhoon Higos | R11 | 96.5；L | 3.00；2020-08-19 07:22 | 0.71；2020-08-19 05:26 | D：前次直接原表相符 | [Table 3.3.4, Shek Pik](https://www.hko.gov.hk/en/publica/tc/tc2020/table334.html) | Shek Pik行未标不完整 |
| E009 2020-10-13 | Tropical Storm Nangka | R11 | 23.0；L | 2.72；2020-10-13 05:57 | 0.74；2020-10-13 13:11 | D：前次直接原表相符 | [Table 3.4.4, Shek Pik](https://www.hko.gov.hk/en/publica/tc/tc2020/table344.html) | Shek Pik行未标不完整 |
| E010 2021-10-09 | Tropical Storm Lionrock | R11 | 230.5；L | 2.91；2021-10-09 22:25 | 0.56；2021-10-09 05:39 | D：前次直接原表相符 | [Table 3.5.4, Shek Pik](https://www.hko.gov.hk/en/publica/tc/tc2021/table354.html) | Shek Pik行未标不完整；网页台风名有拼写误植 |
| E011 2021-10-13 | Typhoon Kompasu | R11 | 149.5；L | 3.38；2021-10-13 02:26 | 1.36；2021-10-13 09:32 | D：前次直接原表相符 | [Table 3.6.4, Shek Pik](https://www.hko.gov.hk/en/publica/tc/tc2021/table364.html) | Shek Pik行未标不完整 |
| E012 2022-07-02 | Typhoon Chaba | R11 | 122.5；L | 2.94；2022-07-02 10:19 | 0.70；2022-07-02 08:19 | D：前次直接原表相符 | [Table 3.1.4, Shek Pik](https://www.hko.gov.hk/en/publica/tc/tc2022/table314.html) | Shek Pik行未标不完整 |
| E013 2022-08-25 | Typhoon Ma-on | R12 | 42.0；L | 2.94；2022-08-25 07:12 | 0.70；2022-08-25 04:39 | D：前次直接原表相符 | [Table 3.4.4, Shek Pik](https://www.hko.gov.hk/en/publica/tc/tc2022/table344.html) | Shek Pik行未标不完整；与Chaba同数值但不同事件，不能据此判为重复记录 |
| E014 2022-11-02 | Severe Tropical Storm Nalgae | R11 | 43.0；L | 2.99；2022-11-02 02:41 | 0.70；2022-11-02 10:05 | D：前次直接原表相符 | [Table 3.6.4, Shek Pik](https://www.hko.gov.hk/en/publica/tc/tc2022/table364.html) | Shek Pik行未标不完整 |
| E015 2023-07-17 | Typhoon Talim | R11 | 73.0；L | 3.01；2023-07-17 08:20 | 0.63；2023-07-17 08:20 | D：前次直接原表相符 | [Table 3.1.4, Shek Pik](https://www.hko.gov.hk/en/publica/tc/tc2023/table314.html) | Shek Pik行未标不完整 |
| E016 2023-09-01 | Super Typhoon Saola | R11 | 105.0；L | 3.07；2023-09-01 10:09 | 0.72；2023-09-02 04:40 | D：前次直接原表相符 | [Table 3.3.5, Shek Pik](https://www.hko.gov.hk/en/publica/tc/tc2023/table335.html) | Shek Pik行未标不完整；两项峰值跨日 |
| E017 2023-10-08 | Severe Typhoon Koinu | HKA | 351.9；L | 2.65；2023-10-06 02:04 | 0.58；2023-10-06 14:50 | D：前次直接原表相符 | [Table 3.5.4, Shek Pik](https://www.hko.gov.hk/en/publica/tc/tc2023/table354.html) | Shek Pik行未标不完整；均比事件锚点早两天 |
| E018 2024-09-05 | Super Typhoon Yagi | R11 | 80.0；L | 2.52；2024-09-05 10:42 | 0.57；2024-09-05 01:10 | D+：完整来源相符 | [Table 3.3.4, Yagi, Shek Pik](https://www.hko.gov.hk/en/publica/tc/tc2024/table334.html)；[本次快照](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/sources/E018_replacement.html) | No table-specific quality footnote or incomplete-data marker is present in the complete HTML table. |
| E019 2024-11-14 | Typhoon Toraji | R11 | 22.0；L | 2.64；2024-11-13 20:19 | 0.40；2024-11-13 20:19 | D+：完整来源相符 | [Table 3.6.4, Toraji, Shek Pik](https://www.hko.gov.hk/en/publica/tc/tc2024/table364.html)；[本次快照](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/sources/E019_table364.html) | No table-specific quality footnote or incomplete-data marker is present in the complete HTML table. |
| E020 2024-11-18 | Super Typhoon Man-yi | R11 | 77.0；L | 3.37；2024-11-18 23:09 | 0.66；2024-11-19 06:22 | D+J：共同驱动限定 | [Table 3.7.3, Man-yi, Shek Pik and joint-effect note](https://www.hko.gov.hk/en/publica/tc/tc2024/table373.html)；[本次快照](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/sources/E020_table373.html) | * The sea level rise (above astronomical tide) was due to the combined effect of the northeast monsoon and Man-yi. |
| E021 2025-07-20 | Typhoon Wipha | R11 | 138.5；L | 2.66；2025-07-20 05:29 | 1.10；2025-07-20 11:56 | D+：完整来源相符 | [July 2025 Monthly Weather Summary, Table 2.3.5, Wipha](https://www.hko.gov.hk/en/publica/mws/files/mws202507.pdf#page=45)；[本次快照](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/sources/HKO_MWS202507.pdf) | Complete page visually checked; Shek Pik has no bracketed or incomplete-data marker. No tide-table-specific quality note is present. |
| E022 2025-09-08 | Severe Tropical Storm Tapah | R11 | 121.5；L | 2.93；2025-09-08 07:33 | 0.62；2025-09-08 07:33 | D+：完整来源相符 | [September 2025 Monthly Weather Summary, Table 2.2.4, Tapah](https://www.hko.gov.hk/en/publica/mws/files/mws202509.pdf#page=32)；[本次快照](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/sources/HKO_MWS202509.pdf) | Complete page visually checked; Shek Pik has no bracketed or incomplete-data marker. The bracketed-data note is above this tide table and belongs to the preceding rainfall table. |
| E023 2025-09-24 | Super Typhoon Ragasa | R11 | 238.5；L | 3.60；2025-09-24 10:46 | 1.55；2025-09-24 10:46 | D+：完整来源相符 | [September 2025 Monthly Weather Summary, Table 2.2.5, Ragasa](https://www.hko.gov.hk/en/publica/mws/files/mws202509.pdf#page=71)；[本次快照](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/sources/HKO_MWS202509.pdf) | Complete page visually checked; Shek Pik has no bracketed or incomplete-data marker. The bracketed-data note is above this tide table and belongs to the preceding rainfall table. Waglan Island is explicitly unavailable; this does not apply to Shek Pik. |

## E020物理定义和影响范围

官方Table 3.7.3将S列标为maximum sea level rise，脚注为东北季风与Man-yi共同作用造成的天文潮以上增水。主稿§3.2/§4.2/§4.3、Table 3、Appendix A（Man-yi*）及event_metadata.csv均保留这一限定，旧列名maximum_storm_surge_m为数值兼容继续使用。W=3.37 mCD、S=0.66 m均不变，没有从共同增水中减去任何推测季风分量。S在当前分析中是各官方表报告的天文潮以上事件极值，不宣称23条有统一的纯台风因果分解。语义/注释遗漏CI-02关闭；跨事件可比性和物理外推仍受限制。

## 入选母体与排除记录

| 阶段/对象 | 可确认事实 | 不能确认的部分 | 状态 |
| --- | --- | --- | --- |
| 拟研究目标总体 | 稿件现在只主张selected inventory的条件分析 | 没有操作定义能决定所有“应被考虑”的香港台风、大澳洪水或阈值超限日 | OPEN：总体与抽样框未闭合 |
| 原始候选登记 | 当前文件提供E001–E023 | 候选事件总数、逐候选纳入/排除原因、未入选事件的缺测情况、筛选日期及责任人均未找到 | OPEN：原始排除数未知，不能写0 |
| 冻结输入清洗 | 23入、23留，唯一非空ID，三列有限；不插补、无重复向量 | 这是既选23条进入清洗后的结果，无法推断初筛未排除任何事件 | PASS_LOCAL，范围受限 |
| 清洗规则 | fallback.yaml配置missing_strategy=drop、duplicate_event_id=error | 没有证据证明历史初筛也按同一规则或统一风球阈值进行 | 规则可复查，初筛历史UNVERIFIED |
| 年份构成 | 2017:5，2018:1，2019:1，2020:2，2021:2，2022–2025各3；共9年 | 未入选年份内事件不在台账，不能据计数推导年发生率 | 描述已核，代表性未核 |
| 雨站组合 | 19 R11、3 HKA（E004/E007/E017）、1 R12（E013） | 优先站、替代站优先级及触发标准没有独立规程或当时选择记录 | 数量已核，替代规则OPEN |
| 事件锚点/窗口 | 每条元数据窗口均为锚点±2日，窗口可重现 | 锚点是最近接近、最高信号、登陆或其他日期未明确；相邻窗口重叠 | 操作复算通过，选择依据OPEN |
| 历史备份线索 | README声称有../climate_Devin_Archive/20261104_cleanup/ | 本次再次确认该路径不存在；已查项目树、相邻目录名称、Git标记及实际存在ZIP，仍未找到历史规程；未穷尽未知作者存储 | NOT_FOUND_AT_RECORDED_PATH |

### 四次非R11选择的可见线索

直接检查相同窗口的R11留存RF格发现下列缺测/标记。这为选择其他站提供可能解释，但没有原始规则，不能把事后观察当作当时决策记录。尤其不能仅因窗口有#便断言全部日量作废；#的具体质量语义及允许替代条件还应对照原站资料说明。

| 事件 | 已选站 | 同窗口R11原始5格 | 本次可作/不可作的判断 |
| --- | --- | --- | --- |
| E004 | Hong Kong International Airport (HKA) | 0.0 / 3.0 / 104.0# / 31.5 / 0.0 | 有缺测或质量标记线索；原始替代触发及站点优先级仍UNVERIFIED |
| E007 | Hong Kong International Airport (HKA) | 0.0 / 1.5# / *** / *** / *** | 有缺测或质量标记线索；原始替代触发及站点优先级仍UNVERIFIED |
| E013 | Discovery Bay (R12) | 0.0# / 7.0# / 64.5 / 0.0 / 0.0 | 有缺测或质量标记线索；原始替代触发及站点优先级仍UNVERIFIED |
| E017 | Hong Kong International Airport (HKA) | *** / *** / *** / *** / *** | 有缺测或质量标记线索；原始替代触发及站点优先级仍UNVERIFIED |

上述检查保存在 [雨站替代线索](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/evidence_consistency_20261104/station_substitution_evidence.json)。`***`按缺测处理，不能补为0；本次实际选用的23个窗口共115格均能解析为数值，未见#或*后缀，但这不消除跨站可比性问题。

## 情景构建可追溯性

冻结输入→Min-Max→ddof=0的CRITIC→一维K-means的本次数值复算得到权重(0.43408132518112047, 0.3352294655633418, 0.23068920925553776)，9/9/5，中心(0.16972654593445516, 0.3258382375944078, 0.6445434818998124)，阈值(0.24778239176443145, 0.48519085974711007)，与修订稿Table 4、§5.1相符。这只确认给定向量的计算，不会认证这些向量的选取或现场代表性。

23事件和9年份的重采样不是扩充出的独立观测。9/23、9/23、5/23只描述既选事件内条件频率，不能作为每年发生概率、重现期或未来气候频率。海平面和增水来自Shek Pik代理站，未通过水动力模型转为大澳洪水深度；人群/资产暴露和干预效益也未由三指标自动校准。

## 项目历史实际检索及未完成原因

当前目录和父目录不构成Git工作树，项目树未发现.git标记，故无法读取提交或分支历史。README和整理记录所指的climate_Devin_Archive/20261104_cleanup/before_cleanup.tar.gz现不存在。实际存在的S11.zip只有普查CSV，Solver_Logs.zip为5,671条求解日志，Run_Sources.zip的6个成员是模型/运行源及工作簿；未含事件最初筛选登记。迁移记录将当前event_metadata.csv追溯至旧experiments/20261103_scenario_stability/inputs路径，证明文件迁移而非最初选择过程。原始Word、保留区域文稿、现存配置和分析方案也未提供完整候选/排除/锚点/站点替代登记。四条R11缺测或标记仅作为线索保留，不改写成当时的决策规程。E019峰值早于台账日、E007和E017的日期差也原样保留，不据此猜定锚点。

[历史检索路径、归档成员和实际命中记录](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/history_search.json)。CI-01保持OPEN，需要作者提供真实历史证据。

## 后续改动的重算门槛

任何事件数值、站点、初筛集合、锚点/窗口或情景输入若改变，必须记录新旧输入与哈希、重算Min-Max、CRITIC、分类/阈值/频率和重采样，并重算全部受影响的优化、EV/EEV/WS、VSS/EVPI、并列策略、敏感性、消融和图表。此次仅补来源与注释，不触发新数值结果；不能以改正文代替重算。
