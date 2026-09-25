from __future__ import annotations
import hashlib,json,sqlite3
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def publish(evidence:pd.DataFrame, themes:pd.DataFrame, questions:pd.DataFrame, hypotheses:pd.DataFrame, funnel:pd.DataFrame, metadata:dict, extra_tables:dict[str,pd.DataFrame]|None=None)->dict:
    target=ROOT/'data/public/recall_atlas_public.sqlite'; target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists(): target.unlink()
    con=sqlite3.connect(target)
    # The deployable snapshot is deliberately source-neutral. URLs and platform
    # identifiers remain only in the checked-in raw research inputs, not in data
    # a dashboard visitor can inspect or export.
    public_evidence=evidence.copy()
    if 'case_id' in public_evidence:
        public_evidence['record_id']=public_evidence['case_id']
        public_evidence['public_excerpt']=public_evidence['original_account']
        public_evidence['source_title']=public_evidence['episode_descriptor']
        public_evidence['themes']=''
    else:
        public_evidence['record_id']=[f'C{i:02d}' for i in range(1,len(public_evidence)+1)]
        public_evidence['source_title']=public_evidence['record_id'].map(lambda x:f'Retrieval case {x}')
    public_evidence['source_platform']='Retrieval Cases'
    public_evidence['source_type']='Recorded account'
    public_evidence=public_evidence.drop(columns=['source_url'],errors='ignore')
    tables={'evidence':public_evidence,'themes':themes,'questions':questions,'hypotheses':hypotheses,'funnel':funnel}
    tables.update(extra_tables or {})
    for name,df in tables.items(): df.to_sql(name,con,index=False)
    con.execute("CREATE VIRTUAL TABLE evidence_fts USING fts5(record_id, public_excerpt, source_title, themes)")
    con.execute("INSERT INTO evidence_fts SELECT record_id,public_excerpt,source_title,themes FROM evidence")
    con.commit(); con.close()
    digest=hashlib.sha256(target.read_bytes()).hexdigest(); metadata['snapshot_sha256']=digest; metadata['public_record_count']=len(public_evidence)
    path=ROOT/'data/manifests/public_snapshot_manifest.json'; path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(metadata,indent=2),encoding='utf-8')
    return metadata
