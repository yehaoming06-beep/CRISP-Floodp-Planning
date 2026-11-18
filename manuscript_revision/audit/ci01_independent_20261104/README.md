# CI-01 独立重建：交付与复现

最终入口为[CI01_Resolution_Report.md](CI01_Resolution_Report.md)。最终状态PARTIALLY RESOLVED，63气旋身份/62警告组，60数值案例、3待核、0实体排除。Screening_Protocol.md是应用前冻结的v1.0，执行时与Source_Conflict_Adjudication.md v1.1结合；原主文不追改。TaiO_Spatial_Sensitivity_Addendum.md是发现新站点资料后的公开补充，非历史规则。

## 当前与历史阶段

- 根目录三张事件CSV：最终63候选及60/3判定；Original23_vs_Reconstructed含原23和40额外候选。
- analysis/scenario_impact.json：最终主链索引，main_fit=reconstructed60_adjudicated；当前主输入analysis/reconstructed_model_input.csv。
- analysis/scenarios/reconstructed60_adjudicated：最终60条CRITIC、聚类及代表值。
- analysis/spatial_impact.json：同一59身份的石壁/大澳比较及原23换大澳的敏感性。
- backend_probability60：最终60条件频率的555配置、3888求解审计行；另有10案例EV同值政策审计。
- backend_probability60_replay：最终555配置完整重复，summary.csv与上项逐字节一致。
- stages/v1_before_secondary_tide_crosscheck：QC新证据出现前的61条输入、分析和代码。backend_probability61为该阶段555组试算；其中manifest指向的通用概率文件后来被最终60更新，**当时实际61频率原件在stage的analysis/backend_probability_update.json、backend_probability61/inputs.json及每个solution参数中保留，哈希可对账**。不要把该目录视为最终QC通过样本。
- analysis/scenarios中名字含reconstructed61_main、warning_group62_unit_sensitivity、omit_explicit_joint_rise_sensitivity的目录是保留的首阶段输出；当前主索引不引用它们。
- snapshots：原始主数据、配置、模型、代码和结果；logs/frozen_inputs_manifest.json记录977文件的原位置/快照/SHA。
- sources/web、sources/pdf、sources/ranges、sources/prior_fix：完整官方响应、PDF、原始字节段和以前完整归档；404响应留存但不作缺失事件证据。原始响应内可能存在无关网页导航文字，只按明确证据范围使用。

## 离线重现

在项目根目录使用已有.venv，或安装snapshots目录中的requirements-lock.txt对应依赖。实际版本另见logs/exact_environment_versions.json。不会联网的主复算命令：

```sh
.venv/bin/python manuscript_revision/audit/ci01_independent_20261104/code/reconstruct.py
.venv/bin/python manuscript_revision/audit/ci01_independent_20261104/code/assess_scenarios.py
.venv/bin/python manuscript_revision/audit/ci01_independent_20261104/code/verify_tides_and_spatial.py
.venv/bin/python manuscript_revision/audit/ci01_independent_20261104/code/verify_delivery.py
```

上述命令只重写本审计目录的派生表和日志，使用已保存的原始来源，不改冻结主项目。verify_delivery会再运行三步、逐字节比较派生输出、独立检查CRITIC/SSE、冻结输入、PDF完整性和已保存的两次555结果。报告重建：

```sh
.venv/bin/python manuscript_revision/audit/ci01_independent_20261104/code/write_reports.py
```

如需自己重新求解完整555组，用一个尚不存在的目录名，已有结果不会被覆盖：

```sh
.venv/bin/python manuscript_revision/audit/ci01_independent_20261104/code/run_backend.py --run-name backend_probability60_reproduction_02
.venv/bin/python manuscript_revision/audit/ci01_independent_20261104/code/audit_backend_ev_ties.py --run-name backend_probability60_reproduction_02
```

求解需可用Gurobi许可证；本次许可证和代码实际可用。当前runner加载最终analysis/backend_probability_update.json，只更改条件频率，保留情景系数；其余555设计与快照相同。复制到其他机器时，保护原工作区的哈希核验需要原目录结构；仅在独立包中运行时，应将冻结清单核验指向对应原件或明确标记原件不可访问，不能当成已通过。

## 下载与PDF检查

collect_sources.py和logs/jobs_*.json保存下载任务，网络重取可能得到新版本，必须保留新旧快照及差异，不能与本次离线复现混为一谈。collect_pdfs.py使用核验Content-Range/长度/Last-Modified的分段下载；pdf_download*.json记录完整性。2025年7/9月重用此前完整官方快照，沿用其原下载记录和SHA，没有虚构本次重下载。

extract_pdf_evidence.py使用已保存PDF，生成文本和目标页图像。code/vendor保留ARS的pdf_read_preflight.py及其audit_snapshot.py依赖，来源为本机academic-research-suite/ars/scripts，供页树三重页数预检。PDF_Visual_Check_Ledger.csv只表示已核看的16个目标页，不是全文技术审读或仪器校准。

logs中的attempt01、crosscheck_before_adjudication等失败/中止记录刻意保留。初次解析遇到研究期外历史2400时刻，已通过先过滤研究期修复；来源冲突触发过暂停，之后公开登记v1.1并重新执行。verify_delivery的初次导入错误已修正；这些不是被隐藏的成功运行。

## 解释限制

任何n_s/N均为给定筛选、QC和可得性下的条件相对频率。不是年发生概率、洪深、同步水文事件或现场干预效果。未决候选、官方正面冲突、无警告影响总体及历史筛选证据均保留。未向外部应用上传、发布或修改论文。
