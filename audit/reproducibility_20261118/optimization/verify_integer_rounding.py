"""Explain small raw HiGHS objective gaps using integer decision reconstruction.
The exact original independent matrix code is copied below at execution time,
changing its return value only; its objective, constraints and solver options
remain byte-for-byte unchanged. This does not change any scientific parameter.
"""
from pathlib import Path
import importlib.util,inspect,json,csv,time
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
path=ROOT/'03_Experiments/Optimization/code/verify_results.py'
spec=importlib.util.spec_from_file_location('matrix_rounding_source',path);checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
source=inspect.getsource(checker.highs).replace('return -float(result.fun)',"return {'objective':-float(result.fun),'rounded_objective':-float(objective @ np.rint(result.x)), 'max_integrality_error':float(np.max(np.abs(result.x-np.rint(result.x)))), 'max_rounded_constraint_violation':float(np.max(np.array(rows) @ np.rint(result.x)-np.array(rhs)))}")
(OUT/'highs_rounding_builder_snapshot.py').write_text(source)
exec(compile(source,str(OUT/'highs_rounding_builder_snapshot.py'),'exec'),checker.__dict__)
rows=[];started=time.monotonic()
for dataset,folder in [('original23','original23_555'),('reconstructed60','reconstructed60_555')]:
    for f in sorted((OUT/folder/'solutions').glob('*.json')):
        raw=json.loads(f.read_text())
        if raw['config']['id'].startswith('old23_verification_'):continue
        p=checker.unpack(raw['parameters']);allowed=set(raw['config'].get('allowed',p['life_score']))
        solved=checker.highs(p,raw['fleet'],allowed)
        row={'dataset':dataset,'id':raw['config']['id'],**solved,'gurobi_objective':raw['summary']['rp'],'raw_objective_abs_gap':abs(solved['objective']-raw['summary']['rp']),'rounded_objective_abs_gap':abs(solved['rounded_objective']-raw['summary']['rp'])}
        row['status']='PASS' if row['raw_objective_abs_gap']<1e-5 and row['rounded_objective_abs_gap']<1e-8 and row['max_rounded_constraint_violation']<1e-6 else 'FAIL'
        rows.append(row)
    print(dataset,'complete',flush=True)
assert len(rows)==1110,len(rows)
with (OUT/'independent_integer_rounding_rows.csv').open('w',newline='') as stream:
    w=csv.DictWriter(stream,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
result={'status':'PASS' if all(row['status']=='PASS' for row in rows) else 'FAIL','configurations':len(rows),'failures':sum(row['status']=='FAIL' for row in rows),'max_raw_objective_abs_gap':max(row['raw_objective_abs_gap'] for row in rows),'max_rounded_objective_abs_gap':max(row['rounded_objective_abs_gap'] for row in rows),'max_integrality_error':max(row['max_integrality_error'] for row in rows),'max_rounded_constraint_violation':max(row['max_rounded_constraint_violation'] for row in rows),'elapsed_seconds':time.monotonic()-started,'interpretation':'Raw solver floating point decision coordinates are within integer tolerances. Integer reconstruction is checked against every independently built inequality, then against the Gurobi RP objective.'}
(OUT/'independent_integer_rounding_validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
