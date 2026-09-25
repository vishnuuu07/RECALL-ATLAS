from pathlib import Path
import sqlite3
db=Path(__file__).resolve().parents[1]/'data/public/recall_atlas_public.sqlite';con=sqlite3.connect(db)
columns={row[1] for row in con.execute('pragma table_info(evidence)')};assert 'source_url' not in columns
bad=con.execute("select count(*) from evidence where source_platform != 'Retrieval Cases'").fetchone()[0];assert bad==0;print('public snapshot is source-neutral')
