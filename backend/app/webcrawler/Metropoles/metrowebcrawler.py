import json
import logging
import os
import time
from queue import Queue

from app.db.articledb import ArticleDB
from app.webcrawler.Metropoles.metrolinkextractor import MetroLinkExtractor
from app.webcrawler.Metropoles.metroscraper import MetroScraper
from ..dowloader import Downloader

logger = logging.getLogger(__name__)

class WebCrawler:
    def __init__(self):
        self.downloader = Downloader()
        self.scraper = MetroScraper()
        self.link_extractor = MetroLinkExtractor()
        self.database = ArticleDB()

        self.Urls_to_visit = Queue()
        self.visited_urls = set()

        # --- PADRÃO G1: Persistência ---
        self.state_file = "crawler_metro_state.json"

        # URL Semente
        self.seed_url = "https://www.metropoles.com/"
        self.Urls_to_visit.put(self.seed_url)

        # Tenta carregar progresso anterior
        self.load_state()

    # ============================================================
    # Métodos de Persistência (IGUAL AO G1)
    # ============================================================
    def save_state(self):
        """Salva as URLs visitadas e a fila de URLs restantes em JSON."""
        try:
            state_data = {
                "visited_urls": list(self.visited_urls),
                "urls_to_visit": list(self.Urls_to_visit.queue),
            }
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(state_data, f, ensure_ascii=False, indent=2)
            logger.info(
                f"[STATE] Progresso salvo em '{self.state_file}' "
                f"({len(self.visited_urls)} visitados, {self.Urls_to_visit.qsize()} na fila)."
            )
        except Exception as e:
            logger.error(f"[STATE] Erro ao salvar progresso: {e}")

    def load_state(self):
        """Carrega o progresso anterior ou cria o arquivo de estado se não existir."""
        try:
            if not os.path.exists(self.state_file):
                return

            with open(self.state_file, "r", encoding="utf-8") as f:
                state_data = json.load(f)
                self.visited_urls = set(state_data.get("visited_urls", []))
                
                # Limpa a fila atual (seed) e carrega a salva
                with self.Urls_to_visit.mutex:
                    self.Urls_to_visit.queue.clear()
                
                for url in state_data.get("urls_to_visit", []):
                    self.Urls_to_visit.put(url)

            logger.info(
                f"[STATE] Progresso carregado — "
                f"{len(self.visited_urls)} visitados, {self.Urls_to_visit.qsize()} pendentes."
            )

        except Exception as e:
            logger.error(f"[STATE] Erro ao carregar progresso: {e}")

    # ============================================================
    # Crawler Principal
    # ============================================================
    def crawl(self, max_pages: int = 100) -> None:
        pages_crawled = 0
        skipped_visited = 0
        skipped_not_article = 0
        failed_downloads = 0

        logger.info(f"[CRAWL] Iniciando Metrópoles com max_pages={max_pages}")
        logger.info(f"[CRAWL] URLs na fila inicial: {self.Urls_to_visit.qsize()}")

        while not self.Urls_to_visit.empty() and pages_crawled < max_pages:
            current_url = self.Urls_to_visit.get()

            if current_url in self.visited_urls:
                skipped_visited += 1
                continue

            # Delay para não ser bloqueado
            time.sleep(0.5) 

            html_data = self.downloader.fetch(current_url)
            if not html_data:
                failed_downloads += 1
                logger.warning(f"[CRAWL] Falha ao baixar: {current_url}")
                self.visited_urls.add(current_url) # Marca como visitado para não tentar de novo logo
                continue

            # --- LÓGICA DE RASPAGEM ---
            if self.scraper.is_article_page(html_data):
                article = self.scraper.scrape_article(current_url, html_data)
                if article:
                    logger.info(f"✅ Artigo extraído: {article.title}")
                    self.database.save_article(article)
                    pages_crawled += 1
                else:
                    logger.warning(f"[CRAWL] Falha ao extrair conteúdo: {current_url}")
            else:
                skipped_not_article += 1
                # logger.debug(f"Não é artigo: {current_url}")

            # --- LÓGICA DE NOVOS LINKS ---
            found_links = self.link_extractor.extract(html_data)
            links_added = 0
            for link in found_links:
                if link not in self.visited_urls:
                    # Proteção para a fila não explodir
                    if self.Urls_to_visit.qsize() < 5000:
                        self.Urls_to_visit.put(link)
                        links_added += 1

            self.visited_urls.add(current_url)

            # --- SALVAMENTO PERIÓDICO (A CADA 20 SUCESSOS OU 50 TOTAIS) ---
            total_ops = pages_crawled + skipped_not_article + skipped_visited
            if pages_crawled > 0 and pages_crawled % 10 == 0:
                 self.save_state()
            elif total_ops % 50 == 0:
                 self.save_state()

        # Finalização
        self.save_state()
        logger.info("\n[CRAWL] ========== FINALIZADO ==========")
        logger.info(f"[CRAWL] Artigos baixados: {pages_crawled}")
        logger.info(f"[CRAWL] Total visitados: {len(self.visited_urls)}")
        logger.info(f"[CRAWL] Fila restante: {self.Urls_to_visit.qsize()}")