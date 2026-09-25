from __future__ import annotations
import pandas as pd

def pct(n: int, d: int) -> float: return round((100*n/d),1) if d else 0.0

def funnel(evidence: pd.DataFrame, raw_count: int) -> pd.DataFrame:
    unique=len(evidence); rel=int(evidence.relevance.isin(['DIRECT','RELATED']).sum()); rich=int(evidence.evidence_depth.isin(['E1','E2']).sum())
    return pd.DataFrame({'stage':['Raw collected','Unique publishable','Relevant signal','Evidence-rich episodes'], 'count':[raw_count,unique,rel,rich], 'denominator':['raw','unique','unique','relevant']})

