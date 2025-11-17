import logging
from typing import List

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from backend.app.ai.ai_models.EmbeddingPlatform import EmbeddingPlatform

logger = logging.getLogger(__name__)


class GoogleEmbedder(EmbeddingPlatform):
    """
    Implementação concreta do EmbeddingPlatform usando os modelos
    de embedding do Google (via LangChain).

    """

    def __init__(self, api_key: str, model_name: str = "models/gemini-embedding-001"):
        """
        Inicializa o cliente de embedding do Google.

        Args:
            api_key (str): A chave de API do Google AI Studio.
            model_name (str, optional): O nome do modelo de embedding a ser usado.
        """
        self.api_key = api_key
        self.model_name = model_name
        try:
            # Inicializa o cliente do LangChain
            self.client = GoogleGenerativeAIEmbeddings(
                model=self.model_name, google_api_key=self.api_key
            )
            logger.info(f"GoogleEmbedder inicializado com o modelo: {self.model_name}")
        except Exception as e:
            logger.error(f"Falha ao inicializar o GoogleGenerativeAIEmbeddings: {e}")
            # Propaga o erro para falhar rapidamente se a chave for inválida
            raise

    def embed_document(self, text: str) -> List[float]:
        """
        Gera o vetor de embedding para um único texto.
        """
        try:
            return self.client.embed_query(text)
        except Exception as e:
            logger.error(f"Erro ao vetorizar documento (embed_query): {e}")
            # Retorna lista vazia em caso de falha na vetorização
            return []

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Gera os vetores de embedding para uma lista de textos.
        """
        if not texts:
            # Evita chamar a API com uma lista vazia
            return []

        try:
            return self.client.embed_documents(texts)
        except Exception as e:
            logger.error(f"Erro ao vetorizar documentos (embed_documents): {e}")
            # Retorna lista vazia em caso de falha na vetorização
            return []
