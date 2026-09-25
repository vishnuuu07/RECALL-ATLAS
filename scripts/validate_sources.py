from pathlib import Path
import sqlite3
db=Path(__file__).resolve().parents[1]/'data/public/recall_atlas_public.sqlite';con=sqlite3.connect(db)
bad=con.execute("select count(*) from evidence where source_url not like 'http%'").fetchone()[0];assert bad==0;print('source URLs valid')
