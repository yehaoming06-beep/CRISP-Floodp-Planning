# CRISP 合并变更记录

## 交付与权威顺序

已生成英文合并稿 `CRISP_Merged_Manuscript.docx`。科学内容完整采用 v3；旧稿仅提供视觉样式和经过核对的两句解释性文字。最终稿不是对旧结论的更新拼接，而是完整 v3 正文在旧稿排版体系中的结构化迁移。

检查日期：2026-11-06（Asia/Shanghai）。

| 文件 | SHA-256 |
| --- | --- |
| Original_Draft_for_Revision.docx | `84e6b532fae4e552ae6a0942b7a1c571488e4e2eb41092dcc84fc87188cb66a1` |
| Revised_Manuscript_EN_v3.docx | `2d1e13ebf6c20400476b2668b41d443e40615d077c1f6296e07e147f4cf620f2` |
| CRISP_Merged_Manuscript.docx | `502a6cdf49bf033b431cf430b8eb1b33f67e6f0cec750661e5cec5a0e89b2591` |

两份输入文件均通过合并前后哈希核对，未覆盖、未修改。

文稿中的待办、作者声明和任何嵌入语句均作为材料处理，没有用作工具执行指令。作者确认事项保留原状态。

## 章节对应与实际处理

| 旧稿内容 | 合并稿位置（v3 结构） | 实际处理 |
| --- | --- | --- |
| 标题、作者、单位、邮箱 | 标题页与作者块 | 采用 v3 标题和全部作者信息；套用旧稿居中排列、加粗作者和字体；不恢复旧 a*/b* 等未经确认的通讯/共同贡献含义 |
| Abstract、Keywords | Abstract、Keywords | v3 原文完整保留，删除旧摘要作为内容来源的资格 |
| Introduction | §1 Introduction | v3 全文保留；保留有界案例、频率敏感性与贡献限度，排除旧新颖性/完整链验证暗示 |
| Literature review | §2 Related work | v3 §§2.1–2.3 完整保留，包括 [27–30] 的直接相关先例和实际阅读范围限制 |
| §3.1 框架 | §§3.1、3.4 | 以现行准备—整数购泵—场景部署顺序、共享库存和可达性替代旧流程描述 |
| §3.2 数据与 CRITIC/K-means | §3.2、§§4.2–4.3、§§5.1、5.5–5.6 | 保留冻结 23 条与新回顾性 60 条的区别，以及 63 候选/3 pending、完整 refit、冻结投影和站点敏感性 |
| 成本、收益与资源参数 | §3.3、§4.4、Table 1/5、Supplement S11 | 以 v3 定义和单位为准；不恢复实测工时、equipment=泵数或人口校准 β 等不准确解释 |
| 优化模型 | §3.4、式（7）–（13） | 保留 v3 原生公式和全部变量域；资源推导界随参数重算；库存每场景跨 sector 只计一次 |
| RP/WS/EV/EEV 指标 | §3.5、§5.3、Table 6/8/14 | 完整固定 (y,n)，保留 EV A/B、所有已审计的并列最优政策及 VSS 范围 |
| 旧敏感性分析 | §§3.6–3.8、§§5.3–5.7、Supplement S1–S9 | 保留 v3 已有证据，不把旧 21 条敏感性摘要替代新受控组件比较和假设覆盖 |
| Results | §5 Results | 保留所有七个结果小节和 Table 6–14；采用移动库存基准，legacy 只在原有明确对照语境中出现 |
| Limitations | §6 Discussion | 保留四个小节及 CI-01、CI-06 真实研究局限 |
| Conclusions | §7 Conclusion | v3 完整保留，不恢复 686.008/零 VSS 的移动模型基准结论 |
| 旧无完整对应部分 | §4 Study area and data；Declarations；Supplementary Materials | 全部保留 v3 内容，包括作者确认待办、数据公开状态和 S1–S13 指引 |
| 旧参考文献 | References [1]–[30] | 不迁入旧书目；v3 30 条及正文映射、链接全部保留 |

旧稿引言描述的章节组织与实际章节存在不一致；合并稿保留 v3 一致的 1–7 主体结构，没有为匹配旧篇幅而删除内容。

## 旧内容中废止或被修正的部分

