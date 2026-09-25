"""Readable, source-backed evidence presentation with safe missing-value handling."""
from __future__ import annotations
import pandas as pd
import streamlit as st
from recall_atlas.research_views import OUTCOME_NOTES


def clean(value, fallback='Not established by source'):
    if value is None or (isinstance(value,float) and pd.isna(value)):
        return fallback
    text=str(value).strip()
    return fallback if text.lower() in ('','nan','none','null','unknown') else text


def record_card(row:pd.Series,expanded=False):
    title=f"{clean(row.get('source_title'),'Retrieval discussion')} · {row['source_platform']} · {row['record_id']}"
    with st.expander(title,expanded=expanded):
        st.write(clean(row.get('public_excerpt'),'No public excerpt available'))
        st.caption(f"{clean(row.get('relevance'))} / {clean(row.get('evidence_depth'))} · Published: {clean(row.get('publication_date'),'Date not recorded')} · ID: {row['record_id']}")
        a,b=st.columns(2)
        with a:
            st.markdown('**Memory clue (coded)**')
            st.write(clean(row.get('memory_type')))
            st.markdown('**Retrieval stage (coded)**')
            st.write(clean(row.get('failure_stage')))
        with b:
            st.markdown('**Workaround (coded)**')
            st.write(clean(row.get('workaround')))
            st.markdown('**Outcome (coded)**')
            st.write(clean(row.get('outcome')))
        note=OUTCOME_NOTES.get(str(row['record_id']))
        if note:st.info('Source-reported outcome: '+note)
        st.caption('Codes are automated and may be incomplete. The excerpt, not the coding, is the source evidence.')
        correction=clean(row.get('classification_correction'),'No change')
        if correction!='No change':st.caption(f'Automated classification correction: {correction}; not independently human-audited.')
        if clean(row.get('source_url'),''):
            st.link_button('Open original source ↗',str(row['source_url']))
