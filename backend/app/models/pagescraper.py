import time
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from app.models.article import Article


class PageScraper(ABC):
    """Abstract base class for page scrapers."""
    def __init__(self, url):
        self.url = url
        self.url_data = self._get_url_data()

        
    @abstractmethod
    def _get_url_data(self) -> BeautifulSoup | None:
        pass
    @abstractmethod
    def scrape_article(self) -> Article | None:
        pass 
