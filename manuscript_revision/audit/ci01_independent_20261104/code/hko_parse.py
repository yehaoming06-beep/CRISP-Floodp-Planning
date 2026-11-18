"""Small standard-library HTML table reader preserving rowspan/colspan."""
from html.parser import HTMLParser
import re

def clean(s):return re.sub(r'\s+',' ',s.replace('\xa0',' ')).strip()

class Reader(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True)
        self.stack=[];self.tables=[];self.links=[];self.link=None;self.text=[];self.skip=0
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in {'script','style'}:self.skip+=1
        if tag=='a':self.link=[a.get('href',''),'']
        if tag=='table':self.stack.append(dict(rows=[],row=None,cell=None))
        if self.stack:
            t=self.stack[-1]
            if tag=='tr':t['row']=[]
            if tag in {'td','th'}:t['cell']=dict(text='',rowspan=int(a.get('rowspan',1)),colspan=int(a.get('colspan',1)),attrs=a)
            if tag in {'br','p','div'} and t['cell']:t['cell']['text']+=' '
    def handle_data(self,data):
        if not self.skip:self.text.append(data)
        if self.link:self.link[1]+=data
        if self.stack and self.stack[-1]['cell'] is not None:self.stack[-1]['cell']['text']+=data
    def handle_endtag(self,tag):
        if tag in {'script','style'}:self.skip=max(0,self.skip-1)
        if tag=='a' and self.link:self.links.append((self.link[0],clean(self.link[1])));self.link=None
        if self.stack:
            t=self.stack[-1]
            if tag in {'td','th'} and t['cell'] is not None:
                if t['row'] is not None:t['row'].append(t['cell'])
                t['cell']=None
            if tag=='tr' and t['row'] is not None:t['rows'].append(t['row']);t['row']=None
            if tag=='table':self.tables.append(self.stack.pop()['rows'])
    def grids(self):
        result=[]
        for rows in self.tables:
            grid=[];occupied={}
            for i,row in enumerate(rows):
                j=0
                for cell in row:
                    while (i,j) in occupied:j+=1
                    for di in range(cell['rowspan']):
                        for dj in range(cell['colspan']):occupied[i+di,j+dj]=clean(cell['text'])
                    j+=cell['colspan']
                n=max((b for a,b in occupied if a==i),default=-1)+1
                grid.append([occupied.get((i,b),'') for b in range(n)])
            result.append(grid)
        return result
