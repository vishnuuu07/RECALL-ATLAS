# Data quality report

Automated gates validate Pydantic schema, unique IDs, HTTP source URLs, non-empty paraphrased excerpts, deterministic content-hash deduplication, FTS5 snapshot construction and manifest reconciliation.

Phase 2 retained the legacy deterministic prediction (`relevance_original`, `evidence_depth_original`, `confidence_original`) beside the corrected focused-audit prediction and a correction string. E1 means a complete, outcome-stated episode; E2 is a substantive but outcome-incomplete episode; E3 is a relevant contextual signal; E4 is uncertain or out of scope. This is a rule-based audit, not an independent human-label accuracy estimate.

Limits: public feedback is self-selected and targeted collection intentionally raises relevant-signal density. Excerpts can omit context. Asset presence, UI state, eligibility, index state and final verified success are usually unobservable. Source mix is more diverse than Phase 1 but remains Reddit/Google Photos Community concentrated; public YouTube comment evidence was inaccessible.
