from __future__ import annotations
import pandas as pd
def status(n:int)->str: return 'Substantial' if n>=5 else 'Directional' if n>=2 else 'Limited' if n else 'No evidence'
def with_status(df:pd.DataFrame)->pd.DataFrame:
    out=df.copy(); out['coverage']=out.evidence_count.map(status); return out

