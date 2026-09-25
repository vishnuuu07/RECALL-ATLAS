from __future__ import annotations
import hashlib, json, urllib.request
from datetime import datetime, timezone

APP_ID='962194608'
def collect(page:int=1)->list[dict]:
    url=f'https://itunes.apple.com/rss/customerreviews/id={APP_ID}/sortBy=mostRecent/page={page}/json'
    with urllib.request.urlopen(url,timeout=30) as response: payload=json.load(response)
    out=[]
    for entry in payload.get('feed',{}).get('entry',[]):
        text=entry.get('content',{}).get('label','').strip()
        if not text: continue
        rid='apple-'+hashlib.sha256((entry['id']['label']).encode()).hexdigest()[:16]
        out.append({'record_id':rid,'source_platform':'Apple App Store','source_type':'app_review','source_url':f'https://apps.apple.com/app/id{APP_ID}','source_title':entry.get('title',{}).get('label'), 'publication_date':entry.get('updated',{}).get('label'), 'collected_at':datetime.now(timezone.utc).isoformat(), 'original_text':text,'public_excerpt':text[:480], 'language':'unknown','collection_query':'Google Photos App Store latest reviews','collection_method':'Apple public customer-review RSS feed','collection_batch':f'appstore-page-{page}','parent_thread_id':None,'licensing_or_access_notes':'Public App Store review; publish only truncated excerpt; no author retained.'})
    return out
