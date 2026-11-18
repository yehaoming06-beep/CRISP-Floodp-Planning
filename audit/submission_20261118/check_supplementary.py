#!/usr/bin/env python3
"""Read-only archive checks; no solver calls, clustering fits or manuscript edits."""
from pathlib import Path
import csv, hashlib, json, re, collections, xml.etree.ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'audit/submission_20261118'
SUP = ROOT / 'supplementary/Supplementary_Methods_and_Results.md'
ORIGINAL = ROOT / 'manuscript_revision/Supplementary_Methods_and_Results.md'
DOC = ROOT / 'manuscript_revision/CRISP_Merged_Manuscript.docx'
V2 = 'manuscript_revision/peer_review_validation_20261105_v2/'
CI = 'manuscript_revision/audit/ci01_independent_20261104/'
files, checks, numeric = {}, [], []

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def source(path):
    p = ROOT / path
    files[path] = {'path': path, 'exists': p.is_file(), 'sha256': digest(p) if p.is_file() else None}
    return p

def rows(path):
    with source(path).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def load(path):
    return json.loads(source(path).read_text())

def check(label, value, detail=None):
    checks.append({'check': label, 'pass': bool(value), 'detail': detail})

def number(table, locator, printed, value):
    printed = str(printed).replace(',', '').replace('−', '-')
    decimals = len(printed.split('.')[1]) if '.' in printed else 0
    tol = 0.50001 * 10 ** -decimals if decimals else 1e-8
    error = abs(float(printed) - float(value))
    numeric.append({'table': table, 'locator': locator, 'printed': printed,
                    'saved_value': float(value), 'absolute_error': error,
                    'rounding_tolerance': tol, 'pass': error <= tol})

def pick(data, **key):
    match = [r for r in data if all(str(r[k]) == str(v) for k,v in key.items())]
    assert len(match) == 1, (key,len(match))
    return match[0]

text = source(str(SUP.relative_to(ROOT))).read_text()
original = source(str(ORIGINAL.relative_to(ROOT))).read_text()
# Relative navigation changes alone may differ between original and relocated copy.
strip_dest = lambda x: re.sub(r'\]\([^\n)]*\)', '](LINK)', x)
check('Reading copy scientific content unchanged', strip_dest(text) == strip_dest(original))
sections = [{'section':m.group(1),'heading':m.group(2), 'line':text[:m.start()].count('\n')+1}
            for m in re.finditer(r'^## (S\d+) (.+)$',text,re.M)]
check('S1 through S13 present exactly once', [s['section'] for s in sections] == [f'S{i}' for i in range(1,14)])
check('Tables S1 through S16 present exactly once', re.findall(r'^\*\*Table S(\d+)\.',text,re.M)==list(map(str,range(1,17))))
check('Figures S1 through S5 present exactly once', re.findall(r'^\*\*Figure S(\d+)\.',text,re.M)==list(map(str,range(1,6))))
links=[]
for m in re.finditer(r'(!?)\[([^\]]*)\]\(([^)]+)\)',text):
    target=m.group(3)
    if re.match(r'[a-z]+://',target): continue
    p=(SUP.parent / target.split('#',1)[0]).resolve()
    item={'label':m.group(2),'target':target,'path':str(p.relative_to(ROOT)),
          'exists':p.exists(),'is_image':m.group(1)=='!'}
    if p.is_file(): item['sha256']=digest(p); source(item['path'])
    links.append(item)
check('All 32 explicit local destinations exist',len(links)==32 and all(x['exists'] for x in links),len(links))

# Parse the sixteen Markdown tables following their captions.
tables={}
for m in re.finditer(r'^\*\*Table S(\d+)\.',text,re.M):
    tail=text[m.end():]
    table_match=re.search(r'\n(\|[^\n]+\n(?:\|[^\n]+\n)+)',tail)
    grid=[[c.strip() for c in line.strip().strip('|').split('|')] for line in table_match.group(1).splitlines()]
    tables[int(m.group(1))]=grid[2:]

