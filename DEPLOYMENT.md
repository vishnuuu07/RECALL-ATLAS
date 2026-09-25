# Streamlit Community Cloud deployment

## Pre-flight

Run these commands from the repository root. They verify the fixed 24-record snapshot, manifest hash, research evidence references and the absence of credential patterns in the public SQLite file.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-research.txt
.\.venv\Scripts\python.exe scripts/verify_submission.py
.\.venv\Scripts\python.exe scripts/validate_data.py
.\.venv\Scripts\python.exe scripts/validate_sources.py
.\.venv\Scripts\python.exe -m pytest -q
```

Do not run collection or `--include-app-store` before public submission. The app runs from the committed SQLite snapshot and requires no secrets.

## GitHub release target

The configured repository is `https://github.com/vishnuuu07/RECALL-ATLAS.git` and the deployment branch is `master`. Push the verified corrective release with:

```powershell
git push origin master
```

If GitHub prompts for authentication, complete it outside the repository. Do not place tokens in project files, Streamlit secrets or shell history.

## Streamlit Community Cloud manual authorisation

1. Sign in at [share.streamlit.io](https://share.streamlit.io/) using the GitHub account that owns or can access the repository.
2. Select **Create app**, then choose `vishnuuu07/RECALL-ATLAS`, branch `master`, and main file path `app.py`.
3. Leave the advanced secrets field empty. Community Cloud will use `runtime.txt`, `requirements.txt` and `.streamlit/config.toml` from the repository.
4. Deploy, wait for the build to complete, and open `https://recall-atlas.streamlit.app/` in a fresh browser session.
5. Confirm the overview shows 24 raw records, 23 relevant signals, 12 evidence-rich episodes and four source categories. Exercise all four pages (Overview, Explore evidence, Opportunities and Methodology), one evidence filter, a source link and one CSV export. The Overview must show its four Matplotlib charts without Plotly/module errors or raw `NULL`/debug output.
6. Record verification only after that public check succeeds.

The expected public URL is `https://recall-atlas.streamlit.app/`; do not treat it as verified until the deployed revision has passed the fresh-browser check.
