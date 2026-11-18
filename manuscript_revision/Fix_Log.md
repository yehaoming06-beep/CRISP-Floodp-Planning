# 审计问题修复记录

日期：2026-11-04（Asia/Shanghai）。本轮以 Citation_Audit.md、Critical_Issues.md、Event_Validation_Audit.md 为依据，修改英文 Markdown、Word、对应生成源和可证明有误的辅助记录。**8项 CI 中5项 CLOSED、1项 PARTIAL、2项 OPEN。** 关闭范围按具体问题界定，不表示整篇来源、历史筛选及实证效度全部通过。

## 已真正解决的问题

| CI | 修复内容 | 实际证据与关闭范围 |
| --- | --- | --- |
| CI-02 CLOSED | 主稿§3.2、§4.2/§4.3、Table 3、Appendix A（Man-yi*）、事件元数据及生成源保留“东北季风与Man-yi共同作用” | 重新取得完整官方Table 3.7.3，核对maximum sea level rise表头、Shek Pik行和共同驱动脚注。E020的W=3.37 mCD、S=0.66 m保持不变，不拆分或虚构纯台风分量。修正的是标签和解释遗漏，跨事件因果可比性仍受限制。 |
| CI-03 CLOSED | 补齐E004/E019/E021/E022/E023完整官方原表；为E018–E023增加Verified来源，保留原URL和失败历史 | E004/E019完整HTML；E021/E022/E023完整官方月报PDF。核对站点、W/S数值、两项峰值日期时间、单位/基准及可见质量脚注，均与冻结值相符。不是以索引片段或“链接存在”判通过。 |
| CI-04 CLOSED | 清空Original_Reference_Disposition.csv的O03 Cai→[6]错误映射，标记本稿未使用；O09继续映射Yang [6] | 原因是生成脚本在全体作者串中搜“Yang,”，误中Cai论文的合作者J. Yang。现按DOI认定作品；无DOI的Maqsood要求首作者签名及完整题名。33条旧条目中7个保留映射逐一对账；当前正文[6]仍为Yang，未改为Cai。 |
| CI-07 CLOSED | 辅助稳定性报告两处、build_report.py、plot_figures.py及captions.json的错误253改为231 | 23个有序点有22个内部空隙，非空连续三段切分为C(22,2)=231。报告和生成模板新增2026-11-04更正历史；253只在明确标识的历史错误记录中保留。SSE及实验结果不变。 |
| CI-08 CLOSED | 辅助说明和主稿§5.1限定为具体指标比较，不宣称K=2是真实类别数 | 全样本silhouette为K2 0.6613216548、K3 0.5377687423；Davies–Bouldin越小越好，K3 0.5011840382优于K2 0.5110220243。三类继续作为既定规划离散化。 |

五条恢复来源的完整定位如下。日期时间按原表记录，月报明确采用UTC+8；2017/2024 HTML表未写独立时区行，不另作时区转换。

