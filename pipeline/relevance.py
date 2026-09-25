from __future__ import annotations
import re

# Kept so every snapshot exposes the prior deterministic prediction beside the
# focused Phase-2 audit result.
IRRELEVANT=re.compile(r'\b(subscription|billing|storage|backup failed|login|deleted|ads?)\b',re.I)
DIRECT=re.compile(r'\b(trying to find|cannot find|can.t find|couldn.t find|no amount of search|tried several|search.*(?:photo|picture|screenshot)|find.*(?:photo|picture|screenshot))\b',re.I)
RELATED=re.compile(r'\b(search|find|result|album|screenshot|filename|scroll)\b',re.I)

ATTEMPT=re.compile(r'\b(search(?:ed|ing)?|quer(?:y|ies)|typ(?:e|ed|ing)|try|tried|look(?:ed|ing)?|scroll(?:ed|ing)?|browse|filter|select(?:ed|ing)?|open(?:ed|ing)?|retriev(?:e|ed|ing))\b',re.I)
TARGET=re.compile(r'\b(photos?|pictures?|images?|videos?|screenshots?|albums?|files?|documents?|bills?|words?|text|filename|faces?|lens|shutter)\b',re.I)
RESULT=re.compile(r'\b(no result|nothing|not found|could not|cannot|can.t|couldn.t|no amount|returned|returning|pulling up|popping up|showing|broad|wrong|unrelated|tiny subset|empty|not (?:show|appear|surface|searchable)|neither searchable|no straightforward|did not retrieve|did not help)\b',re.I)
REFINEMENT=re.compile(r'\b(another|several|multiple|quote|quoting|month|year|date|within|only|scope|folder|album title|browser find|ctrl\+f|manually|workaround|instead)\b',re.I)
OUTCOME=re.compile(r'\b(worked|successful|success|solved|found|marked.*answer|expected results|reported.*work)\b',re.I)
FINALITY=re.compile(r'\b(no luck|no amount|did not help|worked|successful|success|solved|found|marked.*answer|expected results|reported.*work)\b',re.I)
CONTEXT=re.compile(r'\b(remembered|known|particular|exact|old|vintage|family|child|group|location|date|day|month|year|screen name|keyword|file name|metadata|exif)\b',re.I)
NON_RETRIEVAL=re.compile(r'\b(subscription|billing|ads?|login|delete(?:d|ion)?|storage(?: quota)?|crash(?:ed|ing)?|edit(?:ing)?|upload(?:ing)?)\b',re.I)
PRACTICE_ONLY=re.compile(r'\b(reported practices|rather than a failed episode)\b',re.I)

def _legacy(text:str)->tuple[str,str,float]:
    if DIRECT.search(text): return 'DIRECT','E2',.78
    if RELATED.search(text): return 'RELATED','E3',.62
    if IRRELEVANT.search(text): return 'IRRELEVANT','E4',.74
    return 'UNCERTAIN','E4',.45

def classify(text:str, legacy:bool=False)->tuple[str,str,float]:
    """Classify retrieval evidence; E1 requires a traceable multi-step episode."""
    if legacy:
        return _legacy(text)
    attempt=bool(ATTEMPT.search(text)); target=bool(TARGET.search(text)); result=bool(RESULT.search(text))
    refinement=bool(REFINEMENT.search(text)); outcome=bool(OUTCOME.search(text)); context=bool(CONTEXT.search(text))
    if PRACTICE_ONLY.search(text):
        return 'RELATED','E3',.72
    if attempt and target and result:
        if FINALITY.search(text):
            return 'DIRECT','E1',.90
        if context or refinement or outcome:
            return 'DIRECT','E2',.84
        return 'RELATED','E3',.66
    if target and result and (context or refinement or outcome):
        return 'DIRECT','E2',.78
    if target and (context or outcome or re.search(r'easier(?:ly)? to find|difficulty finding',text,re.I)):
        return 'RELATED','E3',.68
    if NON_RETRIEVAL.search(text):
        return 'IRRELEVANT','E4',.78
    if RELATED.search(text):
        return 'UNCERTAIN','E4',.48
    return 'UNCERTAIN','E4',.45
