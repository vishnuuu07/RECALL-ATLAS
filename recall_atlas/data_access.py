from __future__ import annotations
import json, sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / 'data/public/recall_atlas_public.sqlite'
MANIFEST = ROOT / 'data/manifests/public_snapshot_manifest.json'

@st.cache_resource
def connection():
    if not DB.exists(): raise FileNotFoundError(f'Public snapshot missing: {DB}')
    return sqlite3.connect(f'file:{DB}?mode=ro', uri=True, check_same_thread=False)

@st.cache_data
def table(name: str) -> pd.DataFrame:
    return pd.read_sql_query(f'SELECT * FROM {name}', connection())

@st.cache_data
def manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding='utf-8'))

def evidence(filters: dict | None = None, search: str = '', limit: int = 20, offset: int = 0) -> tuple[pd.DataFrame,int]:
    clauses, params = [], []
    filters = filters or {}
    for col, values in filters.items():
        if values:
            clauses.append(f"{col} IN ({','.join('?' for _ in values)})")
            params += list(values)
    if search.strip():
        clauses.append('(public_excerpt LIKE ? OR source_title LIKE ? OR themes LIKE ?)')
        params += [f'%{search.strip()}%'] * 3
    where = (' WHERE ' + ' AND '.join(clauses)) if clauses else ''
    con = connection()
    total = con.execute('SELECT count(*) FROM evidence' + where, params).fetchone()[0]
    frame = pd.read_sql_query('SELECT * FROM evidence' + where + ' ORDER BY publication_date DESC NULLS LAST, record_id LIMIT ? OFFSET ?', con, params=params+[limit,offset])
    return frame,total

