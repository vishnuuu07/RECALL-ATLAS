"""Editorial layer grounded in the fixed 24-record source snapshot.

Statements below are *directions to investigate*, not product telemetry, proof
of causality, or independent verification. IDs are validated against SQLite.
"""
from __future__ import annotations

FINDINGS = [
    {
        'id': 'C1', 'chart_label': 'Collection context / scope', 'title': 'Remembering the collection does not always narrow the search',
        'short': 'Users describe a known album, group or period, yet report being unable to use that context to narrow the task.',
        'episode': 'One user wanted campfire photographs from a particular programme, not every campfire in the library.',
        'observed': 'A broad object search and extra descriptions reportedly did not isolate the intended group of images.',
        'mechanism': 'Possible mismatch between retained collection context and the available search scope; search mode and indexing remain unverified.',
        'qualification': 'Another user reported success by combining an album title with a term; browser Find also worked for an album-navigation task.',
        'question': 'When the person knows an album or event, what do they try first, and can they successfully constrain the retrieval space?',
        'ids': ['community-495705', 'community-78574873', 'community-128230954', 'community-162522212', 'reddit-1g5dmve', 'reddit-1aju75m'],
        'counter_ids': ['community-128230954', 'community-162522212'],
        'metric': 'Verified retrieval success and time to target in known-collection tasks.',
        'status': 'Directional / not validated',
    },
    {
        'id': 'C2', 'chart_label': 'Literal text vs semantic results', 'title': 'Remembered text can be interpreted as a broad semantic cue',
        'short': 'A remembered filename fragment or screenshot word does not necessarily behave like a literal text match.',
        'episode': 'A screenshot search for the word “dinner” initially returned thematically related screenshots rather than the intended text match.',
        'observed': 'The poster reported that quoting the text in a reformulated query worked; a filename query elsewhere returned date-level results.',
        'mechanism': 'A possible expectation gap between literal text/filename matching and semantic retrieval, not proof of a model defect.',
        'qualification': 'The successful quoted-text workaround shows that an existing capability may already address part of this need.',
        'question': 'When someone recalls exact text, do they expect literal matching, know about quoting, and find the correct result?',
        'ids': ['community-106429666', 'reddit-rd8u2q', 'reddit-1i06lg2', 'reddit-1iaob2b', 'reddit-1lklsk2'],
        'counter_ids': ['reddit-1i06lg2'],
        'metric': 'Verified screenshot/document retrieval; queries and refinements per successful target.',
        'status': 'Directional / not validated',
    },
    {
        'id': 'C3', 'chart_label': 'Candidate → nearby photos', 'title': 'A useful candidate may not end the retrieval journey',
        'short': 'Some users describe looking for neighbouring photos by day or rough period after an imperfect search.',
        'episode': 'A poster wanted to jump from a found candidate directly to the surrounding photos from the same day.',
        'observed': 'Another described estimating month and year, then manually browsing; no target success was independently verified.',
        'mechanism': 'Possible handoff friction between result inspection and contextual timeline browsing.',
        'qualification': 'Chronological browsing is an available workaround; the records do not show that a new day view would improve success.',
        'question': 'When someone sees a near match, what makes them think the target is nearby, and where do they navigate next?',
        'ids': ['reddit-1h09vho', 'reddit-1fmvxd6'],
        'counter_ids': ['reddit-1fmvxd6'],
        'metric': 'Time from first useful candidate to verified target; abandonment after a near miss.',
        'status': 'Emerging / not validated',
    },
    {
        'id': 'C4', 'chart_label': 'Sparse / irrelevant results', 'title': 'Reports of missing or irrelevant results need diagnosis',
        'short': 'Search complaints describe sparse, irrelevant or missing results, but the underlying failure cannot be identified from text alone.',
        'episode': 'A long-term dog-photo owner reported that an object search returned only a small subset of images.',
        'observed': 'Other participants reported different behaviour and raised backup/account state as possible explanations.',
        'mechanism': 'Potential index, account, availability, query-interpretation or relevance issue; cause unknown.',
        'qualification': 'These reports cannot establish that the target existed in the searched account or that the index failed.',
        'question': 'Can the participant verify the asset exists, show the account and interface state, and reproduce the mismatch?',
        'ids': ['reddit-1fa4fg1', 'reddit-1ov9y8d', 'reddit-193u8s0', 'reddit-1iaob2b', 'community-400823549'],
        'counter_ids': ['reddit-1ov9y8d', 'reddit-1i06lg2'],
        'metric': 'Confirmed asset presence and verified success after a diagnostic step.',
        'status': 'Needs diagnosis / not validated',
    },
]

