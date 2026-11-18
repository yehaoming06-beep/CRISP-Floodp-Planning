# CI-01 独立历史事件筛选验证报告

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Origin Mode: validate
- Origin Date: 2026-11-04（Asia/Shanghai）
- Verification Status: VERIFIED（限定范围见正文）
- Version Label: CI01-resolution-v1.1

## 结论

**CI-01：PARTIALLY RESOLVED，不能完全关闭。** 已从官方记录独立重建一个明确受限、可逐年核对的候选母体，提出并执行新规程，完成逐事件对账、情景复算与隔离后端敏感性。原作者的最初候选/排除记录、当时锚点和选站决策仍未恢复；新建规则不等于历史规则。

最终是**62组本地警告涉及63个独立气旋身份，60条可作事件R/W/S数值分析，3条待核，0条实体排除**。60条保留旧23全部事件，另加37条。Yagi在60条内，但增水峰值日期仍有限定。未决和缺测不能从台账消失，也不能作为“没有事件”的证据。

## 六项交付

| 文件 | 内容/行数 |
| --- | --- |
| [Candidate_Event_Inventory.csv](Candidate_Event_Inventory.csv) | 63个候选；非由旧23反推 |
| [Screening_Protocol.md](Screening_Protocol.md) | 冻结的新规程v1.0；执行时结合下述QC解释v1.1 |
| [Inclusion_Exclusion_Audit.csv](Inclusion_Exclusion_Audit.csv) | 63行；60 INCLUDE、3 PENDING_DATA、0实体排除 |
| [Original23_vs_Reconstructed.csv](Original23_vs_Reconstructed.csv) | 63行完整外联对账：23原事件+40额外候选 |
| [Scenario_Impact_Assessment.md](Scenario_Impact_Assessment.md) | CRITIC/分类/条件频率、大澳空间敏感性与完整后端重算边界 |
| [CI01_Resolution_Report.md](CI01_Resolution_Report.md) | 本报告；已完成与未关闭范围 |

执行版本是主规程v1.0加[来源冲突QC解释v1.1](Source_Conflict_Adjudication.md)，空间补充另见[TaiO规程](TaiO_Spatial_Sensitivity_Addendum.md)。v1.1是在首轮试算后发现新的正面证据冲突时公开形成，未伪装为事前盲法注册；此前61条数据、代码和555组结果全部保留。

## 1. 当前实际使用的23条与可确认操作

读取并快照保存event_metadata.csv、model_input.csv、27个年度雨量归档、现有HKO来源恢复档、Event_Validation_Audit.md、实际fallback配置、分析代码、工作簿和结果。没有找到新的同时期历史初筛登记，也未把旧审计意见当作已验证的候选规则。

| ID | 旧台账锚点 | 实际事件名 | 实际雨站 |
| --- | --- | --- | --- |
| E001 | 2017-06-12 | Severe Tropical Storm Merbok | R11 |
| E002 | 2017-07-23 | Tropical Storm Roke | R11 |
| E003 | 2017-08-23 | Super Typhoon Hato | R11 |
| E004 | 2017-08-27 | Severe Tropical Storm Pakhar | HKA |
| E005 | 2017-10-15 | Severe Typhoon Khanun | R11 |
| E006 | 2018-09-16 | Super Typhoon Mangkhut | R11 |
| E007 | 2019-07-31 | Tropical Storm Wipha | HKA |
| E008 | 2020-08-19 | Typhoon Higos | R11 |
| E009 | 2020-10-13 | Tropical Storm Nangka | R11 |
| E010 | 2021-10-09 | Tropical Storm Lionrock | R11 |
| E011 | 2021-10-13 | Typhoon Kompasu | R11 |
| E012 | 2022-07-02 | Typhoon Chaba | R11 |
| E013 | 2022-08-25 | Typhoon Ma-on | R12 |
| E014 | 2022-11-02 | Severe Tropical Storm Nalgae | R11 |
| E015 | 2023-07-17 | Typhoon Talim | R11 |
| E016 | 2023-09-01 | Super Typhoon Saola | R11 |
| E017 | 2023-10-08 | Severe Typhoon Koinu | HKA |
| E018 | 2024-09-05 | Super Typhoon Yagi | R11 |
| E019 | 2024-11-14 | Typhoon Toraji | R11 |
| E020 | 2024-11-18 | Super Typhoon Man-yi | R11 |
| E021 | 2025-07-20 | Typhoon Wipha | R11 |
| E022 | 2025-09-08 | Severe Tropical Storm Tapah | R11 |
| E023 | 2025-09-24 | Super Typhoon Ragasa | R11 |

