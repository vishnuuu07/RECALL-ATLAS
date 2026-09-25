"""Offline unsupervised NLP for v0.5; not a classifier accuracy claim.

Uses ML features to discover lexical/semantic-neighbourhood candidates for review;
research answers remain source-linked human-defined mappings. Deterministic.
"""
from __future__ import annotations
import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import normalize

ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/'data/public/recall_atlas_70_cases.sqlite'
OUT=ROOT/'outputs'

def run():
    with sqlite3.connect(f'file:{DB.as_posix()}?mode=ro',uri=True) as con:
        df=pd.read_sql_query('SELECT case_id,retrieval_goal,remembered_clues,initial_action,reported_results,refinement,outcome FROM cases ORDER BY case_id',con)
    docs=df[['retrieval_goal','remembered_clues','initial_action','reported_results','refinement','outcome']].fillna('').agg(' '.join,axis=1)
    vec=TfidfVectorizer(stop_words='english',ngram_range=(1,2),min_df=2,max_df=.88,sublinear_tf=True)
    X=vec.fit_transform(docs)
    components=min(24,X.shape[0]-1,X.shape[1]-1)
    if components<2:raise RuntimeError('Not enough features for validated offline NLP')
    emb=normalize(TruncatedSVD(n_components=components,random_state=42).fit_transform(X))
    n_clusters=5
    model=KMeans(n_clusters=n_clusters,random_state=42,n_init=20)
    labels=model.fit_predict(emb)
    terms=vec.get_feature_names_out()
    results=[]
    for cid in range(n_clusters):
        idx=np.where(labels==cid)[0]
        weights=np.asarray(X[idx].mean(axis=0)).ravel()
        top=[str(terms[i]) for i in weights.argsort()[::-1][:9]]
        results.append(dict(cluster_id=int(cid),rows=len(idx),case_ids=df.iloc[idx].case_id.tolist(),top_terms=top))
    OUT.mkdir(exist_ok=True)
    pd.DataFrame(dict(case_id=df.case_id,ml_cluster=labels.astype(int))).to_csv(OUT/'offline_ml_case_assignments.csv',index=False)
    payload=dict(snapshot='70-case fixed local corpus',status='executed',features='TF-IDF unigrams/bigrams → TruncatedSVD → KMeans',
        purpose='unsupervised similarity exploration, not verified failure labels',model_accuracy='unmeasured',random_seed=42,
        k=n_clusters,records=len(df),silhouette_score=round(float(silhouette_score(emb,labels)),3),clusters=results)
    (OUT/'offline_ml_analysis.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf8')
    print(f"70-case offline ML: {len(df)} documents, k={n_clusters}, silhouette={payload['silhouette_score']}, output={OUT}")

if __name__=='__main__':run()
