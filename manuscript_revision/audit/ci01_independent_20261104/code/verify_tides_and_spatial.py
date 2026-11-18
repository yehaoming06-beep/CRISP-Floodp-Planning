"""Independent official tide-db crosscheck and predeclared Tai O sensitivity."""
from pathlib import Path
import hashlib,json,re
import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score
from reconstruct import OUT,SNAP,COLS,csvout,dump
from assess_scenarios import fit
from crisp_data_layer.config import load_config

def main():
    freeze=json.loads((OUT/'logs/spatial_protocol_freeze.json').read_text())
    assert freeze['sha256']==hashlib.sha256((OUT/'TaiO_Spatial_Sensitivity_Addendum.md').read_bytes()).hexdigest()
    path=OUT/'sources/web/HKO_ssdb_storm.js';db=json.loads(path.read_text(encoding='utf-8-sig'))
    stations=json.loads((OUT/'sources/web/HKO_ssdb_station.js').read_text())
    assert stations['2']['ENG']=='Shek Pik' and stations['10']['ENG']=='Tai O'
    audit=pd.read_csv(OUT/'Inclusion_Exclusion_Audit.csv',keep_default_na=False)
    records=[];checks=[]
    for _,row in audit.iterrows():
        year=int(row.year);name=row.hko_name_raw;month=int(row.first_warning_hkt[5:7])
        named=[(key,v) for key,v in db.items() if int(v['YEAR'])==year and v['ENG'].upper()==name.upper()]
        if name=='NIL' or row.hko_type_raw=='TD/TD':named=[(key,v) for key,v in db.items() if int(v['YEAR'])==year and v['ENG']=='No name' and int(v['MONTH'])==month]
        if row.hko_warning_group_id==201802:
            # Explicitly linked by annual report §3.2 to the same regenerated Son-Tinh.
            named += [('358',db['358'])]
            assert db['358']['YEAR']=='2018' and db['358']['ENG']=='No name' and db['358']['MONTH']=='7'
        assert named,(row.candidate_id,year,name,month)
        sp=[v['REC']['2'] for _,v in named if '2' in v['REC']]
        assert sp and all(r['INCOMPLETE']=='N' for r in sp)
        wr=max(sp,key=lambda r:float(r['SEA']));sr=max(sp,key=lambda r:float(r['SURGE']))
        same=(float(wr['SEA'])==row.W_mCD and float(sr['SURGE'])==row.S_m and wr['SEA_TIME'][:16]==row.W_peak_as_printed and sr['SURGE_TIME'][:16]==row.S_peak_as_printed)
        checks.append(dict(candidate_id=row.candidate_id,warning_group_id=row.hko_warning_group_id,ssdb_record_ids=';'.join(k for k,_ in named),all_four_fields_match=same,Shek_Pik_W_mCD=float(wr['SEA']),Shek_Pik_S_m=float(sr['SURGE']),W_peak_hkt=wr['SEA_TIME'][:16],S_peak_hkt=sr['SURGE_TIME'][:16],INCOMPLETE_flags=';'.join(r['INCOMPLETE'] for r in sp),time_basis='Hong Kong Standard Time, explicitly stated in stormsurgedb.htm',source_url='https://www.hko.gov.hk/wservice/tsheet/pms/ssdb_storm.js'))
        to=[v['REC']['10'] for _,v in named if '10' in v['REC']]
        usable=bool(to) and len(to)==len(named) and all(r['INCOMPLETE']=='N' and re.fullmatch(r'\d+\.\d+',r[k]) for r in to for k in ['SEA','SURGE'])
        qualified=usable and row.screening_status=='INCLUDE'
        if usable:
            wt=max(to,key=lambda r:float(r['SEA']));st=max(to,key=lambda r:float(r['SURGE']))
            W=float(wt['SEA']);S=float(st['SURGE']);wtime=wt['SEA_TIME'][:16];stime=st['SURGE_TIME'][:16]
        else:W=S=wtime=stime=None
        status='INCLUDE_SPATIAL_SENSITIVITY' if qualified else row.decision_reason if usable else 'PENDING_TAIO_DATA'
        records.append(dict(candidate_id=row.candidate_id,original_event_id=row.original_event_id,year=year,event_name=row.event_name,ssdb_record_ids=';'.join(k for k,_ in named),TaiO_data_status='AVAILABLE_UNFLAGGED' if usable else 'PENDING_TAIO_DATA_NOT_ENTITY_EXCLUSION',analysis_status=status,TaiO_W_mCD=W,TaiO_S_m=S,TaiO_W_peak_hkt=wtime,TaiO_S_peak_hkt=stime,TaiO_raw_records=to,ShekPik_W_mCD=row.W_mCD,ShekPik_S_m=row.S_m,delta_TaiO_minus_ShekPik_W_m=W-row.W_mCD if usable else None,delta_TaiO_minus_ShekPik_S_m=S-row.S_m if usable else None,R_mm_day=row.R_mm_day,rain_station=row.rain_station,anchor_date=row.anchor_date,joint_driver_note=row.joint_driver_note,source_url='https://www.hko.gov.hk/en/wservice/tsheet/pms/stormsurgedb.htm?t=STORM&v=31',raw_data_url='https://www.hko.gov.hk/wservice/tsheet/pms/ssdb_storm.js',raw_data_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),identity_note='2018 Son-Tinh includes raw record358 No name second passage, per annual report3.2' if row.hko_warning_group_id==201802 else 'shared combined observation; not assigned independently to components' if row.hko_type_raw=='TD/TD' else 'name/year and official report identity matched'))
    csvout('evidence/Tide_Database_Crosscheck.csv',checks)
    csvout('Supplemental_TaiO_Observations.csv',records)
    conflicts=[r for r in checks if not r['all_four_fields_match']]
    dump('evidence/Tide_Database_Conflicts.json',conflicts)
    # Source conflicts are retained and adjudicated, never overwritten by a vote.
    for conflict in conflicts:
        assert audit.set_index('candidate_id').loc[conflict['candidate_id'],'secondary_source_QC'] in {'PENDING_SOURCE_CONFLICT','PEAK_TIME_CONFLICT_UNRESOLVED'}
    df=pd.DataFrame(records);valid=df[df.analysis_status.eq('INCLUDE_SPATIAL_SENSITIVITY')]
    to=pd.DataFrame(dict(event_id=valid.candidate_id,**{k:valid[v] for k,v in zip(COLS,['R_mm_day','TaiO_W_mCD','TaiO_S_m'])}))
    sp=pd.DataFrame(dict(event_id=valid.candidate_id,**{k:valid[v] for k,v in zip(COLS,['R_mm_day','ShekPik_W_mCD','ShekPik_S_m'])}))
    to.to_csv(OUT/'analysis/TaiO_common_model_input.csv',index=False);sp.to_csv(OUT/'analysis/ShekPik_common_model_input.csv',index=False)
    old=valid[valid.original_event_id.ne('')].sort_values('original_event_id')
    to23=pd.DataFrame(dict(event_id=old.original_event_id,**{k:old[v] for k,v in zip(COLS,['R_mm_day','TaiO_W_mCD','TaiO_S_m'])}))
    config=load_config(SNAP/'05_Code/Scenario_Pipeline/config/fallback.yaml')
    fits={};fit_results={}
    spname=f'ShekPik_common{len(sp)}_spatial';toname=f'TaiO_common{len(to)}_spatial'
    for name,matrix in [(spname,sp),(toname,to),('original23_TaiO_spatial',to23)]:
        r,rec=fit(name,matrix,config);fits[name]=rec;fit_results[name]=r
    labels_sp=fit_results[spname].event_results.scenario
    labels_to=fit_results[toname].event_results.scenario
    pd.DataFrame(dict(candidate_id=sp.event_id,ShekPik_class=labels_sp,TaiO_class=labels_to,class_changed=labels_sp!=labels_to)).to_csv(OUT/'analysis/TaiO_vs_ShekPik_common_Label_Migration.csv',index=False)
    dump('analysis/spatial_impact.json',dict(fits=fits,station_database_crosscheck_all_fields_match=all(r['all_four_fields_match'] for r in checks),candidate_rows_crosschecked=len(checks),warning_groups_crosschecked=audit.hko_warning_group_id.nunique(),spatial_sample_N=len(valid),spatial_pending=df[df.analysis_status.ne('INCLUDE_SPATIAL_SENSITIVITY')][['candidate_id','analysis_status']].to_dict('records'),original23_TaiO_data_available=len(old),common_sample_class_changes=int((labels_sp!=labels_to).sum()),common_sample_ARI=float(adjusted_rand_score(labels_sp,labels_to)),max_abs_W_difference_m=float(valid.delta_TaiO_minus_ShekPik_W_m.abs().max()),max_abs_S_difference_m=float(valid.delta_TaiO_minus_ShekPik_S_m.abs().max()),scope='supplemental fixed-station sensitivity after explicit source-conflict QC; not flood depth or empirical calibration'))
    print(json.dumps(json.loads((OUT/'analysis/spatial_impact.json').read_text()),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
