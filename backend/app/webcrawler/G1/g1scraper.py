import logging
from bs4 import BeautifulSoup

from app.models.article import Article
from app.models.pagescraper import PageScraper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class G1Scraper(PageScraper):

    SELECTORS = {
        "title": "content-head__title",
        "author": "content-publication-data__from",
        "body": "mc-article-body",
    }


    def _extract_body_text(self, container):
        """
        Extract body text preserving paragraph structure.
        (Sua implementação aqui está ótima, sem mudanças)
        """

        paragraphs = container.find_all(
            "p", class_=lambda x: x == "content-text__container"
        )
        if paragraphs:
            return "\n\n".join(
                p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)
            )
        return container.get_text(strip=True)

    def scrape_article(self, url: str, html_data: BeautifulSoup) -> Article | None:
        """
        Raspa o conteúdo de um artigo a partir da URL e do HTML (string).

        Args:
            url (str): A URL original do artigo (para salvar no objeto).
            html_str (str): O conteúdo HTML bruto da página.

        Returns:
            Article: Objeto Article preenchido ou None se a raspagem falhar.
        """

        # Dicionário para armazenar o texto extraído
        elements_text = {}

        # Extrai o texto de cada elemento
        for element, class_name in self.SELECTORS.items():
            found_element = html_data.find(class_=class_name)

            if found_element:
                if element == "body":
                    elements_text[element] = self._extract_body_text(found_element)
                else:
                    elements_text[element] = found_element.get_text(strip=True)
            else:
                elements_text[element] = ""
                logger.debug(
                    f"Elemento '{element}' (classe: '{class_name}') não encontrado em {url}"
                )

        if not elements_text.get("title"):
            logger.error(f"Elemento crítico faltando: title (URL: {url})")
            return None

        if not elements_text.get("body"):
            logger.error(f"Elemento crítico faltando: body (URL: {url})")
            return None

        return Article(
            title=elements_text["title"],
            author=elements_text.get("author", ""),
            url=url,
            content=elements_text["body"],
        )
    

