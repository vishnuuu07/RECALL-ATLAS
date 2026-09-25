from __future__ import annotations
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

PALETTE=['#087e7a','#d99333','#d66356','#537fa1','#625a91','#6c9174']
LAYOUT=dict(template='plotly_white',font=dict(family='Inter'),paper_bgcolor='#fffdf8',plot_bgcolor='#fffdf8',margin=dict(l=12,r=12,t=38,b=12))
def bar(df:pd.DataFrame,x:str,y:str,title:str):
    fig=px.bar(df,x=x,y=y,color=x,color_discrete_sequence=PALETTE,title=title); fig.update_layout(**LAYOUT,showlegend=False); return fig
def journey(df:pd.DataFrame):
    labels=[]
    for v in list(df.memory_type)+list(df.failure_stage)+list(df.outcome):
        if v and v not in labels: labels.append(v)
    index={x:i for i,x in enumerate(labels)}; src=[]; tar=[]; vals=[]
    for _,r in df.iterrows():
        if r.memory_type and r.failure_stage: src.append(index[r.memory_type]);tar.append(index[r.failure_stage]);vals.append(1)
        if r.failure_stage and r.outcome: src.append(index[r.failure_stage]);tar.append(index[r.outcome]);vals.append(1)
    fig=go.Figure(go.Sankey(node=dict(label=labels,pad=14,color='#0b8b84'), link=dict(source=src,target=tar,value=vals,color='rgba(11,139,132,.25)')))
    fig.update_layout(**LAYOUT,title='Observed retrieval journey transitions'); return fig
def heatmap(coverage:pd.DataFrame):
    vals=coverage.pivot(index='group',columns='question_id',values='evidence_count').fillna(0)
    fig=px.imshow(vals,color_continuous_scale=['#f5e6c7','#0b8b84'],title='Evidence-gap heatmap — supporting records by question')
    fig.update_layout(**LAYOUT); return fig

