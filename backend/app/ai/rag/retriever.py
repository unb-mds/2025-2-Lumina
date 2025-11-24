import asyncio
from typing import List


from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from pydantic import Field

from app.services.search_service import SearchService

class NewsRetriever(BaseRetriever):
    """Custom retriever para buscar notícias semelhantes a um prompt."""

    Search_Manager = SearchService()
    search_k: int = 10  # quantidade de documentos retornados

    class Config:
        arbitrary_types_allowed = True

    def _get_relevant_documents(self, query: str) -> List[Document]:
        """Busca notícias no vector store usando similaridade."""
        return self.Search_Manager.search(query, k=self.search_k)
