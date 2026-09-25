# RECALL ATLAS · Google Photos retrieval discovery

An independent, evidence-linked research dashboard; not affiliated with Google.

## What the public app provides

Four reviewer-oriented sections: **Overview**, **Explore evidence**, **Opportunities**, **Methodology**. The research sample contains 24 fixed public-source records, 23 deterministically coded DIRECT/RELATED signals and 12 E1/E2 coded records. Counts are *not* population estimates. Findings remain research hypotheses pending observed user tasks.

The app uses a local SQLite research snapshot, and does not fetch source websites or call models when a visitor opens it. It does not need `.env` or API keys.

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
.\.venv\Scripts\python.exe scripts/verify_submission.py
.\.venv\Scripts\python.exe scripts/validate_data.py
.\.venv\Scripts\python.exe scripts/validate_sources.py
.\.venv\Scripts\python.exe -m pytest -q
```

To refresh only the evidence-specific derived tables (not source records), use `python scripts/refresh_derived_analysis.py`. It recomputes the public manifest checksum. Heavy collection/embedding dependencies are separate in `requirements-research.txt`.

## Deploy

Push to the existing GitHub repository and deploy `app.py` to Streamlit Community Cloud. See `DEPLOYMENT.md`. No environment secrets are required. Confirm that the live site has four sections and visible Matplotlib charts in an incognito browser; a Python health check alone is insufficient.

## Research boundary

The corpus was deliberately enriched for retrieval complaints, is small and self-selected, and contains cross-product context. LLM structured extraction was not used; offline embedding + KMeans use is recorded by the processing manifest. Automated label corrections are not human audit. See `RESEARCH_TO_SOLUTION_HANDOFF.md` and `research/presentation_repair.md`.
