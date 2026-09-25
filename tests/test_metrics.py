import pandas as pd
from recall_atlas.metrics import pct,funnel
def test_percentage_denominator_and_funnel():
    df=pd.DataFrame({'relevance':['DIRECT','IRRELEVANT'],'evidence_depth':['E2','E4']});f=funnel(df,3)
    assert pct(1,2)==50 and list(f['count'])==[3,2,1,1]
