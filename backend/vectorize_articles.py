import logging
import os
from dotenv import load_dotenv
import time

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Adiciona o diretório do projeto ao sys.path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app.db.articledb import ArticleDB
from backend.app.db.vectordb import VectorDB
from backend.app.ai.rag.google_embedder import GoogleEmbedder
from backend.app.ai.rag.text_splitter import TextSplitter

def main():
    """
    Script principal para vetorizar artigos pendentes.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logging.error("A variável de ambiente GOOGLE_API_KEY não foi definida.")
        return

    logging.info("Iniciando o processo de vetorização de artigos...")

    try:
        # 1. Inicializa as dependências
        article_db = ArticleDB(db_path="backend/app/db/articles.db")
        
        # Configura a plataforma de embedding e o divisor de texto
        embedding_platform = GoogleEmbedder(api_key=api_key)
        text_splitter = TextSplitter(chunk_size=1000, chunk_overlap=200)
        
        vector_db = VectorDB(
            embedding_platform=embedding_platform,
            text_splitter=text_splitter,
            db_path="app/db/chroma_db"
        )

        # 2. Busca artigos pendentes de vetorização
        pending_articles = article_db.get_articles_pending_vectorization()

        if not pending_articles:
            logging.info("Nenhum artigo pendente para vetorização.")
            return

        logging.info(f"Encontrados {len(pending_articles)} artigos para vetorizar.")

        # 3. Itera e processa cada artigo
        for article in pending_articles:
            logging.info(f"Vetorizando artigo ID: {article.id} - Título: {article.title}")
            
            # Vetoriza o artigo e obtém o ID do lote (batch)
            batch_id = vector_db.vectorize_article(article)

            if batch_id:
                # 4. Marca o artigo como vetorizado no banco de dados principal
                article_db.mark_as_vectorized(article.id, batch_id)
                logging.info(f"Artigo ID: {article.id} marcado como vetorizado com Batch ID: {batch_id}")
            else:
                logging.error(f"Falha ao vetorizar o artigo ID: {article.id}. O artigo será ignorado por enquanto.")
            
            time.sleep(3)   # Pausa para evitar sobrecarga na API

    except Exception as e:
        logging.error(f"Ocorreu um erro inesperado durante o processo: {e}", exc_info=True)
    finally:
        if 'article_db' in locals() and article_db:
            article_db.close()
        logging.info("Processo de vetorização finalizado.")

if __name__ == "__main__":
    main()
