"""Validate locally stored source provenance; does not claim live URL accessibility."""
from pathlib import Path
import sqlite3
from urllib.parse import urlparse
DB=Path(__file__).resolve().parents[1]/'data/public/recall_atlas_70_cases.sqlite'
with sqlite3.connect(f'file:{DB.as_posix()}?mode=ro',uri=True) as c:
 rows=c.execute('SELECT case_id,source_platform,source_url FROM cases').fetchall()
 assert len(rows)==70
 for cid,platform,url in rows:
  u=urlparse(url)
  assert u.scheme=='https' and u.hostname and u.path,(cid,url)
  assert ('reddit.com' in u.hostname or u.hostname=='support.google.com'),(cid,url)
 print(f'PASS source format: {len(rows)} case URLs; live accessibility NOT independently checked')
