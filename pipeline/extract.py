from __future__ import annotations
import re
THEMES={
'context-to-query gap':r'contextual|programme|event|particular|group|album',
'result relevance or recall':r'unrelated|tiny subset|nothing to do|broad|wrong|not.*result',
'candidate-to-timeline navigation':r'view day|surrounding|that day|manually look|month.*year',
'scope or filter constraint':r'within.*album|album.*search|filename|exact',
'screenshot or document retrieval':r'screenshot|bill|document|OCR',
'feature discoverability':r'folder|explore.tab|setting|backup',
'query reformulation loop':r'several.*query|multiple.*parameter|no amount|tried'
}
def first(pattern,text):
    m=re.search(pattern,text,re.I); return m.group(0) if m else None
def enrich(text:str)->dict:
    lower=text.lower(); themes=[k for k,p in THEMES.items() if re.search(p,lower,re.I)] or ['unclassified retrieval signal']
    memory='Textual/OCR' if any(x in lower for x in ['filename','text','bill','document','screenshot']) else ('Temporal' if any(x in lower for x in ['date','month','year','day']) else ('Relational/contextual' if any(x in lower for x in ['album','group','programme','event']) else ('Visual/object' if any(x in lower for x in ['dog','bike','object','campfire','poodle']) else 'Unknown')))
    asset='Screenshot/document' if any(x in lower for x in ['screenshot','bill','document']) else ('Album photo' if 'album' in lower else 'Photo')
    failure='Candidate evaluation' if any(x in lower for x in ['unrelated','broad','tiny subset','all photos']) else ('Result generation' if any(x in lower for x in ['does not appear','not popping','not found']) else ('Constructing query' if any(x in lower for x in ['filename','query','parameter','search term']) else ('Refinement/navigation' if any(x in lower for x in ['manually','view day','month and year','scroll']) else 'Unknown')))
    workaround='Date/timeline browsing' if any(x in lower for x in ['month','year','day','manually']) else ('Folder/category navigation' if 'folder' in lower else ('Repeated reformulation' if any(x in lower for x in ['several','multiple','no amount']) else 'Unknown'))
    outcome='Unresolved' if any(x in lower for x in ['cannot','couldn','not found','no amount','not popping']) else 'Unknown'
    observed='A retrieval attempt or search constraint is stated in the public record.'
    inferred=('The observed issue may reflect '+themes[0]+'.')
    unknowns='Whether the intended asset existed in the searched library, exact interface state, and final success are not established unless stated.'
    return dict(themes='|'.join(themes),memory_type=memory,asset_type=asset,failure_stage=failure,workaround=workaround,outcome=outcome,observed=observed,inferred=inferred,unknowns=unknowns)

