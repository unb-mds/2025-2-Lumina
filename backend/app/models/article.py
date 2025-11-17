from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import Optional

class Article(BaseModel):
    """
    Modelo Pydantic que representa um Artigo.
    Substitui o @dataclass para integração nativa com o FastAPI.
    """
    
    # Campos obrigatórios que vêm do Scraper
    title: str
    author: str
    url: HttpUrl  # <-- Validação automática de URL
    content: str
    
    # Campos opcionais/gerenciados pelo banco de dados
    id: Optional[int] = Field(default=None)
    saved_at: Optional[datetime] = Field(default=None)
    vectorized_at: Optional[datetime] = Field(default=None)
    vector_db_id: Optional[str] = Field(default=None)
    
    class Config:
        # Permite que o Pydantic funcione bem com objetos de banco de dados
        orm_mode = True