bounds=rows(V2+'runs/primary/ev_bounds.csv')
for cells in tables[1]:
    freq=cells[0].split('-')[0]
    matches=[r for r in bounds if r['frequency']==freq and r['intervention']==cells[1]]
    check('S1 bound repeats consistently across both models/sectors '+freq+'/'+cells[1], len(matches)==4)
    for r in matches:
        for printed,key in zip(cells[2:],['U_A','effective_integer_U_A','U_B']): number('S1',str((freq,cells[1],r['model'],r['location'],key)),printed,r[key])
ev=rows(V2+'runs/primary/ev_summary.csv')
for cells in tables[2]:
    freq=cells[0].split('-')[0]; model='mobile' if 'inventory' in cells[0] else 'legacy'
    for convention in 'AB':
        r=pick(ev,frequency=freq,model=model,convention=convention)
        for printed,key in zip(cells[2:],['rp','ws','ev','selected_ev_n','selected_eev','selected_vss','evpi']):number('S2',str((freq,model,convention,key)),printed,r[key])
optima=rows(V2+'runs/primary/ev_optimal_policies.csv')
for cells in tables[3]:
    freq=cells[0].split('-')[0]; model='mobile' if 'inventory' in cells[0] else 'legacy'
    for convention in 'AB':
        group=[r for r in optima if (r['frequency'],r['model'],r['convention'],r['n'])==(freq,model,convention,cells[2])]
        check('S3 Y0/Y+ two-policy set '+str((freq,model,convention,cells[2])),{int(r['mask']) for r in group}=={5,37})
        for r in group:
            for printed,key in zip(cells[2:],['n','eev','vss']):number('S3',str((freq,model,convention,r['mask'],key)),printed,r[key])
comparison=rows(V2+'runs/primary/ev_fixed_policy_convention_comparison.csv')
for cells in tables[4]:
    r=pick(comparison,frequency=cells[0].split('-')[0],model='mobile' if 'inventory' in cells[0] else 'legacy')
    for printed,key in zip(cells[1:],['paired_policy_count','policies_with_changed_ev_value','maximum_EV_B_minus_A']):number('S4',cells[0]+'/'+key,printed,r[key])
# Table S5 describes switches rather than numerical outcomes; checked by explicit source labels.
check('S5 six component definitions present',[r[0] for r in tables[5]]==['F0','F1','F2','F3','A1','A2'])
components=rows(V2+'runs/primary/component_summary.csv')
for cells in tables[6]:
    group=[r for r in components if r['case'].startswith(cells[0].split()[0]+'_')]
    check('S6 four capital/frequency panels '+cells[0],len(group)==4)
    for printed,(freq,budget) in zip(cells[1:],[('23','2000000'),('60','2000000'),('23','6500000'),('60','6500000')]):
        r=pick(group,frequency=freq,capital_budget_hkd=budget);number('S6',cells[0]+'/'+freq+'/'+budget,printed,r['rp'])
witness=load(V2+'runs/primary/shared_inventory_feasible_set_witness.json')
for cells in tables[7]:
    r=pick(witness['scenarios'],scenario=cells[0])
    for printed,s in zip(cells[1:],r['resource_checks']):number('S7',cells[0]+'/'+s['row'],printed,s['used'])
coverage=rows(V2+'runs/primary/coverage_summary.csv')
for cells in tables[8]:
    r=pick(coverage,frequency=cells[0].split('-')[0],minimum_packages_each_location_each_scenario=cells[1])
    check('S8 status '+cells[0]+'/'+cells[1],cells[2]==r['status'])
    if r['status']=='OPTIMAL':
        for printed,value in zip(cells[3:],[r['rp'],-float(r['delta_vs_no_coverage']),r['n']]):number('S8',cells[0]+'/'+cells[1],printed,value)
    else:check('S8 infeasible objectives remain missing '+cells[0],r['rp']=='' and cells[3]=='Not defined')
