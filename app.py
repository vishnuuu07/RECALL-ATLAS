"""Recall Atlas: a fixed, local retrieval-case research dashboard."""
from __future__ import annotations
import html
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from recall_atlas.styles import inject_css
from recall_atlas.data_access import table,manifest
from recall_atlas.charts import category_chart,themes_chart
from recall_atlas.evidence import record_card
from recall_atlas.research_views import FINDINGS,QUESTIONS,evidence_for,validate_editorial_ids

st.set_page_config(page_title='Recall Atlas | Retrieval Research',page_icon='◌',layout='wide',initial_sidebar_state='expanded')
inject_css()
NAV=['Overview','Explore evidence','Opportunities','Methodology']
with st.sidebar:
    st.markdown('### RECALL ATLAS')
    st.caption('Memory-led photo retrieval research')
    page=st.radio('Research navigation',NAV,label_visibility='collapsed')
    st.divider(); st.caption('Fixed local research snapshot')

@st.cache_data
def load(): return table('retrieval_cases'),table('imported_retrieval_cases'),table('case_overlap_audit'),manifest()
cases,imported,overlaps,meta=load()
missing_ids=validate_editorial_ids(cases)
if missing_ids:
    st.error('Editorial synthesis refers to missing case IDs: '+', '.join(missing_ids));st.stop()

def hero(kicker,title,body):
    st.markdown(f'<div class="hero"><div class="eyebrow">{html.escape(kicker)}</div><h1>{html.escape(title)}</h1><p>{html.escape(body)}</p></div>',unsafe_allow_html=True)
def metric_row(items):
    for col,(n,label) in zip(st.columns(len(items)),items): col.markdown(f'<div class="metric"><div class="n">{html.escape(str(n))}</div><div class="l">{html.escape(label)}</div></div>',unsafe_allow_html=True)
def show_chart(fig):
    st.pyplot(fig,clear_figure=True,use_container_width=True);plt.close(fig)
def export_df(label,frame,name):
    st.download_button(label,frame.to_csv(index=False).encode('utf-8-sig'),name,'text/csv',key='download_'+name)
def case_list(ids,max_show=None):
    frame=cases[cases.case_id.isin(ids)]
    if max_show:frame=frame.head(max_show)
    for i,(_,row) in enumerate(frame.iterrows()):record_card(row,expanded=i==0)

if page=='Overview':
    hero('Research evidence · fixed local dataset','Where does a remembered photo become hard to find?',
         '40 consolidated Retrieval Cases combine the existing corpus with 20 structured workbook cases. Four duplicate episodes were counted once; this is directional research, not a prevalence study.')
    known_outcomes=int((cases.outcome_classification.str.contains('Found',case=False,na=False)).sum())
    metric_row([(len(cases),'Consolidated Retrieval Cases'),(len(imported),'Imported structured cases'),(int((overlaps.counted_in_consolidated_cases=='No').sum()),'Duplicate episodes merged'),(known_outcomes,'Recorded found outcomes')])
    st.markdown('### Retrieval evidence at a glance')
    charts=[
        ('remembered_clues','Remembered clues'),('forgotten_clues','Missing information'),('initial_search_behaviour','Initial search behaviour'),
        ('failure_stage','Failure stages'),('workarounds','Workarounds'),('outcome_classification','Recorded retrieval outcomes'),
    ]
    for left,right in zip(charts[::2],charts[1::2]):
        a,b=st.columns(2,gap='large')
        with a:show_chart(category_chart(cases,left[0],left[1]))
        with b:show_chart(category_chart(cases,right[0],right[1]))
    st.caption('Each visualisation is calculated from the consolidated Retrieval Cases table. Categories are recorded case fields and may overlap in meaning.')
    st.markdown('### Findings to validate')
    stats=pd.DataFrame([{'Finding':f['title'],'Supporting cases':len(f['supporting_ids']),'Contradictory / qualifying cases':len(f['contradictory_ids'])} for f in FINDINGS])
    show_chart(themes_chart(stats.rename(columns={'Finding':'label','Supporting cases':'records'})))
    st.caption('Finding counts are evidence mappings, not prevalence estimates. Supporting and contradictory cases can overlap when a workaround qualifies the same issue.')
    export_df('Export consolidated case counts',pd.DataFrame([{'consolidated_retrieval_cases':len(cases),'imported_cases':len(imported),'duplicate_episodes_merged':int((overlaps.counted_in_consolidated_cases=='No').sum())}]),'overview_counts.csv')

