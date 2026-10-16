"""Plot saved aggregate metrics. Does not read patient data or run models."""

from pathlib import Path

import hashlib,json,os

os.environ.setdefault('MPLCONFIGDIR',str(Path(os.environ.get('TMPDIR','/tmp'))/'portfolio-matplotlib'))

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

import numpy as np

import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

DF=pd.read_csv(ROOT/'results/metrics.csv')

OUT=ROOT/'figures'

OUT.mkdir(exist_ok=True)

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#cbd5e1','axes.labelcolor':'#334155','text.color':'#172554','xtick.color':'#334155','ytick.color':'#64748b','figure.facecolor':'white','axes.facecolor':'white','savefig.facecolor':'white'})

COLORS=['#94a3b8','#0f766e','#2563eb','#e19745','#7c3aed']

manifest=[]

def row(name):
 result=DF[DF.model==name]
 if len(result)!=1:raise ValueError(f'Expected one metric row for {name}')
 return result.iloc[0]

def bars(ax,labels,values,colors=None,ylim=(0,1),digits=4):
 x=np.arange(len(labels));ax.bar(x,values,color=colors or COLORS[:len(labels)],width=.62,zorder=3)
 ax.set_xticks(x,labels);ax.set_ylim(*ylim);ax.grid(axis='y',alpha=.2,zorder=0);ax.set_axisbelow(True)
 for i,v in enumerate(values):ax.text(i,v+(ylim[1]-ylim[0])*.02,f'{v:.{digits}f}',ha='center',fontsize=10)

def save(fig,name,caption,inputs='results/metrics.csv'):
 fig.savefig(OUT/name,dpi=160,bbox_inches='tight');plt.close(fig)
 manifest.append({'path':'figures/'+name,'caption':caption,'inputs':[inputs],'kind':'aggregate_chart','contains_patient_images':False,'model_execution':False,'sha256':hashlib.sha256((OUT/name).read_bytes()).hexdigest()})

def note(fig,text):fig.text(.07,.025,text,fontsize=9,color='#64748b',va='bottom')

def calibration(ax):
 models=['Candidate19 RF Raw','Candidate19 RF Sigmoid','Candidate19 RF Isotonic'];x=np.arange(3)
 for j,(metric,label,color) in enumerate([('brier','Brier','#2563eb'),('ece','ECE','#0f766e')]):
  vals=[row(n)[metric] for n in models];pos=x+(j-.5)*.28;ax.bar(pos,vals,width=.27,label=label,color=color,zorder=3)
  for a,b in zip(pos,vals):ax.text(a,b+.006,f'{b:.4f}',ha='center',fontsize=9)
 ax.set_xticks(x,['Raw RF','Sigmoid','Isotonic']);ax.set_ylim(0,.205);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True);ax.legend(frameon=False,ncol=2,loc='upper right');ax.set_title('Candidate19 | calibration\nFinal-configuration 5-fold OOF',loc='left',weight='bold',pad=15);ax.set_ylabel('Calibration error (lower is better)')

models=['LR','Linear SVM','XGBoost','RF','Keras ANN']
fig,axes=plt.subplots(1,2,figsize=(13,6));bars(axes[0],['LR*','SVM*','XGB','RF','ANN'],[row(n).roc_auc for n in models],['#94a3b8','#94a3b8','#94a3b8','#0f766e','#94a3b8']);axes[0].set_title('Pooled outer OOF | ROC-AUC',loc='left',weight='bold');x=np.arange(5)
for j,(metric,label,color) in enumerate([('sensitivity_recall','Sensitivity','#2563eb'),('specificity','Specificity','#e19745')]):axes[1].bar(x+(j-.5)*.3,[row(n)[metric] for n in models],width=.29,label=label,color=color)
axes[1].set_xticks(x,['LR*','SVM*','XGB','RF','ANN']);axes[1].set_ylim(0,1.08);axes[1].axhline(.95,color='#64748b',ls='--',lw=1,label='Sensitivity target 0.95');axes[1].set_title('Fold-specific thresholds',loc='left',weight='bold');axes[1].legend(frameon=False,fontsize=9,loc='lower left');fig.subplots_adjust(bottom=.22,wspace=.3);note(fig,'Z-Alizadeh development cohort: 303 patients (216 CAD / 87 Normal); outer10 / inner5.\n* LR/SVM: supplied PDF p4 only; personal Nested implementation not available. ANN resumed across environments.');save(fig,'nested_model_comparison.png','Nested pooled 비교. LR/SVM은 PDF 근거만.')
fig,ax=plt.subplots(figsize=(10,6));calibration(ax);fig.subplots_adjust(bottom=.20);note(fig,'303-patient development cohort. Candidate, calibration method and pooled threshold selected on development OOF.\nThis is not a new independent evaluation or the original 10-fold Nested RF result.');save(fig,'calibration_comparison.png','별도최종구성용OOF의Brier/ECE. 원래Nested성능과분리.')
fig,axes=plt.subplots(1,2,figsize=(14,7));bars(axes[0],['Sensitivity','Specificity','ROC-AUC'],[row('RF').sensitivity_recall,row('RF').specificity,row('RF').roc_auc],['#2563eb','#e19745','#0f766e']);axes[0].set_title('RF | pooled outer OOF\n10 outer / 5 inner folds',loc='left',weight='bold',pad=15);calibration(axes[1]);fig.suptitle('Clinical CAD screening | validation and probability calibration',fontsize=18,weight='bold',y=.98);fig.subplots_adjust(top=.84,bottom=.23,wspace=.30);note(fig,'Z-Alizadeh development cohort, n=303. Left and right use different evaluation procedures.\nCalibration: final-configuration OOF selection, not external validation. Mock inference remains incomplete.');save(fig,'portfolio_cover.png','대표후보: RF Nested결과와최종구성용Calibration을분리한패널.')


manifest_path=OUT/'manifest.json'

manifest_path.write_text(json.dumps({'generator':'scripts/plot_results.py','metrics_sha256':hashlib.sha256((ROOT/'results/metrics.csv').read_bytes()).hexdigest(),'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'figures':manifest},ensure_ascii=False,indent=2)+'\n')

print(f'Generated {len(manifest)} aggregate figures')
