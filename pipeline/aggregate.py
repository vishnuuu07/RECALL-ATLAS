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
    relevant=evidence[evidence.relevance.isin(['DIRECT','RELATED'])]
    rows=[]
    for f in FINDINGS:
        subset=relevant[relevant.record_id.isin(f['ids'])]
        rows.append({'theme':f['title'],'evidence_count':len(subset),
                     'rich_count':int(subset.evidence_depth.isin(['E1','E2']).sum()),
                     'source_count':subset.source_platform.nunique(),
                     'source_distribution':' | '.join(subset.source_platform.value_counts().index),
                     'record_ids':'|'.join(subset.record_id),
                     'definition':f['observed']+' Possible interpretation: '+f['mechanism'],
                     'contradictions':f['qualification'],'research_gap':f['question']})
    return pd.DataFrame(rows)


def hypotheses(theme_df:pd.DataFrame)->pd.DataFrame:
    rows=[]
    for f in FINDINGS:
        rows.append({'hypothesis_id':f['id'],'theme':f['title'],'status':f['status'],
                     'statement':f['mechanism'],'supporting_ids':'|'.join(f['ids']),
                     'contradictory_evidence':f['qualification'],
                     'interview_question':f['question'],'potential_outcome':f['metric']})
    return pd.DataFrame(rows)
