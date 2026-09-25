# Recall Atlas — v0.5 research-to-solution handoff

## The decision in one line
The 70-case selected public corpus contains examples of **remembered clues that are difficult to apply in a retrieval task**. The initial product decision remains open: collection-scoped search, literal-term interpretation, and candidate-to-event navigation are distinct tasks. Asset-availability incidents must be diagnosed before treating them as search failures.

**Scope:** 70 structured source-case rows, 60 supplied discussion URLs, 29 manually coded memory-led cases, 29 adjacent search/navigation cases and 12 asset-availability diagnostic cases. Rows are not independent interviews or a representative user sample. Original links were supplied with the workbook and not all have been rechecked for live accessibility. Older 24/40-case snapshots are archival and must not be summed with this collection without source-level reconciliation.

## Answers to the four questions in Part 1

| Assignment question | Evidence-based answer | Illustrative case IDs | Boundary |
|---|---|---|---|
| What kinds of old photos do users struggle to retrieve? | Family/pet and personal memories, events and collection-contained photos, screenshots with remembered words, and one-off objects/keepsakes appear in memory-led accounts. | S02, S10, S08, S32, S04, S43, S01, S21 | Selected examples, not population prevalence; some routes were successful. |
| What do people actually remember? | A mixture of visual objects, an approximate time, people/relationships, events/collections, and words/text. | S02, S03, S23, S04 | The account summary is not an observation of what arose *before* search. |
| What have they forgotten? | Some explicitly lack exact dates, filenames/terms, or their position within the library or album. | S01, S04, S23, S32 | An omitted detail is not proof it was forgotten. |
| How do they formulate incomplete-memory searches? | Descriptive/object terms, screenshot text, person/place/date combinations, and navigation from an identifiable related image; some image-based strategies were only requested rather than executed. | S02, S03, S04, S23, S01 | Exact raw query text is often unavailable; these are reported actions, not instrumented sessions. |

All four answers, four more research questions, case ID mapping, charts, and source-access controls are exposed in the **Research answers** page and visible in condensed form on **Overview**.

## Candidate mechanisms and tests

| Direction | Illustrative evidence | Critical counterexample/uncertainty | Observed task to conduct | Outcome metric |
|---|---|---|---|---|
| Collection-scoped retrieval | S08, S32, S47 | S23 describes an existing route from a known image to the day. | Ask participant to find a specified known image *within* a known album/event, recording the initial query, scope and next steps. | Verified target retrieval, time, steps. |
| Literal words or filename retrieval | S04, S11, S30, S43 | S04 and S35 describe successful reformulations; may be discoverability/indexing, not absent functionality. | Find a known screenshot containing a known phrase; compare literal and broader query attempts. | Correct screenshot within task time; reformulations. |
| Candidate-to-event/context navigation | S08, S23, S32 | S23 reports the difficulty resolved after a sorting change. | Start from a candidate photo of the right event and ask for a different photo from that event. | Time from first useful candidate to verified target; near-miss abandonment. |
| Availability/account diagnosis (separate) | S18, S19, S60 | S58 reports nothing was lost; these cannot establish search failure. | Confirm asset exists in the same account/backup/device before running retrieval tasks. | Share of eligible tasks with confirmed asset presence. |

## What the feedback does and does not establish

- This is a selected, Reddit-heavy collection; topic counts show **case coding**, not rates among Google Photos users.
- 70 source-case rows share 60 URLs. Some comments are from the same discussion, so sources are not automatically independent participants.
- A reported successful workaround is an account, not independently verified task success.
- Q&A reconstructions from supplied workbooks are editorial planning notes, not verbatim interview transcripts or extra cases.
- The historical 24-record NLP pipeline ran Sentence Transformer/KMeans. The 70-case edition now also has an executed **offline exploratory TF-IDF → SVD → KMeans** pass. Weak cluster separation means those model clusters are not validated mechanisms. Curated research themes and answers are independently mapped from case summaries.
- No production success-rate baseline, objective source-asset availability, participant-level behaviour, causal product failure, or feature lift is established by this dataset.

## Target of primary research
Conduct 5–6 genuine, consented retrieval interviews involving a known-to-exist target asset. Before a search, record the remembered/forgotten clue inventory; observe the **actual first query**, result set, interpretation, refinement, available product mode, workaround and end state. Include successful counterexamples and a separate availability-state diagnosis. Do not constrain participants to the dashboard's preferred theme.

## Problem-selection gate
Only after observed retrieval episodes: choose one behavioural situation, one failure mechanism, and one measurable outcome. Compare current Google Photos capabilities and existing workaround discoverability before proposing new functionality. Keep the MVP task narrow enough to deploy and test with three users; use representative, consented assets if the real Google Photos library cannot be accessed by the prototype. Report those assets as representative.

## Metrics and risks
Primary: percentage of eligible users who confirm finding their intended target in the measurement window. Task diagnostic: verified target retrieval within a controlled task; time to target; first-useful-candidate rate; query/refinement count; false-target selection; perceived effort. Guardrails: privacy, false confidence, latency, precise-search regression and asset-availability misdiagnosis. Production baselines are **not supplied** and would need instrumentation.
