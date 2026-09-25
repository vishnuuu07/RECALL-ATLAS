"""Readable, source-neutral retrieval-case presentation."""
from __future__ import annotations
import pandas as pd
import streamlit as st

def clean(value, fallback='Not established'):
    if value is None or (isinstance(value,float) and pd.isna(value)): return fallback
    text=str(value).strip()
    return fallback if text.lower() in ('','nan','none','null','unknown') else text

def record_card(row:pd.Series,expanded=False):
    title=f"{clean(row.get('episode_descriptor'),'Retrieval case')} · {row['case_id']}"
    with st.expander(title,expanded=expanded):
        st.write(clean(row.get('original_account'),'No account summary available'))
        st.caption(f"{clean(row.get('evidence_classification'))} · {clean(row.get('evidence_type'))} · Case ID: {row['case_id']}")
        a,b=st.columns(2)
        with a:
            st.markdown('**Remembered clues**'); st.write(clean(row.get('remembered_clues')))
            st.markdown('**Missing information**'); st.write(clean(row.get('forgotten_clues')))
        with b:
            st.markdown('**Initial behaviour**'); st.write(clean(row.get('initial_search_behaviour')))
            st.markdown('**Failure stage**'); st.write(clean(row.get('failure_stage')))
        st.markdown('**Workaround**'); st.write(clean(row.get('workarounds')))
        st.markdown('**Recorded outcome**'); st.write(clean(row.get('recorded_outcome')))
        st.caption('This is a recorded retrieval account. Editorial reconstructions are not participant quotations or interviews.')
