# CRISP 内容一致性审计

## 结论和核查边界

**科学内容迁移与内部一致性核查：通过。** 合并稿保留 v3 全部正文、公式、表格、图片、参考文献和限定语；唯一科学解释增补是变更记录中列明的两句旧稿 CRITIC 说明。没有恢复旧模型基准或删除新研究证据。

本审计验证指定文稿之间的完整迁移，并核对现有 Supplementary Materials 和部分可直接复算的算术。没有重跑优化、重新核实 30 条外部来源，也没有解决经验校准、历史来源或作者确认问题。“通过”不等同于研究局限已关闭或可直接投稿。

检查日期：2026-11-06（Asia/Shanghai）。

| 文件 | SHA-256 |
| --- | --- |
| Original_Draft_for_Revision.docx | `84e6b532fae4e552ae6a0942b7a1c571488e4e2eb41092dcc84fc87188cb66a1` |
| Revised_Manuscript_EN_v3.docx | `2d1e13ebf6c20400476b2668b41d443e40615d077c1f6296e07e147f4cf620f2` |
| CRISP_Merged_Manuscript.docx | `502a6cdf49bf033b431cf430b8eb1b33f67e6f0cec750661e5cec5a0e89b2591` |

两份输入文件均通过合并前后哈希核对，未覆盖、未修改。

补充材料 `Supplementary_Methods_and_Results.md` 的 SHA-256：`b5913966d2061b1e681ee72ffb553fc348a4088b9fedc8730c3d11abf7113641`。该文件未改写。

## 逐项迁移证据

| 核查项 | v3 | 最终稿 | 核查结果 |
| --- | --- | --- | --- |
| 顶层正文段落 | 255 | 256 | 原 255 段逐字、同序保留，仅增加 1 段 2 句解释 |
| 全体有序正文元素 | 段落、表格、公式、图注及图像段 | 同序迁入 | 排除唯一已登记增补段后，各元素类型和全部文本节点序列相同 |
| 主体章节 | Abstract；§§1–7 | 全部保留 | Introduction、Related work、Methodology、Study area/data、Results、Discussion、Conclusion 完整 |
| 其他重要部分 | Declarations、References、Supplementary Materials | 全部保留 | 待确认事项与补充材料指引未删 |
| 编号公式组 | (1)–(20) | (1)–(20) | 连续、无旧公式替换 |
| 原生数学对象 | 21 | 21 | 展开命名空间后的元素/属性/文本/子节点/尾文本递归相同 |
| 可编辑表格 | 14 | 14 | 逐表行列与每个单元格文本相同 |
| 正文使用的图像 | 2 | 2 | 媒体字节与 SHA-256 相同；只调整显示尺寸 |
| 图表标题 | Table 1–14、Figure 1–2 | 同一序列 | 逐字相同，正文对应未改 |
| 参考文献 | [1]–[30] | [1]–[30] | 连续唯一、全部正文有引用，条目文本相同 |
| 正文数字引文 | v3 序列 | 同一序列 | 无超范围或丢失映射 |
| 超链接 | 33 | 33 | 显示文本、目标、类型和外部模式同序相同 |
| 内部包关系 | 有效 | 有效 | 无缺失目标；6 个页眉/页脚引用类型正确 |

公式的原始 C14N 字节会受到继承的旧稿命名空间声明影响；已经用展开名称的递归结构比较排除仅由外层命名空间导致的差异。公式内容本身未重建、未栅格化。

## 全部公式清单

| 编号 | 数学内容 | 最终页 | 状态 |
| --- | --- | --- | --- |
| 1 | Min–max normalization | 5 | 原生对象与 v3 相同 |
| 2 | Population SD、CRITIC information/weights | 5 | 采用 ddof=0；未恢复旧 N−1 |
| 3 | Composite score | 5 | 相同 |
| 4 | K-means objective | 5 | 相同 |
| 5 | Thresholds、conditional frequencies、class means | 5 | 相同 |
| 6 | Deployment score | 7 | 相同 |
| 7 | RP and scenario recourse | 7 | 相同 |
| 8 | Readiness CU and procurement HKD budgets | 7 | 相同 |
| 9 | Scenario operating/resource constraints | 7 | 相同 |
| 10 | Readiness/deployment linking | 7 | 相同 |
| 11 | Resource-derived valid bound | 7 | 相同 |
| 12 | Shared-stock and access constraints | 7 | 相同 |
| 13 | Binary/integer domains | 7 | 相同 |
| 14 | WS | 8 | 相同 |
| 15 | EV convention A | 8 | 相同 |
| 16 | EV convention B | 8 | 相同 |
| 17 | EEV with all first-stage variables fixed | 8 | 相同 |
| 18 | VSS、EVPI and objective ordering | 8 | 相同 |
| 19 | Min/max VSS over primary EV-optimal policy set | 8 | 两行、两个原生对象均保留，编号只在第 2 行 |
| 20 | Hypothetical minimum geographic deployment | 10 | 相同 |

