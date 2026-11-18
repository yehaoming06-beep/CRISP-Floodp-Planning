"""Aggregate complete official census units into two Tai O research sectors."""
from pathlib import Path
from xml.etree import ElementTree as ET
import csv, json, math
from shapely.geometry import shape, mapping, Point, Polygon, LineString, box
from shapely.ops import unary_union, polygonize, transform
from pyproj import Transformer
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

BASE=Path(__file__).resolve().parents[1]
V1=BASE
GROUPS={'Tai O1':['94404S'],'Tai O2':['94401S','94409','94411']}
NAMES={'Tai O1':'Island-side census sector','Tai O2':'Mainland-side census sector'}

def main():
    (BASE/'01_Data/Spatial').mkdir(parents=True,exist_ok=True)
    (BASE/'04_Results/Study_Area').mkdir(parents=True,exist_ok=True)
    raw=json.loads((BASE/'01_Data/Sources/Census/tai_o_census_ssg.geojson').read_text())
    bycode={f['properties']['ssbg']:f for f in raw['features']}
    with (BASE/'01_Data/Spatial/census_ssg_2021_utf8.csv').open(encoding='utf-8-sig') as f:
        independent={r['ssbg']:r for r in csv.DictReader(f)}
    transform_xy=Transformer.from_crs(4326,2326,always_xy=True).transform
    table=[];geometries={};features=[]
    for zone,codes in GROUPS.items():
        polygons=[]
        for code in codes:
            props=bycode[code]['properties'];csvrow=independent[code]
            for k in ['t_pop','dh','oq']:assert int(props[k])==int(csvrow[k]),(code,k)
            p=shape(bycode[code]['geometry']);assert p.is_valid
            polygons.append(p)
            table.append({'zone':zone,'ssbg':code,'population_2021':int(props['t_pop']),'domestic_households_2021':int(props['dh']),'occupied_quarters_2021':int(props['oq']),
                'source':'CSDI official SSUG_21C layer; cross-checked against official Census CSV','source_url':'https://portal.csdi.gov.hk/geoportal/?datasetId=censtatd_rcd_1635933365202_19171&lang=en'})
        g=unary_union(polygons);assert g.is_valid
        geometries[zone]=g
        selected=[r for r in table if r['zone']==zone]
        props={'zone':zone,'name':NAMES[zone],'census_codes':codes,'population_2021':sum(r['population_2021'] for r in selected),
               'domestic_households_2021':sum(r['domestic_households_2021'] for r in selected),'occupied_quarters_2021':sum(r['occupied_quarters_2021'] for r in selected),
               'census_area_m2':transform(transform_xy,g).area,'definition':'Union of complete official 2021 census small subunit groups, without clipping or population interpolation',
               'flood_exposure':None,'calibrated_beta':None,'administrative_status':'Author-defined research sector, not an official administrative division'}
        features.append({'type':'Feature','properties':props,'geometry':mapping(g)})
    assert geometries['Tai O1'].intersection(geometries['Tai O2']).area<1e-14
    domain=unary_union(list(geometries.values()));bounds=list(domain.bounds)
    result={'type':'FeatureCollection','name':'CRISP_Tai_O_census_aligned_sectors_v2','bbox':bounds,'features':features,
            'attribution':'Census and Statistics Department; Common Spatial Data Infrastructure (CSDI) Portal; subject to CSDI terms and conditions'}
    (BASE/'01_Data/Spatial/tai_o_census_aligned_zones.geojson').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    with (BASE/'01_Data/Spatial/census_units.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(table[0]));w.writeheader();w.writerows(table)
    (BASE/'01_Data/Spatial/census_units.json').write_text(json.dumps(table,ensure_ascii=False,indent=2))
    summary={'as_of':'2026-11-04','census_year':2021,'zones':[f['properties'] for f in features],
             'total_population':sum(f['properties']['population_2021'] for f in features),
             'total_domestic_households':sum(f['properties']['domestic_households_2021'] for f in features),
             'total_occupied_quarters':sum(f['properties']['occupied_quarters_2021'] for f in features),'bounds':bounds,
             'excluded_intersecting_unit':{'code':'94101S','population':682,'census_area_km2':45.87924487066299,'reason':'Extends over a much larger rural area beyond the central settlement; its total is not attributed to Tai O core sectors'},
             'population_method':'Exact aggregation of whole census units; no proportional allocation, centroid assignment, or inferred building population',
             'replaces':'20261103_v1 fixed-window land-backbone definitions for the proposed case-study specification',
             'limitations':['Resident population is not flood-exposed population','Census boundaries include water margins and are not exact current shorelines','No causal intervention effect or calibrated beta is inferred','Not all areas called Tai O administratively are included']}
    (BASE/'01_Data/Spatial/zone_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))

    # Draw geometry and features from archived sources, never invent a hazard footprint.
    root=ET.fromstring((BASE/'01_Data/Sources/Calibration/S20.osm').read_bytes())
    nodes={n.attrib['id']:(float(n.attrib['lon']),float(n.attrib['lat'])) for n in root.findall('node')}
    ways=root.findall('way')
    def tags(w):return {t.attrib['k']:t.attrib['v'] for t in w.findall('tag')}
    def coordinates(w):return [nodes[n.attrib['ref']] for n in w.findall('nd')]
    display=box(bounds[0]-.001,bounds[1]-.0007,bounds[2]+.001,bounds[3]+.0008)
    tx=Transformer.from_crs(4326,2326,always_xy=True)
    projected=transform(tx.transform,display);xmin,ymin,xmax,ymax=projected.bounds
    c=canvas.Canvas(str(BASE/'04_Results/Study_Area/Tai_O_Zones.pdf'),pagesize=(590,570),invariant=1)
    c.setTitle('Tai O census-aligned research sectors')
    scale=min(510/(xmax-xmin),410/(ymax-ymin));ox=40+(510-(xmax-xmin)*scale)/2;oy=110+(410-(ymax-ymin)*scale)/2
    def xy(lon,lat):x,y=tx.transform(lon,lat);return ox+(x-xmin)*scale,oy+(y-ymin)*scale
    def fill(g,color,stroke='#88939D',lw=.5):
        for p in ([g] if g.geom_type=='Polygon' else g.geoms):
            if p.geom_type!='Polygon' or p.is_empty:continue
            path=c.beginPath()
            for ring in [p.exterior,*p.interiors]:
                pts=list(ring.coords);path.moveTo(*xy(*pts[0]))
                for pt in pts[1:]:path.lineTo(*xy(*pt))
                path.close()
            c.setFillColor(HexColor(color));c.setStrokeColor(HexColor(stroke));c.setLineWidth(lw);c.drawPath(path,fill=1,stroke=1,fillMode=0)
    fill(shape(bycode['94101S']['geometry']).intersection(display),'#F0F1F2','#CBD0D4',.3)
    fill(geometries['Tai O1'],'#CAE0EF','#456B88',.8);fill(geometries['Tai O2'],'#F5DEC2','#9B7043',.8)
    for code in ['94401S','94409','94411']:
        unit=shape(bycode[code]['geometry']);parts=[unit] if unit.geom_type=='Polygon' else unit.geoms
        for part in parts:
            p=c.beginPath();pts=list(part.exterior.coords);p.moveTo(*xy(*pts[0]))
            for pt in pts[1:]:p.lineTo(*xy(*pt))
            c.setStrokeColor(HexColor('#A98C6C'));c.setLineWidth(.4);c.setDash(2,2);c.drawPath(p)
    c.setDash()
    for w in ways:
        t=tags(w);pts=coordinates(w)
        if t.get('building') and len(pts)>3 and pts[0]==pts[-1]:
            g=Polygon(pts)
            if g.is_valid and display.intersects(g):
                clipped=g.intersection(display)
                if clipped.geom_type in ('Polygon','MultiPolygon'):fill(clipped,'#8A959F','#7B8690',.2)
        if t.get('natural')=='coastline' or t.get('highway') in ('tertiary','residential','unclassified','pedestrian'):
            g=LineString(pts).intersection(display)
            lines=[g] if g.geom_type=='LineString' else list(g.geoms) if g.geom_type=='MultiLineString' else []
            for line in lines:
                if line.is_empty:continue
                path=c.beginPath();coords=list(line.coords);path.moveTo(*xy(*coords[0]))
                for pt in coords[1:]:path.lineTo(*xy(*pt))
                c.setStrokeColor(HexColor('#83919B'));c.setLineWidth(.3);c.drawPath(path)
    c.setFont('Times-Bold',12);c.setFillColor(HexColor('#254B69'));c.drawString(*xy(113.8540,22.2585),'Tai O1')
    c.setFont('Times-Roman',10);c.drawString(*xy(113.8540,22.2580),'825 residents (2021)')
    c.setFont('Times-Bold',12);c.setFillColor(HexColor('#754821'));c.drawString(*xy(113.8672,22.2517),'Tai O2')
    c.setFont('Times-Roman',10);c.drawString(*xy(113.8672,22.2512),'2,853 residents (2021)')
    for code,dx,dy in [('94404S',-.002,0),('94401S',.0005,-.0015),('94409',.0004,.0004),('94411',-.0003,0)]:
        p=shape(bycode[code]['geometry']).representative_point();c.setFont('Times-Roman',9);c.setFillColor(HexColor('#263238'));c.drawString(*xy(p.x+dx,p.y+dy),code)
    bx,by=xy(display.bounds[0],display.bounds[1]);ex,ey=xy(display.bounds[2],display.bounds[3]);c.setStrokeColor(HexColor('#53616C'));c.setLineWidth(.5);c.rect(bx,by,ex-bx,ey-by)
    nx,ny=ex-20,ey-25;c.setLineWidth(1);c.line(nx,ny-20,nx,ny);p=c.beginPath();p.moveTo(nx,ny+2);p.lineTo(nx-3,ny-4);p.lineTo(nx+3,ny-4);p.close();c.setFillColor(HexColor('#263238'));c.drawPath(p,fill=1,stroke=0);c.setFont('Times-Bold',10);c.drawCentredString(nx,ny+7,'N')
    sx,sy=bx+12,by+15;length=500*scale;c.setLineWidth(1.5);c.line(sx,sy,sx+length,sy);c.line(sx,sy-3,sx,sy+3);c.line(sx+length,sy-3,sx+length,sy+3);c.setFont('Times-Roman',8);c.drawString(sx,sy+5,'0');c.drawRightString(sx+length,sy+5,'500 m')
    for i,text in enumerate([
      'Research sectors comprise complete 2021 census units. Population is resident population, not flood exposure.',
      'Blue: Tai O1 (94404S). Tan: Tai O2 (94401S, 94409, 94411). Grey surroundings: excluded rural unit 94101S.',
      'Census geometry/statistics: Census and Statistics Department, CSDI Portal, retrieved 4 Nov 2026.',
      'Thin dashed lines show component census-unit boundaries within Tai O2.',
      'Contextual coastlines/buildings: OpenStreetMap contributors (ODbL), extract 3 Nov 2026. HK1980 Grid.',
      'CSDI data are subject to CSDI terms: https://portal.csdi.gov.hk/csdi-webpage/doc/TNC'
    ]):c.setFont('Times-Roman',8);c.setFillColor(HexColor('#263238'));c.drawString(40,88-i*13,text)
    c.save()
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__':main()
