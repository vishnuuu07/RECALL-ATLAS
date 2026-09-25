# RECALL ATLAS · Google Photos retrieval discovery

An independent, evidence-linked research dashboard; not affiliated with Google.

## What the public app provides

Four reviewer-oriented sections: **Overview**, **Explore evidence**, **Opportunities**, **Methodology**. The live v0.4 view presents 70 structured, source-linked retrieval-case rows from the supplied workbook, linked to 60 distinct discussion URLs. A case row is not necessarily an independent person or discussion, and editorial reconstructions are not interview transcripts. Counts are *not* population estimates; findings remain research hypotheses pending observed user tasks.

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

To refresh only the evidence-specific derived tables (not source records), use `python scripts/refresh_derived_analysis.py`. It recomputes the public manifest checksum. Heavy collection/embedding dependencies are separate in `requirements-research.txt`.

## Deploy

Push to the existing GitHub repository and deploy `app.py` to Streamlit Community Cloud. See `DEPLOYMENT.md`. No environment secrets are required. Confirm that the live site has four sections and visible Matplotlib charts in an incognito browser; a Python health check alone is insufficient.

## Research boundary

The v0.4 workbook collection was deliberately enriched for retrieval complaints, is small and self-selected, and contains cross-product context. Its source links were supplied with the workbook but have not all been independently rechecked for availability. It does not establish a retrieval-success rate, prevalence, causal failure mode, or a 70-person interview sample. The retained historical pipeline used offline embedding + KMeans as recorded by its processing manifest; no fresh model run is claimed for v0.4. See `RESEARCH_TO_SOLUTION_HANDOFF.md` and `research/presentation_repair.md`.
