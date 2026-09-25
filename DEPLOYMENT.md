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

## GitHub manual authorisation

This local folder has been initialised as a Git repository, but no GitHub account, remote or token is configured. In an authenticated terminal, create an empty GitHub repository and run:

```powershell
git add .
git commit -m "Prepare fixed Phase 2 public snapshot"
git branch -M main
git remote add origin https://github.com/<YOUR-ACCOUNT>/<YOUR-REPOSITORY>.git
git push -u origin main
```

If GitHub prompts for authentication, complete it in the browser or use a credential manager/token outside this project. Do not place tokens in project files, Streamlit secrets or shell history.

## Streamlit Community Cloud manual authorisation

1. Sign in at [share.streamlit.io](https://share.streamlit.io/) using the GitHub account that owns or can access the repository.
2. Select **Create app**, then choose `<YOUR-ACCOUNT>/<YOUR-REPOSITORY>`, branch `main`, and main file path `app.py`.
3. Leave the advanced secrets field empty. Community Cloud will use `runtime.txt`, `requirements.txt` and `.streamlit/config.toml` from the repository.
4. Deploy, wait for the build to complete, and copy the assigned `https://<subdomain>.streamlit.app` URL.
5. Open that URL in an unauthenticated browser session. Confirm the overview shows 24 raw records, 23 relevant signals, 12 evidence-rich episodes and four sources; then exercise all eight sections, an Evidence Explorer query, a source link and one CSV export.
6. Record the actual assigned URL in the release/README only after that public check succeeds.

The project currently has no public deployment URL because GitHub and Streamlit account authorisation are not available in this workspace.
