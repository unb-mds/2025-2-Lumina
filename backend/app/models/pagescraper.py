from abc import ABC, abstractmethod
from app.models.article import Article 

class PageScraper(ABC):
    """Abstract base class for page scrapers."""
    
    def __init__(self):
        pass

    @abstractmethod
    def scrape_article(self, url: str, html_str: str) -> Article | None:
        pass