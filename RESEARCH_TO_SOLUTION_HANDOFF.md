# Recall Atlas: Research-to-solution handoff

## Decision boundary

This handoff synthesizes 40 consolidated Retrieval Cases: the prior 24-case corpus plus 20 structured workbook cases, with four same-episode duplicates merged. It is secondary evidence, not a participant study or a prevalence estimate. Editorial Q&A reconstructions are analyst-derived planning material. They are not quotes, interviews, or additional retrieval episodes.

## Recurring retrieval failures

- Contextual and relational clues are remembered, but the initial route often becomes a simple keyword or broad descriptive search. Supporting cases: `S01`, `C08`, `S08`, `S10`, `S12`, `S13`.
- Exact screenshot or document text can return broad or inconsistent results. Supporting cases: `C20`, `C18`, `C07`, `S15`.
- A relevant candidate does not always connect to nearby dates, trip context, or chronological browsing. Supporting cases: `C08`, `S08`, `S09`, `S14`.
- Some accounts cannot establish whether an asset was present, backed up, or available to the attempted route. Supporting cases: `S18`, `S19`, `S10`.
- Successful routes may demand multiple query variants, scrolling, a copy, another device or folder, or a different search mode. Supporting cases: `C08`, `C20`, `S07`, `S17`, `S19`, `S20`.

## Suggested behavioural segments

These are task-pattern segments, not demographic personas.

| Segment | Characteristic retrieval situation | Example cases |
| --- | --- | --- |
| Context-first recollectors | Remember a relationship, event, collection, or period more readily than searchable labels. | `S01`, `S08`, `S10`, `S12` |
| Text-dependent retrievers | Remember literal text in a screenshot or document and expect it to behave like a text match. | `C20`, `C18`, `C07` |
| Candidate-to-timeline navigators | Find a useful image but need nearby images, dates, or the broader episode. | `C08`, `S08`, `S14` |
| Availability diagnosticians | Need to distinguish a search failure from missing assets, backup state, folders, or device context. | `S18`, `S19` |
| Workaround switchers | Reach another route after friction, such as chronology, reformulation, copies, device checks, or search-mode changes. | `C08`, `C20`, `S07`, `S20` |

## Possible root-cause mechanisms

| Observed behaviour | Possible mechanism | Qualifying evidence |
| --- | --- | --- |
| Relational or event memory is hard to convert into a first query. | Search-entry expectations may not match how people encode context. | `S03` and `S05` report low-effort descriptive or object retrieval. |
| Literal text requests produce broad or inconsistent results. | There may be ambiguity among literal matching, indexing state, and ranked semantic results. | `C20` reports a successful reformulation. |
| A candidate is found but the next relevant photos remain hard to reach. | The handoff between result inspection and temporal/context navigation may be unclear. | `S03` reports direct retrieval without a navigation need. |
| Unresolved retrieval is attributed to search. | Asset presence, backup, account, or folder state may be unverified. | The existing record cannot diagnose a specific cause. |

## Existing capabilities to benchmark

Benchmark the current product before designing an intervention: search by people, things, places, and text in images; date or timeline browsing; albums; result ordering; device/folder checks; and available conversational search modes. Their availability and performance must be observed in the participant’s actual context. A reported workaround does not establish that a new capability is absent.

## Current workarounds

The cases report chronology browsing, query reformulation, exact-text syntax, saving a copy, checking devices or folders, manual location correction, and changing search modes. These routes can indicate a discoverability, navigation, availability, or interpretation problem. They should be compared rather than treated as proof of one mechanism.

## Competing intervention directions

Do not select a final MVP before validation.

| Direction | Intended task | Key risk | Validation comparison |
| --- | --- | --- | --- |
| Context-led query support | Express relationship, event, collection, and period clues together. | May duplicate a usable existing route. | Current search plus ordinary reformulation. |
| Reference-image assistance | Use a known related image to initiate retrieval. | Reference-image availability and benefit are unverified. | Text query and chronological browsing. |
| Literal-text guidance | Help people request, refine, and interpret screenshot or document text. | May not solve indexing or availability issues. | Existing text search and result inspection. |
| Candidate-to-context navigation | Move from a useful candidate to nearby dates or photos. | Nearby items may not contain the target. | Direct chronological browsing. |
| Retrieval diagnostic | Make asset-presence and route state visible before repeated searching. | May add friction to successful tasks. | Unassisted retry and current troubleshooting. |

## What requires validation

Use consented, observed tasks. Record the target asset’s known availability, remembered and forgotten clues, first action, candidate set, interpretation, reformulations, workaround, target verification, and elapsed time. Include easy successes, effortful successes, unresolved tasks, and availability-state issues. Do not classify an unresolved account as failure without checking whether the intended asset exists in the tested library.

## Product-outcome metrics

- Verified target retrieval rate.
- Time from task start to target confirmation.
- First-candidate relevance.
- Query or refinement count per verified success.
- Candidate-to-timeline transition time and near-miss abandonment.
- Route-switch rate and workaround success.
- False-positive target selections.
- Perceived effort and confidence in result meaning.

Report results by task pattern and asset-availability state. Avoid a combined prevalence or business-impact score until a representative, consented study supports one.
