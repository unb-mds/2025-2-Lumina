import logging
from typing import List

from google.api_core.exceptions import ResourceExhausted
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.ai.ai_models.EmbeddingPlatform import EmbeddingPlatform

logger = logging.getLogger(__name__)


class GoogleEmbedder(EmbeddingPlatform):
    """
    Implementação concreta do EmbeddingPlatform usando os modelos
    de embedding do Google (via LangChain).
    """

    def __init__(self, api_key: str, model_name: str = "models/gemini-embedding-001"):
        """
        Inicializa o cliente de embedding do Google.
        """
        self.api_key = api_key
        self.model_name = model_name
        try:
            self.client = GoogleGenerativeAIEmbeddings(
                model=self.model_name, google_api_key=self.api_key
            )
            logger.info(f"GoogleEmbedder inicializado com o modelo: {self.model_name}")
        except Exception as e:
            logger.error(f"Falha ao inicializar o GoogleGenerativeAIEmbeddings: {e}")
            raise

    def embed_document(self, text: str) -> List[float]:
        """
        Gera o vetor de embedding para um único texto.
        """
        try:
            return self.client.embed_query(text)
        except Exception as e:
            # Inspeciona a mensagem da exceção para identificar o erro de rate limit
            if "429" in str(e):
                # Converte o erro genérico em um erro específico para o VectorDB tratar
                raise ResourceExhausted(f"Rate limit da API atingido: {e}") from e
            else:
                logger.error(f"Erro ao vetorizar documento (embed_query): {e}")
                return []

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Gera os vetores de embedding para uma lista de textos.
        """
        if not texts:
            return []

        try:
            return self.client.embed_documents(texts)
        except Exception as e:
            # Inspeciona a mensagem da exceção para identificar o erro de rate limit
            if "429" in str(e):
                # Converte o erro genérico em um erro específico para o VectorDB tratar
                raise ResourceExhausted(f"Rate limit da API atingido: {e}") from e
            else:
                logger.error(f"Erro ao vetorizar documentos (embed_documents): {e}")
                return []
