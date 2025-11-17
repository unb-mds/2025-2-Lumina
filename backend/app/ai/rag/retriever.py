import asyncio
from typing import List

from langchain.schema import Document
from langchain.schema.retriever import BaseRetriever
from pydantic import Field

from backend.app.db.vectordb import VectorDB


class NewsRetriever(BaseRetriever):
    """Custom retriever para buscar notícias semelhantes a um prompt."""

    vectordb: VectorDB = Field(...)
    search_k: int = 5  # quantidade de documentos retornados

    class Config:
        arbitrary_types_allowed = True

    def _get_relevant_documents(self, query: str) -> List[Document]:
        """Busca notícias no vector store usando similaridade."""
        return self.vectordb.search(query, k=self.search_k)
