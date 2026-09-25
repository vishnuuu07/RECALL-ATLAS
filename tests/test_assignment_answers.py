"""Public question-coverage regression tests (no Streamlit required)."""
import sqlite3
from pathlib import Path
import pandas as pd
from recall_atlas.assignment_answers import CASE_LENSES, QUESTIONS, lens_counts, relevant_records, validate_mappings
ROOT=Path(__file__).parents[1]

def data():
    with sqlite3.connect(ROOT/'data/public/recall_atlas_70_cases.sqlite') as conn:
        return pd.read_sql_query('SELECT * FROM cases ORDER BY case_id',conn)

def test_exact_original_assignment_questions_and_evidence_links():
    original=[
        'What kinds of old photos do users struggle to retrieve?',
        'What information do people actually remember about a photo?',
        'What information have they forgotten?',
        'How do users formulate searches when their memory is incomplete?',
    ]
    assert [q['title'] for q in QUESTIONS[:4]]==original
    assert len(QUESTIONS)==8
    df=data();validate_mappings(set(df.case_id))
    assert len(df)==70
    for q in QUESTIONS:
        assert q['answer'] and q['limit'] and q['short']
        assert 0<len(q['ids'])<len(df)
        assert len(relevant_records(q,df))==len(q['ids'])

def test_coded_lenses_do_not_count_adjacent_cases_as_vague_memory():
    df=data()
    core=set(df.loc[df.case_focus=='Memory-led account','case_id'])
    assert len(core)==29
    for category,groups in CASE_LENSES.items():
        for _,ids in groups.items():
            assert set(ids)<=core
        assert sum(lens_counts(category,core).values())>0

def test_exploratory_ai_analysis_has_real_case_assignments():
    assignments=pd.read_csv(ROOT/'outputs/offline_ml_case_assignments.csv')
    assert len(assignments)==70
    assert set(assignments.case_id)==set(data().case_id)
    assert assignments.ml_cluster.nunique()==5
