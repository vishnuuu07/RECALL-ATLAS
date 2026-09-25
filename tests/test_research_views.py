from pathlib import Path
import sqlite3
import pandas as pd
from recall_atlas.research_views import FINDINGS,QUESTIONS,validate_editorial_ids,evidence_for
from recall_atlas.charts import category_chart,themes_chart

def test_editorial_refs_exist_and_question_coverage_is_specific():
    db=Path(__file__).parents[1]/'data/public/recall_atlas_public.sqlite'
    with sqlite3.connect(db) as c: ev=pd.read_sql_query('select * from retrieval_cases',c)
    assert validate_editorial_ids(ev)==[]
    assert len(QUESTIONS)==4
    assert any(0<len(refs)<len(ev) for _,_,_,refs in QUESTIONS)
    for f in FINDINGS:
        assert len(evidence_for(f,ev))==len(f['supporting_ids'])

def test_server_charts_render_without_plotly():
    db=Path(__file__).parents[1]/'data/public/recall_atlas_public.sqlite'
    with sqlite3.connect(db) as c: ev=pd.read_sql_query('select * from retrieval_cases',c)
    stats=pd.DataFrame([{'label':f['title'],'records':len(evidence_for(f,ev))} for f in FINDINGS])
    for fig in [category_chart(ev,'remembered_clues','Remembered clues'),themes_chart(stats)]:
        assert fig is not None
        fig.canvas.draw()
