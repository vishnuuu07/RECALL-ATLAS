from pathlib import Path
import json,sqlite3
def test_snapshot_manifest_reconciles():
    root=Path(__file__).parents[1];m=json.loads((root/'data/manifests/public_snapshot_manifest.json').read_text());con=sqlite3.connect(root/'data/public/recall_atlas_public.sqlite')
    assert con.execute('select count(*) from evidence').fetchone()[0]==m['public_record_count']
    assert len(m['snapshot_sha256'])==64
