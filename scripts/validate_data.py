from pathlib import Path
import json,sqlite3,sys
root=Path(__file__).resolve().parents[1]; db=root/'data/public/recall_atlas_public.sqlite'; manifest=json.loads((root/'data/manifests/public_snapshot_manifest.json').read_text())
con=sqlite3.connect(db); count=con.execute('select count(*) from evidence').fetchone()[0]; missing=con.execute("select count(*) from evidence where record_id is null or source_url not like 'http%' or public_excerpt='' ").fetchone()[0]
assert count==manifest['public_record_count'],(count,manifest['public_record_count']);assert not missing,missing;assert con.execute("select count(*) from sqlite_master where name='evidence_fts'").fetchone()[0]==1
print(f'validated {count} public records; snapshot integrity OK')
