import logging
import uuid
from typing import List, Optional

import chromadb
from chromadb.types import Collection
from langchain.schema import Document

from backend.app.ai.ai_models.EmbeddingPlatform import EmbeddingPlatform
from backend.app.ai.rag.text_splitter import TextSplitter
from backend.app.models.article import Article

logger = logging.getLogger(__name__)


class VectorDB:
    """
    Gerencia a interação com o banco de dados vetorial (ChromaDB).

    Responsabilidades:
    1. Conectar-se ao ChromaDB.
    2. Vetorizar o conteúdo de um artigo usando um `EmbeddingPlatform`.
    3. Salvar os vetores e metadados no ChromaDB.
    4. Buscar artigos por similaridade.
    """

    def __init__(
        self,
        embedding_platform: EmbeddingPlatform,
        text_splitter: TextSplitter,
        db_path: str = "app/db/chroma_db",
        collection_name: str = "lumina_articles",
    ):
        """
        Inicializa o cliente do ChromaDB e a coleção de artigos.

        Args:
            embedding_platform (EmbeddingPlatform): A plataforma (ex: GoogleEmbedder)
                                                    usada para gerar os vetores.
            text_splitter (TextSplitter): A instância para dividir o conteúdo do artigo.
            db_path (str): O caminho no sistema de arquivos para persistir o
                           banco de dados vetorial.
            collection_name (str): O nome da coleção onde os vetores dos
                                   artigos serão armazenados.
        """
        self.embedding_platform = embedding_platform
        self.splitter = text_splitter
        try:
            # 1. Inicializa o cliente ChromaDB com persistência
            self.client = chromadb.PersistentClient(path=db_path)

            # 2. Obtém ou cria a coleção. Não passamos o embedding_function aqui,
            #    pois vamos gerar os embeddings manualmente antes de adicionar.
            self.collection: Collection = self.client.get_or_create_collection(
                name=collection_name,
            )
            logger.info(
                f"Cliente ChromaDB conectado em '{db_path}' e coleção "
                f"'{collection_name}' pronta."
            )
        except Exception as e:
            logger.error(f"Falha ao inicializar o ChromaDB: {e}")
            raise

    def vectorize_article(self, article: Article) -> Optional[str]:
        """
        Processa um artigo: divide em chunks, vetoriza e salva no ChromaDB.

        Args:
            article (Article): O artigo a ser processado.

        Returns:
            Optional[str]: O ID do lote (batch ID) que agrupa todos os chunks
                           deste artigo no banco vetorial, ou None se a
                           vetorização falhar.
        """
        if not article.id:
            logger.error("Artigo sem ID não pode ser vetorizado.")
            raise ValueError("Artigo precisa de um ID para ser vetorizado.")

        # 1. Divide o artigo em chunks de texto com metadados
        chunks = self.splitter.split_article(article)
        if not chunks:
            logger.warning(
                f"Nenhum chunk gerado para o artigo ID {article.id}. "
                "Vetorização abortada."
            )
            return None

        # 2. Extrai o conteúdo e os metadados para o formato do ChromaDB
        documents = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]

        # 3. Gera os embeddings para os documentos
        embeddings = self.embedding_platform.embed_documents(documents)
        if not embeddings or len(embeddings) != len(documents):
            logger.error(
                f"Falha ao gerar embeddings para o artigo ID {article.id}. "
                "Vetorização abortada."
            )
            return None

        # 4. Gera IDs únicos para cada chunk, vinculados ao ID do artigo
        # Ex: "123_0", "123_1", "123_2", ...
        ids = [f"{article.id}_{i}" for i in range(len(chunks))]

        try:
            # 5. Adiciona os chunks (documentos, metadados, ids, embeddings) à coleção
            self.collection.add(
                documents=documents, metadatas=metadatas, ids=ids, embeddings=embeddings
            )

            # 6. Gera um ID único para o lote (batch) de chunks adicionados
            batch_id = str(uuid.uuid4())
            logger.info(
                f"Artigo ID {article.id} vetorizado e salvo no ChromaDB com "
                f"{len(ids)} chunks. Batch ID: {batch_id}"
            )
            return batch_id
        except Exception as e:
            logger.error(
                f"Falha ao salvar chunks do artigo ID {article.id} no ChromaDB: {e}"
            )
            return None

    def search(self, query: str, k: int = 5) -> List[Document]:
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

    def delete_article_by_url(self, url: str) -> int:
        """
        Deleta todos os chunks de um artigo do ChromaDB com base na URL.

        Args:
            url (str): A URL do artigo a ser deletado.

        Returns:
            int: O número de documentos deletados.
        """
        try:
            # O ChromaDB permite deletar por filtro de metadados
            # A URL é armazenada como metadado 'url'
            deleted_ids = self.collection.delete(where={"url": url})
            num_deleted = len(deleted_ids)
            logger.info(
                f"Deletados {num_deleted} chunks associados à URL '{url}' do ChromaDB."
            )
            return num_deleted
        except Exception as e:
            logger.error(f"Falha ao deletar chunks para a URL '{url}' do ChromaDB: {e}")
            return 0
