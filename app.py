"""Recall Atlas public research dashboard. 4-minute reviewer narrative; fixed local data."""
from __future__ import annotations
import html
import json
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from recall_atlas.styles import inject_css
from recall_atlas.data_access import table,manifest
from recall_atlas.metrics import funnel
from recall_atlas.charts import funnel_chart,source_chart,themes_chart,journey_matrix
from recall_atlas.evidence import record_card,clean
from recall_atlas.research_views import FINDINGS,QUESTIONS,evidence_for,validate_editorial_ids

st.set_page_config(page_title='Recall Atlas | Photo Retrieval Research',page_icon='◌',layout='wide',initial_sidebar_state='expanded')
inject_css()
NAV=['Overview','Explore evidence','Opportunities','Methodology']
with st.sidebar:
    st.markdown('### RECALL ATLAS')
    st.caption('Vague-memory photo retrieval research')
    page=st.radio('Research navigation',NAV,label_visibility='collapsed')
    st.divider()
    st.caption('Independent product-management research. Not affiliated with Google.')

@st.cache_data
def load():
    return table('evidence'),manifest()
ev,meta=load()
relevant=ev[ev.relevance.isin(['DIRECT','RELATED'])].copy()
rich=relevant[relevant.evidence_depth.isin(['E1','E2'])].copy()
missing_ids=validate_editorial_ids(ev)
if missing_ids:
    st.error('Evidence mapping refers to missing records: '+', '.join(missing_ids))
    st.stop()

def hero(kicker,title,body):
    st.markdown(f'<div class="hero"><div class="eyebrow">{html.escape(kicker)}</div><h1>{html.escape(title)}</h1><p>{html.escape(body)}</p></div>',unsafe_allow_html=True)

def metric_row(items):
    for col,(n,label) in zip(st.columns(len(items)),items):
        col.markdown(f'<div class="metric"><div class="n">{html.escape(str(n))}</div><div class="l">{html.escape(label)}</div></div>',unsafe_allow_html=True)

def show_chart(fig):
    if fig is None:
        st.info('Not enough recorded transitions for a meaningful chart. See the individual source records.')
    else:
        st.pyplot(fig,clear_figure=True,use_container_width=True)
        plt.close(fig)

def counts(f):
    sub=evidence_for(f,relevant)
    return len(sub),int(sub.evidence_depth.isin(['E1','E2']).sum()),sub.source_platform.nunique()

def finding_card(f):
    n,r,s=counts(f)
    st.markdown('<div class="finding"><div class="eyebrow">Research hypothesis · '+html.escape(f['id'])+'</div><h3>'+html.escape(f['title'])+'</h3><p>'+html.escape(f['short'])+'</p><p><b>'+str(n)+' source-backed records</b> · '+str(r)+' E1/E2 coded records · '+str(s)+' source platforms</p></div>',unsafe_allow_html=True)

def evidence_list(ids,max_show=None):
    subset=ev[ev.record_id.isin(ids)]
    if max_show:subset=subset.head(max_show)
    for _,row in subset.iterrows():record_card(row)

def export_df(label,frame,name):
    st.download_button(label,frame.to_csv(index=False).encode('utf-8-sig'),name,'text/csv',key='download_'+name)

