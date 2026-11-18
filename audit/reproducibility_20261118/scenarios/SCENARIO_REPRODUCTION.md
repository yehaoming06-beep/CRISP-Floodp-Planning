# 場景層獨立復算紀錄（2026-11-18）

## 狀態與範圍

**PASS：從實際 23/60 事件輸入重新計算 CRITIC、嚴重度與分類；Final Paper Table 4、11、12 全部 82 項對照通過。** 先用原研究環境執行，之後在本次新建、未繼承系統套件的 Python 3.12.8 環境再次執行，同樣通過。兩個環境產生的 21 份核心 CSV 逐位元組一致，見 `clean_environment_crosscheck.json`。

原文檔、歷史數據、歷史實驗輸出及科學參數均未修改。本目錄沒有重新從 HKO 來源歸檔抽取整個事件框架；其證據限於已找回的實際輸入表及其與入選清單的對應，不能用本次計算宣稱三個 pending identities 已解決。

## 真實輸入與計算方法

- 23 事件：`01_Data/Events/model_input.csv`，SHA-256 `094bea5ff6b2f5d8d71b60d8fb62772c2af05a2de83eba21fccbffe176fd544d`；在目前 Git 工作目錄中為 ignored local，並未進入 Git。
- 60 事件：`manuscript_revision/audit/ci01_independent_20261104/analysis/reconstructed_model_input.csv`，SHA-256 `7c01d508a17dcb9643a3fd8b9e4f679898b25820fccdbd43b50f0c8f377340e0`；為 untracked local，並未進入 Git。
- 兩張輸入表與 `/Users/yehaoming/Desktop/climate_Devin/` 中對應檔逐位元組相同。60 事件的每項 R/W/S 與 `Inclusion_Exclusion_Audit.csv` 中全部 60 個 eligible identities 的 `model_*` 欄位完全一致。原 23 identities 經新 screening 清單對應後，輸入與原表完全相同。
- 自含程式 `reproduce_scenarios.py` 先用 Min-Max、獨立 scalar Pearson、母體標準差 ddof=0 實作 CRITIC，未從既有結果估計輸入或參數。對一維 H 枚舉所有非空連續三段分割：23 事件 231 組、60 事件 1,711 組，找全局 SSE 最小值。
- 獨立計算完成後，再調用未修改的原 production pipeline 交叉核對：K=3、seed=42、n_init=50、max_iter=300、Lloyd，類內代表值為算術均值。三個 fits（原 23、原 identities 新 screening、重建 60）之間的獨立解與 production labels 無差異；最大權重及 H 誤差均約 1.11e-16。
- 最後才讀取 Final Paper DOCX XML 的實際 captions 和 tables，作為比對目標，沒有修改文檔，也沒有把論文結果當成計算輸入。

## 核心重算值

| 設定 | CRITIC R / W / S | M/S/E counts | thresholds | 全局 SSE |
| --- | --- | --- | --- | --- |
| 原 23（原 identities 新 screening 相同） | 0.434081325181 / 0.335229465563 / 0.230689209256 | 9 / 9 / 5 | 0.247782391764 / 0.485190859747 | 0.146972733252 |
| 重建 60，完整 refit | 0.487216995918 / 0.286080322712 / 0.226702681371 | 35 / 19 / 6 | 0.272564252422 / 0.505236449127 | 0.260494025998 |
| 同 60，固定舊預處理/閾值 | 固定原 23 權重 | 43 / 12 / 5 | 固定原 23 閾值 | 不重新擬合 |

Table 4 所有六位小數數值的最大絕對誤差為 4.819e-7；Table 12 為 4.286e-7，均符合原表六位小數的 0.5e-6 舍入界限。Table 11 權重按相同六位界限檢查；頻率以百分數保留兩位，使用 0.005 個百分點的界限，最大誤差為 0.003333 個百分點。counts 精確匹配，分數形式的頻率另按精確算術比對。

