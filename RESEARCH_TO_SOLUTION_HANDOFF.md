# Recall Atlas — research-to-solution handoff (presentation repair, v0.3)

## Executive research readout

The available public sample supports **investigating**, not choosing, four separate problems: (1) applying remembered album/event context to a search; (2) expressing literal screenshot text and filenames rather than broad semantic terms; (3) moving from a useful candidate into a related time window; and (4) diagnosing sparse/irrelevant results before assuming the target or index is faulty. Source-backed examples include `reddit-1aju75m` (programme-specific campfire images), `reddit-1i06lg2` (quoted screenshot-text workaround), `reddit-1h09vho` (surrounding-day navigation request), and `reddit-1ov9y8d` (incomplete object results with contrary account reports).

**Interpretation:** source reports show distinct possible intervention points, but cannot establish which one drives unsuccessful retrieval or whether current features solve it. Interview evidence and consented, observed retrieval tasks must select the problem. The public-facing dashboard now exposes these directions without fabricated quantitative confidence or a business-impact score.

**Presentation/data repair:** the underlying 24 original evidence records, URLs and prior correction labels are preserved. The 22 research-question answers and four derived finding/hypothesis records are now mapped to specific IDs rather than automatically treating all 23 relevant records as answers to every question. No new collection has been claimed.


## Snapshot and interpretation boundary

The reproducible local snapshot contains 24 raw records, 24 unique/publishable records and 23 corrected relevant signals: Reddit 12, Google Photos Community 9, PIXLS.US photo-management forum 2 and Google Play Store 1. Twelve are substantive retrieval episodes (E1/E2); six are complete, outcome-stated episodes (E1). Counts are a targeted evidence corpus, not frequency estimates or product telemetry.

Every evidence row carries `relevance_original`, `evidence_depth_original`, corrected fields and `classification_correction`. The automated Phase-2 rules audit changed 15 labels/depths; it is not an independent human audit. It upgraded no previously non-relevant labels: the collection was deliberately retrieval-enriched. One weakly supported face-recognition complaint was moved from RELATED/E3 to UNCERTAIN/E4. This is not evidence that face search is ineffective.

## Evidence-backed hypotheses to test

### H1 — People may struggle to translate a remembered collection/context into a bounded search space

Supporting records: `community-495705`, `community-78574873`, `community-128230954`, `community-162522212`, `reddit-1g5dmve`, `reddit-1aju75m`.

Observed mechanism: people describe a child, group/programme, album title, month or destination collection, but global search and album navigation do not always let them apply that context as scope. The apparent failure may be query construction, search mode, collection indexing, or interface placement; the corpus does not establish which.

Contradictory/qualifying evidence: `community-128230954` reports a unique-album-title plus term as an accepted workaround; `community-162522212` reports browser Find working for a known album name. `pixls-47845` shows metadata/tag/location practices can make retrieval tractable in another photo-management context.

Segments to recruit: high-album-count organisers; parents maintaining long-lived child albums; teams retrieving a content subtype for reuse.

Interview questions: “Show the last asset you needed within a known collection. What did you remember: album title, event, people, time or subject? Which clue could you not express or apply? What happened after you committed the query?”

Possible intervention points: expose scope before query commitment; make collection context inspectable/reusable; make the difference between album suggestion and global-photo result explicit. Do not select an implementation before observed-task research.

Metrics: scoped-query adoption; candidate-set size; time to verified retrieval; verified retrieval success among attempts with known collection context.

### H2 — Exact-text, filename and screenshot retrieval may require query syntax users do not discover

Supporting records: `community-106429666`, `reddit-rd8u2q`, `reddit-1i06lg2`, `reddit-1iaob2b`, `reddit-1lklsk2`.

Observed mechanism: users remember text, a filename portion, a screen name or a renamed keyword, but report broad semantic results, date-level results or inconsistent OCR matches. `reddit-1i06lg2` documents a reformulation from an over-broad combined query to quoted text within screenshots.

Contradictory/qualifying evidence: `reddit-1i06lg2` reports the quoted-text refinement worked. That indicates a discoverability/interpretation candidate, not proof of a retrieval-model failure. `community-106429666` also identifies a separate Screenshot category as a navigation alternative.

Segments to recruit: screenshot/document keepers; people who remember an exact string, file fragment or renamed media; users who save messages, receipts and bills as images.

Interview questions: “What exact text or filename fragment did you recall? What did you type first? What did the result set mean to you? Did you know any quoting, category or metadata controls beforehand?”

Possible intervention points: make text-match versus semantic-match mode legible; surface safe query examples at reformulation; offer screenshot/document scope without implying completeness.

