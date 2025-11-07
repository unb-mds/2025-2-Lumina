from app.webcrawler.G1.g1webcrawler import WebCrawler

crawler = WebCrawler()
print("Iniciando crawl de teste...")
crawler.crawl(max_pages=5)

stats = crawler.database.get_stats()
print(f"\nResultados:")
print(f"Artigos salvos: {stats['total']}")
print(f"URLs visitadas: {len(crawler.visited_urls)}")