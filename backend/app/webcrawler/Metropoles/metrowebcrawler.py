import json
import logging
import os
import sys
from queue import Queue

# Ajuste de imports para garantir que funcionem
from app.db.articledb import ArticleDB
from app.webcrawler.dowloader import Downloader
from app.webcrawler.Metropoles.metrolinkextractor import MetroLinkExtractor
from app.webcrawler.Metropoles.metroscraper import MetroScraper

# Configuração de Log
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class MetropolesCrawler:
    def __init__(self):
        self.downloader = Downloader()
        self.scraper = MetroScraper()
        self.link_extractor = MetroLinkExtractor("backend/app/db/articles.d")
        self.database = ArticleDB(db_path=r"C:\Users\Tiago\2025-2-Lumina\backend\app\db\metroarticles.db")

        self.Urls_to_visit = Queue()
        self.visited_urls = set()

        # Caminho do arquivo de persistência (separado do G1 para não conflitar)
        self.state_file = "metropoles_crawler_state.json"

        # Categorias permitidas (Seeds e Filtros)
        # O Metrópoles usa estrutura do tipo: metropoles.com/brasil/titulo
        self.categorias_permitidas = [
            "brasil",
            "mundo",
            "distrito-federal",
            "ciencia",
            "saude",
            "negocios",
        ]

        # Adiciona as seeds iniciais
        base_url = "https://www.metropoles.com"
        self.Urls_to_visit.put(base_url) # Home
        for categoria in self.categorias_permitidas:
            seed_url = f"{base_url}/{categoria}"
            self.Urls_to_visit.put(seed_url)

        # Tenta carregar progresso anterior
        self.load_state()

    # ============================================================
    # Persistência de progresso (Igual ao G1)
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
                f"[STATE] Progresso salvo: {len(self.visited_urls)} visitados, "
                f"{self.Urls_to_visit.qsize()} na fila."
            )
        except Exception as e:
            logger.error(f"[STATE] Erro ao salvar progresso: {e}")

    def load_state(self):
        """Carrega o progresso anterior."""
        try:
            if not os.path.exists(self.state_file):
                logger.info(f"[STATE] Arquivo '{self.state_file}' não encontrado. Iniciando do zero.")
                return

            with open(self.state_file, "r", encoding="utf-8") as f:
                state_data = json.load(f)
                self.visited_urls = set(state_data.get("visited_urls", []))
                for url in state_data.get("urls_to_visit", []):
                    self.Urls_to_visit.put(url)

            logger.info(
                f"[STATE] Progresso carregado: {len(self.visited_urls)} visitados, "
                f"{self.Urls_to_visit.qsize()} pendentes."
            )

        except Exception as e:
            logger.error(f"[STATE] Erro ao carregar progresso: {e}")

    # ============================================================
    # Crawler principal
    # ============================================================
    def crawl(self, max_pages: int = 100) -> None:
        pages_crawled = 0
        skipped_visited = 0
        failed_downloads = 0
        
        logger.info(f"Iniciando Crawler Metrópoles. Meta: {max_pages} artigos.")

        while not self.Urls_to_visit.empty() and pages_crawled < max_pages:
            current_url = self.Urls_to_visit.get()

            if current_url in self.visited_urls:
                skipped_visited += 1
                continue

            # Baixa o HTML
            html_data = self.downloader.fetch(current_url)
            if not html_data:
                failed_downloads += 1
                continue

            # --- LÓGICA DE IDENTIFICAÇÃO DE ARTIGO ---
            # Diferente do G1, o Metrópoles não tem ".ghtml" no final obrigatório.
            # Usamos o método is_article_page do Scraper que checa a meta tag.
            
            is_article = self.scraper.is_article_page(html_data)
            
            # Filtro extra: Só processa artigos das categorias de interesse
            # Ex: evita artigos de "celebridades" ou "coluna-do-fulano" se não estiverem nas categorias
            is_interesting_category = any(cat in current_url for cat in self.categorias_permitidas)

            if is_article and is_interesting_category:
                article = self.scraper.scrape_article(current_url, html_data)
                if article:
                    logger.info(f"Artigo Salvo: {article.title} ({current_url})")
                    self.database.save_article(article)
                    pages_crawled += 1
                else:
                    logger.warning(f"Falha ao extrair dados do artigo: {current_url}")
            
            # --- EXTRAÇÃO DE NOVOS LINKS ---
            # Extrai links tanto de artigos quanto de páginas de seção (home, politica, etc)
            found_links = self.link_extractor.extract(html_data)
            
            for link in found_links:
                if link not in self.visited_urls:
                    # Só adiciona à fila se pertencer a uma categoria permitida
                    # Isso evita que o crawler se perca em subdomínios irrelevantes
                    if any(cat in link for cat in self.categorias_permitidas):
                        self.Urls_to_visit.put(link)

            self.visited_urls.add(current_url)

            # Salvamento periódico (a cada 20 ações)
            total_ops = pages_crawled + skipped_visited + failed_downloads
            if total_ops % 20 == 0:
                self.save_state()
                logger.info(f"Status: {pages_crawled}/{max_pages} coletados. Fila: {self.Urls_to_visit.qsize()}")

        # Finalização
        self.save_state()
        logger.info("========== CRAWLER FINALIZADO ==========")
        logger.info(f"Total artigos salvos: {pages_crawled}")
        logger.info(f"Total visitados: {len(self.visited_urls)}")