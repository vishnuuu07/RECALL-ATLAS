# Data collection log

2026-09-25 Phase 2: manually reviewed publicly indexed, public Google Photos Community and Reddit discussions focused on retrieval behaviour; retained paraphrased excerpts and source URLs. Added public PIXLS.US photo-management forum evidence for metadata/scope retrieval behaviour and one publicly displayed, verified Google Play review concerning face-based retrieval. Added no generic App Store reviews.

Access limits: Reddit API credentials were unavailable, so no API or unauthorised endpoint was used. Google Play did not expose stable per-review URLs in the public rendered view; the source URL is the public app review page. Public search/browser review did not yield relevant, citable YouTube comments. No access control was bypassed.

The pipeline loads all `*_public_records.jsonl` files under `data/raw/`, deduplicates by normalised content, validates provenance, keeps legacy and corrected classifications, then regenerates the SQLite snapshot and exports. See `data/manifests/public_snapshot_manifest.json` for current counts, timestamp and hash.
