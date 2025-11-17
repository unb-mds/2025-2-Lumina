import logging
from typing import Set
from urllib.parse import urljoin, urlparse, urlunparse

from bs4 import BeautifulSoup

from app.models.linkextractor import BaseLinkExtractor

logger = logging.getLogger(__name__)


class MetroLinkExtractor(BaseLinkExtractor):
    """
    Componente stateless responsável por extrair e validar links
    específicos do portal Metrópoles.
    """

    def __init__(self, allowed_domain: str = "www.metropoles.com"):
        self.allowed_domain = allowed_domain
        self.base_url = f"https://{self.allowed_domain}"

        # --- ALTERAÇÃO AQUI ---
        # Lista de prefixos de caminho a serem ignorados
        # Removemos o "/" desta lista
        self.IGNORED_PREFIXES = (
            "/sobre",
            "/expediente",
            "/fale-conosco",
            "/termo-de-uso",
            "/politica-de-privacidade",
            "/autores",
            "/tags",
            "/busca",
            "/ao-vivo",
        )

        # --- NOVO TRECHO ---
        # Lista de caminhos EXATOS a ignorar
        self.IGNORED_PATHS = (
            "/",  # Ignora a própria homepage
        )

        # Lista de sufixos de arquivo a serem ignorados
        self.IGNORED_SUFFIXES = (
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".pdf",
            ".zip",
            ".rar",
            ".mp4",
        )

    def extract(self, html_soup: BeautifulSoup) -> Set[str]:
        """Extrai todos os links válidos de uma página HTML do Metrópoles."""
        found_links: Set[str] = set()

        for link_tag in html_soup.find_all("a", href=True):
            url = link_tag["href"]

            if url.startswith("/"):
                url = urljoin(self.base_url, url)

            clean_url = self.clean_url(url)

            if self._is_valid_url(clean_url):
                found_links.add(clean_url)

        return found_links

    def _is_valid_url(self, url: str) -> bool:
        """
        O "motor de regras" que decide se vale a pena visitar um link do Metrópoles.
        """
        try:
            parsed = urlparse(url)
        except ValueError:
            logger.debug(f"URL com sintaxe inválida, pulando: {url}")
            return False

        # REGRA 1: Ignora esquemas que não sejam HTTP/HTTPS
        if parsed.scheme not in ["http", "https"]:
            return False

        # REGRA 2: Garante que o link está no domínio permitido
        if parsed.netloc != self.allowed_domain:
            return False

        # --- NOVA REGRA ---
        # REGRA 3: Ignora caminhos EXATOS (ex: a homepage "/")
        if parsed.path in self.IGNORED_PATHS:
            return False

        # --- REGRA ALTERADA (AGORA É REGRA 4) ---
        # REGRA 4: Ignora links de "serviço" (ex: /sobre, /fale-conosco)
        if parsed.path.startswith(self.IGNORED_PREFIXES):
            return False

        # REGRA 5: Ignora links de arquivos (ex: .jpg, .pdf)
        if parsed.path.endswith(self.IGNORED_SUFFIXES):
            return False

        # REGRA 6: Garante que é um link de artigo (ex: /secao/nome-artigo)
        # Um link de artigo válido deve ter pelo menos 2 barras no caminho.
        if parsed.path.count("/") < 2:
            return False

        return True

    def clean_url(self, url: str) -> str:
        """
        Remove a query string (parte após '?') e fragmentos (parte após '#')
        de uma URL.
        """
        if not isinstance(url, str):
            logger.warning(f"Entrada não é uma string, retornando como está: {url}")
            return url

        parsed_url = urlparse(url)

        cleaned_url = urlunparse(
            (
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                "",  # Remove a query string
                "",  # Remove o fragmento
            )
        )
        return cleaned_url
