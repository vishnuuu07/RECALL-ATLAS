from __future__ import annotations
import hashlib,json,sqlite3
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def publish(evidence:pd.DataFrame, themes:pd.DataFrame, questions:pd.DataFrame, hypotheses:pd.DataFrame, funnel:pd.DataFrame, metadata:dict)->dict:
    target=ROOT/'data/public/recall_atlas_public.sqlite'; target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists(): target.unlink()
    con=sqlite3.connect(target)
    for name,df in {'evidence':evidence,'themes':themes,'questions':questions,'hypotheses':hypotheses,'funnel':funnel}.items(): df.to_sql(name,con,index=False)
    con.execute("CREATE VIRTUAL TABLE evidence_fts USING fts5(record_id, public_excerpt, source_title, themes)")
    con.execute("INSERT INTO evidence_fts SELECT record_id,public_excerpt,source_title,themes FROM evidence")
    con.commit(); con.close()
    digest=hashlib.sha256(target.read_bytes()).hexdigest(); metadata['snapshot_sha256']=digest; metadata['public_record_count']=len(evidence)
    path=ROOT/'data/manifests/public_snapshot_manifest.json'; path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(metadata,indent=2),encoding='utf-8')
    return metadata
