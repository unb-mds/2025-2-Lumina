from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Article:
    title: str
    author: str
    url: str
    content: str
    id: Optional[int] = None
    crawled_at: Optional[datetime] = None
    vectorized_at: Optional[datetime] = None
    vector_db_id: Optional[str] = None
