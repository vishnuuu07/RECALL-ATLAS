from __future__ import annotations
import pandas as pd

def score(frame:pd.DataFrame, rich_weight:float=1.5, diversity_weight:float=1.0)->pd.DataFrame:
    out=frame.copy(); out['priority_score']=(out['evidence_count']*1 + out['rich_count']*rich_weight + out['source_count']*diversity_weight).round(1); return out.sort_values('priority_score',ascending=False)