deploy=rows(V2+'runs/primary/coverage_deployment.csv')
for cells in tables[9]:
    for freq in ['23','60']:
        for scenario,c in zip(['Moderate','Severe','Extreme'],cells[1:]):
            vals=re.findall(r'\d+',c)
            for printed,(loc,measure) in zip(vals,[('Tai O1','Barrier'),('Tai O1','Warning'),('Tai O2','Warning')]):
                r=pick(deploy,frequency=freq,minimum_k=cells[0],scenario=scenario,location=loc)
                number('S9',str((freq,cells[0],scenario,loc,measure)),printed,r[measure])
            check('S9 Drainage zero '+str((freq,cells[0],scenario)),all(float(r['Drainage'])==0 for r in deploy if (r['frequency'],r['minimum_k'],r['scenario'])==(freq,cells[0],scenario)))
intervals=rows('04_Results/Optimization/uncertainty_intervals.csv')
for cells in tables[10]:
    mode='derived' if cells[0]=='Derived bounds' else 'availability';r=pick(intervals,u_mode=mode,metric=cells[1].lower())
    for printed,key in zip(cells[2:],['p2.5','median','p97.5']):number('S10',str((mode,cells[1],key)),printed,r[key])
legacy=rows('04_Results/Optimization/legacy_correction_comparison.csv')
for cells in tables[11]:
    r=next(r for r in legacy if r['factor'].lower()==cells[0].lower() and float(r['level'])==float(cells[1]))
    for printed,key in zip(cells[2:],['old_rp','corrected_rp','old_evpi','corrected_evpi']):number('S11',cells[0]+'/'+cells[1]+'/'+key,printed,r[key])
old_summary=rows('04_Results/Optimization/summary.csv');new_summary=rows(CI+'backend_probability60/summary.csv')
old_ties=rows('04_Results/Optimization/ev_policy_tie_ranges.csv');new_ties=rows(CI+'backend_probability60/ev_policy_tie_ranges.csv')
for cells in tables[12]:
    case='mobile_baseline' if cells[0]=='2' else f'fleet_{int(cells[0]):02d}'
    r=pick(old_summary,id=case);tie=pick(old_ties,case=case)
    for printed,key in zip(cells[1:5],['new_pumps','rp','eev','vss']):number('S12',case+'/'+key,printed,r[key])
    for printed,key in zip(cells[5].split('–'),['minimum_VSS_over_EV_optima','maximum_VSS_over_EV_optima']):number('S12',case+'/'+key,printed,tie[key])
for cells in tables[13]:
    case='mobile_baseline' if cells[0]=='2' else f'fleet_{int(cells[0]):02d}'
    r=pick(new_summary,id=case);tie=pick(new_ties,case=case)
    number('S13',case+'/rp',cells[1],r['rp']);number('S13',case+'/optimal_count',cells[2],tie['EV_optimal_policies'])
    for printed,key in zip(cells[3].split('–'),['worst_EEV_among_EV_optima','best_EEV_among_EV_optima']):number('S13',case+'/'+key,printed,tie[key])
    for printed,key in zip(cells[4].split('–'),['minimum_VSS_over_EV_optima','maximum_VSS_over_EV_optima']):number('S13',case+'/'+key,printed,tie[key])
events=rows('01_Data/Events/model_input.csv');metadata=rows('01_Data/Events/event_metadata.csv')
for cells in tables[14]:
    event_id=cells[0].split()[0];r=pick(events,event_id=event_id);meta=pick(metadata,event_id=event_id)
    check('S14 date/station '+event_id,cells[0].split()[1]==meta['event_date'] and cells[2] in meta['rainfall_station'])
    for printed,key in zip(cells[3:6],['event_window_max_daily_rainfall_mm','maximum_sea_level_mCD','maximum_storm_surge_m']):number('S14',event_id+'/'+key,printed,r[key])
