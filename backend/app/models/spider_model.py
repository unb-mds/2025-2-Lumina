from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class Spider(ABC):
    """
    Classe base abstrata para todos os "Spiders" (localizadores de links).
    Define a interface que todos devem implementar.
    """
    
    links = []
    
    @abstractmethod
    def find_links(self) -> list[str]:
        """
        Método principal de busca de links.

        Deve visitar uma página (ex: homepage de um jornal)
        e retornar uma LISTA de URLs (strings) para
        os artigos completos.
        """
        pass
