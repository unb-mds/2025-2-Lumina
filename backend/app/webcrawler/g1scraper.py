import requests
from bs4 import BeautifulSoup
from app.ai.models.article_model import Article
from app.ai.models.pagescraper import PageScraper
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class G1Scraper(PageScraper):
    """Scraper for G1 news articles with robust error handling."""
    
    # Class constants for CSS selectors
    SELECTORS = {
        'title': 'content-head__title',
        'subtitle': 'content-head__subtitle',
        'author': 'content-publication-data__from',
        'date': 'content-publication-data__updated',
        'body': 'content-text__container'
    }
    
    def __init__(self, url):
        super().__init__(url)
        self.url_data = None
        self._is_loaded = False
    
    def _get_url_data(self):
        """
        Makes an HTTP request with exponential backoff for retries.
        
        Returns:
            BeautifulSoup: Parsed HTML content or None if all retries fail
        """
        max_tries = 3
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        for tries in range(max_tries):
            try:
                response = requests.get(self.url, headers=headers, timeout=10)
                response.raise_for_status()
                self._is_loaded = True
                return BeautifulSoup(response.text, 'html.parser')
                
            except requests.Timeout:
                logger.warning(f"Attempt {tries + 1}: Request timed out")
            except requests.HTTPError as e:
                logger.error(f"Attempt {tries + 1}: HTTP error {e.response.status_code}")
                # Don't retry on client errors (4xx)
                if 400 <= e.response.status_code < 500:
                    break
            except requests.RequestException as e:
                logger.warning(f"Attempt {tries + 1} failed: {e}")
            
            # Exponential backoff before retry
            if tries < max_tries - 1:
                delay = 2 ** tries
                logger.info(f"Waiting {delay} seconds before retrying...")
                time.sleep(delay)
        
        logger.error(f"Failed to retrieve data from {self.url} after {max_tries} attempts")
        return None
    
    def _load_page(self):
        """Lazy load the page data if not already loaded."""
        if not self._is_loaded and self.url_data is None:
            self.url_data = self._get_url_data()
    
    def _extract_body_text(self, container):
        """
        Extract body text preserving paragraph structure.
        
        Args:
            container: BeautifulSoup element containing the article body
            
        Returns:
            str: Formatted body text with paragraphs separated by double newlines
        """
        paragraphs = container.find_all('p', class_=lambda x: x != 'content-text__advertising')
        
        if paragraphs:
            return '\n\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
        return container.get_text(strip=True)
    
    def scrape_article(self) -> Article | None:
        """
        Scrape article content from the G1 webpage.
        
        Returns:
            Article: Article object with scraped content or None if scraping fails
        """
        # Ensure page is loaded
        self._load_page()
        
        if self.url_data is None:
            logger.error("Cannot scrape article: page data not loaded")
            return None
        
        # Dictionary to store extracted text
        elements_text = {}
        
        # Extract text from each element
        for element, class_name in self.SELECTORS.items():
            found_element = self.url_data.find(class_=class_name)
            
            if found_element:
                if element == 'body':
                    elements_text[element] = self._extract_body_text(found_element)
                else:
                    elements_text[element] = found_element.get_text(strip=True)
            else:
                elements_text[element] = ''
                logger.debug(f"Element '{element}' with class '{class_name}' not found")
        
        # Validate critical elements
        if not elements_text.get('title'):
            logger.error("Missing critical element: title")
            return None
        
        if not elements_text.get('body'):
            logger.error("Missing critical element: body")
            return None
        
        # Log optional missing elements
        optional_elements = ['subtitle', 'author', 'date']
        missing_optional = [elem for elem in optional_elements if not elements_text.get(elem)]
        if missing_optional:
            logger.warning(f"Optional elements not found: {', '.join(missing_optional)}")
        
        return Article(
            title=elements_text['title'],
            subtitle=elements_text.get('subtitle', ''),
            date=elements_text.get('date', ''),
            author=elements_text.get('author', ''),
            url=self.url,
            body=elements_text['body']
        )
