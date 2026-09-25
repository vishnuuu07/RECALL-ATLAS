"""Refresh interpreted tables without modifying the original 24 evidence records.

Use this for editorial/chart fixes; a separate compliant collection operation is
needed for any new real records. Recomputes manifest hash after derived changes.
"""
from __future__ import annotations
import hashlib,json,sqlite3,sys
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from pipeline.aggregate import questions,themes,hypotheses
from recall_atlas.research_views import validate_editorial_ids
DB=ROOT/'data/public/recall_atlas_public.sqlite'
MANIFEST=ROOT/'data/manifests/public_snapshot_manifest.json'
with sqlite3.connect(DB) as c:
    ev=pd.read_sql_query('select * from evidence',c)
    missing=validate_editorial_ids(ev)
    if missing:raise SystemExit('Missing editorial record IDs: '+repr(missing))
    derived={'questions':questions(ev),'themes':themes(ev)}
    derived['hypotheses']=hypotheses(derived['themes'])
    for name,df in derived.items():
        df.to_sql(name,c,index=False,if_exists='replace')
    c.commit()
meta=json.loads(MANIFEST.read_text())
meta['dataset_version']='0.3.0'
meta['pipeline_version']='0.3.0-editorial'
meta['analytical_revision']='Research-question mappings and hypothesis descriptions repaired; 24 underlying evidence rows and classification labels unchanged.'
meta['snapshot_sha256']=hashlib.sha256(DB.read_bytes()).hexdigest()
MANIFEST.write_text(json.dumps(meta,indent=2),encoding='utf-8')
out=ROOT/'outputs'
derived['questions'].to_csv(out/'research_questions.csv',index=False)
derived['themes'].to_csv(out/'findings.csv',index=False)
derived['hypotheses'].to_csv(out/'hypothesis_matrix.csv',index=False)
print(f"Derived tables refreshed: {len(ev)} original records unchanged, {len(derived['questions'])} question mappings, {len(derived['themes'])} hypotheses")