## 全部主文表格清单

| 表号 | 内容 | 行×列（含表头） | 最终页 | 结果 |
| --- | --- | --- | --- | --- |
| 1 | Model notation and unit conventions | 21×3 | 6 | 单元格及结构相同 |
| 2 | Complete census units and 2021 population context | 4×5 | 10 | 单元格及结构相同 |
| 3 | Hazard indicators and source-verification scope | 4×4 | 12 | 单元格及结构相同 |
| 4 | Frozen three-scenario summary | 4×7 | 13 | 单元格及结构相同 |
| 5 | Illustrative readiness expenses and benefit component scores | 4×5 | 13 | 单元格及结构相同 |
| 6 | Baseline benchmarks | 3×7 | 15 | 单元格及结构相同 |
| 7 | Inventory-baseline RP deployment in Tai O1 | 5×6 | 15 | 单元格及结构相同 |
| 8 | Baseline EV convention comparison | 5×6 | 16 | 单元格及结构相同 |
| 9 | Controlled RP component comparison | 5×4 | 17 | 单元格及结构相同 |
| 10 | Hypothetical minimum geographic deployment | 5×4 | 17 | 单元格及结构相同 |
| 11 | Event-frame and preprocessing comparison | 5×5 | 18 | 单元格及结构相同 |
| 12 | Reconstructed 60-event class representatives | 4×7 | 18 | 单元格及结构相同 |
| 13 | Tai O versus Shek Pik on the same 59 identities | 3×5 | 19 | 单元格及结构相同 |
| 14 | Paired baseline comparisons changing only conditional scenario frequencies | 13×5 | 20 | 单元格及结构相同 |

图 1 在第 11 页：census-aligned Tai O sectors，四个完整 census units、2021 人口、排除区域和来源/版权限制完整。图 2 在第 16 页：只表示冻结 23 条、A convention 的采购敏感性；policy-range 阴影未被解释为置信区间，也没有新增 60-event/B 曲线。

## 关键科学区别和数值

| 项目 | 核对结果 |
| --- | --- |
| 共享移动库存 | 每个互斥场景跨两个 sector 的 pumping 总量 ≤ N0+n；不跨不同事件累加；一单位 Drainage 是一台同时分配的泵 |
| 整数采购与可达性 | n 为非负整数；A[j]=0 禁止该 sector pumping；access 是假设，非实测交通证据 |
| EEV | 同时固定 EV 返回的 y、n，然后只重优化原始场景部署 |
| EV A/B | A 平均已推导 bounds；B 先平均 primitive resources 再推导 bound；基准最优集合相同不代表两模型一般等价 |
| 并列最优政策 | 冻结 23-event mobile 有 2 个 EV optima；60-event mobile 有 4 个；完整范围保留 |
| 历史与回顾样本 | 旧 23 条为冻结计算参考；新行政警告框架 63 identities=60 analyzable+3 pending；不是全部 Tai O 洪水普查 |
| 分类语义 | 9/9/5→35/19/6；6 个旧标签改变；对同一 60 条的 frozen projection 是 43/12/5 |
| 两类 59 条分析 | 站点对照的共同 59 排除 Bebinca；严格日期冲突敏感性排除 Yagi，不是同一分析集 |
| 受控 F0–F3 | 区分有限库存、replicated/shared 会计方式和采购整数性；F1→F2 最优值相同而可行域不同；当前约束下 F2/F3 投影等价 |
| 地理覆盖 | k=1 代价 14.206739 / 13.680333 score units；混合部署单位不是人口/同质服务/经验公平；k=6 不可行，目标值未填 0 |
| 推断限度 | 频率替换未重新校准 hazard→response；RP 增长不是观测减损或实地政策改善 |