inputs=load('04_Results/Optimization/baseline_inputs.json')
for cells in tables[15]:
    for printed,key in zip(cells[2:],['deploy_cost','labour','equipment','supply','alpha','upper_bound']):
        for loc in ['Tai O1','Tai O2'] if key!='alpha' else [None]:
            kv={'scenario':cells[0],'intervention':cells[1]}
            if loc:kv['location']=loc
            r=pick(inputs[key],**kv);number('S15',str((cells[0],cells[1],loc,key)),printed,r['value'])
candidates=rows(CI+'Candidate_Event_Inventory.csv');inclusion=rows(CI+'Inclusion_Exclusion_Audit.csv')
for cells in tables[16]:
    c=candidates if cells[0]=='Total' else [r for r in candidates if r['year']==cells[0]]
    a=inclusion if cells[0]=='Total' else [r for r in inclusion if r['year']==cells[0]]
    values=[len({r['hko_warning_group_id'] for r in c}),len(c),sum(bool(r['original_event_id']) for r in c),sum(r['model_eligible']=='True' for r in a),sum(r['model_eligible']!='True' for r in a)]
    for printed,value in zip(cells[1:],values):number('S16',cells[0],printed,value)

# Counts are read from the retained CSV/JSON, not inferred from the manuscript prose.
expected={'legacy_baseline':1,'baseline':1,'legacy_capacity':21,'mobile_capacity':21,'spatial':26,'ablation':8,'oat':56,'joint':400,'fleet':9,'existing_stock':5,'purchase_price':5,'access':2}
counts={}
for label,summary,audit_path,n in [('frozen23',old_summary,'04_Results/Optimization/solver_audit.csv',3875),('reconstructed60',new_summary,CI+'backend_probability60/solver_audit.csv',3888)]:
    audit=rows(audit_path);actual=dict(collections.Counter(r['experiment'] for r in summary))
    counts[label]={'configurations':len(summary),'solver_rows':len(audit),'experiments':actual,'statuses':dict(collections.Counter(r['status'] for r in audit))}
    check(label+' suite exact counts',len(summary)==555 and actual==expected and len(audit)==n and all(r['status']=='OPTIMAL' for r in audit))
primary=load(V2+'runs/primary/validation.json');independent=load(V2+'independent_validation/verification.json')
counts['targeted_supplementary']={k:primary[k] for k in ['solves','optimal','infeasible_expected','ev_specs','enumerated_policies','all_primary_ev_optima','component_cases','coverage_cases']}
counts['targeted_supplementary']['independent_calls']=independent['independent_milp_calls']
counts['targeted_supplementary']['maximum_primary_objective_error']=independent['maximum_primary_objective_error']
check('Supplementary 500/498/2/8/416/20/24/8 and independent 936 counts',list(counts['targeted_supplementary'].values())[:8]==[500,498,2,8,416,20,24,8] and independent['independent_milp_calls']==936)

source(str(DOC.relative_to(ROOT)))
with ZipFile(DOC) as z:doc=ET.fromstring(z.read('word/document.xml'))
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
paragraphs=[''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in doc.find('w:body',ns).findall('w:p',ns)]
# Cross-check main Word numeric tables against the same supplement evidence.
word_tables=[]
for table in doc.find('w:body',ns).findall('w:tbl',ns):
    word_tables.append([[''.join(n.text or '' for n in cell.findall('.//w:t',ns))
                         for cell in row.findall('w:tc',ns)] for row in table.findall('w:tr',ns)])
for cells in word_tables[7][1:]:
    freq='23' if '23' in cells[0] else '60';model='mobile' if 'mobile' in cells[0] else 'legacy'
    for convention in 'AB':
        r=pick(ev,frequency=freq,model=model,convention=convention)
        for printed,key in zip(cells[2:5],['ev','selected_eev','ev_optimal_policy_count']):number('Word8',str((freq,model,convention,key)),printed,r[key])
        for printed,key in zip(cells[5].split('–'),['vss_min','vss_max']):number('Word8',str((freq,model,convention,key)),printed,r[key])
for cells in word_tables[8][1:]:
    for freq,printed in zip(['23','60'],cells[2:]):
        r=next(r for r in components if r['case'].startswith(cells[0]+'_') and r['frequency']==freq and r['capital_budget_hkd']=='2000000')
        number('Word9',cells[0]+'/'+freq,printed,r['rp'])
