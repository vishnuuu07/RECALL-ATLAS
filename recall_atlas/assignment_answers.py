"""Evidence-mapped assignment answers for the v0.5 public research snapshot.

These manually reviewed, descriptive case ID groupings are a presentation lens over
source-case summaries, not new observations or machine-validation claims.
A case may appear in multiple groups; a source-case row is not an independent user.
"""
from __future__ import annotations

from collections import Counter


CASE_LENSES = {
    "asset_types": {
        "People, pets & family": "S02 S03 S10 S34 S40 S52 S54 S57 S69",
        "Trips, events & collections": "S08 S09 S10 S23 S27 S32 S40 S47 S65",
        "Screenshots & remembered text": "S04 S06 S11 S31 S43 S44 S55",
        "Distinctive objects & keepsakes": "S01 S13 S14 S21 S34 S54 S64 S66",
    },
    "remembered": {
        "Object or appearance": "S01 S02 S03 S06 S13 S14 S21 S34 S54 S57 S64 S66",
        "Time or approximate era": "S02 S03 S08 S10 S21 S23 S27 S40 S47 S65 S66",
        "Event, place or collection": "S08 S09 S10 S23 S27 S32 S40 S47 S52 S65 S69",
        "Person or relationship": "S01 S02 S03 S10 S34 S40 S52 S54 S57 S69",
        "Words or text content": "S04 S11 S31 S43 S44 S55",
    },
    "forgotten": {
        "Exact date or year": "S01 S02 S03 S04 S06 S08 S09 S10 S11 S13 S14 S21 S23 S40 S43 S44 S55 S57 S65 S66 S69",
        "Filename or effective search term": "S02 S03 S06 S10 S11 S21 S32 S34 S43 S44 S47 S55 S65 S66",
        "Location in library or collection": "S09 S23 S27 S32 S47 S52",
    },
    "initial_search": {
        "Descriptive or object/person words": "S02 S03 S06 S10 S11 S14 S21 S34 S43 S54 S55 S57 S64 S65 S66 S69",
        "Literal text or screenshot terms": "S04 S11 S43 S55",
        "Memory, album or known-photo navigation": "S08 S09 S23 S32 S40 S52",
        "Related-image strategy requested*": "S01 S13",
    },
}
CASE_LENSES = {kind: {label: tuple(codes.split()) for label, codes in labels.items()} for kind, labels in CASE_LENSES.items()}

