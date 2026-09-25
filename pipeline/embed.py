from __future__ import annotations
import numpy as np
def embed(texts:list[str])->tuple[np.ndarray,str]:
    from sentence_transformers import SentenceTransformer
    model=SentenceTransformer('all-MiniLM-L6-v2')
    return model.encode(texts,normalize_embeddings=True,show_progress_bar=False), 'sentence-transformers/all-MiniLM-L6-v2'

