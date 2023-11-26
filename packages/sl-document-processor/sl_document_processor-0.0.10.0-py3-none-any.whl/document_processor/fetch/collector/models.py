from typing import List, Optional

from pydantic import BaseModel


class URLmetadata(BaseModel):
    url: str
    document_URL: str
    title: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[str] = None


class URLConfig(BaseModel):
    url: str
    max_depth: int = 1
    file_extensions: List[str] = [".pdf"]
    process_static_pages: bool = False
