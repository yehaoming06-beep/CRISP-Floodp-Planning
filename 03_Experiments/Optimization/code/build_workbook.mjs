import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const base=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const data=JSON.parse(await fs.readFile(path.join(base,'../../04_Results/Optimization/report_data.json'),'utf8'));
const out=path.join(base,'../../04_Results/Optimization');
const qa=path.join(base,'../../04_Results/Optimization/workbook_qa');await fs.mkdir(qa,{recursive:true});
const wb=Workbook.create();const summary=wb.worksheets.add('结果概览'),raw=wb.worksheets.add('全部配置'),bounds=wb.worksheets.add('上界修正'),fleet=wb.worksheets.add('库存与并列解'),deploy=wb.worksheets.add('基准部署'),inputs=wb.worksheets.add('假设与来源');
const ink='#263340',navy='#273E58',gray='#EAF0F5';
function table(s,headers,rows,widths,name){
 const last=String.fromCharCode(64+headers.length),end=rows.length+1;
 s.showGridLines=false;s.getRange(`A1:${last}${end}`).values=[headers,...rows];
 s.getRange(`A1:${last}${end}`).format={font:{name:'Arial',size:10,color:ink},verticalAlignment:'center',rowHeight:28};
 s.getRange(`A1:${last}1`).format={fill:navy,font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:38,horizontalAlignment:'center'};
 widths.forEach((w,i)=>s.getRangeByIndexes(0,i,end,1).format.columnWidth=w);
 s.tables.add(`A1:${last}${end}`,true,name).style='TableStyleLight9';s.freezePanes.freezeRows(1);
}
const records=data.summary;
table(raw,['配置ID','实验','因素','水平','U规则','RP 分','WS 分','EV 分','EEV 分','VSS 分','EVPI 分','准备组合','购泵 台','采购 HKD','准备 CU','后悔值 分','固定策略可行'],records.map(r=>[r.id,r.experiment,r.factor,r.level,r.u_mode,r.rp,r.ws,r.ev,r.eev,r.vss,r.evpi,r.plan,r.new_pumps,r.capital_used_hkd??'不适用',r.setup_used,r.regret??'不可行',r.baseline_policy_feasible?'是':'否']),[28,22,30,14,16,17,17,17,17,17,17,75,13,18,17,17,18],'AllRuns');
raw.getRange(`F2:K${records.length+1}`).setNumberFormat('0.000000');raw.getRange(`N2:P${records.length+1}`).setNumberFormat('#,##0.000');raw.getRange(`M2:M${records.length+1}`).setNumberFormat('0');
summary.showGridLines=false;summary.tabColor=navy;
summary.getRange('A2').values=[['移动泵库存模型与实验重跑']];summary.getRange('A2').format.font={name:'Arial',size:15,bold:true,color:ink};
summary.getRange('A3').values=[['2026年11月4日计算快照。改变输入须重新求解；效益单位为模型分数。']];
summary.getRange('A5:I7').values=[['配置ID','RP 分','WS 分','EV 分','EEV 分','VSS 分','EVPI 分','购泵 台','准备组合'],['legacy_baseline',null,null,null,null,null,null,null,null],['mobile_baseline',null,null,null,null,null,null,null,null]];
for(const r of [6,7]){
 for(const [target,source] of [['B','F'],['C','G'],['D','H'],['E','I'],['H','M'],['I','L']])summary.getRange(`${target}${r}`).formulas=[[`=INDEX('全部配置'!${source}2:${source}${records.length+1},MATCH($A${r},'全部配置'!$A$2:$A$${records.length+1},0))`]];
 summary.getRange(`F${r}`).formulas=[[`=B${r}-E${r}`]];summary.getRange(`G${r}`).formulas=[[`=C${r}-B${r}`]];
}
summary.getRange('A3:I18').format.font={name:'Arial',size:10,color:ink};
summary.getRange('A5:I5').format={fill:navy,font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:34,horizontalAlignment:'center'};
summary.getRange('A6:I7').format.rowHeight=34;summary.getRange('B6:G7').setNumberFormat('0.000000');summary.getRange('H6:H7').setNumberFormat('0');
summary.getRange('A10:C16').values=[['基准条件','取值或定义','证据状态'],['新增资本预算 HKD',2000000,'实验条件，非观测政府预算'],['已有库存 台',0,'实验条件，未核实现场库存'],['单台采购参考 HKD',1000000,'官方2025设备报道近似价'],['两区抽水可达性','均可达','条件假设，另跑本土侧和不可达对照'],['运行与效益','原CU及分数','仍是示例系数，未校准为减损金额'],['检验范围','555配置；3,875次主求解','HiGHS核验全部RP；重复运行一致']];
summary.getRange('A10:C10').format={fill:navy,font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:30};summary.getRange('A11:C16').format.rowHeight=30;summary.getRange('B11:B13').setNumberFormat('#,##0');
[32,23,43,18,18,18,18,13,73].forEach((w,i)=>summary.getRangeByIndexes(0,i,18,1).format.columnWidth=w);
table(bounds,['因素','倍数','旧RP 分','修正RP 分','RP变化 分','旧EVPI 分','修正EVPI 分','EVPI变化 分'],data.corrected.map(r=>[r.factor,r.level,r.old_rp,r.corrected_rp,null,r.old_evpi,r.corrected_evpi,null]),[19,12,20,20,20,20,20,20],'BoundsCorrection');
for(let r=2;r<=data.corrected.length+1;r++){bounds.getRange(`E${r}`).formulas=[[`=D${r}-C${r}`]];bounds.getRange(`H${r}`).formulas=[[`=G${r}-F${r}`]];}
bounds.getRange('B2:B22').setNumberFormat('0.00');bounds.getRange('C2:H22').setNumberFormat('0.000000');
const ties=new Map(data.ties.map(r=>[r.case,r]));
table(fleet,['最多可购 台','资本预算 HKD','实际购泵 台','RP 分','WS 分','所选EEV 分','所选VSS 分','所有EV最优策略的VSS下界 分','所有EV最优策略的VSS上界 分'],data.fleet.map(r=>{const t=ties.get(r.level===2?'mobile_baseline':`fleet_${String(r.level).padStart(2,'0')}`);return[r.level,r.level*data.settings.primary_case.purchase_price_hkd,r.new_pumps,r.rp,r.ws,r.eev,r.vss,t.minimum_VSS_over_EV_optima,t.maximum_VSS_over_EV_optima];}),[15,22,15,19,19,19,19,29,29],'FleetSweep');
fleet.getRange('A2:C10').setNumberFormat('#,##0');fleet.getRange('D2:I10').setNumberFormat('0.000000');
table(deploy,['模型','情景','区域','措施','准备 y','部署量（泵台数或其他措施包）'],data.deployment.map(r=>[r.model,r.scenario,r.location,r.intervention,r.prepared,r.x]),[13,21,16,21,14,38],'Deployment');
deploy.getRange('E2:F43').setNumberFormat('0');
const source=data.settings.evidence.source_url;
table(inputs,['参数或约定','数值或定义','单位','状态与限制','来源'],[
 ['泵采购参考',1000000,'HKD/台，2025','近似设备采购价；非大澳专项投标或全寿命费用',source],
 ['泵资本预算',2000000,'HKD','实验条件；独立于原CU预算','本轮实验设置'],
 ['已有可调用库存',0,'台','实验条件；现场真实值未知','本轮实验设置'],
 ['基准可达性','Tai O1、Tai O2','地点','条件假设；步行桥不证明重型设备可达','本轮实验设置'],
 ['抽水部署单位','1次同时分配=1台泵','台','单位约定；原单包消耗/效益未实证校准','移动泵模型v2'],
 ['原准备与运行成本','保留原示例输入','CU','不是港元；Drainage准备成本独立于购置成本','原主参数表'],
 ['效益系数和地点系数','保留原分数与β','分数/系数','人口差异未用于重算β；不是避免损失金额','原主参数表'],
 ['Tai O1居民人口2021',825,'人','只作研究区背景，不是受淹人数','https://portal.csdi.gov.hk/geoportal/?datasetId=censtatd_rcd_1635933365202_19171&lang=en'],
 ['Tai O2居民人口2021',2853,'人','只作研究区背景，不是受淹人数','同上，完整统计小区聚合'],
 ['目标并列规则','最少采购、最少准备费用、准备编码','优先级','部分采购上限下VSS随EV并列策略而变','模型定义；并列解枚举表'],
 ['联合扰动','200组×2种U规则','参数组','假设压力测试，非置信区间；分别重新优化','固定种子20261103'],
 ['运行流量与费用','未完成现场校准','m³/h、HKD、人时','最高流量不直接进入效益，燃料/班组/通达性仍缺数据','前一轮参数证据表']
],[30,46,24,82,100],'Assumptions');
inputs.getRange('A2:E13').format.wrapText=true;inputs.getRange('A2:E13').format.rowHeight=48;
inputs.getRange('B2:B4').setNumberFormat('#,##0');inputs.getRange('B9:B10').setNumberFormat('#,##0');
wb.recalculate();
const check=await wb.inspect({kind:'region',sheetId:'结果概览',range:'A5:I7',maxChars:3500,tableMaxRows:4,tableMaxCols:9});
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!',options:{useRegex:true,maxResults:20},maxChars:1000});
await fs.writeFile(path.join(qa,'inspection.json'),JSON.stringify({summary:check.ndjson,errors:errors.ndjson},null,2));
for(const [sheetName,range,name] of [['结果概览','A2:I16','summary'],['全部配置','A1:I7','all'],['上界修正','A1:H7','bounds'],['库存与并列解','A1:I10','fleet'],['基准部署','A1:F10','deployment'],['假设与来源','A1:E6','assumptions']]){
 const img=await wb.render({sheetName,range,scale:1.4,format:'png'});await fs.writeFile(path.join(qa,`${name}.png`),new Uint8Array(await img.arrayBuffer()));
}
await(await SpreadsheetFile.exportXlsx(wb)).save(path.join(out,'CRISP_Results.xlsx'));
console.log(check.ndjson);
