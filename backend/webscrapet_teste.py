from app.webcrawler.g1scraper import G1Scraper

url = "https://g1.globo.com/sp/sao-paulo/noticia/2025/10/10/policia-civil-localiza-fabrica-clandestina-de-bebidas-ligadas-a-morte-de-duas-pessoas-por-intoxicacao-com-metanol-em-sp.ghtml"

webcralwer = G1Scraper(url)

article = webcralwer.scrape_article()

for key, value in article.__dict__.items():
    print(f"{key}: {value}\n")
