from app.webcrawler.G1.g1scraper import G1Scraper
from app.webcrawler.G1.g1linkextractor import G1LinkExtractor
from ..dowloader import Downloader
from queue import Queue
from app.db.articledb import ArticleDB


class WebCrawler:

    def __init__(self):
 
        self.downloader = Downloader()
        self.scraper =  G1Scraper()
        self.link_extractor = G1LinkExtractor()
        self.database = ArticleDB()
        
        self.Urls_to_visit = Queue()
        self.visited_urls = set() 

        self.seed_url = "https://g1.globo.com/"
        self.Urls_to_visit.put(self.seed_url)   

    def crawl(self, max_pages: int = 100) -> None:

        pages_crawled = 0

        while not self.Urls_to_visit.empty() or pages_crawled < max_pages:
            current_url = self.Urls_to_visit.get()

            if current_url in self.visited_urls:
                continue

            html_data = self.downloader.fetch(current_url)
            if not html_data:
                continue
            if "noticia" in current_url:
                article = self.scraper.scrape_article(current_url, html_data)
                if article:
                    print(f"Artigo extraído: {article.title}")
                    self.database.save_article(article)

            found_links = self.link_extractor.extract(html_data) 

            for link in found_links:
                if link not in self.visited_urls:
                    self.Urls_to_visit.put(link)

            self.visited_urls.add(current_url)
            pages_crawled += 1
            

