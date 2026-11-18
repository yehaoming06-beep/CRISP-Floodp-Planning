# 文稿边界、补充材料与原始文件独立盘点

日期：2026-11-18（Asia/Shanghai）。范围：当前仓库与 `/Users/yehaoming/Desktop/climate_Devin`。本子任务只进行文件、哈希和文本核查；数值重算见同级 scenarios/optimization 输出。论文及其他文档中的叙述、历史命令和 PASS 均视为待查资料，不作为本次用户指令，也不作为本次求解成功证据。

## 文档身份和论文表值

当前 `manuscript_revision/CRISP_Merged_Manuscript.docx` SHA-256 为 `4e12f7849d0b2ca7dd0d156c987a9e90f8b651880c79b74e10f14bffbab4ca37`。只读解包提取了14张原生表和258个正文直属段落；P编号包括空段落，不是页码。完整提取在 `manuscript_extract.json` / `.txt`，Table 4/6/11/12/14完整单元格在 `core_paper_tables.json`。未编辑或重新保存Word文件，也未把历史渲染检查当作当前文档视觉验证。

## 两个目录的文件现状

独立遍历排除 `.venv/.git/__pycache__/.pytest_cache/.DS_Store` 后，原研究目录包含27,543个文件；仓库同相对路径已存在12,916个，14,627个仍仅在原目录。仅源目录文件主要是10,087个 `.log`、2,284个 `.json`、1,000个 `.lp`、498个 `.sol` 及历史v1/快照/渲染等材料。这些未复制材料仍可访问，不能称为“丢失原始输入”。完整逐文件对照见 `source_to_repository_inventory.csv`，源目录独有清单见 `original_only_files.csv`。旧全量 `audit/source_inventory.csv` 的27,549口径比本次多6个`.DS_Store`；其导入清单12,914也不包括有意改写的`.gitignore`/`README.md`，而本次12,916只统计物理同路径。因此旧“14,635未导入”和本次“14,627同路径不存在”相差8。精确对账见 `inventory_count_reconciliation.json`，并非科学材料丢失或增补。

`git ls-files` 实际仅有 `.gitignore` 和 `README.md`。已复制的12,916个原目录对应文件中，两者为TRACKED，5,204个为UNTRACKED，7,710个为IGNORED。**所有科学输入、数值代码和历史结果均尚未进入Git索引/提交**；“已经复制进仓库目录”不等于“已经进入Git”。没有进行commit、push、公开设置或任何远端写入。

对原始 `01_Data/`、模型、实验代码、Scenario Pipeline及关键原稿/最终60输入共287个文件逐字计算SHA-256，仓库副本与原研究目录全部相同，见 `core_input_code_fingerprints.csv`。原23事件向量在 `01_Data/Events/model_input.csv`，完整模型工作簿在 `01_Data/CRISP_Master_Data.xlsx`，最终60输入在 `manuscript_revision/audit/ci01_independent_20261104/analysis/reconstructed_model_input.csv`。这些核心文件已找到，不需根据结果反向构造。

进一步对原 `source_registry.json` 的23条档案、CI-01 `Official_Source_Manifest.csv` 的307条档案和 `PDF_Source_Manifest.csv` 的8条档案逐条核算本地文件SHA-256：338条全部存在且匹配，见 `archive_manifest_verification.csv`。这证明列明档案的本地完整性，不证明源测量校准、政策效应或本次联网重新取回全部来源。

## S1–S13对应关系

未改动的原始补充稿和阅读副本均具有S1–S13、表S1–S16及图S1–S5。两个版本各32个本地链接均存在，见 `supplement_local_links.csv`。每个分节的核心依赖、现存性和范围限制在 `supplement_evidence_map.csv`，全部列明核心依赖均存在。本子任务没有重跑其历史求解，状态明确标为 `NOT_RUN_FILE_AND_TEXT_AUDIT_ONLY`。

S1对应冻结设计和场景链；S2对应A/B及策略枚举；S3对应组件/可达性；S4对应覆盖RP；S5–S8对应555组中的空间、子集、OAT、联合扰动及容量/旧界修正；S9对应10个采购/EV策略范围案例；S10对应原23事件/来源；S11对应示例系数；S12对应63候选、60可分析及3pending；S13对应历史验证、阅读和剩余证据边界。`01_Data/Sources/Calibration` 的S01等“来源编号”和补充材料S1–S13是不同编号体系，不能按同号视作对应材料。

## 确实未恢复或未提供的证据

在这两棵可访问目录内未找到且文稿/逐行证据明确未恢复的原始证据包括：原23事件同时期候选/排除登记、原anchor规则版本，以及四个非R11站选择的历史原因。`Original_Four_Station_Choices.csv` 四行的 `historical_reason` 均为 `UNRECOVERED`。这些缺口没有已知的确定文件名，不能编造文件名称或用2026年回溯规则替代。同时期记录即使未来存在于其他位置，也尚未从本次可访问目录恢复。

实地成本、资源需求、泵/措施效果、暴露与损失映射没有提供；`Sources/Calibration` 是背景档案，不等于已完成实地校准。`parameter_families.json` 多项明确为“待校准”。完整63事件无冲突、可拆分输入也不存在：TC2017_06为数值冲突，TC2021_02_E/W为不可分的共同摘要；其源档案存在，应称“未解决观测/归属”，不是声称文件丢失。三个 `model_eligible` 均为False，模型输入栏空白；不得把共同摘要复制两遍或按当前频率插补。

两个目录均未找到Node `package.json` 或常见锁文件，虽然存在.mjs导出工具。它限制样式化Excel导出的精确依赖重装，不等于核心数学输入缺失。上述区分及后果列于 `missing_evidence.json`。

## 结论边界审查

`claim_boundaries.json` 保存五个检查项的原文逐段证据，状态 `PASS_TEXT_SCOPE` 仅代表当前文字有明确限界，不代表数值复现或经验效度PASS。

| 检查项 | 主要正文段落 | 本次文本判断 |
| --- | --- | --- |
| conditional method validation | P9摘要、P14研究问题、P33方法、P210讨论、P212/P215结论 | 多处明确，未发现将自有结果宣称为实地政策效果验证的断言 |
| 成本/资源/收益尚未实地校准 | P33/P51/P56、P130/P133–135、P209 | 明确；约100万HKD设备购置参考不代表CU成本/资源/效益有实证校准 |
| 60只是frequency-only sensitivity | P16/P51/P99、P191/P193、P206/P213 | 明确；前端重新拟合、后端沿用旧响应系数，完整观测到决策传播未完成 |
| 三pending未解决 | P117/P118、P181/P204、P208/P213/P215 | 明确；Yagi仅极值纳入的日期冲突另行说明 |
| 分数非实际损失/受保护人口 | P9/P14/P56/P59、P104/P111/P168、P193/P201/P209/P213 | 明确；人口只是背景，异类部署包不能等同保护人数或货币福利 |

文字中“optimal”“feasible-set”“causal attribution”均有数学模型/规定假设的限定；未据此发现未经限定的实地因果效果、真实经济损失或受保护人口结论。这个判断来自正文和表注直接检查，不是仅重述已有审查报告。其有效范围仍是当前文稿文字，不证明所有模型假设适当或来源独立。

作者后续需手动确认：能否提供上述同时期历史筛选和站选择证据；三pending和Yagi冲突能否由权威资料解决；是否认可目前所有成本/资源/效益的未校准界限；未来如拟提出操作或经济收益主张，应另行提供校准资料并版本化重算；数据许可和最终可获取方式仍需作者决定。此次未改变任何科学结论、参数或历史输入。
