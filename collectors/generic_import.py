from __future__ import annotations
import json
from pathlib import Path
def load(path:Path)->list[dict]:
    return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]

