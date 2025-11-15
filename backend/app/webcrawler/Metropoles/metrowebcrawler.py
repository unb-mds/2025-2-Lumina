import logging
from queue import Queue

# Importa os componentes específicos do Metrópoles
from app.webcrawler.Metropoles.metroscraper import MetroScraper
from app.webcrawler.Metropoles.metrolinkextractor import MetroLinkExtractor

# Importa os componentes genéricos (Downloader e Banco de Dados)
from ..dowloader import Downloader 
from app.db.articledb import ArticleDB

logger = logging.getLogger(__name__)


class WebCrawler:
    """
    Motor principal do WebCrawler para o portal Metrópoles.
    Esta classe mantém o padrão estrutural do G1.
    """

    def __init__(self):
        
        # Componentes genéricos
        self.downloader = Downloader()
        self.database = ArticleDB()
        
        # Componentes específicos do Metrópoles
        self.scraper = MetroScraper()
        self.link_extractor = MetroLinkExtractor()
        
        # Gerenciamento de fila e URLs visitadas
        self.Urls_to_visit = Queue()
        self.visited_urls = set() 

        # URL Semente (Seed) específica do Metrópoles
        self.seed_url = "https://www.metropoles.com/"
        self.Urls_to_visit.put(self.seed_url) 

    def crawl(self, max_pages: int = 100) -> None:
        """
        Executa o processo de crawling.
        """
        
        logger.info(f"Iniciando crawl do Metrópoles. Max pages: {max_pages}")
        pages_crawled = 0

        while not self.Urls_to_visit.empty() and pages_crawled < max_pages:
            
            # 1. Pega a próxima URL da fila
            current_url = self.Urls_to_visit.get()

            if current_url in self.visited_urls:
                logger.debug(f"URL já visitada, pulando: {current_url}")
                continue

            # 2. Baixa o conteúdo da página
            logger.debug(f"Baixando: {current_url}")
            html_data = self.downloader.fetch(current_url)
            
            if self.scraper.is_article_page(html_data):
                try:
                    logger.info(f"Artigo identificado, raspando: {current_url}")
                    # ... (etc) ...
                except Exception as e:
                    logger.error(...)
            else:
                logger.debug(f"Página é uma seção (sem 'article:section'), pulando raspagem: {current_url}")

            # 3. Lógica de Scrape (Raspagem)
            #    No Metrópoles, assumimos que URLs de ARTIGO NÃO terminam com '/'
            #    e URLs de SEÇÃO (lista) TERMINAM com '/'

            # 4. Lógica de Extração de Links (sempre executa)
            found_links = self.link_extractor.extract(html_data) 

            for link in found_links:
                if link not in self.visited_urls and self.Urls_to_visit.qsize() < (max_pages * 5):
                    self.Urls_to_visit.put(link)

            # 5. Finaliza a página atual
            self.visited_urls.add(current_url)
            pages_crawled += 1
            logger.info(f"Páginas visitadas: {pages_crawled}/{max_pages}")

        logger.info(f"Crawl finalizado. Total de páginas visitadas: {pages_crawled}")