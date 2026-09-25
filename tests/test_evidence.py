from pathlib import Path
import sqlite3
def test_public_evidence_is_source_neutral():
    db=Path(__file__).parents[1]/'data/public/recall_atlas_public.sqlite';con=sqlite3.connect(db)
    columns={r[1] for r in con.execute('pragma table_info(evidence)')}
    assert 'source_url' not in columns
    assert con.execute("select count(*) from evidence where source_platform != 'Retrieval Cases' or public_excerpt='' ").fetchone()[0]==0
    assert con.execute("select count(*) from evidence where public_excerpt like '%http%' ").fetchone()[0]==0
