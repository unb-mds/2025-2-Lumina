import logging
import time
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class Downloader:
    """
    Responsável por baixar o conteúdo de uma URL.
    Implementa retries, backoff exponencial e headers.
    """

    def __init__(self, max_tries=3):
        self.max_tries = max_tries
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def fetch(self, url: str) -> BeautifulSoup | None:
        """
        Makes an HTTP request with exponential backoff for retries.
        (Esta é a sua função _get_url_data, renomeada e movida para cá)
        """
        for tries in range(self.max_tries):
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                return BeautifulSoup(response.text, "html.parser")

            except requests.Timeout:
                logger.warning(f"Attempt {tries + 1}: Request timed out for {url}")
            except requests.HTTPError as e:
                logger.error(
                    f"Attempt {tries + 1}: HTTP error {e.response.status_code} for {url}"
                )
                if 400 <= e.response.status_code < 500:
                    break
            except requests.RequestException as e:
                logger.warning(f"Attempt {tries + 1} failed for {url}: {e}")

            if tries < self.max_tries - 1:
                delay = 2**tries
                logger.info(f"Waiting {delay} seconds before retrying {url}...")
                time.sleep(delay)

        logger.error(
            f"Failed to retrieve data from {url} after {self.max_tries} attempts"
        )
        return None
