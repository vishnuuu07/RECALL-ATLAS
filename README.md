# RECALL ATLAS · Google Photos retrieval discovery

An independent, evidence-linked research dashboard; not affiliated with Google.

## What the public app provides

Five reviewer-oriented sections: **Overview**, **Research answers**, **Explore evidence**, **Opportunities**, **Methodology**. The v0.5 local package presents 70 structured, source-linked retrieval-case rows from the supplied workbook, linked to 60 distinct discussion URLs. A case row is not necessarily an independent person or discussion, and editorial reconstructions are not interview transcripts. Counts are *not* population estimates; findings remain research hypotheses pending observed user tasks.

The app uses the local, read-only `data/public/recall_atlas_70_cases.sqlite` snapshot and does not fetch source websites or call models when a visitor opens it. It does not need `.env` or API keys. The prior 24-source-record / 40-consolidated-case pipeline snapshot remains in `recall_atlas_public.sqlite` with its manifest for lineage; it is not added to the v0.4 70-case headline because overlap has not been independently reconciled.

## Run locally

Create Python 3.12 environment and install runtime packages:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Validate

```powershell
.\.venv\Scripts\python.exe -m pip install pytest
.\.venv\Scripts\python.exe scripts/verify_retrieval_70.py
.\.venv\Scripts\python.exe scripts/verify_submission.py
.\.venv\Scripts\python.exe scripts/validate_data.py
.\.venv\Scripts\python.exe scripts/validate_sources.py
.\.venv\Scripts\python.exe -m pytest -q
```

The 70-case public snapshot is fixed; only run the historical derived-table refresher against its intended archival database. The v0.5 assignment answers are source-linked Python mappings validated by tests. Heavy collection/embedding dependencies are separate in `requirements-research.txt`.

## Deploy

Push to the existing GitHub repository and deploy `app.py` to Streamlit Community Cloud. See `DEPLOYMENT.md`. No environment secrets are required. Confirm that the live site has five sections and visible Matplotlib charts in an incognito browser; a Python health check alone is insufficient.

## Research boundary

The v0.4 workbook collection was deliberately enriched for retrieval complaints, is small and self-selected, and contains cross-product context. Its source links were supplied with the workbook but have not all been independently rechecked for availability. It does not establish a retrieval-success rate, prevalence, causal failure mode, or a 70-person interview sample. The historical 24-case pipeline used embeddings + KMeans. The 70-case v0.5 edition additionally executed exploratory TF-IDF/SVD/KMeans offline (outputs saved); its curated case themes and assignment answers are not machine-validated labels. See `RESEARCH_TO_SOLUTION_HANDOFF.md` and `research/presentation_repair.md`.

## v0.5 reviewer route: the original assignment questions are directly answered

Open **Overview** to see short answers to the exact four Part 1 questions within the first screen, then **Research answers** for eight evidence-mapped questions, coded charts, case-ID examples, source links, and limitations. The counts are non-exclusive analyst codes among 29 memory-led rows of a selected 70-row public corpus. The original 70-row SQLite dataset is not modified by the v0.5 presentation layer.

The offline NLP research pass for the 70-case edition is reproducible with `python scripts/analyze_70_semantics.py` after installing `requirements-research.txt`. Its saved outputs are exploratory unsupervised clusters, not human-reviewed retrieval-failure labels or model-accuracy statistics. Previous Sentence Transformer analysis ran on the historical 24-case corpus, not all 70 cases.
