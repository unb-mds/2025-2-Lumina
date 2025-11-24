import logging
import os
from typing import List

import chromadb
from chromadb.types import Collection
from dotenv import load_dotenv
from langchain_core.documents import Document

from app.ai.rag.google_embedder import GoogleEmbedder
from app.models.article import Article

logger = logging.getLogger(__name__)

load_dotenv()


class SearchService:
    def __init__(self):
        # Carrega a chave de API do Google
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("A variável de ambiente GOOGLE_API_KEY não foi definida.")

        # Inicializa a plataforma de embedding com o Google
        self.embedding_platform = GoogleEmbedder(api_key=api_key)

        # Configura o cliente do banco de dados vetorial
        db_path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "db", "chroma_db")
        collection_name: str = "lumina_articles"
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection: Collection = self.client.get_or_create_collection(
            name=collection_name
        )

        logger.info(
            f"Cliente ChromaDB conectado em '{db_path}' e coleção '{collection_name}' pronta."
        )
        
    def search(self, query: str, k: int = 10) -> List[Document]:
        """
        Busca por documentos similares a uma query no ChromaDB.

        Args:
            query (str): O texto da busca.
            k (int): O número de documentos a serem retornados.

        Returns:
            List[Document]: Uma lista de documentos LangChain.
        """
        # 1. Vetoriza a query de busca
        query_embedding = self.embedding_platform.embed_document(query)
        if not query_embedding:
            logger.warning(f"Não foi possível gerar embedding para a query: '{query}'")
            return []

        # 2. Executa a busca na coleção do ChromaDB
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k,
            )
        except Exception as e:
            logger.error(f"Falha ao executar a busca no ChromaDB: {e}")
            return []

        # 3. Converte os resultados para o formato de Documento LangChain
        documents = []
        if results and results["documents"]:
            for doc_content, metadata in zip(results["documents"][0], results["metadatas"][0]):
                documents.append(Document(page_content=doc_content, metadata=metadata))

        return documents