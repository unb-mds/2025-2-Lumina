import sqlite3
from datetime import datetime
from typing import Optional
from ..models.article import Article


class ArticleDB:
    def __init__(self, db_path: str = "backend/app/db/articles.db"):
        self.conn = sqlite3.connect(db_path)
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
                article.url,
                article.content,
                datetime.now(),
            ),
        )
        self.conn.commit()
        return cursor.lastrowid

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
            articles.append(
                Article(
                    id=row[0],
                    title=row[1],
                    author=row[2],
                    url=row[3],
                    content=row[4],
                    saved_at=row[5],
                    vectorized_at=row[6],
                    vector_db_id=row[7],
                )
            )
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
        return None

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
        return None

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
        cursor = self.conn.execute('SELECT title, url FROM articles ORDER BY id')
        return cursor.fetchall()
    
    def close(self):
        self.conn.close()


