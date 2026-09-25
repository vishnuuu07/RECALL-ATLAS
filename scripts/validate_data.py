from pathlib import Path
import json,sqlite3,sys
root=Path(__file__).resolve().parents[1]; db=root/'data/public/recall_atlas_public.sqlite'; manifest=json.loads((root/'data/manifests/public_snapshot_manifest.json').read_text())
con=sqlite3.connect(db); count=con.execute('select count(*) from retrieval_cases').fetchone()[0]; missing=con.execute("select count(*) from retrieval_cases where case_id is null or original_account='' ").fetchone()[0]
assert count==manifest['public_record_count'],(count,manifest['public_record_count']);assert not missing,missing;assert con.execute("select count(*) from sqlite_master where name='evidence_fts'").fetchone()[0]==1
assert 'source_url' not in {row[1] for row in con.execute('pragma table_info(evidence)')}
print(f'validated {count} consolidated Retrieval Cases; snapshot integrity OK')