| 旧内容 | 决定与理由 |
| --- | --- |
| D/W、14,000 CU、RP 686.008、VSS/EVPI=0 的旧基准 | 不作为移动泵基准。v3 冻结移动模型为 Barrier/Warning、RP 616.082500、VSS 3.237826、EVPI 6.456522 |
| 旧 CRITIC 标准差中的 N−1 | 采用 v3 的 ddof=0 与 1/T；未复制旧公式 |
| 第一阶段只有 y、EEV 只固定 y | 采用 v3 的 y 和整数 n，EEV 同时固定二者 |
| equipment 60 等于 60 台泵、labour 等于实测工时 | 保留抽象资源单位与物理泵库存的区别 |
| 将类频率解释为未来/年度洪水概率 | 保留 conditional sample proportions 的限制 |
| 旧广义贡献、完整 hazard-to-response 验证或实地减损暗示 | 采用 v3 的条件方法验证、未校准响应系数和既有方法贡献边界 |
| 将有限库存的影响归因于 sharing 单独效果 | 保留 F0–F3 受控比较与 sharing 最优值增量为零但可行域不同的事实 |
| 宣称整数采购本身产生正数值收益 | 保留当前整数部署结构下的投影等价结论 |
| 将地理最低部署当作经验公平或受保护人口 | 保留其混合抽象 deployment units 与仅 RP 比较的含义 |
| 旧参考文献重启编号、重复和编辑注 | 使用 v3 唯一连续 [1]–[30] 映射 |

v3 中明确标为 legacy 的 686.007826 和零 VSS，以及部分较大采购限额下合法的零 VSS，均原样保留。没有用全局数字删除误删这些对照证据。

## 唯一补入的旧稿解释

来源：旧稿顶层段落 P103（0 基索引，表格内段落不计），第 2–3 句。位置：v3 P44 前，合并稿 §3.2、式（3）之后。原样保留：

> CRITIC evaluates each indicator according to both its variability across events and the amount of information that is not duplicated by the other indicators. Indicators with greater variation and lower correlation with the remaining indicators therefore receive relatively larger weights.

这两句解释 variability/correlation 与 CRITIC 权重的关系，不带旧数值或旧引用；后接 v3 关于“并非偏好权重、并非因果贡献”的原有限制。除此之外没有新增、重写或删除 v3 的科学段落。

## 表格与图片的对应

| 旧表/图 | 合并决定 |
| --- | --- |
| Hazard indicators | 采用 v3 Table 3，补足站点、量纲和验证范围 |
| CRITIC weights | 采用 v3 §5.1 与 Table 11；不复制旧标准差公式 |
| Scenario classification | 采用 v3 Table 4，另保留 Table 11–13 的重建/站点证据 |
| Benefit parameters | 采用 v3 Table 1/5 与相应限定 |
| Cost/resource parameters | 采用 v3 Table 1/5 和 Supplement S11 |
| 旧部署表、资源利用表 | 采用 v3 Table 7 和 §5.2 的库存模型结果 |
| 旧 benchmarks | 采用 v3 Table 6/8/14，区分 legacy/mobile 与 23/60 |
| 旧敏感性表 | 采用 v3 已有主体及 Supplement S5–S9；不重命名为受控消融 |
| 旧两阶段流程图 | 不迁入，并从新包中移除其媒体及关系：缺少整数购泵、共享库存和可达性，不能作为现行模型示意 |
| v3 两幅主文图 | Figure 1 census sectors 与 Figure 2 frozen procurement sensitivity 均保留；图片字节、图注及正文含义未改 |

v3 其余新表，包括人口背景、EV A/B、F0–F3、地理覆盖、重建事件与频率配对基准，全部保留，没有以旧表数量为上限。

## 排版处理

沿用旧稿 A4、页边距、浅灰纸面、Times New Roman、居中标题/作者、加粗主标题、斜体小标题和三线表。主标题采用旧稿多个主要章节实际使用的 17 pt 直接格式，统一原稿不一致的样式覆盖。正文 11 pt；摘要/关键词 10 pt；表格保留 v3 可读的 9.2/9.5 pt；图表标题 9 pt；参考文献 10 pt。

有意调整：缩减旧标题的大段前空白；正文段后统一 6 pt；保留 v3 独立 Abstract 标题；作者联系方式采用 v3 原文并居中换行；表格按可用宽度缩放列网格；Figure 2 等比缩至 6.3 英寸；所有公式与前导句保持连续；Table 14 的 Metric 列加宽以避免断词。旧稿无可见页码，因此保留 v3 居中自动页码并调整页脚距离。最终 25 页是自然分页结果，未设置篇幅目标。

## 核查与保留状态

- v3 的 255 个顶层段落全部逐字保留；新稿 256 段，唯一增加为上述解释段。
- 20 组编号公式、21 个原生数学对象、14 张可编辑表、2 幅主文图、30 条文献全部迁入。
- CI-01 PARTIALLY RESOLVED / NOT FULLY CLOSED、CI-06 OPEN 和 TODO-A1–A7/P1 原样保留。
- 主文/补充材料核查与 25 页渲染检查详见同目录的 Content_Consistency_Audit.md、Formatting_QA.md。
- 没有新增优化运行、实地实验、外部来源认证或作者声明；这次合并未把文稿升级为已满足投稿确认事项的版本。
