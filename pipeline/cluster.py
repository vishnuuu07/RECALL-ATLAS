from __future__ import annotations
import numpy as np
def cluster(vectors:np.ndarray)->list[int]:
    from sklearn.cluster import KMeans
    if len(vectors)<3:return [0]*len(vectors)
    return KMeans(n_clusters=min(4,len(vectors)),random_state=42,n_init='auto').fit_predict(vectors).tolist()

