from app.webcrawler.G1.g1webcrawler import WebCrawler
import sys

def main():
    print("Iniciando o WebCrawler do G1...")
    try:
        crawler = WebCrawler()
        
        crawler.crawl(max_pages=500) 
        
        print("WebCrawler finalizado com sucesso.")
    except Exception as e:
        print(f"Erro ao executar o WebCrawler: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
