"""Validate the current 70-case local public dataset, not the historical archive."""
import json,sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/'data/public/recall_atlas_70_cases.sqlite'
m=json.loads((ROOT/'data/manifests/retrieval_cases_70_manifest.json').read_text(encoding='utf8'))
with sqlite3.connect(f'file:{DB.as_posix()}?mode=ro',uri=True) as c:
 n=c.execute('SELECT COUNT(*) FROM cases').fetchone()[0]
 ids=c.execute('SELECT COUNT(DISTINCT case_id) FROM cases').fetchone()[0]
 fts=c.execute('SELECT COUNT(*) FROM cases_fts').fetchone()[0]
 distinct=c.execute('SELECT COUNT(DISTINCT source_url) FROM cases').fetchone()[0]
 assert (n,ids,fts,distinct)==(70,70,70,60)
 assert n==m['case_rows'] and distinct==m['distinct_linked_discussions']
 assert c.execute('SELECT COUNT(*) FROM cases WHERE retrieval_goal IS NULL OR trim(retrieval_goal)=""').fetchone()[0]==0
 print(f'PASS current data: {n} rows, {distinct} source URLs, FTS index and required goals')
