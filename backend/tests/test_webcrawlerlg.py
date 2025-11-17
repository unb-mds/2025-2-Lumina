from app.webcrawler.Metropoles.metrowebcrawler import WebCrawler
import logging

logging.basicConfig(level=logging.INFO)

crawler = WebCrawler()

print("Iniciando crawl de teste do Metrópoles...")
crawler.crawl(max_pages=5)

stats = crawler.database.get_stats()

print(f"\nResultados (Metrópoles):")
print(f"Artigos salvos (Total no DB): {stats['total']}")
print(f"URLs visitadas (Nesta sessão): {len(crawler.visited_urls)}")