from pathlib import Path
import sqlite3
def test_evidence_has_provenance():
    db=Path(__file__).parents[1]/'data/public/recall_atlas_public.sqlite';con=sqlite3.connect(db)
    assert con.execute("select count(*) from evidence where source_url not like 'http%' or public_excerpt='' ").fetchone()[0]==0
