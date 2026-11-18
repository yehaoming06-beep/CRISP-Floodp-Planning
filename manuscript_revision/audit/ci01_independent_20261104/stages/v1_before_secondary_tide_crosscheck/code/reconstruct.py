"""Offline, deterministic candidate enumeration and application of frozen v1."""
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import csv, hashlib, json, re
from hko_parse import Reader, clean

OUT=Path(__file__).resolve().parents[1]
SNAP=OUT/'snapshots';WEB=OUT/'sources/web'
DB_URL='https://www.hko.gov.hk/dps/wxinfo/climat/warndb/tc.dat'
NAME_TYPES={'STS':'Severe Tropical Storm','TS':'Tropical Storm','ST':'Severe Typhoon','T':'Typhoon','SuperT':'Super Typhoon','TD':'Tropical Depression','TD/TD':'Two Tropical Depressions'}
COLS=['event_window_max_daily_rainfall_mm','maximum_sea_level_mCD','maximum_storm_surge_m']

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,obj):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False))
def csvout(name,rows,fields=None):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
    fields=fields or list(dict.fromkeys(k for r in rows for k in r))
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for row in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in row.items()})
def readcsv(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def date(y,s,t):
    d,m=map(int,re.sub(r'\s+','',s).split('/'));t=t.replace(':','').zfill(4)
    return datetime(y,m,d,int(t[:2]),int(t[2:]))
def iso(d):return d.isoformat(sep=' ',timespec='minutes')
def signature(signal,begin,end):return str(signal).replace(' ',''),iso(begin),iso(end)

def warnings():
    groups=defaultdict(list);segments=[]
    for line_no,line in enumerate((WEB/'HKO_tc.dat').read_text(encoding='utf-8-sig').splitlines(),1):
        a=line.split('\t')
        if len(a)!=16 or a[1]=='MSN' or a[3] not in {'1','3','8','9','10'}:continue
        if not (2017<=int(a[8])<=2025 or 2017<=int(a[13])<=2025):continue
        begin=date(int(a[8]),a[6]+'/'+a[7],a[5]);end=date(int(a[13]),a[11]+'/'+a[12],a[10])
        if end<datetime(2017,1,1) or begin>=datetime(2026,1,1):continue
        assert a[9]=='X' and a[14]=='X','Unexpected summer-time marker in study period'
        signal=a[3]+(' '+a[4] if a[3]=='8' else '')
        rec=dict(warning_group_id=a[0],type_code=a[1],name=a[2],signal=signal,level=int(a[3]),begin=iso(begin),end=iso(end),source_url=DB_URL,raw_line_number=line_no,raw_line=line)
        groups[a[0]].append(rec);segments.append(rec)
    csvout('evidence/Warning_Segments.csv',segments)
    checks=[]
    for year in range(2017,2026):
        expected=Counter(signature(r['signal'],datetime.fromisoformat(r['begin']),datetime.fromisoformat(r['end'])) for rows in groups.values() for r in rows if int(r['begin'][:4])==year)
        actual=Counter();source_files=[];month_checks=[]
        if year<=2024:
            path=WEB/f'HKO_{year}_table43.html';r=Reader(path.read_text());source_files.append(str(path.relative_to(OUT)))
            assert 'UTC + 8' in clean(' '.join(r.text)) or 'UTC+8' in clean(' '.join(r.text)).replace(' ','')
            for grid in r.grids():
                for row in grid:
                    if len(row)!=7 or not re.fullmatch(r'(1|3|8\s*(NW|NE|SW|SE)|9|10)',row[2]):continue
                    actual[signature(row[2],date(year,row[3],row[4]),date(year,row[5],row[6]))]+=1
        else:
            for month in range(1,13):
                path=WEB/f'HKO_mws2025{month:02}.htm';r=Reader(path.read_text());source_files.append(str(path.relative_to(OUT)))
                month_rows=[]
                for grid in r.grids():
                    if not any('Signal Number' in ' '.join(row) for row in grid[:2]):continue
                    for row in grid:
                        if len(row)!=6 or not re.fullmatch(r'(1|3|8\s*(NW|NE|SW|SE)|9|10)',row[1]):continue
                        sig=signature(row[1],date(year,row[2],row[3]),date(year,row[4],row[5]));actual[sig]+=1;month_rows.append(row)
                month_checks.append(dict(month=month,warning_segments=len(month_rows),table_rows=month_rows,source=str(path.relative_to(OUT)),sha256=sha(path),status='EXPLICIT_ROWS' if month_rows else 'NO_TC_ROWS_IN_COMPLETE_MONTHLY_WARNING_PAGE'))
        rec=dict(year=year,database_segments=sum(expected.values()),comparison_segments=sum(actual.values()),exact_segment_match=expected==actual,database_only=list((expected-actual).elements()),comparison_only=list((actual-expected).elements()),comparison_sources=source_files,monthly_checks=month_checks)
        checks.append(rec)
        assert expected==actual,rec
    dump('evidence/Candidate_Completeness_Check.json',checks)
    return dict(sorted(groups.items()))

def rain_window(day,station):
    dates=[day+timedelta(days=i) for i in range(-2,3)];raw=[];archives=[];urls=[]
    for d in dates:
        p=SNAP/f'01_Data/Sources/HKO/r11_daily/daily_{station}_{d.year}.json';j=json.loads(p.read_text())
        block=next(x['dayData'] for x in j['stn']['data'] if x['code']=='RF')
        value=str(block[d.day-1][d.month]).strip();raw.append(value)
        archives.append(str(p.relative_to(OUT)));urls.append(f'https://www.hko.gov.hk/cis/aws/individual_day/daily_{station}_{d.year}.xml')
    valid=[bool(re.fullmatch(r'\d+(?:\.\d+)?',v)) for v in raw]
    values=[float(v) if ok else None for v,ok in zip(raw,valid)]
    return dict(station=station,dates=[str(d.date()) for d in dates],raw_values=raw,valid_days=sum(valid),usable=all(valid),daily_values_mm=values,archives=sorted(set(archives)),source_urls=sorted(set(urls)),sha256={a:sha(OUT/a) for a in sorted(set(archives))})

def rain(day):
    alternatives=[rain_window(day,s) for s in ['R11','HKA','R12']]
    selected=next((a for a in alternatives if a['usable']),None)
    if selected:
        vals=selected['daily_values_mm'];result=dict(rain_station=selected['station'],rainfall_window_start=selected['dates'][0],rainfall_window_end=selected['dates'][-1],R_mm_day=max(vals),rain_window_sum_mm=sum(vals),event_day_rainfall_mm=vals[2],rain_source_url=';'.join(selected['source_urls']),rain_snapshot=';'.join(selected['archives']),rain_QC='COMPLETE_5_OF_5_UNFLAGGED',rain_station_choice_reason='first complete unflagged station in fixed R11>HKA>R12 order')
    else:result=dict(rain_station='',rainfall_window_start=str((day-timedelta(days=2)).date()),rainfall_window_end=str((day+timedelta(days=2)).date()),R_mm_day=None,rain_window_sum_mm=None,event_day_rainfall_mm=None,rain_source_url='',rain_snapshot='',rain_QC='PENDING_NO_COMPLETE_STATION',rain_station_choice_reason='all stations retained for follow-up; not excluded')
    return result,alternatives

PDF_SPECS={1:(6,20),2:(6,31),3:(7,29),4:(7,45),5:(8,27),6:(8,37),7:(8,46),8:(8,55),9:(9,32),10:(9,52),11:(9,71),12:(10,22),13:(10,34),14:(11,19)}

def tide(year,seq,name):
    if year<2025:
        paths=sorted(WEB.glob(f'HKO_{year}_table3{seq}[0-9].html'));assert len(paths)==1,(year,seq,paths)
        p=paths[0];reader=Reader(p.read_text());text=clean(' '.join(reader.text));tables=reader.grids()
        rows=[row for grid in tables for row in grid if row and re.fullmatch('Shek Pik',row[0],re.I)]
        url=f'https://www.hko.gov.hk/en/publica/tc/tc{year}/'+p.name.split('_',2)[-1]
        loc=re.search(r'Table\s+(3\.\d+\.\d+)',text)[0]
        time_basis='As printed; HTML tide table has no explicit time-zone line; annual section1 distinguishes UTC labels and HKT narrative. No conversion applied.'
        evidence=dict(snapshot=str(p.relative_to(OUT)),sha256=sha(p),url=url,locator=loc,table_grids=tables,full_extracted_text=text,Shek_Pik_rows=rows,time_basis=time_basis,visual_check='HTML complete table including headers/rows/notes parsed, not PDF')
    else:
        month,page=PDF_SPECS[seq]
        rec=next(r for r in json.loads((OUT/'sources/pdf_table_pages.json').read_text()) if r['month']==month and r['pdf_page']==page)
        p=OUT/rec['pdf'];text=(OUT/rec['text_file']).read_text()
        matches=re.findall(r'Shek\s+Pik\s+([^\n]+)',text)
        rows=[['Shek Pik']+m.strip().split() for m in matches]
        pos=text.lower().rfind('times and heights')
        tide_text=text[max(0,pos-40):];loc=re.findall(r'Table\s+(2\.\d+\.\d+)',tide_text)[0]
        loc=f'Table {loc}; {name}; PDF page {page}; printed page {page-3}'
        url=rec['url'];time_basis='UTC+8; monthly PDF page 2 explicitly states all times 8 hours ahead of UTC unless otherwise stated'
        assert name=='NIL' or re.search(re.escape(name),tide_text,re.I),(name,loc)
        evidence=dict(snapshot=str(p.relative_to(OUT)),sha256=sha(p),url=url,locator=loc,full_extracted_text=tide_text,Shek_Pik_rows=rows,time_basis=time_basis,pdf_page=page,printed_page=page-3,image=rec['image'],visual_check='2026-11-04 assistant inspected full rendered page; station, W/S, dates/times, units and tide-specific notes matched')
        text=tide_text
    assert rows and all(len(r)==7 for r in rows),evidence
    assert 'above chart datum' in text.lower() and 'above astronomical tide' in text.lower(),evidence
    numeric=all(re.fullmatch(r'\d+\.\d+',row[k]) for row in rows for k in [1,4])
    if numeric:
        wr=max(rows,key=lambda r:float(r[1]));sr=max(rows,key=lambda r:float(r[4]))
        W=float(wr[1]);S=float(sr[4]);wt=iso(date(year,wr[2],wr[3]));st=iso(date(year,sr[5],sr[6]))
    else:W=S=wt=st=None
    joint=bool(re.search(r'combined\s+effect',text,re.I))
    result=dict(W_mCD=W,S_m=S,W_peak_as_printed=wt,S_peak_as_printed=st,tide_station='Shek Pik (SPW)',tide_source_url=url,tide_snapshot=evidence['snapshot'],tide_sha256=evidence['sha256'],tide_locator=loc,tide_time_basis=time_basis,tide_QC='TARGET_ROW_UNFLAGGED' if numeric else 'PENDING_TARGET_ROW_QC',S_definition='maximum sea level rise above astronomical tide; cyclone and northeast monsoon combined' if joint else 'maximum reported storm surge above astronomical tide; no pure cyclone decomposition inferred',joint_driver_note='; '.join(re.findall(r'[^.\n]*combined\s+effect[^.\n]*',text,re.I)),tide_aggregation_scope='official event summary; exact aggregation endpoints not stated in table',tide_multi_passages=len(rows))
    evidence.update(derived_fields=result)
    return result,evidence

def main():
    freeze=json.loads((OUT/'logs/protocol_freeze.json').read_text());assert freeze['sha256']==sha(OUT/'Screening_Protocol.md')
    groups=warnings();original=readcsv(SNAP/'01_Data/Events/event_metadata.csv')
    inventory=[];audit=[];rain_evidence=[];tide_evidence=[]
    for gid,segs in groups.items():
        year=int(gid[:4]);seq=int(gid[-2:]);name=segs[0]['name'];top=max(r['level'] for r in segs)
        anchor=min(r['begin'] for r in segs if r['level']==top);day=datetime.fromisoformat(anchor).replace(hour=0,minute=0)
        old=next((r for r in original if int(r['event_date'][:4])==year and r['event_name'].split()[-1].upper()==name.upper()),None)
        base=dict(candidate_id=f'TC{year}_{seq:02}',year=year,hko_warning_group_id=gid,event_name=(NAME_TYPES.get(segs[0]['type_code'],segs[0]['type_code'])+' '+(name.title() if name!='NIL' else 'unnamed')).strip(),hko_name_raw=name,hko_type_raw=segs[0]['type_code'],first_warning_hkt=min(s['begin'] for s in segs),last_cancellation_hkt=max(s['end'] for s in segs),highest_local_signal=top,anchor_hkt=anchor,anchor_date=anchor[:10],warning_segment_count=len(segs),candidate_basis='any local HKO TC signal during 2017-2025; no intensity or R/W/S threshold',warning_source_url=DB_URL,warning_snapshot='sources/web/HKO_tc.dat',warning_source_sha256=sha(WEB/'HKO_tc.dat'),warning_raw_line_numbers=';'.join(str(s['raw_line_number']) for s in segs),crosscheck_url=f'https://www.hko.gov.hk/en/publica/tc/tc{year}/table43.html' if year<2025 else f'https://www.hko.gov.hk/en/wxinfo/pastwx/mws2025/mws2025{day.month:02}.htm',bounded_candidate_verification='COMPLETE_CROSSCHECKED_WARNING_FRAME',original_event_id=old['event_id'] if old else '')
        rr,alternatives=rain(day);tt,te=tide(year,seq,name)
        # Official warning group 202102 explicitly covers two distinct depressions.
        # Split identities, preserve shared measurements, and withhold attribution.
        components=['E','W'] if segs[0]['type_code']=='TD/TD' else ['']
        for component in components:
            b={**base,'candidate_id':base['candidate_id']+('_'+component if component else ''),'compound_group_id':gid if component else '', 'component':component,'official_reporting_unit':'two cyclones share warning and tide summary' if component else 'one cyclone','warning_interval_scope':'shared warning group; cancellation is not separately determined for this component' if component else 'all local warning segments for the same cyclone, including repeated passages'}
            if component:b['event_name']='Tropical Depression '+component+' (5-6 July 2021)' if component=='E' else 'Tropical Depression W (5-8 July 2021)'
            inventory.append(b)
            reasons=[]
            if rr['R_mm_day'] is None:reasons.append('PENDING_RAIN')
            if tt['W_mCD'] is None or tt['S_m'] is None:reasons.append('PENDING_TIDE_QC')
            if component:reasons.append('PENDING_COMPOUND_ATTRIBUTION')
            status='INCLUDE' if not reasons else 'PENDING_DATA'
            rec={**b,**rr,**tt,'screening_status':status,'entity_scope_status':'ELIGIBLE','decision_reason':';'.join(reasons) if reasons else 'eligible warning candidate with verified unflagged R/W/S','is_entity_exclusion':False,'model_eligible':not reasons,'model_R_mm_day':rr['R_mm_day'] if not reasons else None,'model_W_mCD':tt['W_mCD'] if not reasons else None,'model_S_m':tt['S_m'] if not reasons else None}
            audit.append(rec)
            rain_evidence.append(dict(candidate_id=b['candidate_id'],selected=rr,all_three_stations=alternatives))
            tide_evidence.append(dict(candidate_id=b['candidate_id'],**te,attribution_status='combined observation cannot be assigned separately' if component else 'one reported cyclone'))
    # Connected components of inclusive five-day windows; retain every identity.
    episode=0;last_end='';overlaps=[]
    for rec in sorted(audit,key=lambda r:(r['rainfall_window_start'],r['candidate_id'])):
        if rec['rainfall_window_start']>last_end:episode+=1
        rec['overlap_episode_id']=f'EP{episode:03}';last_end=max(last_end,rec['rainfall_window_end'])
        peers=[]
        for other in audit:
            if rec is other:continue
            begin=max(rec['rainfall_window_start'],other['rainfall_window_start']);end=min(rec['rainfall_window_end'],other['rainfall_window_end'])
            if begin<=end:
                peers.append(other['candidate_id'])
                if rec['candidate_id']<other['candidate_id']:overlaps.append(dict(candidate_a=rec['candidate_id'],candidate_b=other['candidate_id'],overlap_start=begin,overlap_end=end,shared_warning_group=rec['hko_warning_group_id']==other['hko_warning_group_id']))
        rec['overlapping_candidate_ids']=';'.join(peers)
    csvout('Candidate_Event_Inventory.csv',inventory)
    csvout('Inclusion_Exclusion_Audit.csv',audit)
    csvout('evidence/Overlapping_Windows.csv',overlaps)
    dump('evidence/Rainfall_Station_Window_Details.json',rain_evidence)
    dump('evidence/Tide_Table_Extraction.json',tide_evidence)
    compare=[]
    for old in original:
        rec=next(r for r in audit if r['original_event_id']==old['event_id'])
        ro,alts=rain(datetime.fromisoformat(old['event_date']));selected=re.search(r'\((\w+)\)',old['rainfall_station'])[1]
        fixed=rain_window(datetime.fromisoformat(old['event_date']),selected)
        assert fixed['usable'] and max(fixed['daily_values_mm'])==float(old['event_window_max_daily_rainfall_mm'])
        compare.append(dict(original_event_id=old['event_id'],candidate_id=rec['candidate_id'],event_name=old['event_name'],comparison_type='ORIGINAL_EVENT',original_anchor=old['event_date'],reconstructed_anchor=rec['anchor_date'],anchor_shift_days=(datetime.fromisoformat(rec['anchor_date'])-datetime.fromisoformat(old['event_date'])).days,original_station=selected,reconstructed_station=rec['rain_station'],station_changed=selected!=rec['rain_station'],original_R_mm_day=float(old[COLS[0]]),reconstructed_R_mm_day=rec['R_mm_day'],delta_R_mm_day=rec['R_mm_day']-float(old[COLS[0]]) if rec['R_mm_day'] is not None else None,original_W_mCD=float(old[COLS[1]]),reconstructed_W_mCD=rec['W_mCD'],delta_W_mCD=rec['W_mCD']-float(old[COLS[1]]),original_S_m=float(old[COLS[2]]),reconstructed_S_m=rec['S_m'],delta_S_m=rec['S_m']-float(old[COLS[2]]),new_station_rule_at_old_anchor=ro['rain_station'],new_R_at_old_anchor=ro['R_mm_day'],original_station_values_reproduced=True,reconstructed_status=rec['screening_status'],reason=rec['decision_reason'],official_warning_url=rec['crosscheck_url'],rain_url=rec['rain_source_url'],tide_url=rec['tide_source_url']))
        compare[-1].update(original_window_start=old['rainfall_window_start'],original_window_end=old['rainfall_window_end'],reconstructed_window_start=rec['rainfall_window_start'],reconstructed_window_end=rec['rainfall_window_end'],original_window_total_mm=float(old['event_window_total_rainfall_mm']),reconstructed_window_total_mm=rec['rain_window_sum_mm'],original_event_day_mm=float(old['event_day_rainfall_mm']),reconstructed_event_day_mm=rec['event_day_rainfall_mm'])
    for rec in audit:
        if not rec['original_event_id']:compare.append(dict(original_event_id='',candidate_id=rec['candidate_id'],event_name=rec['event_name'],comparison_type='ADDITIONAL_CANDIDATE',reconstructed_anchor=rec['anchor_date'],reconstructed_station=rec['rain_station'],reconstructed_R_mm_day=rec['R_mm_day'],reconstructed_W_mCD=rec['W_mCD'],reconstructed_S_m=rec['S_m'],reconstructed_status=rec['screening_status'],reason=rec['decision_reason'],official_warning_url=rec['crosscheck_url'],rain_url=rec['rain_source_url'],tide_url=rec['tide_source_url']))
    csvout('Original23_vs_Reconstructed.csv',compare)
    model=[dict(event_id=r['candidate_id'],**{k:r[v] for k,v in zip(COLS,['model_R_mm_day','model_W_mCD','model_S_m'])}) for r in audit if r['model_eligible']]
    csvout('analysis/reconstructed_model_input.csv',model)
    rain_comp=[]
    for station in ['R11','HKA','R12']:
        for year in range(2017,2026):
            archived=SNAP/f'01_Data/Sources/HKO/r11_daily/daily_{station}_{year}.json';live=WEB/f'RF_{station}_{year}.json'
            rain_comp.append(dict(station=station,year=year,archived_sha256=sha(archived),redownloaded_sha256=sha(live),byte_identical=sha(archived)==sha(live),json_equal=json.loads(archived.read_text())==json.loads(live.read_text())))
    dump('evidence/Rainfall_Redownload_Comparison.json',rain_comp)
    summary=dict(candidate_warning_groups=len(groups),candidate_cyclones=len(inventory),candidate_year_counts=dict(sorted(Counter(r['year'] for r in inventory).items())),screening_status_counts=dict(Counter(r['screening_status'] for r in audit)),rain_stations=dict(Counter(r['rain_station'] for r in audit if r['model_eligible'])),original23_anchor_changes=sum(r['anchor_shift_days']!=0 for r in compare[:23]),original23_station_changes=sum(r['station_changed'] for r in compare[:23]),original23_R_changes=sum(abs(r['delta_R_mm_day'])>1e-9 for r in compare[:23] if r['delta_R_mm_day'] is not None),original23_retained=sum(r['reconstructed_status']=='INCLUDE' for r in compare[:23]),original23_vectors_exact=sum(r['delta_R_mm_day']==0 and r['delta_W_mCD']==0 and r['delta_S_m']==0 for r in compare[:23]),overlap_pairs=len(overlaps),pending=[dict(candidate_id=r['candidate_id'],name=r['event_name'],reason=r['decision_reason']) for r in audit if not r['model_eligible']],all_27_rain_json_match=all(r['json_equal'] for r in rain_comp),protocol_sha256=freeze['sha256'])
    dump('analysis/screening_summary.json',summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
