import requests
from bs4 import BeautifulSoup
from app.ai.models.article_model import Article
from app.ai.models.pagescraper import PageScraper
import time
import logging
import re
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class G1Scraper(PageScraper):
    """
    Scraper for G1 news articles with robust error handling. 
    Added some logic to different layouts as blogs, added as well the clean of the unwanted text in the body.  
    """

    # Class constants for CSS selectors
    SELECTORS = {
        "title": "content-head__title",
        "subtitle": "content-head__subtitle",
        "author": "content-publication-data__from",
        "date": "content-publication-data__updated",
        "body": "content-text__container",
    }

    BODY_CONTAINERS = [
        'mc-article-body',  # Notícia padrão
        'post-body',        # Blogs e colunas
        'content-text',     # Fallback
        SELECTORS["body"]   # Container original (apenas para fallback, se necessário)
    ]

        FILTRO_PARAGRAFOS = [
        'Leia também:',
        'O blog',
        'Clique aqui para seguir o canal',
        'WhatsApp',
        'Telegram',
        'crie uma conta Globo gratuita',
        'Para se inscrever',
        'De segunda a sábado, as notícias que você não pode perder diretamente no seu e-mail.'
    ]

    def __init__(self, url):
        super().__init__(url)
        self.url_data: BeautifulSoup | None = None
        self._is_loaded = False

    def _get_url_data(self) -> BeautifulSoup | None:
        """
        Makes an HTTP request with exponential backoff for retries.

        Returns:
            BeautifulSoup: Parsed HTML content or None if all retries fail
        """
        max_tries = 3
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        for tries in range(max_tries):
            try:
                response = requests.get(self.url, headers=headers, timeout=10)
                response.raise_for_status()
                self._is_loaded = True
                return BeautifulSoup(response.text, "html.parser")

            except requests.Timeout:
                logger.warning(f"Attempt {tries + 1}: Request timed out")
            except requests.HTTPError as e:
                logger.error(
                    f"Attempt {tries + 1}: HTTP error {e.response.status_code}"
                )
                # Don't retry on client errors (4xx)
                if 400 <= e.response.status_code < 500:
                    break
            except requests.RequestException as e:
                logger.warning(f"Attempt {tries + 1} failed: {e}")

            # Exponential backoff before retry
            if tries < max_tries - 1:
                delay = 2**tries
                logger.info(f"Waiting {delay} seconds before retrying...")
                time.sleep(delay)

        logger.error(
            f"Failed to retrieve data from {self.url} after {max_tries} attempts"
        )
        return None

    def _load_page(self):
        """Lazy load the page data if not already loaded."""
        if not self._is_loaded and self.url_data is None:
            self.url_data = self._get_url_data()

    def _clean_soup(self):
        """
        Remove HTML blocks indesejados (Newsletter, Mais Lidas) diretamente
        de self.url_data (o objeto BeautifulSoup).
        """
        if self.url_data:
            # 1. Remove o contêiner da Newsletter
            newsletter_elem = self.url_data.find('div', class_='newsletter-g1_container')
            if newsletter_elem:
                newsletter_elem.extract()
                
            # 2. Remove o bloco "MAIS LIDAS" ou outros widgets similares
            mais_lidas_elem = self.url_data.find('div', class_='mc-column entities')
            if mais_lidas_elem:
                mais_lidas_elem.extract()
                
            # 3. Remove publicidade (que pode ser mais genérica que o filtro do corpo)
            ads_elem = self.url_data.find('div', class_='content-text__advertising')
            if ads_elem:
                ads_elem.extract()


    def _extract_enhanced_author(self) -> str:
        """
        Tenta extrair o autor usando a lógica aprimorada (assinatura de blog e dados de publicação).
        """
        # Tenta a assinatura de autor de blog (ex: 'top_signature_text_author-name')
        autor_signature_elem = self.url_data.select_one('.top_signature_text_author-name')
        if autor_signature_elem:
            autor_texto = autor_signature_elem.text.replace('Por ', '').strip()
            if autor_texto:
                return autor_texto
        
        # Tenta o seletor padrão do bloco de publicação ('content-publication-data__from')
        autor_elem = self.url_data.find(class_=self.SELECTORS["author"])
        if autor_elem:
            # Tenta pegar do atributo 'title' (comum no G1)
            autor = autor_elem.get('title', '').strip()
            if autor and autor != "{}":
                return autor

        return "" # Retorna vazio se não encontrar

    def _extract_enhanced_date(self) -> str:
        """
        Extrai a data e aplica regex para limpá-la para o formato DD/MM/AAAA.
        """
        data_elem = self.url_data.find(class_=self.SELECTORS["date"])
        data_completa = data_elem.text.strip() if data_elem else ""
        
        match = re.search(r'(\d{2}\/\d{2}\/\d{4})', data_completa)
        if match:
            return match.group(1)
            
        return data_completa # Retorna o texto bruto se o formato não for encontrado            

    def _extract_body_text(self, container: BeautifulSoup = None):
        """
        Extract body text preserving paragraph structure.

        Args:
            container: BeautifulSoup element containing the article body

        Returns:
            str: Formatted body text with paragraphs separated by double newlines
        """
        # Lógica para encontrar o container mais adequado (Notícia Padrão > Blog > Genérico)
        corpo_container = None
        for class_name in self.BODY_CONTAINERS:
            corpo_container = self.url_data.find('div', class_=class_name)
            if corpo_container:
                break
        
        if not corpo_container:
            logger.warning("Nenhum container de corpo de artigo principal encontrado.")
            return ""

        paragrafos_coletados = []
        
        # Busca tags p, blockquote, ul e li para capturar listas e citações
        elementos_texto = corpo_container.find_all(['p', 'blockquote', 'ul', 'li'])
        
        for elem in elementos_texto:
            texto_limpo = elem.get_text(strip=True)
            
            excluir = False
            
            # Filtro de exclusão por Palavra-Chave
            if any(keyword in texto_limpo for keyword in self.FILTRO_PARAGRAFOS):
                excluir = True
                
            # Filtro de exclusão por Classe (anúncios, etc.)
            if 'class' in elem.attrs and any(cls in self.FILTRO_PARAGRAFOS for cls in elem['class']):
                 excluir = True

            if texto_limpo and not excluir:
                # Formata listas e blockquotes para melhor representação textual
                if elem.name == 'li':
                    paragrafos_coletados.append(f"* {texto_limpo}")
                elif elem.name == 'blockquote':
                    paragrafos_coletados.append(f"> {texto_limpo}")
                else:
                    paragrafos_coletados.append(texto_limpo)

        return "\n\n".join(paragrafos_coletados)


    def scrape_article(self) -> Article | None:
        """
        Scrape article content from the G1 webpage.

        Returns:
            Article: Article object with scraped content or None if scraping fails
        """
        # Ensure page is loaded
        self._load_page()

        if self.url_data is None:
            logger.error("Cannot scrape article: page data not loaded")
            return None

        # NOVA ETAPA: Limpeza Inicial do HTML (remoção de Newsletter/Mais Lidas)
        self._clean_soup()

        # Dictionary to store extracted text
        elements_text = {}

        # 1. Extração de Título e Subtítulo (Mantido o loop original para classes padrão)
        for element, class_name in self.SELECTORS.items():
            if element not in ["author", "date", "body"]: # Exclui os que terão extração aprimorada
                found_element = self.url_data.find(class_=class_name)

                if found_element:
                    elements_text[element] = found_element.get_text(strip=True)
                else:
                    elements_text[element] = ""
                    logger.debug(f"Element '{element}' with class '{class_name}' not found")
        
        # 2. Extração Aprimorada de Autor
        elements_text["author"] = self._extract_enhanced_author()

        # 3. Extração Aprimorada de Data
        elements_text["date"] = self._extract_enhanced_date()

        # 4. Extração Aprimorada do Corpo (Usando o método _extract_body_text modificado)
        # O método _extract_body_text não precisa de um container como argumento agora, pois ele encontra internamente.
        elements_text["body"] = self._extract_body_text()

        # Validate critical elements
        if not elements_text.get("title"):
            logger.error("Missing critical element: title")
            return None

        if not elements_text.get("body"):
            logger.error("Missing critical element: body")
            return None

        # Log optional missing elements
        optional_elements = ["subtitle", "author", "date"]
        missing_optional = [
            elem for elem in optional_elements if not elements_text.get(elem)
        ]
        if missing_optional:
            logger.warning(
                f"Optional elements not found: {', '.join(missing_optional)}"
            )

        return Article(
            title=elements_text["title"],
            subtitle=elements_text.get("subtitle", ""),
            date=elements_text.get("date", ""),
            author=elements_text.get("author", ""),
            url=self.url,
            body=elements_text["body"],
        )