if page=='Overview':
    hero('AI-powered research · fixed local evidence','Where does a remembered photo become hard to find?',
         '24 targeted public records → traceable retrieval hypotheses. This sample reveals research directions, not population prevalence or a confirmed root cause.')
    metric_row([(meta['raw_record_count'],'Public records'),(len(relevant),'Relevant signals'),(len(rich),'E1/E2 coded records'),(ev.source_platform.nunique(),'Source platforms')])
    st.markdown('### The evidence, at a glance')
    a,b=st.columns([1,1],gap='large')
    with a:
        st.markdown('**From collection to useful episodes**')
        show_chart(funnel_chart(funnel(ev,meta['raw_record_count'])))
        st.caption('Purposefully retrieval-enriched collection. The E1/E2 label is an automated coding, not independent verification.')
    with b:
        st.markdown('**Source composition**')
        show_chart(source_chart(ev))
        st.caption('Reddit and Community provide most of the source records. PIXLS.US is cross-product context, not Google Photos evidence.')
    st.markdown('### Four directions emerging from the source records')
    for f in FINDINGS:finding_card(f)
    st.markdown('<div class="notice"><b>Evidence boundary:</b> These records do not establish prevalence, product causality, target availability, verified retrieval success or user-segment size. The six E1 labels mean outcome-stated in public accounts, not independently verified success.</div>',unsafe_allow_html=True)
    st.markdown('### Compare the observed mechanisms')
    df=pd.DataFrame([{'label':f['chart_label'],'records':counts(f)[0],'rich':counts(f)[1],'sources':counts(f)[2]} for f in FINDINGS])
    show_chart(themes_chart(df))
    st.caption('Multi-label research categories: one source may support more than one direction. This is a targeted sample, not a user prevalence ranking.')
    st.markdown('### Where recorded memory meets retrieval breakdown')
    show_chart(journey_matrix(relevant))
    st.caption('Only fields coded as known in both dimensions are included. Automated codes require interview validation; cell counts are not sequential user journeys.')
    export_df('Export overview counts',pd.DataFrame([{'raw':meta['raw_record_count'],'publishable':len(ev),'relevant':len(relevant),'E1_E2':len(rich)}]),'overview_counts.csv')