| 操作项目 | 可确认事实 | 仍不能推定 |
| --- | --- | --- |
| 样本和输入 | 23个唯一非空ID；R/W/S有限；与metadata一致；23入23留 | 这只是既选23条的清洗，不能推出历史候选或排除数 |
| 降雨 | 旧日期±2日；日RF五日最大、当日和累计均可复算 | 旧锚点统一取最近接近/最高信号/登陆日的历史规则未恢复 |
| 站点 | 19 R11、3 HKA(E004/E007/E017)、1 R12(E013) | 四次替代的原始优先级和触发记录未恢复 |
| 潮位/增水 | 均用Shek Pik/SPW事件摘要；23对数值复算相符；Man-yi共同驱动限定保留 | 不是大澳洪深、仪器校准或纯台风因果增水 |
| 清洗配置 | missing_strategy=drop、duplicate_event_id=error、CRITIC ddof0、K3/seed42/n_init50 | 不证明原始初筛按同一缺测规则；本次待核候选没有交给drop静默删除 |
| 旧样本构成 | 包含官方母体中全部22个最高信号≥8的气旋，另加一号Man-yi | 这是事后描述，不能认定恢复了“8号阈值+例外”的历史规则 |

四次非R11选择的新规程兼容性见[逐站五格](evidence/Original_Four_Station_Choices.csv)。本次官方页面解释#为不完整、***为不可得，但“一天有#即整窗转下一站”仍是本次保守QC选择，未声称HKO或原作者采用过该门槛。

## 2. 独立候选母体及完整性边界

定义：2017-01-01至2025-12-31香港时间，任何时刻曾被HKO发出本地热带气旋警告信号的独立气旋。含1号、3号、8/9/10号与未命名低压。同一气旋多次经过合为同一身份，2021年共同警告下的两个低压分列身份但不复制观测。

