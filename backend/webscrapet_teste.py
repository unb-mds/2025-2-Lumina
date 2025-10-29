from app.webcrawler.G1.g1linkextractor import G1LinkExtractor
from app.webcrawler.dowloader import Downloader

downloader = Downloader()
extractor = G1LinkExtractor()

url = "https://g1.globo.com/rj/rio-de-janeiro/noticia/2025/10/29/corpos-sao-levados-por-moradores.ghtml"

html_data = downloader.fetch(url)

if html_data:
    links = extractor.extract(html_data)
    for link in links:
        print(link)
else:
    print("Falha ao baixar o conteúdo da página.")
