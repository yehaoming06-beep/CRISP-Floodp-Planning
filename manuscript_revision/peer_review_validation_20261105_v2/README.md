# 本轮补充验证交付说明

版本：peer_review_validation_20261105_v2；2026-11-05，Asia/Shanghai。用户要求重启后独立保存的结果包。未采纳v1保留在其原目录，本轮不读取其结果；新工具有复用后再审的代码，但本轮重新从冻结输入求解，全部结论来自本目录。

## 五份交付

1. [Peer_Review_Issues.md](Peer_Review_Issues.md)
2. [EV_Convention_Sensitivity.md](EV_Convention_Sensitivity.md)
3. [Controlled_Model_Ablation.md](Controlled_Model_Ablation.md)
4. [Methodological_Contribution_Matrix.md](Methodological_Contribution_Matrix.md)
5. [Revised_Experiment_Recommendations.md](Revised_Experiment_Recommendations.md)

## 实际执行顺序

执行前方法审查及修正→保存执行门→初始化快照/冻结守卫→500次主求解→派生对照和500个模型读回→独立500模型及额外原始EV重建（936次HiGHS）→来源链条审计→综合报告→报告独立复核及最终保全。模型读回和派生表不增加优化次数。

主求解：8个EV规格；26/78个一阶段政策逐规格完整枚举，累计416；20条主最优EEV；24组件RP；8覆盖RP；其余为必要RP/WS/返回EV/EEV，共500。498最优，2个k=6覆盖不可行。独立核验所有主模型及参数/集合/范围；没有重跑冻结555组。

## 文件布局

- `assessment/`：执行前独立评估、控制设计、执行门与原23/60链条审计。
- `snapshots/`：实际使用的原始参数、工作簿、模型、主稿、必要基线和前端摘要快照。
- `code/`：主求解、派生证据、链条审计、独立HiGHS实现；`code/versions/`保留独立核验器初版。
- `runs/primary/parameters/`：按内容哈希引用的完整输入；每次解含parameter_id。
- `runs/primary/solutions/`：500个逐次JSON，包括变量、开关、固定政策、状态、残差及目标。
- `runs/primary/models/`：500个可重读LP；2个不可行情境另有IIS `.ilp`。
- `runs/primary/logs/`、`sol/`：全部Gurobi日志及498个最优原生解。
- `independent_validation/`：独立矩阵、解、逐规格状态/差异、EV重建与范围、覆盖证书、库存见证。
- `literature/`：23条检索式、8个作品逐项取得/阅读范围，未将403/429写为全文核验成功。

## 运行命令与环境

工作目录为 `/Users/yehaoming/Desktop/climate_Devin`。实际解释器为项目 `.venv/bin/python`，Python3.12.8；Gurobi13.0.2、SciPy1.18.1、NumPy2.5.4、openpyxl3.1.5。版本文件及原requirements-lock已归档。Gurobi需要相应可用许可；没有声称无需许可即可复现。

本轮按顺序执行以下命令；控制台记录保留在本目录对应log中：

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python manuscript_revision/peer_review_validation_20261105_v2/code/run_validation.py --initialize
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python manuscript_revision/peer_review_validation_20261105_v2/code/run_validation.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python manuscript_revision/peer_review_validation_20261105_v2/code/finalize_artifacts.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python manuscript_revision/peer_review_validation_20261105_v2/code/verify_independent.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python manuscript_revision/peer_review_validation_20261105_v2/code/verify_independent.py --supplement-primary-witness
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python manuscript_revision/peer_review_validation_20261105_v2/code/audit_scenario_chain.py
```

初始化和主求解器对已存在的目标目录拒绝覆盖。独立核验器的首次成功运行manifest另保留，随后只补见证/引用检查，不再求解；初版代码按原哈希恢复保存。日志运行时间不是确定性数值输出，不能要求字节一致。

在原工作区重跑主模型可用一个**新的、不存在的目录**；无需重新初始化，更不应覆盖primary：

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python manuscript_revision/peer_review_validation_20261105_v2/code/run_validation.py --output /Users/yehaoming/Desktop/climate_Devin/manuscript_revision/peer_review_validation_20261105_v2/runs/reproduction_001
```

`finalize_artifacts.py`和独立核验器默认绑定本轮primary，为保留交付证据不要在原输出上重复执行。若复制整个验证目录开展新独立核验，其相对路径会指向该副本中的primary/snapshots；先保留原交付，再使用新的结果目录。归档清单记录各文件SHA-256，便于作者核对。

## 保全与解释

冻结守卫核对21,678个既有科学源文件，包含原23、最终60、555组、模型及主稿；本轮目录、未采纳v1、`.venv`、`__pycache__`、`.git`和`.DS_Store`明确排除。副本与新结果独立保存。没有直接覆盖主稿，没有改旧问题台账，也没有建立未经证据支持的R/W/S效益函数、人口→β、泵数→保护人数或CU→HKD换算。

EV范围是并列政策范围；覆盖是抽象包数假设；不同可行域的RP差异是约束机会成本。数值核验通过不证明现场有效性、相对模型性能优越、首次创新或CI-01/CI-06已经关闭。
