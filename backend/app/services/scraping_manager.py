
from app.webcrawler.G1.g1scraper import G1Scraper
from app.db.articledb import ArticleDB
from app.models.article import Article

class ScrapingManager:

    SCRAPERS = {
            "g1.globo.com": G1Scraper,
            # Adicione outras fontes aqui
        }

    def __init__(self):
        self.db = ArticleDB()

    def scrape_and_save(self, url: str) -> int | None:
        """
        Identifica a fonte da URL, realiza o scraping e salva o artigo no banco.
        Retorna o ID do artigo salvo ou None se não for salvo.
        """
        scraper = None
       
        for domain, scraper_class in self.SCRAPERS.items():
            if domain in url:
                scraper = scraper_class()
                break        
        if not scraper:
            raise ValueError("Fonte de URL não suportada.")
        
        IsArticleInDB = self.db.get_article_by_url(url)
        if IsArticleInDB:
            return IsArticleInDB.id
        
        article = scraper.scrape(url)
        if article:
            article_id = self.db.save_article(article)
            return article_id
        return None
        