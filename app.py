"""Recall Atlas v0.5 — direct, evidence-linked Part 1 answers.

Runs wholly from a local, versioned SQLite snapshot built from the supplied
70 source-linked account rows. No network access, API keys or LLM calls at runtime.
"""
from __future__ import annotations
import html
import json
import sqlite3
from collections import Counter
from recall_atlas.assignment_answers import QUESTIONS, CASE_LENSES, lens_counts, relevant_records, validate_mappings
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
.block-container{max-width:1540px!important;width:94%!important;padding:1.1rem 1.4rem 3.2rem!important}
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
.qa-card{background:#ffffff;border:1px solid #d9e5df;border-radius:12px;padding:1.05rem 1.25rem;margin:.3rem 0 .65rem;min-height:174px}
.qa-card strong{display:block;font:700 1.15rem Fraunces,Georgia,serif;color:#1e3840;margin:.3rem 0 .55rem}
.qa-card p{margin:.32rem 0;color:#304b50;font-size:1rem;line-height:1.48}
.qa-card small{color:#577079;font-size:.84rem}
.qa-evidence{background:#eef5f1;border-left:4px solid #367368;padding:.75rem 1rem;border-radius:5px;font-size:.96rem}
.sectionline{border-top:1px solid #dce5df;margin:1.2rem 0}
[data-testid="stMarkdownContainer"] p{line-height:1.5}
[data-testid="stDataFrame"]{font-size:1rem!important}

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
validate_mappings(set(cases.case_id))
NAV=['Overview','Research answers','Explore evidence','Opportunities','Methodology']
with st.sidebar:
    st.markdown('### RECALL ATLAS')
    st.caption('Vague-memory photo retrieval · Evidence explorer')
    page=st.radio('Navigate',NAV,label_visibility='collapsed')
    st.divider()
    st.caption(f'{len(cases)} source-case rows · {cases.source_url.nunique()} linked discussions')
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
        st.link_button('Open original discussion for '+r.case_id+' ↗',r.source_url)
        st.caption('Structured source-case summary; not a verbatim interview transcript. Link accessibility not independently rechecked.')

def download(label,df,name):
    st.download_button(label,df.to_csv(index=False).encode('utf-8-sig'),file_name=name,mime='text/csv')

def question_card(q):
    st.markdown(f'<div class="qa-card"><div class="eyebrow">{escape(q["id"])} · ASSIGNMENT QUESTION</div><strong>{escape(q["title"])}</strong><p>{escape(q["short"])}</p><small>Examples: {escape(", ".join(q["ids"][:4]))} · Open Research answers for sources and boundaries.</small></div>',unsafe_allow_html=True)


def answer_detail(q,expanded_evidence=False):
    st.markdown(f'### {q["id"]}. {q["title"]}')
    st.markdown(f'<div class="qa-evidence"><b>Answer from the recorded cases</b><br>{escape(q["answer"])}</div>',unsafe_allow_html=True)
    if q['lens']:
        left,right=st.columns([1,1.07],gap='large')
        with left:
            st.markdown('**Recorded case examples**')
            for _,r in relevant_records(q,cases).head(5).iterrows():
                st.markdown(f'**{escape(r.case_id)}** — {escape(r.retrieval_goal)}')
            st.caption('Source-linked rows; a case can support several answers.')
        with right:
            st.markdown('**Evidence lens — coded case rows**')
            bar(lens_counts(q['lens'],set(cases.case_id)),'question lens',width=7,height=3.4)
            st.caption('Non-exclusive, manually defined codes within the memory-led subset; not Google Photos prevalence.')
    else:
        st.markdown('**Illustrative source-backed records**')
        st.write(', '.join(q['ids']))
    st.caption('**Boundary:** '+q['limit'])
    with st.expander(f'Inspect {q["id"]} source accounts ({len(q["ids"])} mapped examples)',expanded=expanded_evidence):
        st.caption('Source-case summaries, not verbatim interview quotations. Original URLs may need independent rechecking.')
        for _,r in relevant_records(q,cases).iterrows():
            st.markdown(f'**{escape(r.case_id)} — {escape(r.title)}**')
            st.write('**Goal:** '+r.retrieval_goal)
            st.write('**Recorded action:** '+r.initial_action)
            st.write('**Reported outcome:** '+r.outcome)
            st.link_button('Open '+r.case_id+' source for '+q['id']+' ↗',r.source_url)
            st.divider()
    st.divider()


if page=='Overview':
    hero('Research intelligence · fixed local evidence','Why does a remembered photo remain hard to retrieve?',
         'Direct answers to the assignment, recorded behaviours, and distinct problems to test. This selected public-case collection is directional—not a user-population survey.')
    metrics([(len(cases),'Source-case rows'),(int((cases.case_focus=='Memory-led account').sum()),'Memory-led cases'),
             (cases.source_url.nunique(),'Distinct discussion URLs'),(len(findings),'Problem directions')])
    st.markdown('## The four questions in the assignment — answered')
    st.caption('These are source-grounded observations; open Research answers for supporting cases, charts, and what the data cannot establish.')
    qa=st.columns(2,gap='large')
    for i,q in enumerate(QUESTIONS[:4]):
        with qa[i%2]:question_card(q)
    st.markdown('## The problems differ — so their solutions may differ')
    st.caption('Analyst-coded coverage in the 70 source-case rows. Codes overlap; these are not product failure rates.')
    counts={f['title']:count_tag(f['tag']) for f in findings}
    left,right=st.columns([1.1,.9],gap='large')
    with left:
        bar({k if len(k)<46 else k[:42]+'…':v for k,v in counts.items()},'directions',width=8,height=3.65)
    with right:
        st.markdown('**Three concrete contrasts**')
        st.markdown('**Collection scope:** S32 can identify the correct album but has trouble locating a specific image inside it.')
        st.markdown('**Literal clue:** S30 has an exact filename yet does not confirm finding that file.')
        st.markdown('**Related candidate:** S23 reports reaching same-day images after changing result sorting—an existing recovery route.')
        st.info('An apparent missing result is a separate diagnosis: confirm that the asset exists in the right account before calling it a retrieval failure.')
    st.markdown('## How much of the evidence is directly in scope?')
    c1,c2=st.columns(2,gap='large')
    with c1:
        st.markdown('**Case selection**')
        bar(cases.case_focus.value_counts().to_dict(),'scope',height=3.1)
    with c2:
        st.markdown('**Source composition**')
        bar(cases.source_platform.value_counts().to_dict(),'sources',height=2.75)
    st.caption('70 structured cases span 60 supplied discussion URLs; the majority are Reddit. Cases may share a discussion and are not independent interview participants.')
    st.markdown('### What this research changes')
    st.write('**We should not build a generic AI photo chatbot yet.** The cases suggest at least three testable bottlenecks—expressing remembered context, applying exact clues, and progressing from a related result to the target. Interview tasks must establish which mechanism fails in a reproducible retrieval attempt.')
    st.caption('AI-method boundary: the previous 24-record corpus underwent Sentence Transformer/KMeans processing; the 70-case expansion includes a separately executed offline TF-IDF/SVD/KMeans exploratory pass. Final labels and assignment answers are human-defined evidence mappings, not validated model predictions.')
    download('Export source-case table',cases.drop(columns=['tags']), 'recall_atlas_70_cases.csv')

elif page=='Research answers':
    hero('Direct assignment coverage · source-linked answers','What do people remember, forget, search—and do next?',
         'The four questions from Part 1 are answered first. Four further questions compare failures, workarounds and research gaps. Every assertion below points to recorded case IDs.')
    metrics([(4,'Original brief questions'),(8,'Evidence-mapped questions'),(29,'Memory-led case codes'),(60,'Distinct linked discussions')])
    st.warning('Reading rule: selected source cases are not representative of all users. Some fields are missing, and Q&A reconstructions are not independent interview transcripts.')
    for q in QUESTIONS:answer_detail(q)
    st.markdown('### Export question-to-evidence map')
    qdf=pd.DataFrame([{'question_id':q['id'],'question':q['title'],'answer':q['answer'],'example_case_ids':', '.join(q['ids']),'boundary':q['limit']} for q in QUESTIONS])
    download('Export all research answers',qdf,'recall_atlas_assignment_answers.csv')

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
    st.markdown('### Assignment-question coverage')
    st.write('All four original questions and four additional behavioural questions have direct answers, evidence IDs, charts or explicit limitations under **Research answers** in the navigation. They are not hidden behind this technical appendix.')
    st.dataframe(pd.DataFrame([{'ID':q['id'],'Research question':q['title'],'Mapped cases':len(q['ids'])} for q in QUESTIONS]),hide_index=True,use_container_width=True)
    st.markdown('### Research process and next step')
    st.write('Source-linked account → structured retrieval fields → cautious analyst theme → compare successful and unsuccessful routes → reproduce task with participant → choose one tested intervention.')
    st.write('The earlier 24-record pipeline reported Sentence Transformer/KMeans processing. For this 70-case edition an offline exploratory TF-IDF → TruncatedSVD → KMeans model was also executed; the manual case themes and evidence answers are distinct from its unvalidated clusters.')
    ml_file=ROOT/'outputs'/'offline_ml_analysis.json'
    if ml_file.exists():
        ml=json.loads(ml_file.read_text(encoding='utf8'))
        st.caption(f'Offline ML pass: {ml["records"]} case texts · k={ml["k"]} · silhouette={ml["silhouette_score"]} (weak cluster separation; NOT classifier accuracy).')
        with st.expander('Inspect exploratory machine-learning clusters (not research conclusions)'):
            st.dataframe(pd.DataFrame([{'Cluster':x['cluster_id'],'Rows':x['rows'],'Terms':', '.join(x['top_terms'][:7]),'Case IDs':', '.join(x['case_ids'])} for x in ml['clusters']]),use_container_width=True,hide_index=True)
    else:st.warning('70-case offline ML analysis not present; run scripts/analyze_70_semantics.py with requirements-research.txt to reproduce it.')
    st.markdown('### Snapshot validation')
    st.json({k:v for k,v in meta.items() if k not in {'theme_counts'}},expanded=False)
    st.caption('Independent research project · not affiliated with Google. No personal images or private libraries are included in this dashboard.')
    download('Export source manifest',cases[['case_id','source_platform','source_url','source_status']],'recall_atlas_source_manifest.csv')
