import logging
import uuid
from typing import List, Optional

import chromadb
from chromadb.types import Collection

from app.ai.ai_models.EmbeddingPlatform import EmbeddingPlatform
from app.ai.rag.text_splitter import TextSplitter
from app.models.article import Article

logger = logging.getLogger(__name__)


class VectorDB:
    """
    Gerencia a interação com o banco de dados vetorial (ChromaDB).

    Responsabilidades:
    1. Conectar-se ao ChromaDB.
    2. Vetorizar o conteúdo de um artigo usando um `EmbeddingPlatform`.
    3. Salvar os vetores e metadados no ChromaDB.
    """

    def __init__(self,embedding_platform: EmbeddingPlatform, text_splitter: TextSplitter, db_path: str = "app/db/chroma_db",collection_name: str = "lumina_articles",):
        """
        Inicializa o cliente do ChromaDB e a coleção de artigos.

        Args:
            embedding_platform (EmbeddingPlatform): A plataforma (ex: GoogleEmbedder)
                                                    usada para gerar os vetores.
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
            splitter (TextSplitter): A instância para dividir o conteúdo do artigo.

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