elif page=='Explore evidence':
    hero('Structured Retrieval Cases','Inspect recorded retrieval accounts without source links.',
         'Case summaries preserve the retrieval goal, clues, actions, workarounds, outcomes, classifications, and interpretation. They are not participant interview transcripts.')
    a,b,c=st.columns(3)
    query=a.text_input('Search case summaries',placeholder='screenshot, timeline, text…')
    stages=b.multiselect('Failure stage',sorted(cases.failure_stage.dropna().unique()))
    outcomes=c.multiselect('Recorded outcome',sorted(cases.outcome_classification.dropna().unique()))
    mask=pd.Series(True,index=cases.index)
    if query.strip():
        searchable=['episode_descriptor','retrieval_goal','remembered_clues','forgotten_clues','initial_action','workarounds','recorded_outcome']
        mask &= pd.concat([cases[col].fillna('').str.contains(query.strip(),case=False,regex=False) for col in searchable],axis=1).any(axis=1)
    if stages:mask &= cases.failure_stage.isin(stages)
    if outcomes:mask &= cases.outcome_classification.isin(outcomes)
    filtered=cases[mask].sort_values('case_id')
    st.caption(f'{len(filtered)} matching Retrieval Cases. Filters apply before pagination.')
    pages=max(1,(len(filtered)+7)//8);selected=st.number_input('Page',1,pages,1,step=1) if pages>1 else 1
    for i,(_,row) in enumerate(filtered.iloc[(selected-1)*8:selected*8].iterrows()):record_card(row,expanded=i==0)
    export_columns=['case_id','episode_descriptor','retrieval_goal','remembered_clues','forgotten_clues','initial_search_behaviour','initial_action','workarounds','recorded_outcome','outcome_classification','evidence_classification','research_interpretation']
    export_df('Export filtered Retrieval Cases',filtered[export_columns],'retrieval_cases.csv')

elif page=='Opportunities':
    hero('Evidence → mechanism → intervention direction','Compare directions before selecting an MVP.',
         'Each finding separates what was recorded from a possible mechanism. The comparison is designed to choose validation tasks, not to make a feature decision.')
    comparison=pd.DataFrame([{'Finding':f['title'],'Supporting case IDs':', '.join(f['supporting_ids']),'Contradictory / qualifying IDs':', '.join(f['contradictory_ids']),'Product opportunity':f['opportunity'],'Validation question':f['question'],'Product-outcome metric':f['metric']} for f in FINDINGS])
    st.dataframe(comparison[['Finding','Supporting case IDs','Contradictory / qualifying IDs']],hide_index=True,use_container_width=True)
    name=st.selectbox('Investigate a finding',[f['title'] for f in FINDINGS]); finding=next(f for f in FINDINGS if f['title']==name)
    metric_row([(len(finding['supporting_ids']),'Supporting cases'),(len(finding['contradictory_ids']),'Contradictory / qualifying cases'),('Directional','Evidence status')])
    st.markdown('#### Observed behaviour');st.write(finding['observed'])
    st.markdown('#### Possible mechanism');st.write(finding['mechanism'])
    st.markdown('#### Supporting cases');st.write(', '.join(finding['supporting_ids']));case_list(finding['supporting_ids'])
    st.markdown('#### Contradictory or qualifying cases');st.write(', '.join(finding['contradictory_ids']))
    st.markdown('#### Product opportunity');st.write(finding['opportunity'])
    st.markdown('#### Validation question');st.write(finding['question'])
    st.markdown('#### Product-outcome metric');st.write(finding['metric'])
    export_df('Export opportunity comparison',comparison,'opportunity_comparison.csv')

else:
    hero('Methodology and research boundary','A reproducible, source-neutral evidence snapshot.',
         'The dashboard represents secondary Retrieval Cases. It does not claim participant interviews or independently observed task outcomes.')
    st.markdown('### Dataset construction')
    st.write(f'The reproducible pipeline imports all {len(imported)} workbook cases, reviews five same-discussion overlaps, and merges four duplicate episodes. The resulting table contains {len(cases)} Retrieval Cases.')
    st.dataframe(overlaps,hide_index=True,use_container_width=True)
    st.markdown('### Evidence boundary')
    st.write('Editorial Q&A reconstructions are analyst-derived planning material. They are not verbatim statements, independent participants, or additional retrieval episodes. The supplied interview and MVP-session templates are blank and are not counted as completed research.')
    st.markdown('### Existing capabilities to benchmark')
    st.write('Benchmark current search by people, things, places, text in images, date or timeline browsing, albums, result ordering, and available conversational search modes. Capability availability and behavior must be checked in the participant’s actual product context.')
    st.markdown('### What requires validation')
    for _,question,answer,refs in QUESTIONS:
        with st.expander(question):
            st.write(answer);st.caption('Relevant case IDs: '+', '.join(refs))
    st.markdown('### Product-outcome metrics')
    st.write('Use verified target retrieval rate, time to target, first-candidate relevance, reformulations per success, route-switch rate, near-miss abandonment, false-positive selection, and perceived effort. Segment results by memory clue and asset availability state.')
    with st.expander('Snapshot metadata'):st.json(meta)
    export_df('Export overlap review',overlaps,'case_overlap_review.csv')

st.divider();st.caption('RECALL ATLAS · Fixed local Retrieval Cases snapshot · Directional research only')
