"""Reliable server-rendered charts; no browser-side Plotly asset bundle."""
from __future__ import annotations
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

INK='#19333d'; TEAL='#226e68'; MUTED='#607378'; GOLD='#ba7f32'; PAPER='#faf8f3'; GRID='#e7e7dd'

def _figure(width=8, height=3.6):
    fig, ax = plt.subplots(figsize=(width,height), dpi=130)
    fig.patch.set_facecolor(PAPER)
    ax.set_facecolor(PAPER)
    ax.tick_params(colors=INK,labelsize=10,length=0)
    for spine in ax.spines.values(): spine.set_visible(False)
    return fig,ax

def funnel_chart(frame:pd.DataFrame):
    fig,ax=_figure(8,3.3)
    vals=frame['count'].astype(int).tolist(); labels=frame['stage'].str.replace('Unique publishable','Publishable',regex=False).tolist()
    y=np.arange(len(vals)); bars=ax.barh(y,vals,color=[INK,TEAL,'#3d8e83',GOLD],height=.56)
    ax.set_yticks(y,labels=labels);ax.invert_yaxis();ax.set_xlim(0,max(vals)*1.20 if vals else 1)
    ax.set_xticks([])
    for b,v in zip(bars,vals):ax.text(v+.25,b.get_y()+b.get_height()/2,str(v),va='center',color=INK,weight='bold',fontsize=11)
    fig.tight_layout(pad=1.2);return fig

def source_chart(frame:pd.DataFrame):
    counts=frame.source_platform.value_counts().sort_values()
    fig,ax=_figure(8,3.2); y=np.arange(len(counts)); b=ax.barh(y,counts.values,color=TEAL,height=.56)
    ax.set_yticks(y,labels=[s.replace(' photo-management forum',' forum') for s in counts.index]);ax.set_xlim(0,max(counts)*1.19 if len(counts) else 1);ax.set_xticks([])
    for bar,v in zip(b,counts.values):ax.text(v+.15,bar.get_y()+bar.get_height()/2,str(v),va='center',weight='bold',color=INK)
    fig.tight_layout(pad=1.2);return fig

def category_chart(frame:pd.DataFrame,column:str,title:str,max_items:int=7):
    values=frame[column].fillna('Not established').astype(str)
    counts=values.value_counts().head(max_items).sort_values()
    fig,ax=_figure(8,max(3.0,len(counts)*.52+1.15)); y=np.arange(len(counts));bars=ax.barh(y,counts.values,color=TEAL,height=.58)
    labels=[label if len(label)<=42 else label[:39]+'…' for label in counts.index]
    ax.set_yticks(y,labels=labels);ax.set_xlim(0,max(counts.values)*1.18 if len(counts) else 1);ax.set_xticks([]);ax.set_title(title,loc='left',fontsize=12,color=INK,weight='bold',pad=10)
    for bar,value in zip(bars,counts.values):ax.text(value+.1,bar.get_y()+bar.get_height()/2,str(value),va='center',color=INK,weight='bold')
    fig.tight_layout(pad=1.2);return fig

def themes_chart(stats:pd.DataFrame):
    vals=stats.sort_values('records',ascending=True)
    fig,ax=_figure(9,max(3.6,len(vals)*.6+1));y=np.arange(len(vals));bars=ax.barh(y,vals.records,color=TEAL,height=.60)
    ax.set_yticks(y,labels=vals.label); ax.set_xlim(0,max(vals.records)*1.17 if len(vals) else 1)
    ax.set_xlabel('Mapped Retrieval Cases (multi-label; themes overlap)',fontsize=9,color=MUTED)
    ax.grid(axis='x',color=GRID,zorder=0);ax.set_axisbelow(True)
    for bar,v in zip(bars,vals.records):ax.text(v+.1,bar.get_y()+bar.get_height()/2,str(v),va='center',color=INK,weight='bold')
    fig.tight_layout(pad=1.2);return fig

def journey_matrix(frame:pd.DataFrame):
    known=frame[(frame.memory_type!='Unknown')&(frame.failure_stage!='Unknown')]
    c=pd.crosstab(known.memory_type,known.failure_stage)
    if c.empty:return None
    fig,ax=_figure(9,max(3.1,len(c)*.7+1.4))
    im=ax.imshow(c.values,cmap='BuGn',vmin=0,vmax=max(2,int(c.values.max())),aspect='auto')
    ax.set_xticks(range(len(c.columns)),c.columns,rotation=20,ha='right',fontsize=9)
    ax.set_yticks(range(len(c.index)),c.index,fontsize=10)
    for (i,j),n in np.ndenumerate(c.values):ax.text(j,i,str(n) if n else '–',ha='center',va='center',fontsize=10,color=INK if n<2 else 'white',weight='bold')
    fig.tight_layout(pad=1.4);return fig