完整逐項值、正負誤差、絕對誤差與容差見 `paper_comparison.csv` 及 `clean_environment/paper_comparison.csv`。六個原 identities 的分類在完整 60-event refit 後改變，可見 `original23_label_migration.csv`；固定舊規則與完整 refit 的分類不能混用。

## 敏感性實驗

### 原 23 完整穩定性流程

**PASS：原程式在新輸出目錄完整執行，獨立驗證通過。** 全部 9,032 個 resample fits 成功：event bootstrap 3,000、fixed preprocessing 3,000、year bootstrap 2,000、80% subsampling 1,000、leave-one-event-out 23、leave-one-year-out 9；另執行 400 次 initialization 診斷、K=1–6 baseline 診斷，以及 500×4 個 K-bootstrap 診斷。

原獨立驗證腳本重新檢查 9,032 行、252 個分位數摘要行及 49 個 production spot reruns，全部通過。20 張新生成數值 CSV 與原保存表逐項完全相同，max absolute error = 0；所有抽樣索引亦重新生成並與歷史相同。

**限制：其中 37 個 resampling Lloyd fits 並非其樣本的一維全局最優。** 這與原保存紀錄相同，並不代表核心 23/60 baseline 非全局最優；兩個核心 baseline 已經窮舉確認。這個已存在的局部最優現象應在解讀敏感性結果時保留，不能聲稱所有重抽樣 fits 都達到全局最優。

證據：`stability/verification.json`、`stability/historical_comparison.json`、`stability/tables/resample_runs.csv`、`stability_execution.log`、`stability_verification.log`。

### 重建 60 完整條件性 resampling

**PASS：另行獨立重算 2,009 fits。** 使用實際 60-event R/W/S 及入選 ledger 的 year/overlap episode 分組，按 PCG64 seed=20261104 重新生成 9 次 leave-one-year-out、1,000 次 overlap-episode bootstrap、1,000 次 year-block bootstrap。所有 fits 成功；每次以一維全局三段枚舉求解，沒有用歷史 labels 或歷史 indices 當輸入。

重算完成後才與歷史 `analysis/stability_runs.csv` 比較，27 組 method/metric 的最大誤差為 1.8874e-15；獨立生成的所有 indices 與歷史逐項一致。這些分布只屬 conditional sensitivity，不能解讀為年風險、氣候趨勢或可信區間。

證據：`stability60/verification.json`、`stability60/historical_comparison.csv`、`stability60/stability_runs.csv`、`stability60/fresh_resample_indices.json`。

## 環境與重跑

版本：Python 3.12.8、NumPy 2.5.4、pandas 2.3.3、scikit-learn 1.9.1、threadpoolctl 3.7.0、PyYAML 6.0.3。精確 interpreter、平台、套件版本、配置與命令見 `environment.json` 及 `clean_environment/environment.json`。完整 stability 在原研究環境執行；核心 23/60 額外在本次全新安裝的 isolated environment 通過。

從倉庫根目錄，以包含上述依賴的 Python 執行，並指定新的目錄名稱：

```sh
python audit/reproducibility_20261118/scenarios/reproduce_scenarios.py --output audit/reproducibility_20261118/scenarios/new_core_run
python 03_Experiments/Scenario_Stability/code/run_analysis.py --output audit/reproducibility_20261118/scenarios/new_stability_run
python 03_Experiments/Scenario_Stability/code/verify_results.py --output audit/reproducibility_20261118/scenarios/new_stability_run
```

`reproduce_stability60.py` 與 `compare_stability.py` 是本次額外審查程式，預設寫入本目錄下 `stability60/`、`stability/`；重跑前應另複製整個審查工作目錄，避免覆蓋本次新證據。

未解決 identities 仍為 `TC2017_06`、`TC2021_02_E`、`TC2021_02_W`。本次可復算證據證明已找回輸入下的數值計算成立，沒有證明成本、資源、收益係數經過實地校準，也沒有證明 model scores 等於實際經濟損失或受保護人口。
