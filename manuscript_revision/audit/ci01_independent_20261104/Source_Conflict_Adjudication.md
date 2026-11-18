# 官方来源冲突的QC解释与执行登记 v1.1

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Origin Mode: validate
- Origin Date: 2026-11-04（Asia/Shanghai）
- Verification Status: ANALYZED
- Version Label: CI01-source-conflict-QC-v1.1

本登记在首轮61条试算后、最终QC重建和重算前形成。它公开细化主规程§4的质量控制，不冒充最初历史标准或事先盲法预注册。主规程v1.0文件与哈希不修改；61条输入、结果和代码快照保留在stages/v1_before_secondary_tide_crosscheck，555组试算保留在backend_probability61。

统一处理原则：若已取得的官方来源对同一事件、同一站、同一物理量的**数值**明确冲突，且不能确定官方修订先后/更正依据，则该站事件暂不作为已核清完整案例。记录候选资格和两套数值，为PENDING_SOURCE_CONFLICT，不算实体排除，也不按多数表决认定哪套是真值。若冲突仅涉及峰值日期，而事件身份、W/S数值和基准均一致，则在只使用事件R/W/S极值的本次模型中允许带明确时间限定的数值分析；峰值日期仍UNRESOLVED，不用于峰值同步、连续过程或小时水文验证。该区别是一项本次研究者的方法选择，不是HKO质量认证。

## TC2017_06：2017年9月未命名热带低压

- [年度Table 3.6.3](https://www.hko.gov.hk/en/publica/tc/tc2017/table363.html)：Shek Pik W=2.23 mCD，23/9 23:32；S=0.26 m，24/9 11:17。
- [2017年9月官方月报，PDF p.28/印刷p.26，Table 2.3.3](https://www.hko.gov.hk/en/publica/mws/files/mws201709.pdf#page=28)：与上述年度原表四字段一致。完整PDF通过预检，并核看原页。
- [官方增水数据库原始记录354](https://www.hko.gov.hk/wservice/tsheet/pms/ssdb_storm.js)：同名同年同月，Shek Pik W=2.48 mCD，24/9 06:42；S=0.29 m，24/9 04:28；INCOMPLETE=N。数据库数值也与Mawar报告的数值相同，但这只能提示需查询更正，不能据此断言复制错误。
- 处置：候选保留；最终主模型PENDING_SOURCE_CONFLICT；数值全部留在台账，不选较大/较小者，不作实体排除。官方月报和年报可能来自同一编制链，两者相符不能证明测量真值。

## TC2024_03 / E018：Yagi

- [年度Table 3.3.4](https://www.hko.gov.hk/en/publica/tc/tc2024/table334.html)及[2024年9月月报，PDF p.29/印刷p.26](https://www.hko.gov.hk/en/publica/mws/files/mws202409.pdf#page=29)：Shek Pik S=0.57 m，5/9 01:10；W=2.52 mCD，5/9 10:42。
- 官方增水数据库记录393：W/S数值和W时刻相同，但S时刻为6/9 01:10。两种S日期均在同一气旋警告期及本方案9/3—9/7雨窗内。
- 处置：保留R=80 mm/day、W=2.52 mCD、S=0.57 m的数值分析，标记PEAK_TIME_CONFLICT_UNRESOLVED。不给S日期选择“正确值”，不称时间字段全部验证通过，不覆盖旧元数据。另给完全不采用两处来源冲突事件的严格敏感性。

## 最终重建及影响范围

由此，主方案63个气旋候选中，60条进入最终数值模型，3条待核（2017低压数值冲突；2021东/西两个低压共用摘要的归属未分离），实体排除仍为0。Yagi为60条中带峰值时间限定的记录。因此“60可分析”不等于所有时空字段、仪器质量和洪深均已验证。

这次调整由新发现的官方正面冲突触发，不按样本数、CRITIC权重或优化结果选择。最终复算另存reconstructed60_adjudicated与backend_probability60；前一阶段61条输出不删除。对官方冲突的最终关闭仍需更正说明或可比原始连续测潮记录。更广义无本地警告气旋的影响母体和原作者初筛历史仍未恢复，CI-01不能因此全部关闭。
