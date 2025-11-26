import pytest
from unittest.mock import MagicMock
from datetime import datetime
import sqlite3
from app.db.articledb import ArticleDB
from app.models.article import Article

@pytest.fixture
def db():
    """Fixture que cria um banco em memória para cada teste."""
    database = ArticleDB(db_name=":memory:")
    yield database
    database.close()

@pytest.fixture
def sample_article():
    """Fixture para um artigo padrão."""
    return Article(
        title="Título Teste",
        author="Autor Teste",
        url="http://teste.com/artigo1",
        content="Conteúdo do artigo."
    )

class TestArticleDB:

    # --- CREATE ---

    def test_save_article_success(self, db, sample_article):
        """Testa se salva corretamente e gera um ID."""
        article_id = db.save_article(sample_article)
        
        assert isinstance(article_id, int)
        assert article_id > 0
        
        # Verifica se salvou os dados corretos
        saved = db.get_article_by_id(article_id)
        assert saved.title == sample_article.title
        assert str(saved.url) == str(sample_article.url)
        assert saved.saved_at is not None

    def test_save_article_duplicate_url(self, db, sample_article):
        """Testa o INSERT OR IGNORE para URLs duplicadas."""
        db.save_article(sample_article)
        db.save_article(sample_article)
        
        stats = db.get_stats()
        assert stats["total"] == 1

    # --- READ ---

    def test_get_article_by_id_not_found(self, db):
        assert db.get_article_by_id(999) is None

    def test_get_article_by_url_success(self, db, sample_article):
        db.save_article(sample_article)
        found = db.get_article_by_url(str(sample_article.url))
        
        assert found is not None
        assert found.title == sample_article.title

    def test_get_article_by_url_not_found(self, db):
        assert db.get_article_by_url("http://nao-existe.com") is None

    def test_get_all_articles(self, db):
        for i in range(3):
            a = Article(title=f"T{i}", author="A", url=f"http://url{i}.com", content="C")
            db.save_article(a)
            
        all_articles = db.get_all_articles()
        assert len(all_articles) == 3
        assert all_articles[0].title == "T2"

    def test_get_all_titles_and_urls(self, db, sample_article):
        db.save_article(sample_article)
        result = db.get_all_titles_and_urls()
        
        assert len(result) == 1
        assert result[0] == (sample_article.title, str(sample_article.url))

    # --- UPDATE ---

    def test_update_article_success(self, db, sample_article):
        aid = db.save_article(sample_article)
        
        updates = {"title": "Novo Título", "content": "Novo Conteúdo"}
        updated_article = db.update_article(aid, updates)
        
        assert updated_article is not None
        assert updated_article.title == "Novo Título"
        assert updated_article.content == "Novo Conteúdo"
        assert updated_article.author == sample_article.author

    def test_update_article_invalid_fields_mixed(self, db, sample_article):
        """
        Tenta atualizar campos mistos (um válido e outros inválidos).
        Deve atualizar o válido e ignorar os outros.
        """
        aid = db.save_article(sample_article)
        
        updates = {"id": 999, "url": "http://hacker.com", "title": "Título Seguro"}
        updated = db.update_article(aid, updates)
        
        assert updated.id == aid
        assert str(updated.url) == str(sample_article.url)
        assert updated.title == "Título Seguro"

    def test_update_article_no_valid_fields(self, db, sample_article):
        """
        NOVO: Tenta atualizar APENAS campos inválidos.
        Cobre as linhas 140-141 (if not set_clause).
        """
        aid = db.save_article(sample_article)
        
        # Nenhum destes campos é permitido para update
        updates = {"id": 999, "url": "http://hacker.com", "created_at": "2025"}
        updated = db.update_article(aid, updates)
        
        # O artigo deve retornar intacto
        assert updated.id == aid
        assert updated.title == sample_article.title

    def test_update_article_not_found(self, db):
        res = db.update_article(999, {"title": "X"})
        assert res is None

    def test_update_article_empty_data(self, db, sample_article):
        aid = db.save_article(sample_article)
        res = db.update_article(aid, {})
        assert res.title == sample_article.title

    # --- DELETE ---

    def test_delete_article_success(self, db, sample_article):
        aid = db.save_article(sample_article)
        assert db.delete_article(aid) is True
        assert db.get_article_by_id(aid) is None

    def test_delete_article_not_found(self, db):
        assert db.delete_article(999) is False

    # --- RAG / Vectorization Control ---

    def test_pending_vectorization_logic(self, db):
        a1 = Article(title="A1", author="A", url="http://u1.com", content="C")
        a2 = Article(title="A2", author="A", url="http://u2.com", content="C")
        id1 = db.save_article(a1)
        id2 = db.save_article(a2)

        pending = db.get_articles_pending_vectorization()
        assert len(pending) == 2
        
        db.mark_as_vectorized(id1, "vec_id_123")
        
        pending_after = db.get_articles_pending_vectorization()
        assert len(pending_after) == 1
        assert pending_after[0].id == id2

        art1 = db.get_article_by_id(id1)
        assert art1.vectorized_at is not None
        assert art1.vector_db_id == "vec_id_123"

        stats = db.get_stats()
        assert stats["total"] == 2
        assert stats["pending_vectorization"] == 1
        assert stats["vectorized"] == 1

    # --- Exception Handling (Cobertura Hardcore) ---

    def test_update_sql_error(self, db, sample_article):
        """Simula erro de banco no UPDATE (rollback)."""
        aid = db.save_article(sample_article)
        
        db.conn = MagicMock()
        db.conn.execute.side_effect = sqlite3.Error("Erro forçado")
        
        result = db.update_article(aid, {"title": "Novo"})
        
        assert result is None
        db.conn.rollback.assert_called_once()

    def test_delete_sql_error(self, db):
        """Simula erro de banco no DELETE."""
        db.conn = MagicMock()
        db.conn.execute.side_effect = sqlite3.Error("Erro forçado")
        
        assert db.delete_article(1) is False
        db.conn.rollback.assert_called_once()