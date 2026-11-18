"""Compare newly solved metrics to printed manuscript and archived results."""
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import csv,json,hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
metrics=['rp','ws','ev','eev','vss','evpi']
new={}
for dataset,folder in [('original23','original23_555'),('reconstructed60','reconstructed60_555')]:
    with (OUT/folder/'summary.csv').open(encoding='utf-8-sig') as stream:
        new[dataset]={r['id']:r for r in csv.DictReader(stream)}
paper=ROOT/'manuscript_revision/CRISP_Merged_Manuscript.docx'
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
root=ET.fromstring(ZipFile(paper).read('word/document.xml'))
tables=[]
for t in root.findall('.//w:tbl',ns):
    tables.append([[''.join(c.itertext()) for c in row.findall('w:tc',ns)] for row in t.findall('w:tr',ns)])
rows=[]
def cmp(table,model,metric,column,paper_value,recomputed):
    reference=float(paper_value.replace('−','-').replace('+',''))
    error=recomputed-reference
    rows.append({'table':table,'model':model,'metric':metric,'column':column,'paper_text':paper_value,'recomputed':recomputed,'signed_error':error,'absolute_error':abs(error),'rounding_tolerance':0.000000501,'status':'PASS' if abs(error)<=0.000000501 else 'FAIL'})
for model,row in zip(['legacy_baseline','mobile_baseline'],tables[5][1:]):
    for metric,text in zip(metrics,row[1:]):cmp(6,model,metric,'original23',text,float(new['original23'][model][metric]))
for row in tables[13][1:]:
    label,metric,oldtext,newtext,deltatext=row
    model='legacy_baseline' if label=='Legacy abstract' else 'mobile_baseline'
    old=float(new['original23'][model][metric.lower()]);fresh=float(new['reconstructed60'][model][metric.lower()])
    for col,text,value in [('original23',oldtext,old),('reconstructed60',newtext,fresh),('delta',deltatext,fresh-old)]:cmp(14,model,metric.lower(),col,text,value)
with (OUT/'paper_table6_table14_comparison.csv').open('w',newline='') as stream:
    writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
history=[]
for dataset,path in [('original23',ROOT/'04_Results/Optimization/summary.csv'),('reconstructed60',ROOT/'manuscript_revision/audit/ci01_independent_20261104/backend_probability60/summary.csv')]:
    with path.open(encoding='utf-8-sig') as stream:old={r['id']:r for r in csv.DictReader(stream)}
    assert set(old)==set(new[dataset])
    for ident,r in new[dataset].items():
        errors={metric:float(r[metric])-float(old[ident][metric]) for metric in metrics}
        history.append({'dataset':dataset,'id':ident,'experiment':r['experiment'],**{f'delta_{k}':v for k,v in errors.items()},'max_abs_error':max(abs(v) for v in errors.values()),'plan_matches':r['plan']==old[ident]['plan'],'new_pumps_match':float(r['new_pumps'])==float(old[ident]['new_pumps']),'status':'PASS' if max(abs(v) for v in errors.values())<1e-9 and r['plan']==old[ident]['plan'] else 'FAIL'})
with (OUT/'historical_1110_comparison.csv').open('w',newline='') as stream:
    writer=csv.DictWriter(stream,fieldnames=list(history[0]));writer.writeheader();writer.writerows(history)
result={'status':'PASS' if all(r['status']=='PASS' for r in rows+history) else 'FAIL','paper_cells_compared':len(rows),'paper_failures':sum(r['status']=='FAIL' for r in rows),'max_abs_paper_rounding_error':max(r['absolute_error'] for r in rows),'historical_configurations_compared':len(history),'historical_failures':sum(r['status']=='FAIL' for r in history),'max_abs_historical_metric_difference':max(r['max_abs_error'] for r in history),'paper_sha256':hashlib.sha256(paper.read_bytes()).hexdigest()}
(OUT/'comparison_validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
