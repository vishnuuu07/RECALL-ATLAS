# Repository Guidelines

## Project Structure & Module Organization

`app.py` is the Streamlit entry point and reads the local, read-only SQLite snapshot through `recall_atlas/data_access.py`. Keep dashboard presentation helpers in `recall_atlas/`; do not introduce live collection into the app. `pipeline/` converts checked-in raw JSONL evidence into the snapshot, with schema validation, deterministic classification, extraction, aggregation and publication. Source-specific collectors are under `collectors/`. The public deployment artifact is `data/public/recall_atlas_public.sqlite`, described by `data/manifests/public_snapshot_manifest.json`. Research boundaries and handoff material live in `research/` and `RESEARCH_TO_SOLUTION_HANDOFF.md`.

## Build, Test, and Development Commands

Use Python 3.12. Run the dashboard with `python -m streamlit run app.py` after installing `requirements.txt`. Run `python -m pytest -q` for the test suite, or `python -m pytest tests/test_app.py -q` for the Streamlit rendering checks. Run `python scripts/verify_submission.py`, `python scripts/validate_data.py`, and `python scripts/validate_sources.py` before a public release.

`python pipeline/run_pipeline.py` rebuilds from committed `data/raw/*_public_records.jsonl` only. Do not pass `--include-app-store` for the fixed public snapshot: it deliberately opts into transient collection and changes reproducible counts.

## Testing Guidelines

Tests use pytest and cover schema, classification, deduplication, snapshot reconciliation, metrics and all eight Streamlit sections. Snapshot-facing changes must keep the manifest count/hash and SQLite evidence count aligned. Preserve `relevance_original`, `evidence_depth_original`, and `classification_correction`; deterministic corrections are not human-label evidence.

## Commit & Pull Request Guidelines

This folder was initialised without prior Git history, so no commit convention exists yet. Use concise imperative subjects. For any data or synthesis change, state the manifest count/hash impact, affected record IDs, provenance, and validation commands in the pull request. Do not commit `.venv`, credentials, private raw data, or generated temporary browser artifacts.
