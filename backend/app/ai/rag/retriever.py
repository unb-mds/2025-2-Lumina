from typing import List, ClassVar

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from app.services.search_service import SearchService


class NewsRetriever(BaseRetriever):
    """Custom retriever para buscar notícias semelhantes a um prompt."""

    Search_Manager: ClassVar[SearchService] = SearchService()
    search_k: int = 5  # quantidade de documentos retornados

    def _get_relevant_documents(self, query: str) -> List[Document]:
        """Busca notícias no vector store usando similaridade."""
        return self.Search_Manager.search(query, k=self.search_k)
