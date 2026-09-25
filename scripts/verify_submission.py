"""Submission gates for the fixed public Recall Atlas snapshot."""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "public" / "recall_atlas_public.sqlite"
MANIFEST = ROOT / "data" / "manifests" / "public_snapshot_manifest.json"
HANDOFF = ROOT / "RESEARCH_TO_SOLUTION_HANDOFF.md"
EXPECTED = {"raw_record_count": 24, "unique_record_count": 24, "public_record_count": 24}
SENSITIVE = re.compile(r"(?i)(api[_-]?key|secret|bearer\s+|password\s*[:=]|ghp_[A-Za-z0-9]|xox[baprs]-|AKIA[0-9A-Z]{16})")


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for key, expected in EXPECTED.items():
        if manifest.get(key) != expected:
            raise SystemExit(f"{key} is {manifest.get(key)!r}, expected fixed snapshot value {expected}")
    digest = hashlib.sha256(DB.read_bytes()).hexdigest()
    if digest != manifest.get("snapshot_sha256"):
        raise SystemExit("SQLite digest does not match the public snapshot manifest")

    con = sqlite3.connect(DB)
    evidence = con.execute("SELECT * FROM evidence").fetchall()
    columns = [row[1] for row in con.execute("PRAGMA table_info(evidence)")]
    if len(evidence) != EXPECTED["public_record_count"]:
        raise SystemExit("Dashboard evidence table does not match manifest public_record_count")
    prohibited_columns = {"author", "author_name", "email", "username", "credential", "token", "password"}
    if prohibited_columns.intersection(columns):
        raise SystemExit("Public evidence table contains a prohibited personal-data or credential column")
    for row in evidence:
        for value in row:
            if isinstance(value, str) and SENSITIVE.search(value):
                raise SystemExit("Potential credential material found in public SQLite data")

    ids = {row[0] for row in con.execute("SELECT record_id FROM evidence")}
    for table, field in (("themes", "record_ids"), ("hypotheses", "supporting_ids")):
        for (value,) in con.execute(f"SELECT {field} FROM {table}"):
            missing = set(filter(None, str(value).split("|"))) - ids
            if missing:
                raise SystemExit(f"{table}.{field} references missing evidence IDs: {sorted(missing)}")
    handoff_ids = set(re.findall(r"`([A-Za-z0-9_-]+)`", HANDOFF.read_text(encoding="utf-8"))) & ids
    if len(handoff_ids) < 10:
        raise SystemExit("Research handoff does not contain the expected supporting evidence references")
    print(f"submission gates passed: {len(evidence)} records, {len(handoff_ids)} handoff evidence IDs, no credential patterns")


if __name__ == "__main__":
    main()
