# AI processing methodology

Offline pipeline: Unicode/whitespace normalisation; exact content-hash deduplication; transparent regex baseline for relevance/tags; `sentence-transformers/all-MiniLM-L6-v2` embeddings; KMeans on vectors; human-readable taxonomy review. No LLM extraction was run. Clusters are supporting signals, not ground truth. Independent label accuracy is unmeasured.
