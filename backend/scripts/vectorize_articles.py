import logging
import os
import time

from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração básica de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Adiciona o diretório do projeto ao sys.path
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.ai.rag.ollama_embedder import OllamaEmbeddings
from backend.app.db.articledb import ArticleDB
from backend.app.db.vectordb import VectorDB


def main():
    try:
        EMBEDDING_MODEL = "bge-m3" 
        embedder = OllamaEmbeddings(model_name=EMBEDDING_MODEL)
        article_db = ArticleDB(db_path=r"C:\Users\Tiago\2025-2-Lumina\backend\app\db\articles.db")
        vector_db = VectorDB(db_path=r"C:\Users\Tiago\2025-2-Lumina\backend\app\db\chroma_db"
                             , embedding_platform=embedder)


        pending_articles = article_db.get_articles_pending_vectorization()
        
        if not pending_articles:
                logging.info("Nenhum artigo pendente para vetorização.")
                return

        logging.info(f"Encontrados {len(pending_articles)} artigos para vetorizar.")

        for article in pending_articles:
            logging.info(f"Vetorizando artigo ID: {article.id} - Título: {article.title}")
            batch_id = vector_db.vectorize_whole_article(article=article)
            if batch_id:
                article_db.mark_as_vectorized(article.id, batch_id)
                logging.info(f"Artigo ID: {article.id} marcado como vetorizado com Batch ID: {batch_id}")
            else:
                logging.error(f"Falha ao vetorizar o artigo ID: {article.id}. O artigo será ignorado por enquanto.")

   
    except Exception as e:
        logging.error(
            f"Ocorreu um erro inesperado durante o processo: {e}", exc_info=True
        )
    finally:
        if "article_db" in locals() and article_db:
            article_db.close()
        logging.info("Processo de vetorização finalizado.")
    
if __name__ == "__main__":
   main()