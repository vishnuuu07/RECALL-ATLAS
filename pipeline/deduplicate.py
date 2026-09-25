from __future__ import annotations
def deduplicate(records:list[dict])->tuple[list[dict],int]:
    seen=set(); out=[]; removed=0
    for r in records:
        if r['content_hash'] in seen: removed+=1; continue
        seen.add(r['content_hash']); out.append(r)
    return out,removed

