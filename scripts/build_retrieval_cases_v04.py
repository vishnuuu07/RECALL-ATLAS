"""Build a read-only 70-case research snapshot from structured, source-linked workbook rows.

Input JSONs are produced from the supplied XLSX using artifact_tool and committed as
normalized workbook exports. The 8 Q&A reconstructions are *not* interview data, are
not imported, and are never treated as independent cases.

Counting unit: case row (S01-S70); separate unique thread URL count. No claim that
all cases represent independent users or distinct discussions.
"""
from __future__ import annotations
import collections
import hashlib
import json
import re
import sqlite3
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'imports'/'recall_70_workbook_rows.json'
SRC=ROOT/'data'/'imports'/'source_metadata_first20.json'
OUT=ROOT/'data'/'public'/'recall_atlas_70_cases.sqlite'
MANIFEST=ROOT/'data'/'manifests'/'retrieval_cases_70_manifest.json'

# Research codes below are transparent analyst mappings of the *recorded accounts*.
# They are multi-label case groupings, not externally validated model predictions.
THEMES={
 'Collection / scope': 'S08 S23 S25 S27 S32 S38 S39 S47 S49 S50 S51 S52 S53 S70',
 'Literal text / file cue': 'S04 S11 S16 S22 S30 S31 S35 S43 S44 S55 S67 S68',
 'Candidate → surrounding context': 'S08 S09 S23 S32 S40 S51',
 'Sparse / irrelevant results': 'S02 S04 S10 S12 S14 S15 S20 S21 S24 S25 S28 S30 S33 S34 S36 S38 S43 S44 S46 S54 S55 S57 S64 S65 S66 S67 S68 S69',
 'Asset availability / indexing diagnosis': 'S07 S18 S19 S22 S26 S29 S40 S42 S56 S58 S59 S60 S61',
 'Related-image clue': 'S01 S13 S23',
 'Reported successful route or workaround': 'S02 S03 S04 S05 S06 S20 S23 S25 S26 S29 S31 S35 S37 S45 S48 S50 S51 S58 S62 S64 S68',
}
THEMES={k:set(v.split()) for k,v in THEMES.items()}
ASSET_DIAG=set('S07 S18 S19 S22 S26 S29 S42 S56 S58 S59 S60 S61'.split())
CORE=set('S01 S02 S03 S04 S06 S08 S09 S10 S11 S13 S14 S21 S23 S27 S31 S32 S34 S40 S43 S44 S47 S52 S54 S55 S57 S64 S65 S66 S69'.split())
FOUND=set('S02 S03 S04 S05 S06 S20 S23 S26 S29 S31 S35 S37 S45 S64 S68'.split())
PARTIAL=set('S07 S08 S16 S17 S22 S25 S48 S50 S51 S56 S58 S61 S62'.split())

FINDINGS=[
 dict(id='F1',title='Knowing the collection is not the same as searching within it',tag='Collection / scope',
      observed='Some account holders knew the event, album or cohort but described global results or an album that did not jump to the intended photo.',
      examples=['S08','S32','S47'], qualification='S23 reports an existing way to navigate from a known image to its day. Do not imply that no contextual navigation feature exists.',
      question='Ask someone to find an item in a known album or trip. Compare their first query, search scope, result inspection and next action.',
      metric='Verified retrieval within the intended collection; steps and time to target.'),
 dict(id='F2',title='Exact words or filenames are not always treated as exact clues',tag='Literal text / file cue',
      observed='Cases describe queries for screenshot text or a filename that returned conceptually related or date-related results rather than the expected literal match.',
      examples=['S04','S30','S43'],qualification='S04 and S35 describe successful quoted-term workarounds; test whether the capability is available and understood before inventing it.',
      question='Give an existing screenshot containing a known literal phrase. Observe search wording, returned matches and whether the user discovers exact-text behavior.',
      metric='Correct screenshot retrieval and number of reformulations.'),
 dict(id='F3',title='A near match can still leave the intended memory out of reach',tag='Candidate → surrounding context',
      observed='Accounts describe locating a reference image or partial event set but needing another action to reach surrounding images.',
      examples=['S08','S23','S32'],qualification='S23 reports a path that resolved navigation, so this may be a discoverability/flow problem rather than a missing capability.',
      question='After a user finds a photo from the right day, observe how they navigate to a different image from the same event.',
      metric='Time from first relevant candidate to verified target; abandoned near misses.'),
 dict(id='F4',title='Missing results need availability diagnosis before product blame',tag='Asset availability / indexing diagnosis',
      observed='Some reports describe entire periods or videos absent; the record alone cannot separate forgotten context from backup/account/indexing state.',
      examples=['S18','S19','S60'],qualification='S26 found a known set through date search; S58 reported nothing was ultimately lost. These are not confirmed vague-memory failures.',
      question='First establish that the intended asset exists in the selected account and collection, then reproduce any retrieval mismatch.',
      metric='Share of attempted tasks with independently confirmed asset presence before retrieval diagnosis.'),
]


def plat(url):
  h=urlparse(url).netloc.lower()
  if 'reddit.com' in h:return 'Reddit'
  if 'support.google.com' in h:return 'Google Photos Community'
  return 'Other linked platform'

def safe(x):
  return str(x).strip() if x is not None else ''

