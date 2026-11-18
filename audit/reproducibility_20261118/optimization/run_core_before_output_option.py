from pathlib import Path
from dataclasses import replace
import sys,json,platform,hashlib,importlib.metadata as md,time,csv
ROOT=Path(__file__).resolve().parents[3]
sys.path[:0]=[str(ROOT/'02_Model'),str(Path(__file__).resolve().parent)]
from crisp_parameters import load_inputs,_parameters_to_json
from crisp_model import Runner,PumpFleet,load_case_settings
from independent_enumeration import enumerate_case
OUT=Path(__file__).resolve().parent
paths=[ROOT/'01_Data/CRISP_Master_Data.xlsx',ROOT/'03_Experiments/Experiment_Protocol.json',ROOT/'02_Model/crisp_parameters.py',ROOT/'02_Model/crisp_model.py',OUT/'independent_enumeration.py',Path(__file__)]
p=load_inputs(paths[0]);settings=load_case_settings(paths[0],paths[1]);fleet=PumpFleet(**{**settings['primary_case'],'accessible_locations':tuple(settings['primary_case']['accessible_locations'])})
manifest={'python':sys.version,'platform':platform.platform(),'executable':sys.executable,'packages':{n:md.version(n) for n in ['gurobipy','numpy','pandas','scipy','openpyxl']},'input_sha256':{str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},'source':'actual master workbook, not saved baseline_inputs/solutions','scope':'conditional method validation; illustrative resource/cost/benefit coefficients held fixed','settings':settings}
# Manifest is written below after dataset arguments have been parsed.
# Fresh 60-case classifications generated in the sibling audit, not historical summary.
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--counts-file',type=Path);ap.add_argument('--skip-original23',action='store_true');args=ap.parse_args()
cases=[] if args.skip_original23 else [('original23',p)]
if args.counts_file:
    update=json.loads(args.counts_file.read_text());raw=update['fits']['reconstructed60'];counts=dict(zip(p.scenarios,raw['counts']));N=sum(counts.values());assert N==60
    p60=replace(p,probabilities={s:counts[s]/N for s in p.scenarios});cases.append(('reconstructed60',p60))
    manifest['fresh_scenario_counts_input']={'path':str(args.counts_file),'sha256':hashlib.sha256(args.counts_file.read_bytes()).hexdigest(),'counts':counts}
(OUT/('environment_and_inputs_60.json' if args.skip_original23 else 'environment_and_inputs_23.json')).write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
rows=[];comparison=[];started=time.monotonic()
for name,q in cases:
    directory=OUT/'core'/name;directory.mkdir(parents=True,exist_ok=False)
    (directory/'inputs_from_workbook.json').write_text(json.dumps(_parameters_to_json(q),indent=2,ensure_ascii=False))
    runner=Runner(directory)
    try:
        for model,f in [('legacy',None),('mobile',fleet)]:
            solved=runner.evaluate(q,{'id':model+'_baseline','experiment':'baseline'},fleet=f)
            enumerated=enumerate_case(q,f)
            (directory/(model+'_enumeration.json')).write_text(json.dumps(enumerated,indent=2,ensure_ascii=False))
            for metric in ['rp','ws','ev','eev','vss','evpi']:
                delta=enumerated[metric]-solved['summary'][metric]
                comparison.append({'dataset':name,'model':model,'metric':metric,'gurobi':solved['summary'][metric],'enumeration':enumerated[metric],'delta':delta,'status':'PASS' if abs(delta)<1e-6 else 'FAIL'})
            assert all(abs(enumerated[k]-solved['summary'][k])<1e-6 for k in ['rp','ws','ev','eev','vss','evpi'])
            rows.append({'dataset':name,'model':model,**solved['summary']})
            print(name,model,solved['summary'],flush=True)
        (directory/'solver_audit.json').write_text(json.dumps(runner.audit,indent=2))
    finally:runner.close()
for filename,records in [('core60_metrics.csv' if args.skip_original23 else 'core_metrics.csv',rows),('independent_core60_comparison.csv' if args.skip_original23 else 'independent_core_comparison.csv',comparison)]:
    with (OUT/filename).open('w',newline='') as stream:
        w=csv.DictWriter(stream,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
(OUT/('core60_validation.json' if args.skip_original23 else 'core_validation.json')).write_text(json.dumps({'status':'PASS','configurations':len(rows),'metric_checks':len(comparison),'all_independent_enumeration_matches':True,'max_abs_difference':max(abs(row['delta']) for row in comparison),'elapsed_seconds':time.monotonic()-started},indent=2))
