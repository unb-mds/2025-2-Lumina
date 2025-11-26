import sqlite3
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
import os

from ..models.article import Article  # Isto agora é o seu modelo Pydantic

# Configura o logger
logger = logging.getLogger(__name__)


class ArticleDB:
    def __init__(self, db_name: str = "articles.db"):
        if db_name == ":memory:":
            self.db_path = ":memory:"
        else:
            # Construct default path relative to the current file (articledb.py)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(current_dir, db_name)
            
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):
        """Cria a tabela de artigos com campos de controle para RAG"""
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                url TEXT UNIQUE NOT NULL,
                content TEXT NOT NULL,
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                vectorized_at TIMESTAMP NULL,
                vector_db_id TEXT NULL,
                UNIQUE(url)
            )
        """
        )
        self.conn.commit()

    def _row_to_article(self, row: tuple) -> Article:
        """Helper para converter uma linha do banco (tuple) em um objeto Article."""
        return Article(
            id=row[0],
            title=row[1],
            author=row[2],
            url=row[3],
            content=row[4],
            saved_at=row[5],
            vectorized_at=row[6],
            vector_db_id=row[7],
        )

    # --- C (CREATE) ---
    def save_article(self, article: Article) -> int:
        """Salva um artigo minerado no banco"""
        cursor = self.conn.execute(
            """
            INSERT OR IGNORE INTO articles (title, author, url, content, saved_at)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                article.title,
                article.author,
                # O Pydantic HttpUrl será convertido para string aqui
                str(article.url),
                article.content,
                datetime.now(),
            ),
        )
        self.conn.commit()
        return cursor.lastrowid

    # --- R (READ) ---
    def get_article_by_id(self, article_id: int) -> Optional[Article]:
        """Busca um artigo pelo seu ID."""
        cursor = self.conn.execute(
            """
            SELECT id, title, author, url, content, saved_at,
                   vectorized_at, vector_db_id
            FROM articles
            WHERE id = ?
        """,
            (article_id,),
        )
        row = cursor.fetchone()
        if row:
            return self._row_to_article(row)
        return None

    def get_article_by_url(self, url: str) -> Optional[Article]:
        """Busca um artigo pela URL (útil para evitar duplicatas)"""
        cursor = self.conn.execute(
            """
            SELECT id, title, author, url, content, saved_at,
                   vectorized_at, vector_db_id
            FROM articles
            WHERE url = ?
        """,
            (url,),
        )
        row = cursor.fetchone()
        if row:
            return self._row_to_article(row)
        return None

    def get_all_articles(self) -> List[Article]:
        """(NOVO) Busca TODOS os artigos do banco."""
        cursor = self.conn.execute(
            """
            SELECT id, title, author, url, content, saved_at,
                   vectorized_at, vector_db_id
            FROM articles
            ORDER BY id DESC
        """
        )
        articles = []
        for row in cursor.fetchall():
            articles.append(self._row_to_article(row))
        return articles

    # --- U (UPDATE) ---
    def update_article(
        self, article_id: int, data: Dict[str, Any]
    ) -> Optional[Article]:
        """
        (NOVO) Atualiza campos específicos de um artigo (title, author, content).
        Retorna o artigo atualizado se for encontrado.
        """
        if not data:
            return self.get_article_by_id(article_id)  # Nada a fazer

        set_clause = []
        values = []
        
        # Garante que apenas colunas seguras possam ser atualizadas
        allowed_columns = ["title", "author", "content"]
        
        for key, value in data.items():
            if key in allowed_columns:
                set_clause.append(f"{key} = ?")
                values.append(value)

        if not set_clause:
            logger.warning(f"Tentativa de update no artigo {article_id} sem campos válidos.")
            return self.get_article_by_id(article_id)
        
        values.append(article_id)
        query = f"UPDATE articles SET {', '.join(set_clause)} WHERE id = ?"

        try:
            cursor = self.conn.execute(query, tuple(values))
            self.conn.commit()

            if cursor.rowcount == 0:
                logger.warning(f"Artigo {article_id} não encontrado para atualizar.")
                return None
            
            # Retorna o artigo com os novos dados
            return self.get_article_by_id(article_id)
        
        except sqlite3.Error as e:
            logger.error(f"Erro ao atualizar artigo {article_id}: {e}")
            self.conn.rollback()
            return None

    # --- D (DELETE) ---
    def delete_article(self, article_id: int) -> bool:
        """
        (NOVO) Deleta um artigo pelo ID.
        Retorna True se o artigo foi deletado, False caso contrário.
        """
        try:
            cursor = self.conn.execute(
                "DELETE FROM articles WHERE id = ?",
                (article_id,)
            )
            self.conn.commit()
            
            # cursor.rowcount > 0 significa que uma linha foi afetada (deletada)
            return cursor.rowcount > 0
        
        except sqlite3.Error as e:
            logger.error(f"Erro ao deletar artigo {article_id}: {e}")
            self.conn.rollback()
            return False

    # --- Métodos de Controle RAG (existentes) ---
    def get_articles_pending_vectorization(self) -> list[Article]:
        """Retorna artigos que ainda não foram vetorizados"""
        cursor = self.conn.execute(
            """
            SELECT id, title, author, url, content, saved_at, 
                   vectorized_at, vector_db_id
            FROM articles
            WHERE vectorized_at IS NULL
            ORDER BY saved_at ASC
        """
        )
        articles = []
        for row in cursor.fetchall():
            articles.append(self._row_to_article(row))
        return articles

    def mark_as_vectorized(self, article_id: int, vector_db_id: str):
        """Marca um artigo como vetorizado e salva o ID do banco vetorial"""
        self.conn.execute(
            """
            UPDATE articles
            SET vectorized_at = ?, vector_db_id = ?
            WHERE id = ?
        """,
            (datetime.now(), vector_db_id, article_id),
        )
        self.conn.commit()

    # --- Métodos de Stats (existentes) ---
    def get_stats(self) -> dict:
        """Retorna estatísticas do banco"""
        cursor = self.conn.execute(
            """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN vectorized_at IS NULL THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN vectorized_at IS NOT NULL THEN 1 ELSE 0 END) as vectorized
            FROM articles
        """
        )
        row = cursor.fetchone()
        return {"total": row[0], "pending_vectorization": row[1], "vectorized": row[2]}

    def get_all_titles_and_urls(self) -> list[tuple[str, str]]:
        """Retorna lista com (título, url) de todos os artigos"""
        cursor = self.conn.execute("SELECT title, url FROM articles ORDER BY id")
        return cursor.fetchall()
    
    def reset_all_vectorization_status(self) -> int:
        """
        Reseta o status de vetorização de TODOS os artigos.
        Útil se você mudou seu modelo de embeddings ou limpou seu banco vetorial.
        """
        cursor = self.conn.execute(
            """
            UPDATE articles
            SET vectorized_at = NULL, 
                vector_db_id = NULL
            WHERE vectorized_at IS NOT NULL
            """
        )
        self.conn.commit()
        return cursor.rowcount

    def close(self):
        self.conn.close()