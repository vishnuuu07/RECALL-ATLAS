from __future__ import annotations
import hashlib, re, unicodedata
def clean(text:str)->str: return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',text or '')).strip()
def content_hash(text:str)->str: return hashlib.sha256(clean(text).lower().encode()).hexdigest()

