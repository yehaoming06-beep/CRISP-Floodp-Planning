"""Build a self-contained reading report from saved numerical results and figures."""
import argparse
import base64
import html
import json
import re
from pathlib import Path
import markdown
import numpy as np
import pandas as pd

BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parents[1]
INPUTS=ROOT/"01_Data/Events"
S=['Moderate','Severe','Extreme']; Q=['rainfall','sea_level','storm_surge']
MN={'event_bootstrap':'事件bootstrap','year_bootstrap':'年份分塊bootstrap','fixed_preprocess':'凍結歸一化與權重',
    'subsample80':'18/23不放回子抽樣','leave_one_event':'逐事件刪除','leave_one_year':'逐年刪除'}

def number(x):
    if pd.isna(x): return '—'
    if isinstance(x,(float,np.floating)): return f'{x:.4f}'
    return str(x)

def md_table(df):
    rows=['| '+' | '.join(map(str,df.columns))+' |','| '+' | '.join(['---']*len(df.columns))+' |']
    rows+=['| '+' | '.join(number(v).replace('|','/').replace('\n',' ') for v in row)+' |' for row in df.itertuples(index=False,name=None)]
    return '\n'.join(rows)

def main(out):
    t=out/'tables'; f=out/'figures'
    r=pd.read_csv(t/'resample_runs.csv'); sm=pd.read_csv(t/'resample_summary.csv')
    w=pd.read_csv(t/'baseline_weights.csv'); bs=pd.read_csv(t/'baseline_scenarios.csv'); e=pd.read_csv(t/'baseline_events.csv')
    memberships=pd.read_csv(t/'event_membership_stability.csv'); ranks=pd.read_csv(t/'weight_rank_frequencies.csv')
    k=pd.read_csv(t/'k_diagnostics.csv'); kb=pd.read_csv(t/'k_bootstrap_runs.csv')
    a=json.loads((out/'baseline_audit.json').read_text()); counts=json.loads((out/'run_counts.json').read_text())
    def stat(m,metric): return sm[(sm.method==m)&(sm.metric==metric)].iloc[0]
    def interval(m,metric):
        v=stat(m,metric); return f'{v.q025:.4f}–{v.q975:.4f}'
    tables={}
    def table(name,df):
        tables[name]=df
        df.to_csv(t/(name+'.csv'),index=False)
        # Plain LaTeX tabular: no optional dataframe template dependencies.
        escape=lambda x: number(x).replace('\\','\\textbackslash{}').replace('_','\\_').replace('%','\\%').replace('&','\\&').replace('#','\\#')
        rows=['\\begin{tabular}{'+'l'*len(df.columns)+'}','\\hline',
              ' & '.join(escape(c) for c in df.columns)+' \\\\','\\hline']
        rows+=[' & '.join(escape(v) for v in row)+' \\\\' for row in df.itertuples(index=False,name=None)]
        rows+=['\\hline','\\end{tabular}']
        (t/(name+'.tex')).write_text('\n'.join(rows),encoding='utf-8')
        return md_table(df)
    wt=[]
    for _,row in w.iterrows():
        q=row.indicator
        wt.append({'指標':q,'基線權重':row.weight,'事件95%範圍':interval('event_bootstrap','w_'+q),
            '年份95%範圍':interval('year_bootstrap','w_'+q),
            '事件權重居首比例':ranks[(ranks.method=='event_bootstrap')&(ranks.indicator==q)].top_weight_fraction.iloc[0]})
    stability=[]
    for method,cnt in counts.items():
        v=stat(method,'ARI'); ex=stat(method,'exact_projection_ARI'); hs=stat(method,'H_spearman')
        stability.append({'方法':MN[method],'成功/嘗試':f"{cnt['successful']}/{cnt['attempted']}",
            'ARI中位數':v['median'],'ARI範圍':f'{v.q025:.4f}–{v.q975:.4f}' if 'leave_' not in method else f'{v["min"]:.4f}–{v["max"]:.4f}',
            '全局解ARI中位數':ex['median'],'H排序Spearman中位數':hs['median']})
    frequencies=[]
    for _,row in bs.iterrows():
        s=row.scenario
        frequencies.append({'場景':s,'事件數':int(row['count']),'原頻率':row.probability,
            '事件完整流程95%範圍':interval('event_bootstrap','p_train_'+s),
            '年份完整流程95%範圍':interval('year_bootstrap','p_train_'+s),
            '固定分類Wilson95%參照':f'{row.wilson_low_fixed_labels:.4f}–{row.wilson_high_fixed_labels:.4f}'})
    centers=[]; reps=[]
    for i,s in enumerate(S):
        centers.append({'量':s+' center','原值':bs.center.iloc[i],
            '事件95%範圍':interval('event_bootstrap','center_'+s),'年份95%範圍':interval('year_bootstrap','center_'+s)})
        for q in Q:
            reps.append({'場景':s,'指標':q,'原代表均值':bs['mean_'+q].iloc[i],
                '事件95%範圍':interval('event_bootstrap','rep_'+s+'_'+q),
                '年份95%範圍':interval('year_bootstrap','rep_'+s+'_'+q)})
    for i in [1,2]:
        centers.append({'量':'tau'+str(i),'原值':a['thresholds'][i-1],
            '事件95%範圍':interval('event_bootstrap','tau'+str(i)),
            '年份95%範圍':interval('year_bootstrap','tau'+str(i))})
    member=memberships[memberships.method=='event_bootstrap'].merge(e[['event_id','event_name','H']],on='event_id')
    member=member[['event_id','event_name','H','baseline_scenario','agreement','p_Moderate','p_Severe','p_Extreme','n_oob','oob_agreement']]
    exactstats=[]
    for method,g in r.groupby('method',sort=False):
        exactstats.append({'方法':MN[method],'擬合數':len(g),'非全局最低SSE數':int((g.lloyd_sse_gap>1e-10).sum()),
            'Lloyd平均ARI':g.ARI.mean(),'全局解平均ARI':g.exact_projection_ARI.mean(),
            '最大SSE差':g.lloyd_sse_gap.max()})
    winners=kb.loc[kb.groupby('replicate').silhouette.idxmax(),'k'].value_counts().reindex(range(2,6),fill_value=0)
    kw=pd.DataFrame({'K':winners.index,'勝出次數':winners.values,'比例':winners.values/kb.replicate.nunique()})
    contrasts=[]
    for method in ['event_bootstrap','year_bootstrap']:
        g=r[r.method==method]
        for q1,q2 in [('rainfall','sea_level'),('sea_level','storm_surge')]:
            vals=(g['w_'+q1]-g['w_'+q2]).to_numpy()
            contrasts.append({'方法':MN[method],'權重差':q1+' - '+q2,
                'q025':np.quantile(vals,.025),'中位數':np.median(vals),'q975':np.quantile(vals,.975),
                '差大於零比例':np.mean(vals>0)})
    loo=r[r.method=='leave_one_event'][['deleted_event','ARI','agreement','w_rainfall','w_sea_level','w_storm_surge','p_train_Extreme']]
    lyo=r[r.method=='leave_one_year'][['deleted_year','n_train','ARI','agreement','w_rainfall','w_sea_level','w_storm_surge']]
    lyo.deleted_year=lyo.deleted_year.astype(int)
    alt=pd.read_csv(t/'competing_partitions.csv'); competitor=alt[(alt.count_Moderate==17)&(alt.count_Severe==4)&(alt.count_Extreme==2)].iloc[0]
    init=pd.read_csv(t/'initialization_runs.csv')
    nonoptimal=int((r.lloyd_sse_gap>1e-10).sum())
    manifest=json.loads((out/'manifest.json').read_text())
    verify=json.loads((out/'verification.json').read_text()) if (out/'verification.json').exists() else {'status':'尚未執行'}
    repro=json.loads((out/'reproducibility.json').read_text()) if (out/'reproducibility.json').exists() else {'status':'尚未執行'}
    captions=json.loads((f/'captions.json').read_text())
    text=f'''# 23條事件的CRITIC權重與K-means場景穩定性審核

日期：2026-11-03。審核對象：CRISP R-W-S fallback，2017—2025年23條已選事件。

更正紀錄 2026-11-04：原文及圖9說明將連續三段切分數誤寫為253，現更正為231，即C(22,2)。僅更正計數文字；凍結輸入、SSE、分類及重抽樣結果未改動。

## Material Passport

本報告使用`01_Data/Events/`中凍結的模型輸入、事件來源名錄、原設定及已存結果，統一使用當前生產管線與兩張參考表格，歷史副本已歸檔。計算與原輸出已重現並進行數值核查。這不等於逐條核實香港天文台原始觀測，也不證明樣本完整或代表Tai O全部洪水。無插補、無事件刪除、無數值缺失、無重複三指標向量。分析階段及復現驗證均已完成；沒有尚待批准的計算步驟。

## 1. 可支持的結論

1. **基線計算正確且可重現**：CRITIC權重為{w.weight.iloc[0]:.6f}、{w.weight.iloc[1]:.6f}、{w.weight.iloc[2]:.6f}；23個H及分類與原管線、已存CSV一致。K=3類大小為9/9/5。
2. **權重存在可見抽樣不確定性**：降雨權重在事件bootstrap中居首的比例為{ranks[(ranks.method=='event_bootstrap')&(ranks.indicator=='rainfall')].top_weight_fraction.iloc[0]:.1%}。不能將基線排序視作確定結論，也不能將資料離散性權重解讀成災害因果貢獻或政策偏好。
3. **分群對樣本變動敏感**：事件bootstrap ARI中位數{stat('event_bootstrap','ARI')['median']:.3f}，年份bootstrap為{stat('year_bootstrap','ARI')['median']:.3f}。即使凍結歸一化與權重、只重擬合聚類，也沒有消除不穩定性。
4. **固定基線上隨機初始化穩定，不代表樣本穩定**：原設定n_init=50時，200個種子全部回到同一分類；單次初始化ARI最小為{init[init.n_init==1].ARI.min():.3f}。對重抽樣資料，仍有{nonoptimal}/{len(r)}次50初始化未達全局最低SSE，已另計全局解ARI作對照，沒有隱藏這項算法誤差。
5. **三類應視為建模用的相對分級**：全樣本K=2輪廓系數{k.loc[k.k==2,'silhouette'].iloc[0]:.3f}，高於K=3的{k.loc[k.k==3,'silhouette'].iloc[0]:.3f}。目前證據不足以確認存在三種天然、可外推的災害類型。

## 2. 資料與適用範圍

降雨是事件日前後各2日（共5日）窗口的**最大日累積雨量**，不是最大小時雨強。海平面是Shek Pik最高水位（mCD），S保留該站官方表中的天文潮以上增水（m），不是Tai O淹水深度；E020的0.66 m是東北季風與Man-yi共同作用造成的maximum sea level rise，不是分離估計的純台風分量。三項最大值未必同時發生。降雨來源包含19條Ngong Ping、3條機場、1條Discovery Bay記錄，站點混用可能影響尺度與相關性。原始來源URL、站點及品質註記完整保留於`01_Data/Events/event_metadata.csv`。

年份分布：

{table('T01_year_counts',pd.read_csv(t/'year_counts.csv'))}

總量只有23事件、9年份塊；Extreme基線只有5事件。抽樣入選規則及未入選事件的母體名錄尚不完整。這是**選定事件中的條件分布**，不是所有日、所有年份、全部洪水或未來氣候下的無條件分布。年份並非密集時間序列，不能藉此估計可靠的自相關或長期氣候趨勢。

## 3. 基線公式、實作及論文表格核對

各指標均採「數值越大，危害分數越高」方向，逐欄Min-Max：`z_ij=(x_ij-min_j)/(max_j-min_j)`；Pearson相關矩陣為r；`C_j=sd(z_j)×Σ_k(1-r_jk)`，`w_j=C_j/ΣC_j`；`H_i=Σ_j w_j z_ij`。這個變異與衝突的加權思想來自[CRITIC原論文](https://doi.org/10.1016/0305-0548(94)00059-H)，本次對具體公式及邊界處理以歸檔程式作為可執行定義。

K-means只作用在一維H，並非三項原指標的多變量聚類。固定K=3、seed=42、n_init=50、max_iter=300、Lloyd；按中心遞增標為Moderate/Severe/Extreme。兩個閾值為相鄰中心中點，等於閾值時歸入較高類。初始化設定依[scikit-learn KMeans文件](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)明確指定，避免版本預設值改變。

{table('T02_baseline_critic',w)}

原CSV權重最大絕對差{a['max_abs_weight_error']:.2e}；H最大差{a['max_abs_H_error']:.2e}。與生產管線H最大差{a['production_H_max_abs_error']:.2e}。枚舉排序23條H的全部231種二切點（C(22,2)），基線K=3 SSE={a['exact_global_sse']:.12f}，確認達到全局最低值。

ddof=0改為1時，三個標準差同乘√(23/22)={a['ddof_std_ratio']:.6f}，CRITIC歸一權重因共同因子抵消而不變（數值差{a['ddof_weight_max_abs_change']:.2e}）。論文中標準差和信息量仍應與設定統一，不能因最終權重相同便混用中間量。

**展示用XLSX核對**：兩張原表的權重、9/9/5計數、頻率及四捨五入的代表值與基線相符。但CRITIC表把降雨描述為“Maximum rainfall intensity”，與最大日總雨量的實際輸入不符；場景表“Representative Rainfall (mm)”也未交代5日窗口及日累積基礎。建議改為“Event-window maximum daily rainfall (mm/day)”，並把Probability標為“Conditional frequency among selected events”。原表已保留，未直接覆寫。單元格抽取存於`publication_table_cells.json`。

## 4. 重抽樣與穩定性設計

方案在本次運算前保存於`分析方案.md`，屬探索性審核而非外部預註冊。主種子20261103；NumPy SeedSequence為事件、年份、子抽樣建立獨立亂數流。全部抽樣索引（從0起算）保存在`resample_indices.json`，含事件ID順序與年份抽中名單。

- 事件bootstrap：有放回抽23行，B=3000，完整重估Min-Max、CRITIC、H、K=3。
- 年份分塊bootstrap：從9個已觀察年份中有放回抽9個年份塊，B=2000，每塊所有事件完整保留，樣本長度可變。這是年份cluster bootstrap，不是按連續年份窗口的moving-block bootstrap。
- 凍結預處理對照：使用與事件bootstrap相同的3000組索引，固定全樣本Min-Max和CRITIC權重，只重擬合K=3。這是敏感性對照，不是無資料洩漏的驗證流程。
- 80%子抽樣：不放回抽18條，B=1000；逐事件刪除23次；逐年份刪除9次。

重抽樣的重複行保留為抽樣權重，沒有被去重。每次依當次訓練Min-Max、權重和中心，將**共同23條原始事件投射**後比較。投射值超出訓練[0,1]時不裁切，因未見極值是抽樣敏感性的一部分。所有ARI、共分群及按排序等級對齊的Jaccard使用共同23行；場景訓練頻率則分母為當次重抽樣行數，另存原23行投射頻率。

ARI採機會校正，1表示兩分類完全一致；它不是洪水分類準確率，沒有真實標籤可用。[ARI官方定義](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_rand_score.html)。本次Jaccard是**按中心等級對齊的投射集合交並比**，不等同於Hennig原方法中逐群取最大相似群的bootstrap統計；[Hennig原論文](https://doi.org/10.1016/j.csda.2006.11.025)也指出穩定性本身不保證類型有意義。

區間統一採成功擬合的2.5%及97.5%經驗分位數。這是條件於現有資料與抽樣機制的**95%重抽樣範圍**，沒有在n=23、Min-Max極值和離散分類下證明名義覆蓋率。刪除檢驗只報最小至最大值。完整明細保留退化原因和成功分母，本次全部成功，0次退化或排除。

## 5. CRITIC權重結果

{table('T03_weight_ranges',pd.DataFrame(wt))}

{table('T04_weight_contrasts',pd.DataFrame(contrasts))}

兩個權重邊際區間重疊不等於差異檢定，故另報配對權重差與差大於零的比例；這些比例不解讀成權重大小關係為真的貝氏後驗機率或p值。標準差與相關性都是從同一小樣本估得，重抽樣數增加不會增加獨立事件數。

## 6. 分群穩定性、近似競爭分割與算法誤差

{table('T05_stability',pd.DataFrame(stability))}

完整資料全局解9/9/5的SSE為{a['exact_global_sse']:.6f}；另有17/4/2的自洽局部解，SSE為{competitor.sse:.6f}，僅多{competitor.sse_gap:.6f}（{competitor.sse_gap/a['exact_global_sse']:.2%}），但對原分類ARI僅{competitor.ARI_to_baseline:.3f}。這種低目標差而高分類差的競爭切分，解釋為何很小的樣本變化也可造成大幅類別變動。`competing_partitions.csv`還列出其他連續切分；其中self_consistent=False的強制切分並非Lloyd固定點，不應稱為另一個自洽K-means解。

{table('T06_global_optimum_audit',pd.DataFrame(exactstats))}

全局解審核採獨立的排序切點枚舉／前綴和SSE公式；以1e-10判定Lloyd非最優。主分析保留原50次初始化結果，另報全部重抽樣的全局投射ARI，因此可以看出樣本不穩定並非主要由隨機初始化造成。H排序的Spearman相關通常高於離散分類一致性，意味分數排序與三類邊界的穩定性需要分開判斷。

## 7. 場景頻率、中心、閾值及代表量

{table('T07_scenario_frequencies',pd.DataFrame(frequencies))}

Wilson欄只是假設事件獨立且分類事先固定時的逐類二項95%參照，忽略資料選擇、年內依賴與分類估計，並不是完整流程區間或三類同時區間。完整流程Extreme的事件bootstrap中位數為{stat('event_bootstrap','p_train_Extreme')['median']:.4f}，低於基線{bs.probability.iloc[2]:.4f}；排序後最上層類在部分重抽樣中只代表少數最頂端事件，不能將其視為固定不變的同一種物理極端災害。

{table('T08_centers_thresholds',pd.DataFrame(centers))}

每次重估Min-Max與權重後，H的座標系也改變。中心及閾值區間是整個程序的輸出變動範圍，不能直接當成固定物理刻度上的門檻信賴區間。以下原量綱代表值是每次**訓練類內算術均值**，含重複抽樣行：

{table('T09_representative_hazards',pd.DataFrame(reps))}

代表量和綜合分數不是物理聯合水文模型。本次不把代表量重新注入後端MILP，也不宣稱這些區間等於決策效益的不確定性；主模型目前使用固定輸入概率，後續若傳播到決策層，需明確聯動機制，不能只替換結果表。

## 8. 逐事件與刪除影響明細

下表為全部23條記錄。agreement是3000次事件bootstrap投射回原分類的比例；p欄是投射到三類的比例。OOB是該事件完全未被抽入訓練時的子集，分母n_oob另列。OOB比較對象仍是使用過全樣本的基線分類，不能稱為外部準確率。

{table('T10_all_event_stability',member)}

最不穩定者包括E017 Koinu、E011 Kompasu與E015 Talim，並非只涉及原始閾值最近的一條事件。完整流程可能整體更換切分方式，因此需要共分群圖輔助理解。

{table('T11_leave_one_event',loo)}

{table('T12_leave_one_year',lyo)}

逐事件刪除後，降雨權重仍全部居首；但分群ARI最低達{stat('leave_one_event','ARI')['min']:.3f}。兩種穩定性並不能互相替代。以上範圍是完整刪除集合的影響診斷，不是抽樣分布的信賴區間。

## 9. K的敏感性

{table('T13_k_diagnostics',k)}

{table('T14_bootstrap_k_preference',kw)}

輪廓系數衡量群內緊密度與群間分離度，詳見[官方定義](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html)。K=2在基線輪廓系數較高；其他指標也不一致支持K=3，較大K還產生2條甚至1條記錄的小群。前500次事件bootstrap只在K=2—5中比較輪廓系數，沒有把K=6納入這項抽樣比較；含重複行的內部指標偏好不能直接當作真實K的機率。若需要三個決策場景，可保留K=3作規劃約定，但必須同時揭露分類穩定性不足。

## 10. 樣本量限制與可行性邊界

- **不可從23條提高到3000條證據**：B只控制蒙地卡羅精度。事件B=3000的任一比例估計最大蒙地卡羅標準誤約0.0091；年份B=2000約0.0112。這不是母體估計誤差，分位端點仍有模擬波動。
- **事件獨立性未證明**：同年事件及重疊天氣背景可能相關。年份分塊保留年內依賴，但僅9塊，且仍假設年份可交換，未處理跨年依賴、氣候趨勢或取樣機制改變。不能因做過分塊就宣稱依賴問題解決。依賴資料需要保留相應結構的抽樣設計，可參照[統計課程的dependent-data bootstrap說明](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/ADAfaEPoV.pdf)。
- **極端尾部覆蓋不足**：5個Extreme記錄不足以估計罕見尾部、重現期、百年洪水、極值分布或氣候變遷效應。未觀察到的更極端事件不可能由經驗bootstrap創造。
- **分類是從同一資料學到**：沒有獨立驗證集或洪水真實類別標籤。未使用大比例留出集或複雜多參數混合模型，因會進一步耗損極少數尾端觀測。沒有對K=3給出顯著性p值，也未把穩定性閾值當作普遍有效標準。
- **非光滑估計**：Min-Max極值、聚類切分及排序等級的變動可能不適合簡單常態近似或偏差修正信賴區間。本次不強行套用BCa或漸近標準誤；百分位範圍只作穩健性診斷。
- **資料品質與空間代理**：逐行官方來源尚未重新核驗；多站降雨代理及非同步最大值無法由重抽樣補救。需要更長且有完整入選規則的事件資料、同步本地觀測及獨立年份驗證後，才能提高實證主張。

## 11. 統計解讀完整性檢查（11項）

Simpson悖論：已展示年份組成，不作合併相關的因果解讀；生態謬誤：不從年份或群均值推斷單事件機制；偽重複：明列23事件、9年份及B；碰撞偏誤：事件篩選可能限制條件母體，無法排除；基率忽略：場景頻率明確限定在已選事件；均值回歸：不作前後改善主張；存活者／入選偏誤：未入選與缺測替代機制未充分核驗；多重搜尋：完整報告預定K對照，沒有挑顯著結果；分析分岔：保留執行前探索方案、固定種子、全部失敗計數及算法對照；相關非因果：CRITIC權重不解讀成因果；反向因果：本次沒有方向性因果估計。這些是解讀範圍檢查，不是母體偏誤已被消除的證明。

## 12. 復現、驗證與交付

Python {manifest['python'].split()[0]}，本次套件版本完整鎖定於`requirements-lock.txt`；主要套件為NumPy {manifest['packages']['numpy']}、pandas {manifest['packages']['pandas']}、scikit-learn {manifest['packages']['scikit-learn']}。固定單執行緒，避免低維小樣本運算的執行緒差異。原設定、資料、產線副本與程式SHA-256存於manifest；驗證腳本以獨立公式重算基線，逐一核查全部{len(r)}個重抽樣結果、分位摘要、代表均值、投射分類及共分群矩陣，並以原生產程式抽查重跑49次。完整第二次運算的比對狀態見`reproducibility.json`，數值核查狀態見`verification.json`。

本次數值驗證：**{verify['status']}**。完整第二次執行比較：**{repro['status']}**；20個基礎CSV逐位元一致、18個NPZ陣列精確一致、4個JSON結構一致。比較不要求PDF生成時間或輸出路徑元資料相同。圖表經實際渲染檢查，未進行外部或跨模型審查。執行時的輸入／程式雜湊與最終交付檔案雜湊分別記錄，不以後來的文件修改替代執行紀錄。

從交付目錄執行：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-lock.txt
.venv/bin/python 03_Experiments/Scenario_Stability/code/run_analysis.py
.venv/bin/python 03_Experiments/Scenario_Stability/code/verify_results.py
.venv/bin/python 03_Experiments/Scenario_Stability/code/plot_figures.py
.venv/bin/python 03_Experiments/Scenario_Stability/code/build_report.py
```

完整第二次運算另存目錄後比較：

```bash
.venv/bin/python 03_Experiments/Scenario_Stability/code/run_analysis.py --output 04_Results/Reproductions/Scenario_Stability
.venv/bin/python 03_Experiments/Scenario_Stability/code/verify_results.py --output 04_Results/Reproductions/Scenario_Stability
.venv/bin/python 03_Experiments/Scenario_Stability/code/compare_runs.py 04_Results/Scenario_Stability 04_Results/Reproductions/Scenario_Stability
```

輸出路徑不依賴目前工作目錄；`run_analysis.py`使用本交付的原管線副本，無須讀取原專案目錄。單獨重畫可用`code/gen_fig01.py`至`code/gen_fig10.py`，或`plot_figures.py --figure 02`。圖版PDF為向量輸出，PNG為300 dpi。CSV保留完整精度；報告四位小數只為閱讀，不用來回算。源資料與原模型未被改寫。

## 13. 完整圖版
'''
    for idx,(name,cap) in enumerate(sorted(captions.items()),1):
        text+=f'\n### 圖{idx}\n\n![圖{idx}](figures/{name}.png)\n\n{cap}\n\n[向量PDF](figures/{name}.pdf)\n'
    text+='\n## 14. 全部數據表與原始輸出索引\n\n'
    for path in sorted(t.glob('*.csv')):
        text+=f'- [{path.name}](tables/{path.name})\n'
    text+='\n所有摘要表亦有同名LaTeX檔（T01—T14）；圖說及LaTeX插圖片段位於figures/。`event_projections.npz`保存每次成功擬合對23行的標籤、H與OOB遮罩，方法內順序對應resample_runs.csv。`resample_summary.csv`的刪除法q欄僅為數值分位摘要，解讀時應使用min/max；所有未使用的OOB分母為0時記為缺值，不補成零。\n'
    (out/'完整分析報告.md').write_text(text,encoding='utf-8')
    body=markdown.markdown(text,extensions=['tables','fenced_code'])
    # Self-contained HTML embeds the rendered figures; table/PDF links remain useful beside the report.
    def embed(match):
        path=out/match.group(1)
        return 'src="data:image/png;base64,'+base64.b64encode(path.read_bytes()).decode()+'"'
    body=re.sub(r'src="(figures/[^\"]+\.png)"',embed,body)
    css='body{max-width:1150px;margin:45px auto;padding:0 28px;font:16px/1.7 system-ui;color:#1c2833}h1,h2,h3{line-height:1.4}h2{border-bottom:1px solid #ddd;padding-top:20px}table{border-collapse:collapse;font-size:12px;display:block;overflow-x:auto;margin:20px 0}th,td{border-bottom:1px solid #ddd;padding:7px 10px;white-space:nowrap}th{background:#f2f5f8}img{max-width:100%;height:auto}pre{background:#f4f5f6;padding:18px;overflow:auto}a{color:#006eaa}@media print{body{max-width:none;font-size:10pt}h2{break-before:page}img{max-height:85vh;object-fit:contain}table{font-size:8pt}}'
    (out/'完整分析報告.html').write_text('<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>23事件穩定性審核</title><style>'+css+'</style><body>'+body+'</body></html>',encoding='utf-8')
    print('Report saved:',out/'完整分析報告.html')

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,default=ROOT/'04_Results/Scenario_Stability'); args=ap.parse_args(); main(args.output.resolve())
