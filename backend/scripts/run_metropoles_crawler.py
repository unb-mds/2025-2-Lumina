import sys
import logging



import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.webcrawler.Metropoles.metrowebcrawler import MetropolesCrawler

def main():
    print("Iniciando o WebCrawler do Metrópoles...")
    try:
        crawler = MetropolesCrawler()
        
        # Defina aqui quantos artigos quer baixar nesta execução
        crawler.crawl(max_pages=5500)

        print("WebCrawler finalizado com sucesso.")
    except KeyboardInterrupt:
        print("\nCrawler interrompido pelo usuário via teclado.")
        # O crawler salva o estado automaticamente em loops, mas podemos forçar se quisermos
    except Exception as e:
        print(f"Erro crítico ao executar o WebCrawler: {e}")
        logging.exception("Detalhes do erro:")
        sys.exit(1)

if __name__ == "__main__":
    main()