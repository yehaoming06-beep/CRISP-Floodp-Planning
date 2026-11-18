# CRISP 正式仓库候选审阅

日期：2026-11-18（Asia/Shanghai）。本轮仅整理仓库交付、许可通知与可移植核对命令；没有修改Final Paper、模型、冻结实验设计或科学结论。原文件均仍保留在本地。**未暂存、Commit、Push、创建Release或更改Private可见性。**

## 文件选择与体积

起点为29,805候选，475,299,454 bytes（475.3 MB / 453.3 MiB）。本轮精简至约3,440个Git文件、68 MB，减少约86%；16,717个证据成员完整压缩保留，不能把数量下降解释为证据删除。精确最终数字由 [selection_summary.json](selection_summary.json) 给出；[submission_files.tsv](submission_files.tsv) 是本轮唯一待提交路径清单，含大小与SHA。不要使用旧 `audit/submission_20261118/git_submission_files.tsv`，也不要执行不加范围的批量暂存。

| 类别 | 选择与理由 |
| --- | --- |
| 1 必须交付 | `02_Model`、`03_Experiments`、Scenario_Pipeline、便携入口、锁定依赖；六个根最小输入、最终60输入/裁定；冻结23/60汇总/审计；S1–S13及32链接目标；必要v2模型/工作簿快照；130项数值证据；三份完整证据归档。 |
| 2 建议本地保留的扩展审计 | 早期两套555重复日志/解、CI01重复snapshots与replay、重复稳定性表/图、旧全工作区清单及早期打包清单；不进入本轮Git。根CSV/JSON汇总、独立核验结论仍在；被精简的是副本和历史细节，不是唯一必要输入。 |
| 3 第三方hold | 原始HKO/DSD/CEDD/其他网站PDF/HTML/JSON、报告提取页、地图/OSM/Census空间输入及未确认vendor。保留本地，Git仅含必要数值输入、通知、官方链接/来源清单/校验和。 |
| 4 排除 | Cookie/响应头、缓存/编译文件、本地复查目录、环境/凭据模式、新生成输出、旧稿/Word原件/稿件提取和编辑历史等；无科研输入必要性或含个人联系元数据。 |

[分类汇总](classification_summary.json) 区分原29,805候选与全本地快照；[压缩逐文件分类](local_file_classification.csv.gz) 记录相对路径、类别、选择方式、理由、字节数/SHA及已登记官方URL。原29,805候选中的raw类为0，因为既有ignore已将raw hold；本轮额外审计了被忽略资料。文件数量统计不会把归档成员当作单独Git文件重复计算。

三个归档共16,717成员、200,530,950解压bytes，保留最终完整clean_run、原始冻结555解、S9全部EV并列审计及补充重跑。原始文件未删，解压后逐字节恢复原路径；[成员清单与归档SHA](evidence_archives.json) 和 [说明](../../results/evidence/README.md) 可独立审核。基线解和全部补充正文链接目标直接可读。解压不是核心复现前置步骤。

## 许可与安全

