from pydantic import BaseModel, HttpUrl, Field, ConfigDict
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
    
    # --- Campo Para o Admin Unificado ---
    source_db: Optional[str] = Field(default=None)    # Ex: "articles.db"
    source_label: Optional[str] = Field(default=None) # Ex: "G1"

    # Configuração para Pydantic V2
    model_config = ConfigDict(from_attributes=True)