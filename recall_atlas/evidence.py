from __future__ import annotations
import streamlit as st
import pandas as pd

def record_card(row: pd.Series) -> None:
    title=f"{row['record_id']} · {row['source_platform']} · {row['relevance']} / {row['evidence_depth']}"
    with st.expander(title):
        st.write(row['public_excerpt'])
        if row.get('classification_correction') != 'No change':
            st.caption(f"Automated rule correction: {row['classification_correction']} (not an independent human audit; original prediction retained in export)")
        st.caption(f"Published: {row['publication_date'] or 'unknown'} · confidence: {row['confidence']:.2f}")
        for item in str(row['themes']).split('|'):
            if item: st.markdown(f"<span class='tag'>{item}</span>",unsafe_allow_html=True)
        st.markdown(f"**Observed:** {row['observed'] or 'Unknown'}")
        st.markdown(f"**Inferred:** {row['inferred'] or 'Unknown'}")
        st.markdown(f"**Unknown:** {row['unknowns'] or 'Not established'}")
        st.markdown(f"[Open original public source]({row['source_url']})")
