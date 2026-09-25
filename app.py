"""Recall Atlas v0.4 — evidence-first public research explorer.

Runs wholly from a local, versioned SQLite snapshot built from the supplied
70 source-linked account rows. No network access, API keys or LLM calls at runtime.
"""
from __future__ import annotations
import html
import json
import sqlite3
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

ROOT=Path(__file__).resolve().parent
DB=ROOT/'data'/'public'/'recall_atlas_70_cases.sqlite'
META=ROOT/'data'/'manifests'/'retrieval_cases_70_manifest.json'
SYN=ROOT/'outputs'/'retrieval_case_synthesis.json'
INK='#1e3840'; TEAL='#356a65'; GOLD='#ad8241'; LIGHT='#e6ece6'; MUTED='#566b70'

st.set_page_config(page_title='Recall Atlas | Retrieval Research',page_icon='◌',layout='wide',initial_sidebar_state='expanded')
st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,600;9..144,700&display=swap');
.stApp{background:#faf9f5;color:#1e3840;font-family:'DM Sans',sans-serif}
.block-container{max-width:1360px!important;padding:1.25rem 2.1rem 3.4rem!important}
h1,h2,h3{font-family:Fraunces,Georgia,serif!important;color:#1e3840!important;letter-spacing:-.015em}
h1{font-size:2.2rem!important;line-height:1.15!important}h2{font-size:1.5rem!important}h3{font-size:1.2rem!important}
[data-testid="stSidebar"]{background:#1e3840}[data-testid="stSidebar"] *{color:#f6f7f1!important}
[data-testid="stSidebar"] [role="radiogroup"] label{padding:.42rem .15rem;font-size:1rem!important}
.hero{background:linear-gradient(105deg,#1e3840,#39685d);color:white;border-radius:15px;padding:1.45rem 1.8rem;margin-bottom:1rem}
.hero h1{color:white!important;margin:.28rem 0 .55rem!important;font-size:2.2rem!important}
.hero p{color:#e7f1ed!important;margin:0!important;font-size:1rem}
.eyebrow{color:#a6ded0;letter-spacing:.12em;text-transform:uppercase;font-weight:700;font-size:.72rem}
.metric{border:1px solid #dce5df;background:white;border-radius:12px;padding:1rem 1.1rem;min-height:100px}
.metric strong{font:700 2rem Fraunces,Georgia,serif;color:#34695f}.metric small{font-size:.85rem;color:#4f666a}
.insight{background:white;border:1px solid #dae2dc;border-radius:12px;padding:1rem 1.15rem;margin:.45rem 0}
.insight h3{font-size:1.21rem!important;margin:.1rem 0 .4rem!important}.insight p{font-size:.96rem;margin:.28rem 0}
.insight .eyebrow{color:#367d6f}.notice{background:#fff1dc;border-left:4px solid #b8813b;border-radius:5px;padding:.75rem 1rem;margin:.8rem 0;font-size:.95rem}
[data-testid="stExpander"]{background:#fff;border:1px solid #dfe4df;border-radius:9px}
[data-testid="stDataFrame"]{border:1px solid #dce4e1;border-radius:8px}
[data-testid="stHorizontalBlock"]{align-items:stretch}
footer{color:#60716e}small{font-size:.86rem}
@media(max-width:750px){.block-container{padding:.8rem .7rem 2rem!important}.hero{padding:1rem}.hero h1{font-size:1.7rem!important}}
</style>''',unsafe_allow_html=True)

@st.cache_data

def load():
    with sqlite3.connect(f'file:{DB.as_posix()}?mode=ro',uri=True) as con:
        cases=pd.read_sql_query('SELECT * FROM cases ORDER BY case_id',con)
    cases['tags']=cases.theme_labels.map(json.loads)
    meta=json.loads(META.read_text(encoding='utf8'))
    findings=json.loads(SYN.read_text(encoding='utf8'))['findings']
    return cases,meta,findings

cases,meta,findings=load()
NAV=['Overview','Explore evidence','Opportunities','Methodology']
with st.sidebar:
    st.markdown('### RECALL ATLAS')
    st.caption('Vague-memory photo retrieval · Evidence explorer')
    page=st.radio('Navigate',NAV,label_visibility='collapsed')
    st.divider()
    st.caption('70 source-case rows · 60 linked discussion URLs')
    st.caption('Independent research. Not affiliated with Google.')


def escape(s):return html.escape(str(s))

def hero(kicker,title,subtitle):
    st.markdown(f'<div class="hero"><div class="eyebrow">{escape(kicker)}</div><h1>{escape(title)}</h1><p>{escape(subtitle)}</p></div>',unsafe_allow_html=True)

def metrics(items):
    for col,(v,label) in zip(st.columns(len(items)),items):
        col.markdown(f'<div class="metric"><strong>{escape(v)}</strong><br><small>{escape(label)}</small></div>',unsafe_allow_html=True)

def bar(data,title,width=8.5,height=3.2,color=TEAL):
    items=[(str(k),int(v)) for k,v in data.items() if int(v)>0]
    if not items:
        st.info('No classified case rows in this selection.');return
    items=sorted(items,key=lambda x:x[1],reverse=True)
    fig,ax=plt.subplots(figsize=(width,height))
    fig.patch.set_facecolor('#faf9f5');ax.set_facecolor('#faf9f5')
    vals=[v for _,v in items]
    ax.barh(list(range(len(items))), vals, color=color, height=.55)
    ax.set_yticks(list(range(len(items))),[k for k,_ in items],fontsize=10,color=INK)
    ax.invert_yaxis();ax.tick_params(axis='y',length=0);ax.tick_params(axis='x',colors=MUTED,labelsize=9)
    ax.set_xlim(0,max(vals)*1.14+0.5)
    ax.spines[:].set_visible(False)
    ax.grid(axis='x',alpha=.14);ax.set_axisbelow(True)
    for i,v in enumerate(vals):ax.text(v+.15,i,str(v),va='center',fontsize=10,color=INK,fontweight='bold')
    fig.tight_layout(pad=1.6)
    st.pyplot(fig,use_container_width=True,clear_figure=True);plt.close(fig)

def count_tag(tag,frame=cases):return int(frame.tags.map(lambda x:tag in x).sum())

def case_box(r,expanded=False):
    name=f"{r.case_id} · {r.title[:88]}"
    with st.expander(name,expanded=expanded):
        st.write('**Retrieval goal:** '+r.retrieval_goal)
        st.write('**Remembered:** '+r.remembered_clues)
        st.write('**Not known / not remembered:** '+r.forgotten_clues)
        st.write('**Initial action:** '+r.initial_action)
        st.write('**Reported result:** '+r.reported_results)
        st.write('**Next step:** '+r.refinement)
        st.write('**Workaround:** '+r.workaround)
        st.write('**Reported outcome:** '+r.outcome)
        st.caption('Case focus: '+r.case_focus+' · Analyst tags: '+(', '.join(r.tags) if r.tags else 'No tag assigned'))
        if r.source_excerpt:
            st.caption('Source excerpt/supplied account summary: '+r.source_excerpt)
        st.link_button('Open supplied original discussion',r.source_url)
        st.caption('Structured source-case summary; not a verbatim interview transcript. Link accessibility not independently rechecked.')

def download(label,df,name):
    st.download_button(label,df.to_csv(index=False).encode('utf-8-sig'),file_name=name,mime='text/csv')

if page=='Overview':
    hero('Research intelligence · local and inspectable','70 accounts. Four distinct retrieval questions.',
         'A targeted source-linked case collection: what people recall, try, and report next. Counts describe this collection, not all Google Photos users.')
    metrics([(len(cases),'Source-case rows'),(cases.source_url.nunique(),'Distinct discussion URLs'),
             ((cases.case_focus=='Memory-led account').sum(),'Memory-led case coding'),(len(findings),'Research directions')])
    st.markdown('### What is in this collection?')
    left,right=st.columns(2,gap='large')
    with left:
        st.markdown('**Source composition**')
        bar(cases.source_platform.value_counts().to_dict(),'sources',height=2.35)
    with right:
        st.markdown('**Research scope of coded case rows**')
        bar(cases.case_focus.value_counts().to_dict(),'scope',height=2.45,color='#4b8378')
    st.markdown('### Four evidence-led questions worth testing')
    cols=st.columns(2,gap='medium')
    for i,f in enumerate(findings):
        n=count_tag(f['tag'])
        with cols[i%2]:
            st.markdown(f'<div class="insight"><div class="eyebrow">{escape(f["id"])} · {n} coded case rows</div><h3>{escape(f["title"])}</h3><p>{escape(f["observed"])}</p><p style="color:#556971;font-size:.88rem"><b>Qualifying evidence:</b> {escape(f["qualification"])}</p></div>',unsafe_allow_html=True)
    st.markdown('### Compare the reported behaviours')
    a,b=st.columns(2,gap='large')
    with a:
        st.markdown('**Theme coverage (multi-label codes)**')
        bar({k:count_tag(k) for k in ['Collection / scope','Literal text / file cue','Candidate → surrounding context','Related-image clue']},'themes',height=3.25)
        st.caption('A case may be assigned more than one analyst-defined theme. These counts are not a popularity ranking.')
    with b:
        st.markdown('**Source-reported resolution category**')
        bar(cases.outcome_group.value_counts().to_dict(),'reported outcomes',height=3.25,color=GOLD)
        st.caption('"Reported target/route found" includes a successfully found navigation route, not necessarily the target asset. This is not a verified retrieval success rate.')
    st.markdown('### The actual research handoff')
    st.write('Start with a known target and reproduce the current flow. Compare **collection-scoped search**, **literal-text expectation**, and **candidate-to-event navigation** against existing features before choosing one narrow MVP. First rule out missing-account or backup issues.')
    download('Export the complete case table',cases.drop(columns=['tags']), 'recall_atlas_70_cases.csv')

elif page=='Explore evidence':
    hero('Every statement is traceable','Inspect the account before accepting the theme.',
         'Source-linked summaries retain original account context, actions and reported outcomes; source websites are never needed to render the dashboard.')
    q=st.text_input('Search goals, clues, actions and results',placeholder='album, screenshot, family, exact text…')
    ca,cb,cc=st.columns(3)
    chosen_source=ca.multiselect('Source',sorted(cases.source_platform.unique()))
    chosen_focus=cb.multiselect('Research scope',sorted(cases.case_focus.unique()))
    chosen_tags=cc.multiselect('Research themes',list(sorted(set(t for xs in cases.tags for t in xs))))
    mask=pd.Series(True,index=cases.index)
    if q.strip():
        fields=['title','retrieval_goal','remembered_clues','forgotten_clues','initial_action','reported_results','refinement','workaround','outcome']
        mask &= pd.concat([cases[c].fillna('').str.contains(q.strip(),case=False,regex=False) for c in fields],axis=1).any(axis=1)
    if chosen_source:mask &= cases.source_platform.isin(chosen_source)
    if chosen_focus:mask &= cases.case_focus.isin(chosen_focus)
    if chosen_tags:mask &= cases.tags.map(lambda tags:any(t in tags for t in chosen_tags))
    sub=cases[mask]
    st.caption(f'{len(sub)} matching case rows · {sub.source_url.nunique()} linked discussions · filters applied before pagination')
    if sub.empty:st.info('No matching records. Change or clear filters.')
    else:
        max_pages=max(1,(len(sub)+7)//8)
        pg=st.number_input('Page',min_value=1,max_value=max_pages,value=1,step=1) if max_pages>1 else 1
        for i,(_,r) in enumerate(sub.iloc[(pg-1)*8:pg*8].iterrows()):case_box(r,expanded=(i==0))
    download('Export filtered cases',sub.drop(columns=['tags']),'recall_atlas_filtered_cases.csv')

elif page=='Opportunities':
    hero('Evidence → counterexample → validation task','Decide what to investigate, not what to ship.',
         'Four intervention areas are competing research hypotheses. A successful workaround may indicate an existing feature rather than an entirely new capability.')
    summary=pd.DataFrame([{'Question':f['title'],'Coded cases':count_tag(f['tag']),'Illustrative case IDs':', '.join(f['examples']),'Status':'Unvalidated'} for f in findings])
    st.dataframe(summary,hide_index=True,use_container_width=True)
    selected=st.selectbox('Investigate a research question',[f['title'] for f in findings])
    f=next(x for x in findings if x['title']==selected)
    rows=cases[cases.tags.map(lambda t:f['tag'] in t)]
    metrics([(len(rows),'Coded case rows'),(rows.source_url.nunique(),'Distinct linked discussions'),(len(f['examples']),'Illustrative cases')])
    st.markdown('#### Observed accounts');st.write(f['observed'])
    st.markdown('#### Why that is not yet a proven root cause');st.info(f['qualification'])
    st.markdown('#### Test in an actual retrieval session');st.write(f['question'])
    st.markdown('#### Outcome to measure');st.write(f['metric'])
    st.markdown('#### Inspect illustrative evidence')
    for i,cid in enumerate(f['examples']):
        for _,r in cases[cases.case_id==cid].iterrows():case_box(r,expanded=i==0)
    st.markdown('#### Nearby evidence / counterexamples')
    qualifying=cases[cases.theme_labels.str.contains('Reported successful route or workaround',regex=False)]
    st.caption('Read reported successful routes as comparison cases. Do not assume that an existing capability is missing without reproducing the task.')
    st.dataframe(qualifying[['case_id','retrieval_goal','outcome']].head(8),hide_index=True,use_container_width=True)
    download('Export opportunity comparison',summary,'recall_atlas_opportunities.csv')

else:
    hero('Transparent method · honest boundaries','Source-linked accounts, not a participant panel.',
         'The collection supports research hypotheses and concrete follow-up tasks, not population rates, causal proof or claims of 70 conducted interviews.')
    st.markdown('### Dataset construction')
    st.write('The supplied workbook contains 70 structured rows (S01–S70). Every row contains an account summary and a supplied discussion link. Ten rows share a URL with another row; this is why 70 case rows represent 60 distinct links. Different comments on one thread are not automatically independent corroboration.')
    st.write('Only the structured episode fields were imported. The eight editorial Q&A reconstructions per case were not counted as separate records or treated as verbatim quotations. Cases S01–S20 use the earlier workbook’s source metadata; S21–S70 use the source URL given in the row’s final annotation.')
    st.write('The scope and themes are explicit analyst mappings (see scripts/build_retrieval_cases_v04.py), not newly measured model accuracy. The original 24-record snapshot remains in the repository for historical reproducibility; it is not added to the 70-case headline to avoid unreviewed duplication.')
    st.markdown('### Where the source rows came from')
    st.dataframe(pd.DataFrame([{'Source':k,'Case rows':v} for k,v in meta['source_distribution'].items()]),hide_index=True,use_container_width=True)
    st.warning('Links were supplied in the workbook but have not all been independently rechecked for accessibility. Source coverage is mostly Reddit; case counts are descriptive, not representative.')
    st.markdown('### Research questions: what this evidence can and cannot answer')
    qlist=[
      ('What old visual assets are discussed?','Photos, screenshots, videos, albums and related visual assets are described. Case selection prevents a population-frequency claim.','S02, S04, S19, S32'),
      ('What is remembered?','Accounts contain explicit people, object, approximate period, text, location and collection clues.','S01, S02, S03, S04, S08'),
      ('What is forgotten?','Some disclose a missing date, filename or indexing detail; others omit this information. Missing descriptions are not evidence of forgetting.','S01, S02, S04, S21'),
      ('How do people first search?','Examples include descriptive phrases, exact terms, date search, album browsing, and using a related image. Reconstructed prompts are not original spoken interviews.','S02, S04, S23, S30'),
      ('What happens after an unsuccessful attempt?','Some report chronological browsing, quoted text, mode-switching or another navigation route. Many end states remain unknown.','S02, S04, S20, S23'),
      ('Which failure cause is proven?','None by case narratives alone. Check the target exists, account scope and actual search behaviour in consented tasks.','S18, S19, S58'),
    ]
    for question,answer,ids in qlist:
        with st.expander(question):st.write(answer);st.caption('Illustrative source IDs: '+ids)
    st.markdown('### Research process and next step')
    st.write('Source-linked account → structured retrieval fields → cautious analyst theme → compare successful and unsuccessful routes → reproduce task with participant → choose one tested intervention.')
    st.write('The earlier 24-record pipeline reports an offline Sentence Transformer/KMeans stage. This 70-case extension is explicitly a structured, manually mapped import; no fresh model run is claimed for it.')
    st.markdown('### Snapshot validation')
    st.json({k:v for k,v in meta.items() if k not in {'theme_counts'}},expanded=False)
    st.caption('Independent research project · not affiliated with Google. No personal images or private libraries are included in this dashboard.')
    download('Export source manifest',cases[['case_id','source_platform','source_url','source_status']],'recall_atlas_source_manifest.csv')
