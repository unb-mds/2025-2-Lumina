import sys
import os
import logging

current_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(current_dir)

sys.path.append(current_dir)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

from app.webcrawler.Metropoles.metrowebcrawler import WebCrawler

def main():
    print(f"=== Iniciando Crawler Metrópoles ===")
    print(f"Diretório de execução: {os.getcwd()}") 
    
    try:
        crawler = WebCrawler()
        
        crawler.crawl(max_pages=50)

        print("=== Finalizado com sucesso ===")

    except KeyboardInterrupt:
        print("\nParando execução... (O progresso foi salvo)")
        sys.exit(0)
    except Exception as e:
        print(f"Erro crítico: {e}")

        print("Dica: Verifique se a pasta 'backend/app/db' existe.")
        sys.exit(1)

if __name__ == "__main__":
    main()