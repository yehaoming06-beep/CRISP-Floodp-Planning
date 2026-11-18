# 核心优化与555设计独立复算记录

2026-11-18（Asia/Shanghai）。范围：真实工作簿输入 → 新求解结果；不以历史summary/solution作为求解输入；历史值仅用于求解完成后的比较。所有新增文件位于本目录，未更改Final Paper、科学参数、源工作簿或历史输出。

## 输入、方法、环境

- 实际参数：`01_Data/CRISP_Master_Data.xlsx`，SHA-256 `e6b93f8bb0e7b886226d27068e8cfeeebfaa92e668eb25f77ee3b1d35083794e`。仓库副本、原研究工作区、CI01快照逐字节一致；模型文件也与快照一致。原始23频率从工作簿读取；60频率从本次独立重算的`../scenarios/scenario_reproduction_summary.json`内35/19/6类别计数生成，其余系数全部保持原值。
- 四个核心模型（23/60 × legacy/mobile）先用Gurobi原模型从输入重新求解，再独立穷举全部可行readiness掩码、采购数量及所有有界整数部署向量。穷举不导入原模型构建器、不读已有解，仅共享工作簿解析器。26个legacy第一阶段策略、78个mobile策略；每个模型同时穷举原场景及EV均值模型，再计算RP、WS、EV、EEV、VSS、EVPI。按原模型采购最少→准备费用最少→掩码最小次序打破EV并列。
- 原工作区环境：Python3.12.8、Gurobi13.0.2、NumPy2.5.4、SciPy1.18.1、pandas2.3.3、openpyxl3.1.5；macOS27.0.1 arm64。许可证真实建模求解通过。环境完整记录在`environment_and_inputs_23.json`及`environment_and_inputs_60.json`。
- root另建不继承系统包的全新环境，安装15项锁定依赖后，本目录`clean_environment/`再次从真实输入复跑4模型24指标及独立穷举，通过，最大误差`1.1368683772161603e-13`。此项不是仅借用原venv。新环境解释器及包版本记于`clean_environment/environment_and_inputs_23.json`。

## 核心比较

`paper_table6_table14_comparison.csv`逐格比较论文Table6、Table14全部48格（含Table14三个数值列与Δ）。全部满足论文六位小数舍入容差`5.01e-7`，最大绝对差`4.2028988644915444e-7`。`core_metrics.csv`、`core60_metrics.csv`及`clean_environment/core_metrics.csv`保留未舍入值；两份`independent_core*_comparison.csv`及clean版本保存独立穷举比较。Table4/11/12属于场景复算，见相邻scenarios目录。

60事件mobile存在4个EV最优第一阶段策略；其EEV范围为600.2030833333334–626.4976666666668。原选定次序（convention A）取600.2030833333334，VSS34.31358333333333。因此该单值依赖已披露的EV并列处理，不宜描述为所有EV最优策略共有的唯一VSS。该现象与历史论文/补充声明相符，不是本次新发现的数值不一致。

## 555组及EV并列补充实验

| 输入频率 | 完整设计 | 主Gurobi记录 | 独立HiGHS RP最优值 | EV并列额外配置 | 并列穷举策略数 | 并列额外求解 |
|---|---:|---:|---:|---:|---:|---:|
| 23事件 | 555 | 3875 | 555 | 10 | 1716 | 1796 |
| 60事件 | 555 | 3888 | 555 | 10 | 1716 | 1808 |

主设计全部真实重新运行并OPTIMAL；60的3888包括原23的两个验证配置及一条原策略在新频率下的固定评价。每个555的构成为：基线2、legacy容量21、mobile容量21、空间26、消融8、OAT56、联合扰动400、库存采购上限9、已有库存5、价格5、可达性2。两次运行分别约21.3秒和23.7秒；200对联合扰动的固定种子和所有参数均未改。独立矩阵HiGHS重新求解每个RP，同时重建/检查RP、WS、EV、EEV与基线固定策略的可行性和目标，并确认EEV的全部第一阶段readiness与采购被固定。

`historical_1110_comparison.csv`证明两个555共1110配置的六指标、准备策略和采购数与各自历史结果完全一致（数值差0）。S9额外政策枚举确实另行跑过，并非仅555中有对应名字；`ev_tie_history_comparison.csv`的20配置240项与历史完全一致。各额外求解皆OPTIMAL。没有覆盖历史ev_policy_tie_ranges等文件。

HiGHS原始浮点目标最大差分别`3.5839774454871076e-6`和`1.648215516070195e-6`，通过原独立验证器`1e-5`容差，**不能称原始浮点目标六位小数完全一致**。对此另做1110次独立矩阵重解，取整其整数变量，并逐条检查原矩阵约束：最大整数偏差`6.339639677666042e-7`，取整后最大约束违反0、取整目标与Gurobi最大差`1.1368683772161603e-13`。原始和取整差均保留在`independent_integer_rounding_rows.csv`；该检查只重构整数解，不更改任何科学系数或优化参数。

## 执行与可移植适配

原23使用未经修改的`run_experiments.py --output`及`verify_results.py`。60的`run_frequency60_555.py`保留原backend循环及模型，改为独立输出目录和当前相同字节的模型路径，读取本次新类别计数生成的频率；历史控制仅用于完成求解后比较。未伪造历史全工作区守卫通过。其源自原脚本的hash差异可通过本目录审计脚本与原脚本直接审查。

```sh
# 以下示例目的目录必须是新的，避免覆盖本次输出。
PY=/absolute/path/to/fresh/venv/bin/python
$PY audit/reproducibility_20261118/optimization/run_core.py \
  --counts-file audit/reproducibility_20261118/scenarios/scenario_reproduction_summary.json \
  --output audit/reproducibility_20261118/optimization/another_clean_core
$PY 03_Experiments/Optimization/code/run_experiments.py \
  --run-id another23 --output audit/reproducibility_20261118/optimization/another23
$PY 03_Experiments/Optimization/code/verify_results.py audit/reproducibility_20261118/optimization/another23
$PY audit/reproducibility_20261118/optimization/run_frequency60_555.py --run-name another60
$PY 03_Experiments/Optimization/code/audit_ev_ties.py audit/reproducibility_20261118/optimization/another23
```

`run_ev_ties60.py`和`verify_frequency60.py`绑定本次60新输出；可核对其简短wrapper后改为新的输出名。`finalize_optimization_audit.py`生成集中清单`optimization_audit_summary.json`。

首次增加独立输出参数时，wrapper误把枚举程序源码查到输出目录，导致求解前FileNotFoundError；完整失败日志为`clean_environment_attempt01_console.log`。源码定位修正后新环境四模型全部通过。该失败不是缺原始数据、许可或依赖障碍，未更改科学参数。`core/initial_*`保留同一审查内较早核心交叉核验，最终新环境证据以`clean_environment/`为准；`run_core_before_output_option.py`保留当时脚本字节及hash供追溯。

## 限度

本项无仍未解决的许可证/求解器/依赖BLOCKED。555和S9十配置并列枚举在原研究venv复跑，新环境仅额外复跑四核心模型。主555独立最优性检查覆盖RP，其他求解检查可行性与目标重建；四核心六指标才具有完整独立穷举证明。官方归档→60事件源重建未由本项复跑；三个pending事件、实地成本/资源/收益校准、模型分数和真实损失/受保护人口之间的缺失映射均保持未解决。结果只支持conditional method validation及frequency-only sensitivity。
