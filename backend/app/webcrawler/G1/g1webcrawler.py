from app.webcrawler.G1.g1scraper import G1Scraper
from dowloader import Downloader
from queue import Queue


class WebCrawler:

    def __init__(self):
 
        self.downloader = Downloader()
        self.scraper =  G1Scraper()
        

        self.Urls_to_visit = Queue()
        self.visited_urls = set()