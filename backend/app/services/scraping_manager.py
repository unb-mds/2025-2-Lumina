from app.db.articledb import ArticleDB
from app.webcrawler.dowloader import Downloader
from app.webcrawler.G1.g1scraper import G1Scraper


class ScrapingError(Exception):
    """Custom exception for scraping errors."""

    pass


class ScrapingManager:
    SCRAPERS = {
        "g1.globo.com": G1Scraper,
        # Adicione outras fontes aqui
    }

    def __init__(self):
        self.db = ArticleDB()
        self.downloader = Downloader()

    def scrape_and_save(self, url: str) -> tuple[int, bool]:
        """
        Identifica a fonte da URL, realiza o scraping e salva o artigo no banco.

        Retorna uma tupla (article_id, created), onde `created` é:
        - True se o artigo foi raspado e salvo com sucesso.
        - False se o artigo já existia no banco de dados.

        Lança as seguintes exceções:
        - ValueError: Se a URL não pertence a uma fonte suportada.
        - ScrapingError: Se o conteúdo não puder ser extraído da página.
        """

        url_str = str(url)

        scraper = None

        for domain, scraper_class in self.SCRAPERS.items():
            if domain in url_str:
                scraper = scraper_class()
                break
        if not scraper:
            raise ValueError("Fonte de URL não suportada.")

        existing_article = self.db.get_article_by_url(url)
        if existing_article and existing_article.id is not None:
            return existing_article.id, False

        try:
            html_data = self.downloader.fetch(url)
            if not html_data:
                raise ScrapingError(f"Não foi possível baixar o conteúdo da URL: {url}")

            article = scraper.scrape_article(url, html_data)
            if not article:
                raise ScrapingError(
                    "Não foi possível extrair o conteúdo do artigo da URL."
                )
        except Exception as e:
            raise ScrapingError(f"Falha no scraping: {e}") from e

        article_id = self.db.save_article(article)
        if article_id is None:
            # Isso pode acontecer se o INSERT OR IGNORE falhar de forma inesperada
            # ou se a URL foi adicionada por outro processo entre a verificação e a inserção.
            existing = self.db.get_article_by_url(url)
            if existing and existing.id:
                return existing.id, False
            raise ScrapingError(
                "Falha ao salvar o artigo no banco de dados após o scraping."
            )

        return article_id, True
