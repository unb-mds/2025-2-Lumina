import os
import sys
import logging

# Configuração básica de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Adiciona o diretório do projeto ao sys.path para permitir importações relativas
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, "..")
sys.path.append(project_root)

from app.db.articledb import ArticleDB


def main():
    """
    Exibe o status do banco de dados de artigos, incluindo
    o total, pendentes e vetorizados.
    """
    article_db = None
    try:
        # Caminho relativo para o banco de dados de artigos
        article_db_path = os.path.join(project_root, "app", "db", "articles.db")
        metroarticle_db_path = os.path.join(project_root, "app", "db", "metroarticles.db")
        article_db = ArticleDB(db_path=article_db_path)
        metroarticle_db = ArticleDB(db_path=metroarticle_db_path)

        stats = article_db.get_stats()

        print("\n--- Status do Banco de Dados de Artigos ---")
        print(f"Total de artigos: {stats['total']}")
        print(f"Artigos pendentes de vetorização: {stats['pending_vectorization']}")
        print(f"Artigos vetorizados: {stats['vectorized']}")
        print("------------------------------------------\n")

        print("\n--- Status do Banco de Dados de Artigos Metrópoles ---")
        metro_stats = metroarticle_db.get_stats()
        print(f"Total de artigos: {metro_stats['total']}")
        print(f"Artigos pendentes de vetorização: {metro_stats['pending_vectorization']}")
        print(f"Artigos vetorizados: {metro_stats['vectorized']}")
        print("------------------------------------------\n")

    except Exception as e:
        logging.error(
            f"Ocorreu um erro ao obter o status do banco de dados: {e}", exc_info=True
        )
    finally:
        if article_db:
            article_db.close()
            logging.info("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    main()
