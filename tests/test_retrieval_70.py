"""Pure-Python v0.4 regression checks; no Streamlit runtime needed."""
import json,sqlite3
from pathlib import Path
ROOT=Path(__file__).parents[1]
DB=ROOT/'data/public/recall_atlas_70_cases.sqlite'
M=ROOT/'data/manifests/retrieval_cases_70_manifest.json'

def test_case_and_source_units():
  with sqlite3.connect(DB) as con:
    assert con.execute('SELECT COUNT(*) FROM cases').fetchone()[0]==70
    assert con.execute('SELECT COUNT(DISTINCT source_url) FROM cases').fetchone()[0]==60
    assert con.execute('SELECT COUNT(*) FROM cases_fts').fetchone()[0]==70

def test_provenance_and_no_fake_interviews():
  with sqlite3.connect(DB) as con:
    names=[x[1] for x in con.execute('PRAGMA table_info(cases)')]
    assert 'interview_transcript' not in names
    for (u,) in con.execute('SELECT source_url FROM cases'):
      assert u.startswith('https://')

def test_coding_and_manifest_consistent():
  m=json.loads(M.read_text())
  with sqlite3.connect(DB) as con:
    assert sum(v for _,v in con.execute('SELECT source_platform,COUNT(*) FROM cases GROUP BY source_platform'))==m['case_rows']
    counts=dict(con.execute('SELECT outcome_group,COUNT(*) FROM cases GROUP BY outcome_group'))
    assert counts==m['outcome_groups']
    assert con.execute('SELECT COUNT(*) FROM cases WHERE theme_labels IS NULL').fetchone()[0]==0