候选从[官方本地警告数据库](https://www.hko.gov.hk/en/wxinfo/climat/warndb/warndb1.shtml)实际加载的[tc.dat](https://www.hko.gov.hk/dps/wxinfo/climat/warndb/tc.dat)构造；与2017—2024逐年Table4.3及2025年1—12月完整官方月报网页逐信号段交叉核对。九年203段完全一致。2017—2024的航运警告表、盆地清单、章节与原始索引亦保留，未把航运警告直接当本地警告。2025年度常见URL返回404，不据此漏掉全年事件；其37段信号由全年月报补齐核对。

| 年 | 本地警告组 | 气旋身份 | 旧23条数 | 最终数值分析 | 待核 |
| --- | --- | --- | --- | --- | --- |
| 2017 | 7 | 7 | 5 | 6 | 1 |
| 2018 | 6 | 6 | 1 | 6 | 0 |
| 2019 | 5 | 5 | 1 | 5 | 0 |
| 2020 | 5 | 5 | 2 | 5 | 0 |
| 2021 | 7 | 8 | 2 | 6 | 2 |
| 2022 | 6 | 6 | 3 | 6 | 0 |
| 2023 | 5 | 5 | 3 | 5 | 0 |
| 2024 | 7 | 7 | 3 | 7 | 0 |
| 2025 | 14 | 14 | 3 | 14 | 0 |

这一完整性只适用于**本地警告气旋框**。香港行政警告不证明每条均导致大澳水浸；没有本地警告的远距离气旋、残余环流或季风关联降雨，以及无气旋洪灾未形成完整母体。不能宣称已穷尽所有“大澳相关气旋影响/洪灾”。HKO对2021两个低压共用警告的说明保留在[官方报告§3.2](https://www.hko.gov.hk/en/publica/tc/tc2021/section3_2rpt.html)快照；Son-Tinh二次经过按[2018报告§3.2](https://www.hko.gov.hk/en/publica/tc/tc2018/section3_2rpt.html)确认，不把数据库No name第二次经过误加为另一气旋。

## 3. 新规程执行、对账和未决

新锚点是最高本地信号首次发出的香港日期；雨窗±2日；雨站固定R11→HKA→R12，每站五日全部未标记才可用，整窗选站，不逐日拼接或按大小选站。没有为得到23而设置风球、雨量、潮位或灾损阈值。

| 原ID | 旧锚点 | 新锚点 | R/W/S变化 |
| --- | --- | --- | --- |
| E011 | 2021-10-13 | 2021-10-12 | 全为0 |
| E012 | 2022-07-02 | 2022-07-01 | 全为0 |
| E013 | 2022-08-25 | 2022-08-24 | 全为0 |
| E019 | 2024-11-14 | 2024-11-13 | 全为0 |
| E022 | 2025-09-08 | 2025-09-07 | 全为0 |

其余18条锚点相同。全部23条的已选站和R/W/S数值均不变，未据此宣布找回历史规则。27份官方RF响应本次重新下载，与原归档**27/27逐字节相同**。最终60条雨站为54 R11、4 HKA、2 R12。

| 待核身份/限定 | 证据 | 处置 |
| --- | --- | --- |
| TC2017_06 未命名低压 | 年报/月报W=2.23,S=0.26；官方数据库W=2.48,S=0.29 | 候选保留；PENDING_SOURCE_CONFLICT，不作实体排除 |
| TC2021_02_E、TC2021_02_W | 两个独立低压共用警告及R/W/S摘要，不能逐气旋分离 | 候选各一行；PENDING_COMPOUND_ATTRIBUTION，不复制为两个样本 |
| TC2024_03 / E018 Yagi | W/S数值一致，S日期5Sep与6Sep冲突 | 允许事件极值数值分析，峰值时间UNRESOLVED；另做避开全部冲突的59条敏感性 |

2017—2024共有48张完整官方潮表、2025有14个完整月报目标原表。8份相关完整月报PDF通过页数与SHA预检，14个2025目标页和2个冲突目标页均核看。官方增水数据库是额外官方证据，不是独立仪器复测；62个警告组中60组的W/S及两项峰值时刻相符，另有上述两组冲突。未用来源多数表决、同值或质量标记N推断仪器准确。

Man-yi、Fengshen、Fung-wong的天文潮以上水位上升均保留与东北季风共同驱动的限定。W/S各自取事件极值，不要求同时，S不由W减去另一时刻天文潮峰值，更不是地面洪深。

## 4. 对分析及优化的影响

完整结果在[影响评估](Scenario_Impact_Assessment.md)。旧23重建后输入不变；扩展到最终60条后权重为0.487217 / 0.286080 / 0.226703，计数35/19/6，条件频率58.33%/31.67%/10.00%。旧23中的6条标签因全重拟合而变化。大澳与石壁同一59身份比较，有10条标签变化，说明站点空间选择也是实质影响源。

已完成最终60频率下的555组既有配置及一次完整重复，555行摘要逐字节一致；另完成10案例EV同值政策穷举。只更新条件频率，其他示例资源/效益系数固定。没有已验证的R/W/S→资源/效益映射，因此未宣称完成实证全链不确定性传播。未决全63候选的最终类别与频率仍不可识别，不能用60条结果冒充全母体最终模型。

## 5. CI-01处理判定

| 事项 | 判定 | 关闭范围/剩余条件 |
| --- | --- | --- |
| 现有23条实际输入及可见操作 | VERIFIED_LOCAL | 数值/窗口/站点构成可复现；非原始初筛证明 |
| 限定本地警告候选框 | RECONSTRUCTED_COMPLETE_WITHIN_DEFINED_FRAME | 九年203段双清单核对；63身份含共同警告的两组件 |
| 更广义大澳相关气旋/洪灾母体 | UNRESOLVED | 无本地信号、残余环流与复合影响范围未闭合 |
| 本次新规程与逐候选判定 | EXECUTED_WITH_PENDING_ITEMS | 60数值分析、3待核、Yagi峰值日期限定；0实体排除 |
| 原始历史筛选、锚点、四次选站决策 | OPEN | 仍需作者同时期候选/排除台账、规则版本及决策记录；新规程不代替 |
| 官方数值/日期冲突和共同摘要归属 | OPEN | 需官方更正或可比连续实测/天文潮，及明确分析单位 |
| 条件情景与后端计算复现 | VERIFIED_CONDITIONAL | 555组概率敏感性完整执行并重复；效益/成本实证映射与长期风险模型未完成 |
| CI-01总体 | PARTIALLY RESOLVED / NOT FULLY CLOSED | 有可复现的独立重建，不能认证原23初筛无偏或历史程序 |

## 6. 保留与复现

所有写入限定在本独立目录。已保存原始输入快照、官方响应（包括404/失败历史）、URL、HTTP头、UTC下载时间或明确时间未知标记、文件SHA、分段下载记录、PDF预检/原页图像、逐站五格、抽样索引及全部求解日志。977个冻结文件和对应快照复核未变，原Event_Validation_Audit.md与论文未覆盖。

离线重建/情景/空间的102个输出逐字节重现；NumPy CRITIC和独立动态规划SSE核验通过。详见[最终验证JSON](logs/Final_Verification.json)、[官方下载台账](Official_Source_Manifest.csv)、[PDF原件台账](PDF_Source_Manifest.csv)和[复现说明](README.md)。完整性和计算通过不等于观测无误、筛选无偏或CI-01完全关闭。
