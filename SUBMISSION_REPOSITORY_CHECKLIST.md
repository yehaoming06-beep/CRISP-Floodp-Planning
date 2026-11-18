# CRISP 正式仓库交付检查单

2026-11-18，Asia/Shanghai。本文件与 [DELIVERY_REPORT](audit/delivery_20261118/DELIVERY_REPORT.md) 描述本轮精简后的候选，不沿用旧版29,805文件清单。未暂存、Commit、Push、Tag、Release或更改Private可见性；Final Paper未改。

- [x] 对29,805个原候选逐文件分类，并额外盘点被忽略的原始来源/缓存。没有删除原研究文件。
- [x] 保留核心23/60、两套555必要输入/配置/生产代码/模型、核心结果、S1–S13、32补充链接目标及130项比较证据。
- [x] 三个确定性证据归档完整保存16,717个原文件，逐成员大小/SHA一致；唯一S9并列最优证据、冻结解和最终干净运行均保留。提供校验/恢复入口。
- [x] 六个根最小输入与v2快照工作簿精确放行；官方raw、未确认vendor、地图及Word原件继续hold。
- [x] 官方HKO完整法律通知、适用非商业条件与规定免责声明已随包保存；338条来源记录含官方URL及SHA，全部本地匹配。没有代作者添加统一代码或数据许可证。
- [x] 全候选及归档解压内容扫描未检出常见凭据、Cookie或Auth；含作者邮箱的旧稿/提取副本不提交。历史用户名/工作区路径作为来源记录保留，非运行依赖。
- [x] README与 [REPRODUCE.md](REPRODUCE.md) 提供相对路径、固定依赖、核心/两套555/130比较及既有软件测试命令；不依赖仓库外研究文件。
- [x] 对最终科学选择树进行独立目录执行；最新状态以 [selected_tree_test.json](audit/delivery_20261118/selected_tree_test.json) 为准。旧干净安装/运行证据仍保存。不能把导出树测试称为已提交Clone。
- [x] 精确待提交清单/大小/SHA在 [submission_files.tsv](audit/delivery_20261118/submission_files.tsv)，总数/总字节见 [selection_summary.json](audit/delivery_20261118/selection_summary.json)。校验命令 `python3.12 src/verify_delivery.py`。
- [ ] 用户审阅本轮Git改动摘要并明确确认Commit/Push。
- [ ] 以有权访问此Private仓库的账号完成Git认证；当前连接器404，HTTPS无可用用户名凭据，未尝试Push。
- [ ] 对确认后实际提交并Push的commit执行真正全新Clone及REPRODUCE命令，再校验清单。
- [ ] 完成上述步骤后，再创建限定数值输入→结果范围的 `v1.0-submission`；不声称完整官方原档案→输入复现、完整CI01/v2历史守卫或实地有效性。

当前判定：**本地候选可供Commit审核；Push尚需确认和认证；现在不能创建Release。** 原始来源重建不影响已包含数值输入的核心复现，但仍没有经确认的全量冻结源档案独立公开获取路径。受限/未确认raw不通过`git add -f`绕过。