| Mobile benchmark（model-score units） | Frozen 23 | Reconstructed 60 |
| --- | --- | --- |
| RP | 616.082500 | 634.516667 |
| WS | 622.539022 | 639.741667 |
| Selected EV | 621.392391 | 601.907167 |
| Selected EEV | 612.844674 | 600.203083 |
| Selected VSS | 3.237826 | 34.313583 |
| EVPI | 6.456522 | 5.225000 |
| 所有已审计 EV optima 的 VSS 范围 | 3.237826–3.237826 | 8.019000–34.313583 |

两频率下 RP 仍为 Tai O1 的 Barrier/Warning、n=0；频率重加权的 RP 差为 +18.434167，原 first-stage policy 的 regret 为 0。60-event 返回的 EV 政策买 1 台泵，冻结频率返回政策买 2 台泵。legacy 686.007826/零 VSS 只保留 v3 原有明确标签与比较语境，未标成 mobile baseline。

单位检查：R 为所选五天窗口内最大日累计量，mm/day；W 为 mCD，S 为源报告 residual rise 的 m，W/S 不要求同时达峰，均不是陆地淹没深度。CU 与 HKD 不换算；equipment=60 是抽象资源容量，不是 60 台物理泵；labour 不是已校准 staff-hours；scores 不是货币福利或实际避免损失。

## 主文与补充材料

| 主文内容 | 对应补充部分 | 核查 |
| --- | --- | --- |
| 既有运行和独立计算范围 | S1、S1.1、S13.1 | 555 configurations、500 targeted solves（498 optimal+2 intentional infeasible）、936 independent calls 及 1.3074×10⁻¹¹ 数值差的报告范围一致 |
| EV A/B、有效 bounds、完整政策范围 | S2，Tables S1–S4 | 定义、23/60 最优政策数与 EEV/VSS 范围一致 |
| 受控组件与 access | S3，Tables S5–S7 | 两 capital panels、F0–F3 与共享库存可行域 witness 一致 |
| 假设覆盖 | S4，Tables S8–S9 | k=0/1/2/6、机会成本和不可行性一致；只报告 RP |
| 非主文敏感性与采购证据 | S5–S9 | 保留正文指引及 A-only 适用范围 |
| 冻结 23 条事件 | S10，Table S14 | E001–E023 完整，历史 anchors 与新规则差异未被抹平 |
| 响应资源与 bounds | S11，Table S15 | 输入定义与 D/B/W bounds 一致 |
| 候选框架与 pending | S12，Table S16 | 62 warning groups、63 identities、60 analyzable、3 pending 一致 |
| 外部材料实际阅读范围/开放问题 | S13.1–S13.3 | 与贡献边界和 CI 状态一致 |

现有 Supplement 包含 S1–S13、16 张表、5 个补充图声明和 4 个补充公式编号。主文 S1/S1.1/S2–S13/S13.1 等指向均存在。归档日志中的旧 61/new61/pending-two 标签已在补充材料说明为 superseded，未提升为最终样本。此次没有另建或改写 Supplement。

独立算术交叉核对基于已写出的输入：Table 7 的三个场景 score 重构为 661.815000、616.000000、533.912500，两种频率加权得到上述 RP；地理 k=1 机会成本、S11 全部 U、共享库存 witness 和 k=6 的 504>400 labour 证书均一致。这不是新实验或优化重跑。

## 必须保留的真实开放状态

- **CI-01 PARTIALLY RESOLVED / NOT FULLY CLOSED**：历史候选/排除清单、原始 anchors 和四个当时的 station-substitution 决策未恢复；TC2017_06 数值冲突与两个 2021 shared-summary identities 仍 pending；Yagi 仅在同意的 extrema 范围纳入，日期冲突保留。来源数值相符不等于仪器校准。
- **CI-06 OPEN**：R/W/S 到实际泵效能、资源、CU 成本或 benefit 的映射没有经验校准；可调用设备、local access、pump head/outlet/flow、人员/燃料/维修及 avoided losses 未获所需实测支持。
- **作者/投稿确认**：TODO-A1–A7、TODO-P1 全部保留，包括通讯/贡献/利益冲突/资助/伦理/公开归档等既有待确认状态。未凭旧作者星号、现有文件或排版工作编造声明。

可复核证据位于工作目录 `/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/merge_work`：final_independent_audit.json/md、source_audit_findings.md、independent_source_arithmetic.json、build_manifest.json、render_geometry.json。它们是内部检查材料，最终交付以四个指定文件为准。
