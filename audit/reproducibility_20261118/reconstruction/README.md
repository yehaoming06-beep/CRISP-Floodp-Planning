# 冻结来源档案至最终60事件输入的离线重新执行

日期：2026-11-18（Asia/Shanghai）。本次确实执行了冻结的 `reconstruct.main()`；未读取已有60事件输入作为生成输入，也未从既有分类或优化结果反向制造数据。

原始 `manuscript_revision/audit/ci01_independent_20261104/code/reconstruct.py` 与 `hko_parse.py` 保持不变。包装程序只将 `OUT`、`SNAP`、`WEB` 改指本目录的独立 `stage/`，算法、来源内容、协议和QC裁定均不变；不伪造或更新历史完整性guard。设置了 `sys.dont_write_bytecode`，导入原代码不会在其目录新写字节码。复制输入均为普通文件，没有建立符号链接。

## 输入及执行

复制336个已存在输入，共107,131,528字节，包括档案网页/警告表/雨量响应、27个站年雨量JSON、原23事件metadata、冻结筛选和QC文件、6个实际引用的PDF、15个历史提取页文本及其索引。逐文件原路径、stage路径、字节数、源/副本SHA-256在 `copied_input_manifest.csv`；原始代码与包装脚本哈希在 `code_manifest.json`。未复制图片。

实际执行命令：

```sh
/var/folders/63/_93zr4n96qqf58fvm9plk4b40000gn/T/crisp-repro-20261118-bk2m6vpz/bin/python audit/reproducibility_20261118/reconstruction/run_offline_reconstruction.py
```

执行环境和命令的完整记录见 `execution_environment.json`；运行标准输出见 `execution_stdout.log`。来源至输入重建运行耗时0.414秒。重建代码只使用标准库，不调用网络或求解器。包装程序在 `stage/` 已存在时明确拒绝覆盖；重新运行须使用新的同级输出目录，不能删掉旧结果后声称同一运行。

## 结果

| 输出 | 原档行数 | 新运行行数 | 不同单元格 | 最大数值绝对误差 | 字节一致 |
| --- | ---: | ---: | ---: | ---: | --- |
| Candidate_Event_Inventory.csv | 63 | 63 | 0 | 0 | 是 |
| Inclusion_Exclusion_Audit.csv | 63 | 63 | 0 | 0 | 是 |
| analysis/reconstructed_model_input.csv | 60 | 60 | 0 | 0 | 是 |

全部11项生成CSV/JSON均与当前原档逐字一致，解析后也相同；完整逐项结果见 `output_comparison.csv`，`cell_differences.csv`只有表头。`validation.json`记录状态 `REPRODUCED_FROZEN_OFFLINE_RECONSTRUCTION`。所复制原输入与比较参考输出在运行后哈希均保持不变。

重新执行得到62警告组、63气旋身份、60纳入、3 pending，雨站54 R11 / 4 HKA / 2 R12；原23事件R/W/S向量全部23/23一致，5个anchor日期改变，0个站或R数值改变。27对档案雨量响应仍字节相同。TC2017_06仍为来源数值冲突，TC2021_02_E和TC2021_02_W仍为不可拆分的共同观测，不补齐、不复制为两条独立分析记录。

## 解释边界

这是**冻结档案、规则和既定QC裁定的独立新执行**，使用原始确定性实现；不是另写一套筛选算法或重新独立裁定所有争议。它证明这套既存档案/规则可重新生成同一最终60输入和候选裁定链。

2025年潮位值仍来自已保存的历史PDF提取文本。本次复制并校验了对应PDF，但没有重新提取PDF、目视核对页面或作新的来源权威性裁定。`stage/evidence/Tide_Table_Extraction.json` 中 `visual_check` 的“2026-11-04 assistant inspected...”字样为原程序写出的**继承历史文本**，不代表2026-11-18新做的视觉验证；`image`字段也为继承定位，图片未复制到stage。`Rainfall_Redownload_Comparison.json` 的“redownloaded”同样指历史保存的再下载档案，不代表本次进行了联网下载。

该结果不恢复原23事件同时期筛选意图，不解决三pending或Yagi日期冲突，不校准仪器、成本、资源或收益，也不证明60事件为完整洪水总体。CRITIC/K-means与优化重算应单独读取它实际生成的60行向量并报告。
