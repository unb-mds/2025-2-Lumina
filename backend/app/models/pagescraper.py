import requests
from bs4 import BeautifulSoup
from app.models.article import Article
import time


class PageScraper:
    def __init__(self, url):
        self.url = url
        self.url_data = self._get_url_data()

    def _get_url_data(self):
        """
        Makes an HTTP request with exponential backoff for retries.
        """
        max_tries = 3
        for tries in range(max_tries):
            try:
                response = requests.get(self.url, timeout=10)
                response.raise_for_status()
                return BeautifulSoup(response.text, "html.parser")
            except requests.RequestException as e:
                print(f"Attempt {tries + 1} failed: {e}")
                if tries < max_tries - 1:
                    delay = 2**tries
                    print(f"Waiting for {delay} seconds before retrying...")
                    time.sleep(delay)

        print(f"Failed to retrieve data from {self.url} after {max_tries} attempts.")
        return None

    def scrape_article(self) -> Article | None:
        pass  # Funcionalidade em desenvolvimento
