from __future__ import annotations
import json
import pandas as pd
import streamlit as st
from recall_atlas.styles import inject_css
from recall_atlas.data_access import table, manifest, evidence
from recall_atlas.metrics import pct
from recall_atlas.charts import bar, journey, heatmap
from recall_atlas.evidence import record_card
from recall_atlas.opportunities import score
from recall_atlas.question_coverage import with_status

st.set_page_config(page_title='Recall Atlas', page_icon='◌', layout='wide', initial_sidebar_state='expanded')
inject_css()
PAGES=['Research overview','Research questions','Memory & retrieval journey','Failure mechanisms','Opportunity lab','Evidence explorer','Research bridge','Methodology & audit']
with st.sidebar:
    st.markdown('## RECALL ATLAS')
    st.caption('Vague-memory photo retrieval research')
    page=st.radio('Navigate',PAGES,label_visibility='collapsed')
    st.divider(); st.caption('Independent product-management research. Not affiliated with Google.')

ev=table('evidence'); th=table('themes'); qs=table('questions'); hy=table('hypotheses'); fn=table('funnel'); meta=manifest()
relevant=ev[ev.relevance.isin(['DIRECT','RELATED'])]
def hero(kicker,title,body):
    st.markdown(f"<section class='hero'><div class='eyebrow'>{kicker}</div><h1>{title}</h1><p>{body}</p></section>",unsafe_allow_html=True)
def metric_row(items):
    cols=st.columns(len(items))
    for c,(value,label) in zip(cols,items): c.markdown(f"<div class='metric'><div class='n'>{value}</div><div class='l'>{label}</div></div>",unsafe_allow_html=True)
def download(label,frame,name): st.download_button(label,frame.to_csv(index=False).encode(),name,'text/csv')

if page=='Research overview':
    hero('AI-powered discovery of vague-memory retrieval','From fragmented feedback to research-worthy mechanisms.','Business objective: increase the percentage of users who successfully retrieve a photo they remember but cannot precisely describe when they begin searching.')
    metric_row([(meta['raw_record_count'],'raw collected records'),(len(relevant),'relevant retrieval signals'),(int(ev.evidence_depth.isin(['E1','E2']).sum()),'evidence-rich episodes'),(ev.source_platform.nunique(),'source platforms')])
    left,right=st.columns([1,1.2]); left.plotly_chart(bar(fn,'stage','count','Research funnel'),use_container_width=True); right.plotly_chart(journey(relevant),use_container_width=True)
    st.subheader('What the corpus directionally suggests')
    for _,r in th.sort_values('evidence_count',ascending=False).head(4).iterrows():
        st.markdown(f"<div class='card'><b>{r.theme.title()}</b> · {r.evidence_count} relevant records across {r.source_count} source(s). <br><small>{r.contradictions}</small></div>",unsafe_allow_html=True)
    st.markdown("<div class='warning'><b>Interpretation boundary.</b> These are public-feedback signals, not Google Photos telemetry or representative user percentages. Rich full retrieval episodes are limited; outcomes and verification require primary research.</div>",unsafe_allow_html=True)
    download('Export research funnel',fn,'recall-atlas-funnel.csv')

elif page=='Research questions':
    hero('Assignment coverage','22 questions, evidence mapped — gaps kept visible.','Every answer names its denominator and preserves uncertainty rather than converting generic feedback into behavioural facts.')
    covered=with_status(qs); metric_row([(len(covered[covered.coverage!='No evidence']),'questions with signal'),(len(covered[covered.coverage=='No evidence']),'primary-research gaps'),(len(relevant),'relevant-record denominator')])
    st.plotly_chart(heatmap(covered),use_container_width=True)
    group=st.selectbox('Question group',['All']+sorted(covered.group.unique().tolist()))
    view=covered if group=='All' else covered[covered.group==group]
    for _,r in view.iterrows():
        with st.expander(f"{r.question_id} · {r.coverage} · {r.question}"):
            st.write(r.answer); st.caption(f"Evidence: {r.evidence_count}/{r.denominator} relevant records · confidence: {r.confidence}")
            st.write('Interview follow-up:',r.interview_follow_up)
            if r.evidence_ids: st.code(r.evidence_ids,language=None)
    download('Export research-question coverage',covered,'recall-atlas-question-coverage.csv')