elif page=='Explore evidence':
    hero('Every claim has a source','Read the retrieval episodes, not just their labels.',
         'Search a locally stored, read-only research snapshot. The original-source link is optional and never required to render this dashboard.')
    c1,c2=st.columns([2,1]); q=c1.text_input('Search excerpts and titles',placeholder='Album, screenshot, filename, date…');source=c2.multiselect('Source',sorted(ev.source_platform.unique()))
    c3,c4,c5=st.columns(3)
    relevance=c3.multiselect('Evidence relevance',sorted(ev.relevance.unique()),default=['DIRECT','RELATED'])
    depths=c4.multiselect('Evidence depth',sorted(ev.evidence_depth.unique()))
    categories=c5.multiselect('Research direction',[f['title'] for f in FINDINGS])
    mask=pd.Series(True,index=ev.index)
    if q.strip():
        mask &= (ev.public_excerpt.fillna('').str.contains(q.strip(),regex=False,case=False)|ev.source_title.fillna('').str.contains(q.strip(),regex=False,case=False))
    if source:mask &= ev.source_platform.isin(source)
    if relevance:mask &= ev.relevance.isin(relevance)
    if depths:mask &= ev.evidence_depth.isin(depths)
    if categories:
        ids=set().union(*(set(f['ids']) for f in FINDINGS if f['title'] in categories))
        mask &= ev.record_id.isin(ids)
    filtered=ev[mask].sort_values(['source_platform','record_id'])
    st.caption(f'{len(filtered)} matching records · {int(filtered.evidence_depth.isin(["E1","E2"]).sum())} E1/E2 coded. Full filters applied before pagination.')
    max_pages=max(1,(len(filtered)+7)//8)
    p=st.number_input('Page',1,max_pages,1,step=1) if max_pages>1 else 1
    current=filtered.iloc[(p-1)*8:p*8]
    if current.empty:st.info('No matching evidence. Adjust or reset the filters.')
    for i,(_,r) in enumerate(current.iterrows()):record_card(r,expanded=(i==0))
    export_df('Export filtered evidence',filtered[['record_id','source_platform','source_url','public_excerpt','relevance','evidence_depth','themes']], 'filtered_evidence.csv')

elif page=='Opportunities':
    hero('Evidence → hypothesis → observed task','Four problem directions. No preselected feature.',
         'Compare real retrieval examples and counterexamples before choosing what to test in five or six interviews.')
    rows=[]
    for f in FINDINGS:
        n,r,s=counts(f)
        rows.append({'Hypothesis':f['title'],'Source records':n,'E1/E2 coded':r,'Sources':s,'Status':f['status']})
    stats=pd.DataFrame(rows)
    st.dataframe(stats,hide_index=True,use_container_width=True)
    st.caption('Counts are overlapping, deliberately collected research records. No combined business-impact score or prevalence estimate is asserted.')
    choice=st.selectbox('Investigate a hypothesis',[f['title'] for f in FINDINGS]);f=next(x for x in FINDINGS if x['title']==choice)
    n,r,s=counts(f)
    metric_row([(n,'Supporting records'),(r,'E1/E2 coded'),(s,'Source platforms')])
    st.markdown('#### What the actual record describes')
    st.write(f['episode']);st.markdown('**Observed:** '+f['observed'])
    st.markdown('**Possible mechanism — not proven:** '+f['mechanism'])
    st.markdown('**Counterevidence / qualifying context:** '+f['qualification'])
    st.markdown('**Interview test:** '+f['question'])
    st.markdown('**Outcome to measure:** '+f['metric'])
    st.markdown('#### Source evidence');evidence_list(f['ids'])
    st.markdown('#### What might overturn the hypothesis?')
    st.info('Observe a consented retrieval task where the same clues lead to verified success using an existing capability. Compare effort and end state before proposing a new intervention.')
    st.markdown('#### Research-to-solution gate')
    st.write('Only select a solution after observed tasks establish the target asset exists, document the current search/refinement path, and identify a reproducible failure not adequately addressed by available product capabilities.')
    export_df('Export opportunity comparison',stats,'opportunity_comparison.csv')

else:
    hero('Transparent methodology','Small, targeted corpus. Clear limits.',
         'The method is documented so evaluators can distinguish real source evidence from automated classification and research hypotheses.')
    st.markdown('### How the engine works')
    st.markdown('**Collect → Normalise → Deduplicate → Deterministic relevance/taxonomy → Offline sentence embeddings and KMeans → Evidence mapping → Publish snapshot.**')
    st.write('The processing manifest reports sentence-transformers/all-MiniLM-L6-v2 and KMeans during the offline build. No LLM structured extraction ran. Fifteen automated rule corrections were retained next to legacy labels; no independent human-label accuracy estimate exists.')
    st.markdown('### Source health')
    health=ev.groupby('source_platform').agg(records=('record_id','size'),relevant=('relevance',lambda x:x.isin(['DIRECT','RELATED']).sum()),E1_E2=('evidence_depth',lambda x:x.isin(['E1','E2']).sum())).reset_index()
    health['Relevant / source (%)']=(health.relevant/health.records*100).round(1)
    st.dataframe(health,hide_index=True,use_container_width=True)
    st.warning('The corpus was collected using retrieval-focused queries and is not representative. The Google Play record is UNCERTAIN/E4; PIXLS.US is cross-product context. No gold-standard human-labeled set was collected.')
    st.markdown('### Assignment questions — evidence mapped')
    st.caption('Each question receives its own narrowly selected source references. Unsupported questions remain explicit gaps rather than claiming support from all 23 relevant records.')
    groups=['All']+sorted({g for g,*_ in QUESTIONS});chosen=st.selectbox('Research-question group',groups)
    selected=[(i,g,q,a,refs) for i,(g,q,a,refs) in enumerate(QUESTIONS,1) if chosen=='All' or g==chosen]
    for i,g,q,a,refs in selected:
        valid=[rid for rid in refs if rid in set(relevant.record_id)]
        with st.expander(f'Q{i} · {"Evidence gap" if not valid else str(len(valid))+" linked records"} · {q}'):
            st.write(a)
            if valid:
                st.caption('Directional source records: '+', '.join(valid)+'. These are not a representative denominator.')
                evidence_list(valid)
            else:st.info('Requires primary research; no defensible record-level answer in this snapshot.')
    st.markdown('### Existing capabilities and limitations')
    st.markdown('- [Search people, things and places](https://support.google.com/photos/answer/15235862)\n- [Ask Photos](https://support.google.com/photos/answer/15318661)\n- [Face groups](https://support.google.com/photos/answer/6128838)')
    st.caption('Documentation establishes capability, not whether a specific user had access or could use it in their reported situation.')
    with st.expander('Snapshot metadata and reproducibility'):
        st.json(meta)
        st.caption('Automated integrity checks do not replace independent source verification or observed user studies.')
    export_df('Export source health',health,'source_health.csv')
    export_df('Export assignment coverage',pd.DataFrame([{'question_id':f'Q{i}','group':g,'question':q,'answer':a,'supporting_ids':'|'.join(refs)} for i,(g,q,a,refs) in enumerate(QUESTIONS,1)]),'research_question_coverage.csv')

st.divider()
st.caption('RECALL ATLAS · Independent product-management research · Fixed local evidence snapshot · Not affiliated with Google')
