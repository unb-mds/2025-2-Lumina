import logging
from abc import ABC, abstractmethod
from typing import Set

from bs4 import BeautifulSoup

# Configuração do logging
logger = logging.getLogger(__name__)


class BaseLinkExtractor(ABC):
    """
    Componente "stateless" responsável por extrair, limpar e validar
    """

    def __init__(self, allowed_domain):
        self.allowed_domain = allowed_domain

    @abstractmethod
    def extract(self, base_url: str, html_soup: BeautifulSoup) -> Set[str]:
        """
        Extrai todos os links válidos de uma página HTML.
        """
        pass

    @abstractmethod
    def _is_valid_url(self, url: str) -> bool:
        """
        O "motor de regras" que decide se vale a pena colocar um link na fila de urls a visitar.
        """

    @abstractmethod
    def clean_url(self, url: str) -> str:
        """
        Remove a query string (parte após '?') de uma URL e fragmentos
        """