Metrics: first-query precision; reformulation count; syntax/control discovery rate; verified screenshot/document retrieval success.

### H3 — A relevant candidate may not provide a low-friction route to related photos from the same event/day

Supporting records: `reddit-1h09vho`, `reddit-1fmvxd6`. `community-495705` concerns month-level retrieval inside a child album and is relevant to collection scope, not direct evidence of candidate-to-timeline navigation.

Observed mechanism: after imperfect search or a partial candidate, people estimate a date, browse month/year manually, or ask for a jump to the surrounding day. This is candidate-to-timeline navigation evidence; it does not show that every target is temporally adjacent or that a day view would solve the attempt.

Contradictory/qualifying evidence: `reddit-1fmvxd6` describes manual month/year browsing as an available workaround, not a confirmed failure. Asset presence, date accuracy and final target verification remain unknown.

Segments to recruit: event-oriented recallers; people who remember a rough date but not visual keywords; people who can recognise a related image faster than they can formulate a query.

Interview questions: “When you found a near miss, what made you believe the target was nearby? Did you navigate by date, album, location or a second search? When did you stop?”

Possible intervention points: test related-time navigation from a candidate; communicate temporal scope; preserve a reversible path back to the search result.

Metrics: candidate-to-related-navigation use; number of candidates inspected; time from first useful candidate to verified target; abandonment after a near miss.

### H4 — Result relevance/completeness concerns are reported, but the underlying cause is not identifiable from feedback alone

Supporting records: `reddit-1fa4fg1`, `reddit-1ov9y8d`, `reddit-193u8s0`, `reddit-1iaob2b`, `community-400823549`.

Observed mechanism: remembered object/text cues are described as returning irrelevant, incomplete or missing results. The records cannot distinguish indexing delay, backup/account/scope state, query interpretation, changed capability, model behaviour or an absent target.

Contradictory/qualifying evidence: `reddit-1ov9y8d` includes another participant reporting different object-search results and suggesting a backup check. `reddit-1i06lg2` reports a successful refinement. Neither establishes a root cause for the failed reports.

Segments to recruit: long-tenure, large-library users; people searching old screenshots/documents; users who report a capability changed over time. Stratify by backup/account state and web/mobile surface.

Interview questions: “How do you know the asset exists in this library? Can you locate it by timeline or another device? What platform, account, and search mode were used? What exact candidates did the system return?”

Possible intervention points: diagnosis before remediation; make scope/account/index-state cues observable; provide candidate-feedback paths only after distinguishing asset absence from retrieval failure.

Metrics: diagnosable-attempt rate; confirmed asset-presence rate; false-negative candidate rate on consented tasks; verified retrieval success after a diagnostic step.

## Existing capabilities to check in research

The application’s capability audit links to Google documentation for search across people/things/places, albums/documents/text, Ask Photos, and face groups. Public records also mention Screenshot categories, quoted text, album-title-plus-term search, browser Find and manual timeline browsing. Capability mention or documentation is not evidence that it was available to, discovered by, or effective for the reporting user. Test account eligibility, platform, region, feature state and task comprehension before claiming a gap.

## Workarounds observed

Album title plus another term (`community-128230954`); browser Find or alphabetical/recent ordering for albums (`community-78574873`, `community-162522212`); quote screenshot text (`reddit-1i06lg2`); move through month/year or surrounding-day photos (`reddit-1fmvxd6`, `reddit-1h09vho`); select the actual folder when metadata scope is empty (`pixls-39727`); metadata/tags/location/contact-sheet practices (`pixls-47845`). A workaround can be burdensome and still work; it must not be treated as a failure-free outcome.

## Unsupported claims and research limits

Do not claim a root cause, prevalence, causal impact, universal regression, user segment size or an MVP from this corpus. No record proves target availability, exact UI state, result ranking, underlying index state, or independently verified retrieval success except where the author explicitly reports a local outcome. The Google Play review has no stable per-review URL, and its label is retained as UNCERTAIN.

Collection was limited to publicly indexed/publicly displayed material and paraphrased excerpts. Reddit’s authorised API was not configured, Google Play exposes only a small rendered review sample without a stable per-review link, and no relevant, citable YouTube comments were accessible through public search/browser review. No access controls were bypassed. Targeted collection also means the high relevant-signal density is expected and non-representative.

## Decision gate

Run consented, observed retrieval tasks before selecting a final MVP. For each hypothesis, require a reproducible clue pattern, a documented current-capability path, a verified end state, and a comparison against the workaround before prioritising an intervention.