def read():
  raw=json.loads(DATA.read_text(encoding='utf-8'))
  previous={x['Case ID']:x for x in json.loads(SRC.read_text(encoding='utf-8'))}
  seen=set(); entries=[]
  for r in raw:
    cid=safe(r['case_id'])
    assert re.fullmatch(r'S\d{2}',cid) and cid not in seen,(cid,'duplicate ID')
    seen.add(cid)
    note=safe(r.get('Q8_reconstructed_response'))
    p=previous.get(cid)
    if p:
      url=safe(p.get('Public source URL'))
      excerpt=safe(p.get('Short source excerpt'))
      source_date=safe(p.get('Public post date'))
      relevance=safe(p.get('Research relevance'))
      if not excerpt: excerpt=safe(p.get('Source-account summary'))
      outcome=safe(r.get('outcome'))
    else:
      match=re.search(r'https?://[^\s\]\)]+',note)
      assert match, f'No supplied URL for {cid}'
      url=match.group(0).rstrip('.,;')
      excerpt=''
      source_date=''
      relevance='Not independently assessed'
      outcome=note.split('[PUBLIC')[0].strip()
    assert url.startswith('https://'),cid
    tags=[k for k,v in THEMES.items() if cid in v]
    scope='Asset-availability diagnostic' if cid in ASSET_DIAG else ('Memory-led account' if cid in CORE else 'Adjacent search/navigation')
    out='Reported target/route found' if cid in FOUND else ('Partial or workaround only' if cid in PARTIAL else 'Unresolved / not confirmed')
    entries.append(dict(case_id=cid,title=safe(r.get('case_title')) or safe(r.get('retrieval_goal'))[:90],
        source_url=url,source_platform=plat(url),source_date=source_date,
        source_excerpt=excerpt,case_focus=scope,source_relevance=relevance,
        retrieval_goal=safe(r.get('retrieval_goal')),remembered_clues=safe(r.get('remembered_clues')),
        forgotten_clues=safe(r.get('forgotten_clues')),initial_action=safe(r.get('initial_action')),
        reported_results=safe(r.get('reported_results')),refinement=safe(r.get('refinement')),
        workaround=safe(r.get('workaround')),outcome=outcome,outcome_group=out,
        theme_labels=json.dumps(tags,ensure_ascii=False),editorial_classification='Manually mapped source-case category; not independently observed',
        source_status='Linked URL supplied in workbook; live availability not independently reverified'))
  assert len(entries)==70 and len(seen)==70
  return entries

def build():
  rows=read(); OUT.parent.mkdir(parents=True,exist_ok=True);MANIFEST.parent.mkdir(parents=True,exist_ok=True)
  if OUT.exists():OUT.unlink()
  con=sqlite3.connect(OUT)
  con.execute('''CREATE TABLE cases (
  case_id TEXT PRIMARY KEY,title TEXT,source_url TEXT,source_platform TEXT,source_date TEXT,source_excerpt TEXT,
  case_focus TEXT,source_relevance TEXT,retrieval_goal TEXT,remembered_clues TEXT,forgotten_clues TEXT,
  initial_action TEXT,reported_results TEXT,refinement TEXT,workaround TEXT,outcome TEXT,outcome_group TEXT,
  theme_labels TEXT,editorial_classification TEXT,source_status TEXT)''')
  cols=list(rows[0]);con.executemany(f"INSERT INTO cases ({','.join(cols)}) VALUES ({','.join('?' for _ in cols)})",[[x[k] for k in cols] for x in rows]);
  con.execute('CREATE INDEX case_source_idx ON cases(source_platform)')
  con.execute('CREATE INDEX case_focus_idx ON cases(case_focus)')
  con.execute('CREATE VIRTUAL TABLE cases_fts USING fts5(case_id UNINDEXED,title,retrieval_goal,remembered_clues,forgotten_clues,initial_action,reported_results,refinement,workaround,content="cases",content_rowid="rowid")')
  con.execute('INSERT INTO cases_fts(cases_fts) VALUES("rebuild")')
  con.commit();con.close()
  digest=hashlib.sha256(OUT.read_bytes()).hexdigest()
  manifest={'dataset_version':'0.4','case_rows':len(rows),'distinct_linked_discussions':len({r['source_url'] for r in rows}),
     'source_distribution':dict(collections.Counter(r['source_platform'] for r in rows)),
     'case_focus_distribution':dict(collections.Counter(r['case_focus'] for r in rows)),
     'outcome_groups':dict(collections.Counter(r['outcome_group'] for r in rows)),
     'theme_counts':{t:sum(t in json.loads(r['theme_labels']) for r in rows) for t in THEMES},
     'source_urls':'Supplied by workbook; live accessibility has not been independently verified',
     'case_unit':'A source-case row, not necessarily an independent person or discussion',
     'analysis_boundary':'Editorial reconstructions are not transcript quotes or directly observed interviews',
     'snapshot_sha256':digest}
  MANIFEST.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
  (ROOT/'outputs'/'retrieval_case_synthesis.json').parent.mkdir(exist_ok=True)
  (ROOT/'outputs'/'retrieval_case_synthesis.json').write_text(json.dumps({'findings':FINDINGS,'manifest':manifest},indent=2,ensure_ascii=False)+'\n',encoding='utf8')
  print(json.dumps(manifest,indent=2,ensure_ascii=False))

if __name__=='__main__':build()
