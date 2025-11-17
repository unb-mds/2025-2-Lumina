import logging
from typing import Set
from urllib.parse import urljoin, urlparse, urlunparse

from bs4 import BeautifulSoup

from app.models.linkextractor import BaseLinkExtractor

logger = logging.getLogger(__name__)


class G1LinkExtractor(BaseLinkExtractor):
    def __init__(self, allowed_domain: str = "g1.globo.com"):
        self.allowed_domain = allowed_domain

    def extract(self, html_soup: BeautifulSoup) -> Set[str]:
        found_links: Set[str] = set()
        base_url = f"https://{self.allowed_domain}"
        for link_tag in html_soup.find_all("a", href=True):
            url = link_tag["href"]

            if url.startswith("/"):
                url = urljoin(base_url, url)

            clean_url = self.clean_url(url)

            if self._is_valid_url(clean_url):
                found_links.add(clean_url)

        return found_links

    def _is_valid_url(self, url: str) -> bool:
        """
        O "motor de regras" que decide se vale a pena visitar um link.
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

        # REGRA 3: Garante que o link leva a uma página de notícia ou seção
        if not (parsed.path.endswith("ghtml") or parsed.path.endswith("/")):
            return False

        return True

    def clean_url(self, url: str) -> str:
        if not isinstance(url, str):
            logger.warning(f"Entrada não é uma string, retornando como está: {url}")
            return url
        # 1. Parseia a URL em seus componentes
        parsed_url = urlparse(url)

        # 2. Reconstrói a URL usando urlunparse sem query e fragments
        cleaned_url = urlunparse(
            (
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                "",
                "",
            )
        )
        return cleaned_url
