"""Deterministic import of the checked-in Retrieval Cases research workbook.

The workbook is retained unchanged in ``data/raw`` as the provenance artifact.
This module derives public-safe case tables from it: the public snapshot never
contains URLs, platform names, account handles, or clickable source references.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re

import pandas as pd


WORKBOOK_NAME = "Recall_Atlas_Evidence_Tracked_Research.xlsx"

# These are source-discussion overlaps that were reviewed at episode level.
# S10 is deliberately not an episode duplicate: it is a separate account in
# the same discussion as a legacy case.
EPISODE_DUPLICATES = {
    "S02": "C08",
    "S04": "C20",
    "S11": "C18",
    "S16": "C07",
}
DISCUSSION_OVERLAPS = {
    "S02": "Same retrieval episode",
    "S04": "Same retrieval episode",
    "S10": "Same discussion; distinct retrieval episode",
    "S11": "Same retrieval episode",
    "S16": "Same retrieval episode",
}


def _clean(value: object, fallback: str = "Not established") -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return fallback
    value = re.sub(r"\s+", " ", str(value)).strip()
    return fallback if not value or value.lower() == "nan" else value


def _sheet(path: Path, name: str) -> pd.DataFrame:
    """Read the workbook's tabular sheets without altering their values."""
    frame = pd.read_excel(path, sheet_name=name, header=3, dtype=object)
    return frame.dropna(how="all").copy()


def _failure_stage(results: str, outcome: str) -> str:
    text = f"{results} {outcome}".lower()
    if "irrelevant" in text or "semantic" in text:
        return "Results mismatch"
    if "partial" in text or "adjacent" in text or "wider set" in text:
        return "Candidate-to-timeline navigation"
    if "absent" in text or "not visible" in text or "availability" in text:
        return "Asset availability diagnosis"
    if "unresolved" in text or "not recovered" in text or "incomplete" in text:
        return "Outcome unresolved"
    if "found" in text or "successful" in text:
        return "Retrieval completed"
    return "Not established"


def _search_behaviour(action: str) -> str:
    text = action.lower()
    if "scroll" in text or "chronolog" in text or "timeline" in text:
        return "Timeline browsing"
    if "community" in text or "ask" in text:
        return "Help-seeking / capability question"
    if "category" in text or "recently" in text:
        return "Category or recency navigation"
    if "search" in text or "query" in text or "keyword" in text or "term" in text:
        return "Keyword or descriptive search"
    return "Search or navigation action"


def _imported_cases(path: Path) -> pd.DataFrame:
    source = _sheet(path, "Source Cases").set_index("Case ID")
    coding = _sheet(path, "Episode Coding").set_index("Case ID")
    audit = _sheet(path, "Evidence Audit").set_index("Case ID")
    rows: list[dict] = []
    for case_id in coding.index:
        code, src, review = coding.loc[case_id], source.loc[case_id], audit.loc[case_id]
        results = _clean(code["Reported results"])
        outcome = _clean(code["Reported outcome"])
        rows.append({
            "case_id": case_id,
            "case_type": "Retrieval Case",
            "episode_descriptor": _clean(code["Episode descriptor"]),
            "original_account": _clean(src["Source-account summary"]),
            "retrieval_goal": _clean(code["Retrieval goal"]),
            "remembered_clues": _clean(code["Remembered clues"]),
            "forgotten_clues": _clean(code["Forgotten clues"]),
            "initial_search_behaviour": _search_behaviour(_clean(code["Initial action"])),
            "initial_action": _clean(code["Initial action"]),
            "reported_results": results,
            "query_reformulation": _clean(code["Refinement"]),
            "workarounds": _clean(code["Workaround"]),
            "recorded_outcome": outcome,
            "outcome_classification": _clean(code["Outcome code"]),
            "evidence_classification": _clean(src["Research relevance"]),
            "evidence_type": _clean(src["Evidence type"]),
            "research_interpretation": _clean(src["Open validation question"]),
            "failure_stage": _failure_stage(results, outcome),
            "record_kind": "Imported workbook case",
            "canonical_case_id": EPISODE_DUPLICATES.get(case_id, case_id),
        })
    return pd.DataFrame(rows)


