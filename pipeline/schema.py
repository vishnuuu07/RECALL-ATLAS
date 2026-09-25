from __future__ import annotations
from pydantic import BaseModel, HttpUrl
from typing import Optional

class SourceRecord(BaseModel):
    record_id:str; source_platform:str; source_type:str; source_url:str; source_title:Optional[str]=None
    publication_date:Optional[str]=None; collected_at:str; original_text:str; public_excerpt:str
    language:Optional[str]=None; collection_query:str; collection_method:str; collection_batch:str
    parent_thread_id:Optional[str]=None; licensing_or_access_notes:Optional[str]=None

