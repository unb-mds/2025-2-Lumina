import json
import os
from queue import Queue
from app.webcrawler.G1.g1scraper import G1Scraper
from app.webcrawler.G1.g1linkextractor import G1LinkExtractor
from ..dowloader import Downloader
from app.db.articledb import ArticleDB


class WebCrawler:

    def __init__(self):
        self.downloader = Downloader()
        self.scraper = G1Scraper()
        self.link_extractor = G1LinkExtractor()
        self.database = ArticleDB()

        self.Urls_to_visit = Queue()
        self.visited_urls = set()

        # Caminho do arquivo de persistência
        self.state_file = "crawler_state.json"

        # Categorias permitidas para crawlear
        self.categorias_permitidas = [
            "politica",
            "economia",
            "mundo",
            "tecnologia"
        ]

        # Adiciona as páginas iniciais de cada categoria
        for categoria in self.categorias_permitidas:
            seed_url = f"https://g1.globo.com/{categoria}"
            self.Urls_to_visit.put(seed_url)

        # Tenta carregar progresso anterior
        self.load_state()

    # ============================================================
    # Persistência de progresso
    # ============================================================
    def save_state(self):
        """Salva as URLs visitadas e a fila de URLs restantes em JSON."""
        try:
            state_data = {
                "visited_urls": list(self.visited_urls),
                "urls_to_visit": list(self.Urls_to_visit.queue)
            }
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(state_data, f, ensure_ascii=False, indent=2)
            print(f"[STATE] Progresso salvo em '{self.state_file}' "
                  f"({len(self.visited_urls)} visitados, {self.Urls_to_visit.qsize()} na fila).")
        except Exception as e:
            print(f"[STATE] Erro ao salvar progresso: {e}")

    def load_state(self):
        """Carrega o progresso anterior ou cria o arquivo de estado se não existir."""
        try:
            if not os.path.exists(self.state_file):
                # Cria arquivo vazio se não existir
                empty_state = {"visited_urls": [], "urls_to_visit": []}
                with open(self.state_file, "w", encoding="utf-8") as f:
                    json.dump(empty_state, f, ensure_ascii=False, indent=2)
                print(f"[STATE] Arquivo '{self.state_file}' criado (novo progresso).")
                return

            with open(self.state_file, "r", encoding="utf-8") as f:
                state_data = json.load(f)
                self.visited_urls = set(state_data.get("visited_urls", []))
                for url in state_data.get("urls_to_visit", []):
                    self.Urls_to_visit.put(url)

            print(f"[STATE] Progresso carregado — "
                f"{len(self.visited_urls)} visitados, {self.Urls_to_visit.qsize()} pendentes.")

        except Exception as e:
            print(f"[STATE] Erro ao carregar progresso: {e}")


    def reset_state(self):
        """Apaga o progresso salvo (recomeça do zero)."""
        if os.path.exists(self.state_file):
            os.remove(self.state_file)
            print("[STATE] Progresso resetado.")

    # ============================================================
    # Crawler principal
    # ============================================================
    def crawl(self, max_pages: int = 100) -> None:
        pages_crawled = 0
        skipped_visited = 0
        skipped_not_article = 0
        skipped_wrong_category = 0
        failed_downloads = 0

        print(f"[CRAWL] Iniciando com max_pages={max_pages}")
        print(f"[CRAWL] Categorias: {', '.join(self.categorias_permitidas)}")
        print(f"[CRAWL] URLs na fila inicial: {self.Urls_to_visit.qsize()}")
        print(f"[CRAWL] URLs já visitados: {len(self.visited_urls)}")

        while not self.Urls_to_visit.empty() and pages_crawled < max_pages:
            current_url = self.Urls_to_visit.get()

            if current_url in self.visited_urls:
                skipped_visited += 1
                if skipped_visited % 50 == 0:
                    print(f"[CRAWL] {skipped_visited} URLs já visitados pulados até agora")
                continue

            html_data = self.downloader.fetch(current_url)
            if not html_data:
                failed_downloads += 1
                print(f"[CRAWL] Falha ao baixar ({failed_downloads} falhas): {current_url}")
                continue

            # Verifica se é um artigo válido DAS CATEGORIAS PERMITIDAS
            is_article = (
                "noticia" in current_url
                and current_url.endswith(".ghtml")
                and any(categoria in current_url for categoria in self.categorias_permitidas)
            )

            if is_article:
                article = self.scraper.scrape_article(current_url, html_data)
                if article:
                    categoria_artigo = next(
                        (cat for cat in self.categorias_permitidas if cat in current_url),
                        "desconhecida"
                    )
                    print(f"Artigo extraído [{categoria_artigo}]: {article.title}")
                    self.database.save_article(article)
                    pages_crawled += 1
                else:
                    print(f"[CRAWL] Falha ao extrair artigo de: {current_url}")
            else:
                if current_url.endswith(".ghtml"):
                    if not any(cat in current_url for cat in self.categorias_permitidas):
                        skipped_wrong_category += 1
                        if skipped_wrong_category <= 10:
                            print(f"[DEBUG] Artigo de outra categoria pulado: {current_url}")
                    else:
                        skipped_not_article += 1
                else:
                    skipped_not_article += 1

            # Extrai novos links - FILTRA para adicionar apenas links das categorias permitidas
            found_links = self.link_extractor.extract(html_data)
            links_added = 0

            for link in found_links:
                if link not in self.visited_urls:
                    if any(categoria in link for categoria in self.categorias_permitidas):
                        self.Urls_to_visit.put(link)
                        links_added += 1

            self.visited_urls.add(current_url)

            # Salva progresso periodicamente (a cada 50 URLs processadas)
            total_processed = (
                pages_crawled + skipped_visited + skipped_not_article + failed_downloads + skipped_wrong_category
            )
            if total_processed % 50 == 0:
                self.save_state()

            # Log de progresso a cada 10 artigos extraídos
            if pages_crawled > 0 and pages_crawled % 10 == 0:
                print(f"[PROGRESSO] {pages_crawled}/{max_pages} artigos | "
                      f"Fila: {self.Urls_to_visit.qsize()} URLs | "
                      f"Links adicionados agora: {links_added} | "
                      f"Visitados: {len(self.visited_urls)}")

            # Log detalhado a cada 100 URLs processados
            if total_processed % 100 == 0:
                print(f"[CHECKPOINT] Total URLs processados: {total_processed}")
                print(f"  - Artigos extraídos: {pages_crawled}")
                print(f"  - Pulados (já visitados): {skipped_visited}")
                print(f"  - Pulados (não-artigos): {skipped_not_article}")
                print(f"  - Pulados (outra categoria): {skipped_wrong_category}")
                print(f"  - Falhas de download: {failed_downloads}")
                print(f"  - URLs na fila: {self.Urls_to_visit.qsize()}")

        # Log final detalhado
        self.save_state()
        print("\n[CRAWL] ========== FINALIZADO ==========")
        print(f"[CRAWL] Motivo: {'Fila vazia' if self.Urls_to_visit.empty() else 'Limite de páginas atingido'}")
        print(f"[CRAWL] Total artigos extraídos: {pages_crawled}")
        print(f"[CRAWL] Total URLs processados: {len(self.visited_urls)}")
        print(f"[CRAWL] URLs pulados (já visitados): {skipped_visited}")
        print(f"[CRAWL] URLs pulados (não-artigos): {skipped_not_article}")
        print(f"[CRAWL] URLs pulados (outra categoria): {skipped_wrong_category}")
        print(f"[CRAWL] Falhas de download: {failed_downloads}")
        print(f"[CRAWL] URLs restantes na fila: {self.Urls_to_visit.qsize()}")
        print("[CRAWL] ====================================\n")
