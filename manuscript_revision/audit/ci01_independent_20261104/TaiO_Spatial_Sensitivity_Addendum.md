# 大澳潮站空间敏感性补充规程 v1.0

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Origin Mode: validate
- Origin Date: 2026-11-04（Asia/Shanghai）
- Verification Status: ANALYZED
- Version Label: CI01-supplement-spatial-v1

本补充在发现HKO官方增水数据库同时登记Tai O站后提出。制定时已查看其资料覆盖和个别观测，尚未重拟合大澳站情景；不是历史规则，也不是事先盲法预注册。**不改变已冻结的主规程**，不把大澳/石壁值混合成一条新主序列，不覆盖主61条或冻结23条。

目的有二：（1）用独立官方增水数据库交叉核对主方案Shek Pik数值、峰值时刻和质量标记；（2）量化潮站空间选择对情景结果的影响。大澳站水位仍是相对于海图基准面的海面高度，不是大澳街道洪深。

资料为HKO页面[Storm Surge Records](https://www.hko.gov.hk/en/wservice/tsheet/pms/stormsurgedb.htm?t=STORM&v=31)实际加载的ssdb_storm.js、ssdb_station.js、ssdb_year.js和ssdb_track.js完整原始JSON响应。页面明确时间为香港标准时间，SEA为mCD、SURGE为天文潮以上m；完整/不完整/临时标记由原页面JavaScript定义，不能把雨量#含义移用于潮位数据库。INCOMPLETE=N才通过本补充QC；Y/C或未解释标记均保留待核。

按year+官方事件名匹配，并逐条核对峰值年月/官方报告身份。未命名事件以年份和发生月/官方报告区别。2018年7月数据库将Son-Tinh第二次经过另记为No name，只有在官方年度报告§3.2明确其为Son-Tinh再发展和第二次经过的证据下，才合并为同一候选，分别取两次报告的W/S最大值；所有原始行仍保存。2021年两个热带低压的共同摘要不拆分为两个可分析观测。

大澳站不在某事件REC中、值缺失或有质量标记时，标记PENDING_TAIO_DATA；该事件气旋资格不受影响，不作实体排除，亦不拿Shek Pik补大澳。官方Man-yi/Fengshen/Fung-wong共同驱动脚注在大澳残差解释中继续保留，不声称因果分解。

比较采用（a）同一可分析身份交集上的Shek Pik和Tai O各自完整重拟合，确保差异不来自样本数；（b）原23身份换Tai O的重拟合，以分离站点选择与样本扩展；（c）把共同警告记录只当一条观测的主规程单位敏感性已单独完成。保留rain站、锚点和±2日窗口，K=3等计算配置固定。新站资料只支持这项描述性敏感性分析，不自动提升为经实证校准的主模型。

如有后端结果，沿用主分析的明确约束：仅更新条件情景频率、固定其余情景系数；不能把它称为完整观测到效益重标定。补充规程和执行代码均留存哈希、原始JSON和匹配台账。