HKO数值按免费、非商业研究的附条件来源授权保留；政府/HKO所有权、原始网站/刊物来源、研究加工说明、完整官方权利通知/适用条件和官方规定免责声明均随包提供。不是无限制数据授权或HKO背书。见 [THIRD_PARTY_NOTICES](../../THIRD_PARTY_NOTICES.md)；官方来源为 [网站条件](https://www.hko.gov.hk/en/appweb/applink.htm)、[刊物条件](https://www.hko.gov.hk/en/publica/non-commercialuse.htm) 与 [权利通知](https://www.hko.gov.hk/en/readme/readme.htm)。后续商业使用须另行满足官方授权要求。

DSD与CEDD原作品的公开再分发未清除，完整原报告/提取页不提交；Boston/JRC完整归档及vendor未确认逐件许可，也不提交。OSM并非绝不能公开，但须履行ODbL/署名等条件，本轮不纳入地图；Census统计与空间服务分别适用自身条件。全部这些raw资料均不是所列数值复现命令的外部必需输入。官方条款直接链接见 [权利矩阵](../Data_Rights_and_Access.md#third-party-rights-matrix)。

[source_access.csv](../../data/provenance/source_access.csv) 合并23+307+8=338条来源记录，含官方URL、相对held路径、SHA与条款；338本地来源哈希全部匹配。逐文件分类还保留未入Git材料的SHA；未登记的旧副本/提取页/vendor来源仍不作已授权或可自动下载声明。

独立安全扫描覆盖初始候选、精简候选和三个归档的每个解压成员，未发现常见私钥、Token、密码/WLS赋值、Cookie/Auth头或凭据URL；三份XLSX的XML也已检查。含个人联系邮箱的旧稿/提取副本已排除，剩余邮箱是HKO官方法律通知的联系地址。历史用户名与研究目录路径保留在2,434个逻辑文件（123个普通候选、其余在历史证据归档），不是运行所需路径；完整clean_run归档无此命中。模式扫描不能证明不存在所有未知形式秘密。[扫描记录](security_scan.json)。

## S1–S13、数值与独立复现

S1–S13原文未变，16表、5图、32补充本地链接完整。现有98项结构检查、768项补充/相关主文数值比较，以及130项论文比较均在原容差内；46个对照源文件SHA匹配。保留原有研究限制：原23筛选历史缺证、缺实地校准、3个pending、37次Lloyd非全局最优、最终60移动泵4个EV最优策略及约定A的VSS口径。

[REPRODUCE.md](../../REPRODUCE.md) 给出实际GitHub URL、完整环境/核心/两套555/130比较/软件测试命令。所有新入口按文件位置推导根目录，无仓库外本机绝对路径依赖。原始模型和设计未改；唯一核对器改动是允许对新生成core CSV运行48格比较并写入新目录，不改变比较公式/容差。

最终科学选择树从Git候选精确导出至独立临时目录，不复制ignored材料；复用此前已全新安装且不继承system packages的Python环境。最新执行结果及真实日志见 [selected_tree_test.json](selected_tree_test.json) 与 `selected_tree_results/`。本轮第一尝试已通过all+130，但新加入的测试命令缺PYTHONPATH，且复用环境的访问守卫缺环境参数；记录保留为 `attempt01_*`，未当作最终全流程PASS。修正的是测试命令与验证环境，不是模型或数值。最终运行以守卫自检成功、实际执行0次用户研究目录读取和全部步骤通过为准。此守卫是Python文件访问检查，不是原生库操作系统级隔离。当前没有提交，故不能称真实GitHub Clone已通过。

## 独立获取边界与交付结论

所列核心23/60与两套555命令无需仓库外研究数据。外部前置条件为：有权访问Private仓库的GitHub账号、Python/网络包安装及适用Gurobi许可；固定小模型在此前restricted非生产许可下完成，无个人求解器凭证入包。HiGHS核验RP与已存解的可行性/目标，不冒称独立重优化全部WS/EV/EEV。

完整官方原档案→数值输入重建另需按338条清单从官方获取精确冻结版本、遵守逐项许可并核SHA。现场网页若已变化不能替代旧版本；仍没有保证所有冻结源档案可独立获得的分发服务。完整CI01/v2历史全集守卫不在本精简Clone通过范围。详见 [外部来源边界](../../REPRODUCE.md#external-source-boundary)。

- **Commit：**本地候选准备供用户审阅；最终清单/包校验/选择树测试PASS后，可在用户明确确认后提交。
- **Push：**还需要用户确认和有权限的GitHub认证。当前连接器查询返回404，HTTPS只读访问因无用户名凭据失败；没有尝试Push，也不据此推定仓库不存在或改变可见性。
- **必要材料未入Git：**当前HEAD只有README和.gitignore，全部科学材料尚未正式跟踪；本轮清单已选齐数值路线所需材料，部分完整证据压缩保存。raw并非该路线缺失输入，但全源重建仍缺独立获取保障。
- **`v1.0-submission`：**现在不创建。用户确认并完成Commit/Push后，需对该确切commit做真正全新Clone与完整命令验收，再创建明确限定“数值输入→结果”的Private submission Release。未授权公开或更改仓库可见性。
