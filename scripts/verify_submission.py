"""Submission gates for CURRENT public 70-case v0.5 snapshot.

The historical 24/40-case database remains archival and is not the dashboard's source.
"""
from __future__ import annotations
import hashlib
import json
import re
import sqlite3
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from recall_atlas.assignment_answers import QUESTIONS, validate_mappings
DB=ROOT/'data/public/recall_atlas_70_cases.sqlite'
MANIFEST=ROOT/'data/manifests/retrieval_cases_70_manifest.json'
HANDOFF=ROOT/'RESEARCH_TO_SOLUTION_HANDOFF.md'
PROHIBITED={'author','author_name','email','username','credential','token','password'}
SENSITIVE=re.compile(r'(?i)(api[_-]?key\s*[:=]|bearer\s+[A-Za-z0-9._-]+|password\s*[:=]|ghp_[A-Za-z0-9]+|xox[baprs]-[A-Za-z0-9]+|AKIA[0-9A-Z]{16})')

def main():
    m=json.loads(MANIFEST.read_text(encoding='utf8'))
    assert hashlib.sha256(DB.read_bytes()).hexdigest()==m['snapshot_sha256'],'Current snapshot checksum mismatch'
    with sqlite3.connect(f'file:{DB.as_posix()}?mode=ro',uri=True) as con:
        n,urls=con.execute('SELECT COUNT(*),COUNT(DISTINCT source_url) FROM cases').fetchone()
        assert (n,urls)==(70,60)==(m['case_rows'],m['distinct_linked_discussions'])
        cols=[c[1] for c in con.execute('PRAGMA table_info(cases)')]
        assert not PROHIBITED.intersection(cols),'Prohibited public columns'
        assert con.execute('SELECT COUNT(*) FROM cases WHERE source_url NOT LIKE "https://%"').fetchone()[0]==0
        ids={r[0] for r in con.execute('SELECT case_id FROM cases')}
        validate_mappings(ids)
        for r in con.execute('SELECT * FROM cases'):
            for val in r:
                assert not (isinstance(val,str) and SENSITIVE.search(val)),'Potential credential-pattern content'
    text=HANDOFF.read_text(encoding='utf8')
    referenced=set(re.findall(r'\bS\d{2}\b',text))
    assert len(referenced & ids)>=15,'Handoff must include actual current snapshot evidence IDs'
    assert '40 consolidated Retrieval Cases' not in text,'Stale handoff'
    assert len(QUESTIONS)==8
    print(f'PASS current submission: {n} cases / {urls} URLs, 8 question mappings, {len(referenced&ids)} handoff IDs, source and secret checks, checksum OK')

if __name__=='__main__':main()
