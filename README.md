# RECALL ATLAS

An independent research dashboard for public evidence about vague-memory photo retrieval. It is not affiliated with Google.

## Run locally

Use Python 3.12:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

The application reads only `data/public/recall_atlas_public.sqlite` and `data/manifests/public_snapshot_manifest.json`. It makes no collection, embedding, or model call on page load.

## Verify the fixed public snapshot

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-research.txt
.\.venv\Scripts\python.exe scripts/verify_submission.py
.\.venv\Scripts\python.exe scripts/validate_data.py
.\.venv\Scripts\python.exe -m pytest -q
```

The reproducible Phase 2 snapshot contains the committed `data/raw/*_public_records.jsonl` inputs. `pipeline/run_pipeline.py` rebuilds only from those local files by default. Transient App Store collection is opt-in via `--include-app-store` and must not be used to recreate the fixed 24-record public snapshot.

## Deploy

Push the repository to GitHub, then create a Streamlit Community Cloud app using `app.py` and `requirements.txt`. No runtime secrets are required. Follow [DEPLOYMENT.md](DEPLOYMENT.md) and verify the assigned public URL after deployment.

## Evidence boundary

Public excerpts are anonymised and short. The corpus is targeted, self-selected secondary evidence—not product telemetry, an independent human-label study, or a population estimate. Review the source links and [research handoff](RESEARCH_TO_SOLUTION_HANDOFF.md) before interpreting findings.