# Research questions use intentionally narrow evidence mappings. Missing information
# is shown as a gap, not automatically attributed to every relevant record.
QUESTIONS = [
    ('Memory', 'What kinds of old photos and visual assets do users struggle to retrieve?', 'The sample contains ordinary photos, album-contained images and screenshot/document searches; it does not establish population frequencies.', ['community-495705','reddit-1aju75m','reddit-1iaob2b','reddit-193u8s0']),
    ('Memory', 'What information do users actually remember?', 'Some explicitly recall an album, a group/programme, an approximate period, a filename or on-screen text.', ['reddit-1aju75m','community-78574873','reddit-1fmvxd6','reddit-1i06lg2']),
    ('Memory', 'What information have they forgotten?', 'The corpus does not consistently record forgotten clues; ask this directly during observed retrieval tasks.', []),
    ('Query', 'How do users formulate an initial search with incomplete memory?', 'Cases mention an object, filename, album title, approximate time or screenshot text, but exact initial query strings are often missing.', ['reddit-rd8u2q','reddit-1fmvxd6','community-78574873','reddit-1i06lg2']),
    ('Query', 'Which remembered clues are omitted from the initial query?', 'The records generally do not establish all remembered clues before searching, so omissions cannot be reliably measured.', []),
    ('Memory', 'Do memory types lead to different retrieval behaviour?', 'The corpus contains different approaches but is too small and self-selected for a comparative behaviour claim.', ['reddit-1fmvxd6','reddit-1g5dmve','reddit-1i06lg2']),
    ('Journey', 'Where does the retrieval journey break down?', 'Observed reports include broad candidates, failure to scope to a collection, and difficulty moving from a result to surrounding images.', ['reddit-rd8u2q','reddit-1g5dmve','reddit-1h09vho']),
    ('Journey', 'What happens after the first unsuccessful attempt?', 'Some users describe manual timeline browsing, additional query variants, or category/album workarounds; outcomes are mostly not stated.', ['reddit-1fmvxd6','reddit-rd8u2q','community-162522212']),
    ('Query', 'How do users refine or reformulate searches?', 'One screenshot-text poster reports a successful quoted-text refinement; others describe multiple unsuccessful variants.', ['reddit-1i06lg2','reddit-rd8u2q','reddit-1jbiao1']),
    ('Query', 'Which refinements help, fail or loop?', 'The reported quoted-text and browser-Find workarounds succeeded locally; repeated search variants elsewhere did not. This is not controlled comparison.', ['reddit-1i06lg2','community-162522212','reddit-rd8u2q']),
    ('Journey', 'Why do users fail when candidate results appear?', 'Candidate recognition itself is not established. Some records describe broad results or a desire to navigate to nearby photos.', ['reddit-rd8u2q','reddit-1h09vho']),
    ('Journey', 'What enables confirmation of the correct photo?', 'Independently verified target recognition is not measured in public posts.', []),
    ('Workarounds', 'What external workarounds do users employ?', 'Reported alternatives include browser Find, album-title-plus-term search, timeline browsing and metadata/folder filters.', ['community-162522212','community-128230954','reddit-1fmvxd6','pixls-39727']),
    ('Workarounds', 'What do successful workarounds reveal?', 'Quoted text, browser Find and correcting folder scope suggest opportunities to examine discoverability and scope, not new-capability absence.', ['reddit-1i06lg2','community-162522212','pixls-39727']),
    ('Opportunity', 'Which mechanisms recur across independent sources?', 'Known collection/scope and text-query issues appear in more than one source; records remain purposively sampled.', ['community-495705','reddit-1g5dmve','community-106429666','reddit-1i06lg2']),
    ('Opportunity', 'Which findings could reflect source-selection bias?', 'Search terms and source accessibility purposively enriched the dataset for retrieval complaints; rates are not representative.', ['community-495705','reddit-1g5dmve']),
    ('Opportunity', 'Which existing capabilities address observed problems?', 'Public posts mention quoted text, browser Find, album-title-plus-term and category navigation; confirm current official availability by platform.', ['reddit-1i06lg2','community-128230954','community-162522212']),
    ('Opportunity', 'Which gaps might remain despite those capabilities?', 'Some posters still report a burden applying collection context or interpreting literal versus semantic matches; reproduce before claiming a product gap.', ['reddit-1aju75m','community-78574873','community-106429666']),
    ('Opportunity', 'Which findings are contradicted?', 'Success reports for quoted text and album navigation qualify claims that no workable retrieval paths exist.', ['reddit-1i06lg2','community-128230954','community-162522212']),
    ('Opportunity', 'What can public feedback not establish?', 'Root cause, prevalence, asset presence, actual candidate sets and independently verified success require primary research.', []),
    ('Opportunity', 'Which opportunities might improve verified retrieval?', 'Collection-scoped discovery, literal-text expectations and candidate-to-context navigation are hypotheses to evaluate with observed tasks.', ['reddit-1aju75m','reddit-1i06lg2','reddit-1h09vho']),
    ('Opportunity', 'Which problems are feasible to reproduce in an MVP?', 'Constrained collection lookup and screenshot-text tasks can be prototyped with consented/representative assets; user validation is pending.', ['community-495705','reddit-1i06lg2']),
]


# Source-reported outcomes are described independently from coarse automated labels.
# Do not interpret a successful workaround as independently verified target retrieval.
OUTCOME_NOTES = {
    'reddit-rd8u2q': 'Reported failure to find target through filename-query variants; final retrieval not verified.',
    'reddit-1jbiao1': 'Reported unsuccessful search using multiple parameters; no observed target verification.',
    'reddit-1aju75m': 'Reported that added descriptions did not isolate desired pictures; final retrieval not established.',
    'community-162522212': 'Poster reported browser Find worked for locating an album; target-photo retrieval not established.',
    'reddit-1i06lg2': 'Poster reported quoted screenshot-text refinement worked; no independently observed task.',
    'pixls-39727': 'Poster reported that correcting folder scope gave expected results in another photo-management product.',
    'community-128230954': 'Poster marked album-title-plus-term suggestion as an answer; independent task verification unavailable.',
}


def evidence_for(finding: dict, records):
    """Return only IDs actually available in current snapshot."""
    return records[records.record_id.isin(finding['ids'])]


def validate_editorial_ids(records) -> list[str]:
    ids = set(records.record_id)
    used = {i for f in FINDINGS for i in f['ids'] + f['counter_ids']}
    used |= {i for _, _, _, refs in QUESTIONS for i in refs}
    return sorted(used - ids)