elif page=='Memory & retrieval journey':
    hero('Memory → action → breakdown → next move','Only transitions observed in the fixed evidence snapshot.','Use the filters to see the records beneath the path; a blank or unknown field means the source did not establish it.')
    c1,c2,c3,c4=st.columns(4)
    source=c1.multiselect('Source',sorted(ev.source_platform.unique())); memory=c2.multiselect('Memory type',sorted(ev.memory_type.unique())); stage=c3.multiselect('Failure stage',sorted(ev.failure_stage.unique())); outcome=c4.multiselect('Outcome',sorted(ev.outcome.unique()))
    filters={'source_platform':source,'memory_type':memory,'failure_stage':stage,'outcome':outcome}; frame,_=evidence(filters,limit=500)
    frame=frame[frame.relevance.isin(['DIRECT','RELATED'])]
    st.plotly_chart(journey(frame),use_container_width=True)
    st.subheader(f'Supporting records ({len(frame)})')
    for _,r in frame.head(12).iterrows(): record_card(r)

elif page=='Failure mechanisms':
    hero('Mechanisms, not merely complaints','What the records show; what they cannot prove.','A failed query is a symptom. A mechanism is a cautious explanation linking remembered clues, interaction, results and next action.')
    chosen=st.selectbox('Mechanism',th.theme.tolist()); r=th[th.theme==chosen].iloc[0]
    a,b,c=st.columns(3); a.metric('Supporting records',r.evidence_count);b.metric('Evidence-rich',r.rich_count);c.metric('Source diversity',r.source_count)
    st.markdown(f"<div class='card'><b>Definition</b><br>{r.definition}<br><br><b>Source distribution</b><br>{r.source_distribution}<br><br><b>Contradictions</b><br>{r.contradictions}<br><br><b>Gap</b><br>{r.research_gap}</div>",unsafe_allow_html=True)
    st.subheader('Representative evidence')
    ids=r.record_ids.split('|'); [record_card(ev[ev.record_id==i].iloc[0]) for i in ids[:5]]
    download('Export theme analysis',th,'recall-atlas-themes.csv')

elif page=='Opportunity lab':
    hero('Opportunity lab','A transparent research-prioritisation heuristic — not an impact forecast.','Stress-test mechanisms by excluding sources, retaining only richer episodes, or changing the evidence and corroboration weights.')
    x,y,z=st.columns(3); exclude=x.selectbox('Exclude a source',['None']+sorted(ev.source_platform.unique().tolist())); rich_only=y.toggle('Evidence-rich only',False); richness=z.slider('Evidence richness weight',0.0,3.0,1.5,.1)
    subset=relevant.copy();
    if exclude!='None': subset=subset[subset.source_platform!=exclude]
    if rich_only: subset=subset[subset.evidence_depth.isin(['E1','E2'])]
    rebuilt=[]
    for theme in th.theme:
        f=subset[subset.themes.str.contains(theme,regex=False)]; rebuilt.append({'theme':theme,'evidence_count':len(f),'rich_count':int(f.evidence_depth.isin(['E1','E2']).sum()),'source_count':f.source_platform.nunique()})
    ranked=score(pd.DataFrame(rebuilt),richness,1.0); st.caption('Score = records + (evidence-rich records × weight) + source count. It ranks interview attention only.')
    st.dataframe(ranked,use_container_width=True,hide_index=True)
    st.plotly_chart(bar(ranked,'theme','priority_score','Sensitivity-adjusted research priority'),use_container_width=True)
    st.subheader('Opportunity stress test')
    for _,r in ranked.head(4).iterrows():
        st.markdown(f"<div class='card'><b>{r.theme.title()}</b><br>Independent-source support: {'yes' if r.source_count>1 else 'not yet'} · Generic-only complaint? review evidence manually · Existing capability: assess against documented Search, collections and Ask Photos · Disproof: observe successful, reproducible retrieval with the same clue set.</div>",unsafe_allow_html=True)
    download('Export opportunity comparison',ranked,'recall-atlas-opportunities.csv')

