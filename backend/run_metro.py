import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

from app.webcrawler.Metropoles.metrowebcrawler import WebCrawler

def main():
    print("=== Iniciando Crawler Metrópoles ===")
    try:
        crawler = WebCrawler()

        crawler.crawl(max_pages=50)

        print("=== Finalizado com sucesso ===")

    except KeyboardInterrupt:
        print("\nParando execução... (O progresso foi salvo)")
        
        sys.exit(0)
    except Exception as e:
        print(f"Erro crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()