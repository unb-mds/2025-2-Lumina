from abc import ABC, abstractmethod
from typing import List


class EmbeddingPlatform(ABC):
    """
    Interface abstrata para plataformas de embedding.

    Define os métodos que qualquer implementação de cliente de embedding
    (como Google, OpenAI, etc.) deve fornecer.
    """

    @abstractmethod
    def embed_document(self, text: str) -> List[float]:
        """
        Gera o vetor de embedding para um único texto.

        Args:
            text (str): O texto a ser vetorizado.

        Returns:
            List[float]: O vetor de embedding.
        """
        pass

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Gera os vetores de embedding para uma lista de textos.

        Args:
            texts (List[str]): A lista de textos a ser vetorizada.

        Returns:
            List[List[float]]: Uma lista de vetores de embedding.
        """
        pass
