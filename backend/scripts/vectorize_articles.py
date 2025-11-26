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

# Adiciona o diretório do projeto ao sys.path para permitir importações relativas
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, "..")
sys.path.append(project_root)

from app.ai.rag.google_embedder import GoogleEmbedder
from app.db.articledb import ArticleDB
from app.db.vectordb import VectorDB


def main():
    # Carrega a chave de API do Google
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        logging.error("A variável de ambiente GOOGLE_API_KEY não foi definida.")
        sys.exit(1) # Sai se a chave da API não estiver configurada

    try:
        # Inicializa o embedder do Google
        EMBEDDING_MODEL = "models/gemini-embedding-001"
        embedder = GoogleEmbedder(api_key=google_api_key, model_name=EMBEDDING_MODEL)
        
        # Caminhos relativos para os bancos de dados
        article_db_path = os.path.join(project_root, "app", "db", "articles.db")
        vector_db_path = os.path.join(project_root, "app", "db", "chroma_db")

        article_db = ArticleDB(db_path=article_db_path)
        vector_db = VectorDB(db_path=vector_db_path, embedding_platform=embedder)

        pending_articles = article_db.get_articles_pending_vectorization()
        
        if not pending_articles:
                logging.info("Nenhum artigo pendente para vetorização.")
                return

        logging.info(f"Encontrados {len(pending_articles)} artigos para vetorizar.")

        for article in pending_articles:
            logging.info(f"Processando artigo ID: {article.id} - Título: {article.title}")
            
            # A lógica de retentativa para TPM e outros erros está dentro deste método
            batch_id = vector_db.vectorize_whole_article(article=article)
            
            if batch_id:
                article_db.mark_as_vectorized(article.id, batch_id)
                logging.info(f"Artigo ID: {article.id} marcado como vetorizado.")
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