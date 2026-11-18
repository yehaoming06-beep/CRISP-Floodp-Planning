from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
BASE=Path(__file__).resolve().parents[1]
DATA=json.loads((BASE.parents[1]/'04_Results/Optimization/report_data.json').read_text())
OUT=BASE.parents[1]/'04_Results/Optimization/figures'
plt.rcParams.update({'font.family':'serif','font.serif':['Times New Roman','DejaVu Serif'],
    'font.size':10,'axes.labelsize':10,'xtick.labelsize':9,'ytick.labelsize':9,
    'legend.fontsize':9,'axes.spines.top':False,'axes.spines.right':False,
    'pdf.fonttype':42,'savefig.dpi':300,'savefig.bbox':'tight','savefig.pad_inches':.05})
COLORS=['#0072B2','#D55E00','#009E73','#CC79A7']
def save(fig,name):
    for ext in ['pdf','png']:fig.savefig(OUT/f'{name}.{ext}')
    plt.close(fig)