def _legacy_cases(evidence: pd.DataFrame) -> pd.DataFrame:
    """Create a neutral public case view for the existing fixed corpus."""
    rows: list[dict] = []
    for index, (_, row) in enumerate(evidence.reset_index(drop=True).iterrows(), 1):
        case_id = f"C{index:02d}"
        rows.append({
            "case_id": case_id,
            "case_type": "Retrieval Case",
            "episode_descriptor": f"Consolidated retrieval case {case_id}",
            "original_account": _clean(row.get("public_excerpt")),
            "retrieval_goal": _clean(row.get("source_title"), "Retrieval goal not established"),
            "remembered_clues": _clean(row.get("memory_type")),
            "forgotten_clues": "Not established by this record",
            "initial_search_behaviour": "Recorded search or navigation",
            "initial_action": "Not separately recorded",
            "reported_results": _clean(row.get("public_excerpt")),
            "query_reformulation": "Not separately recorded",
            "workarounds": _clean(row.get("workaround")),
            "recorded_outcome": _clean(row.get("outcome")),
            "outcome_classification": "Legacy coded outcome",
            "evidence_classification": _clean(row.get("relevance")),
            "evidence_type": "Recorded account",
            "research_interpretation": "Legacy corpus record retained for consolidated analysis.",
            "failure_stage": _clean(row.get("failure_stage")),
            "record_kind": "Existing corpus case",
            "canonical_case_id": case_id,
        })
    return pd.DataFrame(rows)


def import_workbook(evidence: pd.DataFrame, raw_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    """Return imported cases, de-duplicated consolidated cases, overlap audit and metadata."""
    path = raw_dir / WORKBOOK_NAME
    if not path.exists():
        raise FileNotFoundError(f"Required research workbook missing: {path}")
    imported = _imported_cases(path)
    legacy = _legacy_cases(evidence)
    consolidated = pd.concat(
        [legacy, imported[~imported.case_id.isin(EPISODE_DUPLICATES)]], ignore_index=True
    )
    audit = pd.DataFrame([
        {"imported_case_id": key, "legacy_case_id": EPISODE_DUPLICATES.get(key, "Not merged"), "overlap_assessment": value,
         "counted_in_consolidated_cases": "No" if key in EPISODE_DUPLICATES else "Yes"}
        for key, value in DISCUSSION_OVERLAPS.items()
    ])
    raw_tabs = pd.ExcelFile(path).sheet_names
    metadata = {
        "workbook_name": WORKBOOK_NAME,
        "workbook_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "workbook_sheet_names": raw_tabs,
        "imported_retrieval_case_count": len(imported),
        "same_discussion_overlap_count": len(DISCUSSION_OVERLAPS),
        "duplicate_episode_count": len(EPISODE_DUPLICATES),
        "distinct_same_discussion_case_count": 1,
        "consolidated_retrieval_case_count": len(consolidated),
    }
    return imported, consolidated, audit, metadata


def overlap_report(audit: pd.DataFrame, metadata: dict) -> str:
    rows = [
        "# Retrieval-case overlap report",
        "",
        f"- Imported workbook cases: {metadata['imported_retrieval_case_count']}",
        "- Existing corpus cases: 24",
        f"- Same-discussion overlaps reviewed: {metadata['same_discussion_overlap_count']}",
        f"- Duplicate retrieval episodes merged: {metadata['duplicate_episode_count']}",
        f"- Consolidated retrieval cases: {metadata['consolidated_retrieval_case_count']}",
        "",
        "The report intentionally omits URLs and platform names. Case S10 shares a discussion with a legacy record but is a distinct account and retrieval episode, so it remains counted.",
        "",
        "| Imported case | Consolidated case | Assessment | Counted |",
        "| --- | --- | --- | --- |",
    ]
    rows += [f"| {r.imported_case_id} | {r.legacy_case_id} | {r.overlap_assessment} | {r.counted_in_consolidated_cases} |" for r in audit.itertuples()]
    return "\n".join(rows) + "\n"