elif page=='Evidence explorer':
    hero('Evidence explorer','Inspect the source before accepting the synthesis.','The dashboard queries a local, read-only SQLite snapshot with a full-text index; it never fetches source websites on page load.')
    c1,c2,c3=st.columns(3); query=c1.text_input('Full-text search'); source=c2.multiselect('Source',sorted(ev.source_platform.unique())); relevance=c3.multiselect('Relevance',sorted(ev.relevance.unique()))
    c4,c5,c6=st.columns(3); memory=c4.multiselect('Memory type',sorted(ev.memory_type.unique())); theme=c5.multiselect('Mechanism',sorted(th.theme.unique())); outcome=c6.multiselect('Outcome',sorted(ev.outcome.unique()))
    filters={'source_platform':source,'relevance':relevance,'memory_type':memory,'outcome':outcome}; frame,total=evidence(filters,query,limit=20)
    if theme: frame=frame[frame.themes.apply(lambda s:any(t in s for t in theme))]
    st.caption(f'{total} matching local records before client-side mechanism filter. Page size: 20.')
    for _,r in frame.iterrows(): record_card(r)
    download('Export anonymised evidence',frame,'recall-atlas-evidence.csv')

elif page=='Research bridge':
    hero('Secondary evidence → primary research','A decision bridge designed to be challenged.','No interviews are represented as completed. Each hypothesis remains a direction to test with an observed retrieval episode.')
    for _,r in hy.iterrows():
        with st.expander(f"{r.hypothesis_id} · {r.status} · {r.theme}"):
            st.write(r.statement); st.markdown(f"**Public evidence:** `{r.supporting_ids}`");st.write('**Contrary evidence:**',r.contradictory_evidence);st.write('**Interview test:**',r.interview_question);st.write('**Potential metric:**',r.potential_outcome)
            st.info('Interview finding: pending — do not infer confirmation from this secondary corpus.')
    st.subheader('Negative evidence ledger')
    st.write('No substantial public evidence in this snapshot establishes candidate recognition, verified success, or which workaround actually succeeds. Absence here is not proof of absence in the product.')
    download('Export hypothesis matrix',hy,'recall-atlas-hypotheses.csv')

else:
    hero('Methodology & audit','Reproducible, local, and explicit about limitations.','Dataset version '+meta['dataset_version']+' · snapshot SHA-256 '+meta['snapshot_sha256'][:16]+'…')
    st.subheader('Processing record'); st.json({k:meta[k] for k in ['raw_record_count','duplicates_removed','unique_record_count','source_counts','classification_correction_count','ai_model_version','ai_processing','audit_status']})
    st.caption('E1 = complete, outcome-stated retrieval episode; E2 = substantive but outcome-incomplete episode; E3 = relevant contextual signal; E4 = uncertain or out of scope. Corrections are deterministic rules, not an independent human audit.')
    st.subheader('Source-health monitor'); source_health=ev.groupby('source_platform').agg(records=('record_id','count'),relevant=('relevance',lambda x:int(x.isin(['DIRECT','RELATED']).sum())),rich=('evidence_depth',lambda x:int(x.isin(['E1','E2']).sum())),median_excerpt_chars=('public_excerpt',lambda x:int(x.str.len().median()))).reset_index(); source_health['relevant_signal_density_%']=source_health.apply(lambda r:pct(r.relevant,r.records),axis=1);st.dataframe(source_health,use_container_width=True,hide_index=True)
    largest=source_health.records.max()/len(ev)
    if largest>.5: st.markdown(f"<div class='warning'><b>Concentration warning.</b> The largest source accounts for {largest:.0%} of publishable records. App reviews supply scale but are not used alone to infer detailed retrieval journeys.</div>",unsafe_allow_html=True)
    st.subheader('Capability audit')
    st.markdown('- [Search people, things and places](https://support.google.com/photos/answer/15235862): classic search, people/pets, albums, documents, places and text matching; availability varies by region/account.\n- [Ask Photos](https://support.google.com/photos/answer/15318661): conversational option; opt-in and availability caveats apply.\n- [Face groups](https://support.google.com/photos/answer/6128838): named people/pets can become searchable.\n\nDocumentation establishes capability, not whether it resolved a particular public feedback case.')
    st.subheader('Limits')
    st.write('Public feedback is self-selected; records can conflate backup, indexing and retrieval; personal libraries and actual success outcomes are not observable. Model accuracy is unmeasured because no independent gold labels were collected. Review source links and run primary interviews before selecting an MVP.')
    download('Export source health',source_health,'recall-atlas-source-health.csv')

st.divider();st.caption('RECALL ATLAS · Independent product-management research · Fixed local snapshot · Not affiliated with Google')