| 事件 | Shek Pik W mCD / 峰值 | S m / 峰值 | 原表及有效定位 |
| --- | --- | --- | --- |
| E004 Pakhar | 2.38 / 2017-08-27 12:22 | 0.67 / 2017-08-27 06:52 | [官方Table 3.4.4](https://www.hko.gov.hk/en/publica/tc/tc2017/table344.html)，完整HTML |
| E019 Toraji | 2.64 / 2024-11-13 20:19 | 0.40 / 2024-11-13 20:19 | [官方Table 3.6.4](https://www.hko.gov.hk/en/publica/tc/tc2024/table364.html)，完整HTML；锚点仍为11月14日，未推断其历史定义 |
| E021 Wipha | 2.66 / 2025-07-20 05:29 | 1.10 / 2025-07-20 11:56 | [2025年7月月报](https://www.hko.gov.hk/en/publica/mws/files/mws202507.pdf#page=45)，Table 2.3.5，PDF第45页/印刷第42页 |
| E022 Tapah | 2.93 / 2025-09-08 07:33 | 0.62 / 2025-09-08 07:33 | [2025年9月月报](https://www.hko.gov.hk/en/publica/mws/files/mws202509.pdf#page=32)，Tapah Table 2.2.4，PDF第32页/印刷第29页 |
| E023 Ragasa | 3.60 / 2025-09-24 10:46 | 1.55 / 2025-09-24 10:46 | [2025年9月月报](https://www.hko.gov.hk/en/publica/mws/files/mws202509.pdf#page=71)，Table 2.2.5，PDF第71页/印刷第68页 |

五条Shek Pik行均未标不完整数据。九月两页的方括号质量说明属于前一张雨量表；Ragasa的无资料说明针对Waglan Island。未将其他站/其他表的质量脚注移用到Shek Pik，也未把没有标记解释为仪器无误差。

两份PDF初次整文件下载均中断，失败记录保留。随后完成161段HTTP 206续传，每段核对范围、长度和Last-Modified，组合后分别为17,550,025字节/87页、24,443,418字节/136页。三路页数一致且无解析修复警告，并实际核看表格原页，才关闭CI-03。完整文件、原页图像、提取文本、逐字段记录和SHA-256均位于 [修复证据目录](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104)。详见 [Event_Source_Updates.csv](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/Event_Source_Updates.csv) 和 [分段获取记录](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/range_download_log.json)。

## 仅通过限制性表述处理

**CI-05 PARTIAL。** 已取得Gabrel等的[作者版全文](https://optimization-online.org/wp-content/uploads/2012/07/3537.pdf)，版本为2012年7月、2013年5月修订。实际读取并核看§2.2 Static Robust Optimization（PDF/印刷第2页）及§2.3/§2.3.1（第4页）：前者讨论无后续补救的静态决策，后者综述多阶段及可调整两阶段问题。正文从宽泛技术断言缩窄为综述涉及的主题，并明确版本边界。2014出版商全文返回403，未核对作者版与最终版逐段一致性，因此保持PARTIAL，不能称最终出版版验证通过。[11]CRITIC原文公式逐式审读也未完成，未增添任何已完成宣称。

## 必须由作者补充的新证据

**CI-01 OPEN。** 已查项目树、原始Word及保留区域文稿、现存配置/分析方案、迁移登记、Git标记及三个实际存在的ZIP。项目没有Git工作树；README明确列出的清理备份路径当前不存在。迁移登记能证明现存事件文件来自旧路径，不能证明最初候选母体、排除、锚点或站点替代规则。未找到可关闭这些问题的当时记录。四条非R11事件的R11缺测或质量标记仍只作线索，未据此补造历史规程。

**CI-06 OPEN。** 没有新增现场运行、暴露、损失或效益数据；CU、效益、库存/预算/可达性等假设仍是条件性方法演示。求解器一致性和555配置不能替代实测校准，情景重采样也未传播到全部后端优化。

具体作者补证清单见 [Remaining_Blockers.md](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/Remaining_Blockers.md)。

## 一致性与影响范围

- 模型、主工作簿、配置、model_input.csv、23条事件数值、站点、日期/窗口和筛选集合不变；event_metadata.csv仅E020的data_quality_note追加注释。既有官方来源归档和结果文件未覆盖。
- CRITIC权重、9/9/5划分、阈值、条件频率、SSE、9,032条重采样、555配置、所有优化结果和七张主稿图像不变。本轮没有触发数值重算；这不是“重算已通过”的宣称。
- 主稿通过两轮有哈希前置条件的逐块补丁修改；第一轮保留218/231块，第二轮保留230/231块。最终与修正后的章节/模板重新组装结果一致。18组公式保持原样，Word保留19个原生公式对象、13张表、7张图。23页Word逐页检查并修整图注/附录分页。
- Markdown与Word逐段/逐单元格可见内容、超链接、20条参考文献及29个展开后的正文引用对账；原文献处置、当前引用上下文和三份审计已同步。具体检查结果见 [一致性验证](/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/audit/fixes_20261104/consistency_validation.json)。
- 原报告和原处置表完整保存于before目录；evidence_consistency_20261104是前次审计快照，其旧失败/错误状态没有伪装成当前结果。当前状态以三份更新报告及fixes_20261104内的current记录为准。Manuscript_Change_Log保留前一轮历史并追加本轮记录。
- 前次审计生成脚本的常规入口转发到当前生成器，避免重新生成旧错误结论；原脚本字节另存before。历史证据JSON未覆盖或改成通过。

后续若改变事件数值、站点、筛选/锚点/窗口规则或情景输入，须明确新旧输入及版本、重算全部受影响的归一化、CRITIC、分群/频率/稳定性、优化比较和图表；不得只改正文并继续沿用冻结结果。
