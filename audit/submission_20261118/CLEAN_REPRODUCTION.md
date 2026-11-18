# 独立目录复现检查

日期：2026-11-18（Asia/Shanghai）。结论：**待提交候选文件树的核心23/60及两套555通过；当前已提交HEAD的实际Clone不通过。** 两种状态必须分开报告。

## 已提交仓库与候选文件树

实际执行本地 `git clone --local --no-hardlinks`，得到的提交只有 `.gitignore` 和 `README.md`，没有工作簿或研究代码，无法运行核心复现。记录见 `actual_clone_test.txt`。用户要求不Commit/Push，因此本次未制造临时提交，也未把该Clone称为完整通过。

另用独立临时Git索引导出全部选定候选文件至仓库外干净目录，没有复制ignored资料，没有符号链接到研究目录。真实工作区的Git索引、HEAD未变。`tested_final_candidate_manifest.json`记录所测候选路径、大小和逐文件SHA；代码审查后修正的最终入口用于本次最终运行。最终新增的检查报告、输出归档和Git清单不改变已测科学代码。`git_submission_files.tsv`是完成整理后的最终候选清单，不能与测试开始时的快照数量混用。

## 环境与隔离措施

- 新建Python3.12.8环境，`include-system-site-packages = false`；15项直接依赖全新安装，`pip check`通过，完整传递版本保存在 `clean_freeze.txt`。
- 安装仅显式使用系统可信CA证书；没有关闭TLS验证、读取个人pip配置或继承原研究环境。
- 最终运行使用新建空HOME和明确环境变量列表，清除Python路径覆盖；不提供Gurobi许可变量或外部凭证。
- 临时环境内安装 `file_access_guard.py`：Python文件访问审计拒绝 `/Users/yehaoming/` 下文件，因此不能读取本工作区、原研究目录和用户配置。所有子Python进程均加载该守卫，记录没有任何被拒绝访问尝试。守卫是Python层检查，不声称是操作系统对原生扩展/系统库的完全隔离。
- Gurobi13.0.2探测为默认restricted license（LicenseID为0，仅保存布尔判断），小规模冻结模型全部成功。未依赖本机个人学术许可。仍须遵守Gurobi许可及规模限制，不保证所有平台或扩展模型都适用。

安装、环境、许可探测、守卫记录和真实执行命令见 `clean_install.txt`、`clean_pip_check.txt`、`clean_solver_probe.txt`、`file_access_guard.txt`、`final_clean_run_exit.json` 与 `clean_run/execution.json`。

## 最终执行与结果

从候选根目录实际运行：

```sh
<fresh-python> -I src/reproduce_submission.py all \
  --output results/reproductions/submission_clean_final
```

`<fresh-python>` 是独立目录中新安装的解释器，真实绝对路径保存在执行JSON中，复现入口本身没有绑定该路径。输出完整复制回 `audit/submission_20261118/clean_run/`，共8,964文件；每项源/归档SHA一致，见 `clean_output_manifest.json`。

| 检查 | 实测结果 |
| --- | --- |
| 原23/最终60场景 | 9/9/5、35/19/6；生产实现与独立CRITIC/全局三段拟合一致；82个论文单元格通过 |
| 四核心模型 | 23/60×legacy/mobile；24指标与穷举一致，最大差1.137e-13 |
| 新核心对照Table6/14 | 48单元格通过，最大显示舍入误差4.203e-7；与场景共130项 |
| 原23完整套件 | 555配置、3,875条主求解均OPTIMAL；六指标/策略与历史一致 |
| 最终60完整套件 | 555配置、3,888条主求解均OPTIMAL；只更新新拟合频率，六指标/策略与历史一致 |
| 独立HiGHS | 每套555个RP最优值及保存解可行性/目标重构通过；原始目标最大差3.584e-6/1.648e-6，均低于原1e-5容差 |
| 既有软件测试 | 17项通过；仅有简化PATH找不到sysctl导致joblib改用逻辑CPU计数的非失败警告 |

第一轮候选导出也通过；最终结果采用代码审查修正失败传播后的版本，没有覆盖第一轮运行。补充的48格比较初次仅因Unicode负号解析失败，修正字符串解析后通过，记录保存在 `fresh_core_table_parser_attempt.txt`；该过程没有重新求解或改动数值输入。

## 明确没有通过或没有覆盖的部分

1. **实际Git Clone仍BLOCKED**：研究材料未提交；提交后须对所选提交再做真正Clone检查。本次候选导出PASS不能代替该步骤。
2. **官方原始档案→最终60输入的公开Clone链未建立**：之前本地来源重建有执行证据，但raw archives、提取/QC材料仍受分发限制，尚无已验证的公开获取方案。
3. **CI01/v2全历史工作区守卫未在精简候选树通过**：缺少历史全集；未重置守卫或伪造通过。保存的500/936结果已做证据与正文核对，不等于本次完整v2干净重跑。
4. 未做新的科学实验、实地校准、来源在线重下载、PDF重提取/裁定、全部稳定性/v2干净重跑或其他操作系统认证。
5. 历史筛选证据不完整、三个pending、37次Lloyd局部最优及EV最优策略并列仍未解决。

当前结果支持准备候选材料供审核，尚不支持宣布完整公开归档或直接创建 `v1.0-submission`。
