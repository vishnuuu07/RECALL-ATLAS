from __future__ import annotations
def validate(records:list[dict])->list[str]:
    errors=[]; ids=[r['record_id'] for r in records]
    if len(ids)!=len(set(ids)):errors.append('record IDs are not unique')
    for r in records:
        if not r.get('source_url','').startswith('http'):errors.append(f"invalid source URL: {r['record_id']}")
        if not r.get('public_excerpt'):errors.append(f"missing excerpt: {r['record_id']}")
    return errors

