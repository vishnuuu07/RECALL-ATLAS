"""Run as python scripts/verify_retrieval_70.py before publishing v0.4."""
from __future__ import annotations
import hashlib,json,sqlite3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/'data/public/recall_atlas_70_cases.sqlite'
M=ROOT/'data/manifests/retrieval_cases_70_manifest.json'
S=ROOT/'outputs/retrieval_case_synthesis.json'

def main():
  m=json.loads(M.read_text(encoding='utf8'))
  assert hashlib.sha256(DB.read_bytes()).hexdigest()==m['snapshot_sha256'],'Snapshot digest mismatch'
  with sqlite3.connect(DB) as con:
    count,urls=con.execute('SELECT COUNT(*), COUNT(DISTINCT source_url) FROM cases').fetchone()
    assert (count,urls)==(70,60),(count,urls)
    assert con.execute('SELECT COUNT(*) FROM cases WHERE source_url NOT LIKE "https://%"').fetchone()[0]==0
    assert con.execute('SELECT COUNT(DISTINCT case_id) FROM cases').fetchone()[0]==70
    assert con.execute('SELECT COUNT(*) FROM cases_fts').fetchone()[0]==70
    ids={r[0] for r in con.execute('SELECT case_id FROM cases')}
    for (tags,) in con.execute('SELECT theme_labels FROM cases'):assert isinstance(json.loads(tags),list)
    for f in json.loads(S.read_text(encoding='utf8'))['findings']:
      assert set(f['examples']) <= ids,(f['id'],'missing evidence')
    assert dict(con.execute('SELECT source_platform,COUNT(*) FROM cases GROUP BY source_platform'))==m['source_distribution']
  print(f'PASS: {count} case rows, {urls} distinct supplied discussion URLs, source/finding mappings valid, snapshot checksum valid')

if __name__=='__main__':main()
