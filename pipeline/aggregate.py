"""Evidence-specific derived tables for the fixed Recall Atlas corpus.

Never count all relevant records as answering an arbitrary research question.
Research claims remain directional and point to actual source identifiers.
"""
from __future__ import annotations
import pandas as pd
from recall_atlas.research_views import FINDINGS,QUESTIONS


def questions(evidence:pd.DataFrame)->pd.DataFrame:
    relevant=evidence[evidence.relevance.isin(['DIRECT','RELATED'])]
    existing=set(relevant.record_id)
    rows=[]
    for i,(group,question,answer,source_ids) in enumerate(QUESTIONS,1):
        ids=[x for x in source_ids if x in existing]
        rows.append({'question_id':f'Q{i}', 'group':group,'question':question,
                     'answer':answer,'evidence_count':len(ids),'denominator':len(relevant),
                     'evidence_ids':'|'.join(ids),'confidence':'Directional, targeted corpus' if ids else 'Unanswered',
                     'interview_follow_up':'Observe a real attempt and capture recalled clues, initial query, results, subsequent action and confirmed outcome.'})
    return pd.DataFrame(rows)


def themes(evidence:pd.DataFrame)->pd.DataFrame:
    rows=[]
    for f in FINDINGS:
        rows.append({'theme':f['title'],'evidence_count':len(f['supporting_ids']),
                     'rich_count':0,'source_count':0,'source_distribution':'Source-neutral Retrieval Cases',
                     'record_ids':'|'.join(f['supporting_ids']),
                     'definition':f['observed']+' Possible interpretation: '+f['mechanism'],
                     'contradictions':' | '.join(f['contradictory_ids']),'research_gap':f['question']})
    return pd.DataFrame(rows)


def hypotheses(theme_df:pd.DataFrame)->pd.DataFrame:
    rows=[]
    for f in FINDINGS:
        rows.append({'hypothesis_id':f['id'],'theme':f['title'],'status':'Directional / requires validation',
                     'statement':f['mechanism'],'supporting_ids':'|'.join(f['supporting_ids']),
                     'contradictory_evidence':'|'.join(f['contradictory_ids']),
                     'interview_question':f['question'],'potential_outcome':f['metric']})
    return pd.DataFrame(rows)