for cells in word_tables[9][1:]:
    for freq,printed in zip(['23','60'],cells[1:3]):
        r=pick(coverage,frequency=freq,minimum_packages_each_location_each_scenario=cells[0])
        check('Word10 status '+freq+'/'+cells[0],cells[3]==r['status'])
        if cells[3]=='OPTIMAL':
            for n,value in zip(printed.split(' / '),[float(r['rp']),-float(r['delta_vs_no_coverage'])]):number('Word10',freq+'/'+cells[0],n,value)
        else:check('Word10 undefined '+freq,printed=='Not defined')
for cells in word_tables[13][1:]:
    case='legacy_baseline' if cells[0].startswith('Legacy') else 'mobile_baseline';key=cells[1].lower()
    old=float(pick(old_summary,id=case)[key]);new=float(pick(new_summary,id=case)[key])
    for printed,value in zip(cells[2:],[old,new,new-old]):number('Word14',case+'/'+key,printed,value)
references=[]
for i,p in enumerate(paragraphs,1):
    if re.search(r'\bS(?:1[0-3]|[1-9])(?:\.\d+)?\b',p):references.append({'paragraph':i,'text':p,'references':re.findall(r'\bS(?:1[0-3]|[1-9])(?:\.\d+)?\b',p)})
valid_refs=set(re.findall(r'^#{2,3} (S\d+(?:\.\d+)?)\b',text,re.M))
check('All explicit Word supplementary references resolve',all(r in valid_refs for p in references for r in p['references']))
check('Current Word explicitly names retained supplement',any('Supplementary_Methods_and_Results.md accompanies this candidate' in p for p in paragraphs))
check('Word original suite count 555/3875','555 configurations and 3,875 main Gurobi solves' in paragraphs[139])
check('Word final60 suite count 555/3888','555 configurations and 3,888 solver-audit rows' in paragraphs[187])
check('Word targeted suite count 500/498/2/936',all(v in paragraphs[193] for v in ['500 main solves','498 OPTIMAL','two intentionally INFEASIBLE','936 independent HiGHS']))
check('All numeric table transcriptions within printed rounding',all(r['pass'] for r in numeric),len(numeric))
result={'audit_date':'2026-11-18','scope':'READ_ONLY_ARCHIVAL_ALIGNMENT_NO_NEW_SCIENTIFIC_EXPERIMENTS',
        'status':'PASS' if all(c['pass'] for c in checks) else 'FAIL','manuscript_sha256':digest(DOC),
        'original_supplement_sha256':digest(ORIGINAL),'reading_copy_sha256':digest(SUP),
        'sections':sections,'tables':list(tables),'figures':list(range(1,6)),
        'local_links':links,'manuscript_references':references,'experiment_counts':counts,
        'checks':checks,'numeric_comparisons':numeric,'source_files':list(files.values()),
        'limitations':['Historical original23 screening/anchor/station-decision evidence remains unrecovered.',
                       'No field calibration or validated hazard-to-response mapping.',
                       'Three pending identities remain unresolved; Yagi peak-date conflict remains.',
                       '37 of 9032 historical Lloyd resampling/deletion fits are nonglobal.',
                       'EV-optimal policy ties change EEV/VSS; selection convention and ranges remain necessary.',
                       'Current merged Word hash differs from historical rendering QA; no new Word visual QA.',
                       'Local link presence does not establish third-party redistribution rights or Git tracking.']}
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'supplementary_index.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
with (OUT/'supplementary_numeric_comparisons.csv').open('w',encoding='utf-8',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(numeric[0]));writer.writeheader();writer.writerows(numeric)
print(json.dumps({'status':result['status'],'checks':len(checks),'failed_checks':[c for c in checks if not c['pass']], 'numeric_comparisons':len(numeric),'failed_numeric':[c for c in numeric if not c['pass']], 'linked_destinations':len(links)},ensure_ascii=False))