# Entries use the wording of the user's brief for the first four questions.
QUESTIONS = [
    dict(id="Q1", title="What kinds of old photos do users struggle to retrieve?", short="Personal memories, event/collection photos, screenshots, and distinctive objects all appear in the selected accounts.",
         answer="The memory-led subset includes family and pet images (S02, S10), trips or album-bound photos (S08, S32), screenshots containing remembered words (S04, S43), and one-off objects or keepsakes (S01, S21). There is no evidence here that one asset type is most problematic for Google Photos users overall.",
         ids="S02 S10 S08 S32 S04 S43 S01 S21", lens="asset_types",
         limit="The chart counts overlapping analyst-coded examples among 29 memory-led rows, not mutually exclusive types or population prevalence."),
    dict(id="Q2", title="What information do people actually remember about a photo?", short="People retain a mixture of visual, temporal, relational, textual and event clues—not just one search keyword.",
         answer="Examples include cat colour, stairs and a pet name (S02); two people, tulips and approximate age (S03); an identifiable related photograph from the same day (S23); and a word from a screenshot (S04). We can describe recorded clues, but not what each person spontaneously recalled before searching.",
         ids="S02 S03 S23 S04 S01 S65", lens="remembered",
         limit="Coded details come from source-case accounts. The original pre-search memory was not directly observed."),
    dict(id="Q3", title="What information have they forgotten?", short="Exact dates, filenames and a route back into the right part of the library are explicit gaps in several cases.",
         answer="The older vase's date was unknown (S01); the screenshot date was forgotten (S04); and a related photo helped recover the day of a target (S23). The exact position within a known album was unavailable in S32. However, an account that omits a detail does not prove the user forgot it.",
         ids="S01 S04 S23 S32 S02 S06", lens="forgotten",
         limit="Counts refer only to explicitly documented missing details in selected memory-led cases; unreported details are not coded as forgotten."),
    dict(id="Q4", title="How do users formulate searches when their memory is incomplete?", short="The recorded actions mix object words, descriptions, literal text, and navigation from a known image or collection.",
         answer="S02 tried cat-colour terms and later stairs/name/year clues; S03 used a scene description; S04 combined a screenshot term with quoted text; S23 searched for a related object from the same day. S01 asked about using a newer image rather than demonstrating an executed image query. Exact original query strings are not preserved consistently.",
         ids="S02 S03 S04 S23 S01 S54", lens="initial_search",
         limit="These are reported actions, not instrumented search logs. The starred group contains a requested/proposed strategy, not executed queries."),
    dict(id="Q5", title="What happens after the first unsuccessful attempt?", short="Some people reformulate, browse chronologically, switch modes or use a nearby photo; many outcomes remain unknown.",
         answer="The pet photo was reportedly found through chronological browsing after descriptive search (S02). A screenshot was found after a narrower quoted-term search (S04). S23 reports success after changing result sorting. S20 found expected results in Classic rather than newer search. These accounts show different recovery routes, not a single universal failure.",
         ids="S02 S04 S08 S20 S23 S30 S64 S68", lens=None,
         limit="Reported outcomes are not independently observed. Most of the 70 case rows do not confirm target-level success."),
    dict(id="Q6", title="Which retrieval problems and opportunity areas differ?", short="Collection scope, exact text, candidate-to-context navigation, and asset availability call for different interventions.",
         answer="Collection-scoped search is illustrated by S32/S47; literal-term expectations by S30/S43; reaching nearby photos after finding a candidate by S08/S23; and missing-asset diagnosis by S18/S58. S23, S31, S35 and S68 also document existing successful routes, so we must not declare those capabilities absent.",
         ids="S32 S47 S30 S43 S08 S23 S18 S58 S31 S35 S68", lens=None,
         limit="Analyst-defined categories can overlap. Counts guide follow-up research; they are not rates of product failure."),
    dict(id="Q7", title="What can successful workarounds teach us?", short="Some paths already work. We must test discoverability and effort before proposing a missing feature.",
         answer="S23 reports navigating through date grouping after a related match; S31 reports later success with image descriptions; S35 reports a quoted file-type term; S68 reports retrieving desired keyword matches through Classic search. These are counterexamples to an unqualified 'Google Photos cannot do this' claim.",
         ids="S23 S31 S35 S68 S02 S04", lens=None,
         limit="A documented success with one item or route does not establish that the desired target is consistently retrieved for all users."),
    dict(id="Q8", title="What must still be validated before choosing an MVP?", short="We need to observe actual queries, confirm that the target exists, and measure the time from first clue to verified retrieval.",
         answer="The source cases cannot isolate an algorithmic issue from indexing, account/backup state, existing-feature discoverability or query choice. Observe 5–6 consented retrieval tasks and compare the first query, result interpretation, next action and target confirmation. Exclude missing-source-asset tasks when testing retrieval effectiveness.",
         ids="S18 S23 S30 S32 S47 S58", lens=None,
         limit="No production telemetry, target-level verified success rate, or controlled comparison is supplied in the research workbook."),
]
for q in QUESTIONS:
    q["ids"] = tuple(q["ids"].split())


def validate_mappings(case_ids: set[str]) -> None:
    """Fail closed if a curated case reference disappears from the published snapshot."""
    for dimension, groups in CASE_LENSES.items():
        for group, ids in groups.items():
            missing = set(ids) - case_ids
            if missing:
                raise ValueError(f"Missing {dimension}/{group} records: {sorted(missing)}")
    for question in QUESTIONS:
        missing = set(question["ids"]) - case_ids
        if missing:
            raise ValueError(f"Missing {question['id']} records: {sorted(missing)}")


def lens_counts(dimension: str, available_ids: set[str] | None = None) -> dict[str, int]:
    available_ids = available_ids or set(c for groups in CASE_LENSES.values() for ids in groups.values() for c in ids)
    return {label: len(set(ids) & available_ids) for label, ids in CASE_LENSES[dimension].items()}


def relevant_records(question: dict, frame):
    return frame[frame.case_id.isin(question["ids"])]
