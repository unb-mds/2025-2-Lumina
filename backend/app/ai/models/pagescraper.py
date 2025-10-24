from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

from .article_model import Article


class PageScraper(ABC):
    def __init__(self, url):
        self.url = url

    @abstractmethod
    def _get_url_data(self) -> BeautifulSoup | None:
        """Get data from URL"""
        pass

    @abstractmethod
    def scrape_article(self) -> Article | None:
        """Scrape article data from the page"""
        pass
