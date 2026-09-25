# Presentation and analysis repair · 25 September 2026

- Kept all 24 fixed public evidence records unchanged; did not add unverified sources.
- Removed Plotly from public runtime to avoid the reported browser-side dynamic-import failure; use Matplotlib static figures and Streamlit filters.
- Replaced eight navigation destinations with four reviewer-friendly sections, while retaining all 22 assignment questions in Methodology.
- Removed generic 23-of-23 answers for unrelated questions: each question has narrow source-ID references or explicitly states insufficient evidence.
- Replaced generic theme descriptions with four source-specific hypotheses and counterexamples, labelled directional/not validated.
- Removed internal NULL/debug output from public rendering; missing values now show 'Not established by source'.
- No claim of human audit, model accuracy, independently verified success, population prevalence or causal root cause.
- Local snapshot metadata and SHA were recomputed after refreshing derived analytical tables; source evidence table itself is unchanged.

Deployment must be independently checked in an incognito browser after the local changes are committed and pushed. Container-level testing here does not substitute for an actual Streamlit deployment check.
