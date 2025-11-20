import pytest
import sqlite3
from app.db.articledb import ArticleDB
from app.models.article import Article

@pytest.fixture
def db_memoria():
    """Cria uma base de dados temporária em memória para testes."""
    db = ArticleDB(db_path=":memory:")
    return db

@pytest.fixture
def artigo_exemplo():
    return Article(
        url="http://example.com/teste",
        title="Título de Teste",
        author="Autor de Teste",
        content="Conteúdo de teste.",
    )

def test_guardar_artigo(db_memoria: ArticleDB, artigo_exemplo: Article):
    """Testa guardar um artigo na base de dados."""
    id_artigo = db_memoria.save_article(artigo_exemplo)
    assert id_artigo is not None

    cursor = db_memoria.conn.cursor()
    cursor.execute("SELECT * FROM articles WHERE id=?", (id_artigo,))
    linha = cursor.fetchone()
    assert linha is not None
    assert linha[1] == artigo_exemplo.title
    # CORREÇÃO: Compara string com string (o URL do banco vem como texto)
    assert linha[3] == str(artigo_exemplo.url)

def test_guardar_artigo_duplicado(db_memoria: ArticleDB, artigo_exemplo: Article):
    """Testa guardar um artigo duplicado (deve ser ignorado)."""
    id1 = db_memoria.save_article(artigo_exemplo)
    id2 = db_memoria.save_article(artigo_exemplo)
    
    # Dependendo da implementação, pode retornar None ou o ID existente.
    # O importante é que não crie um novo registo.
    cursor = db_memoria.conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM articles")
    contagem = cursor.fetchone()[0]
    assert contagem == 1

def test_obter_artigo_por_url(db_memoria: ArticleDB, artigo_exemplo: Article):
    """Testa recuperar um artigo pelo seu URL."""
    db_memoria.save_article(artigo_exemplo)
    # CORREÇÃO: Passa o URL como string para a busca
    artigo_recuperado = db_memoria.get_article_by_url(str(artigo_exemplo.url))
    
    assert artigo_recuperado is not None
    assert artigo_recuperado.title == artigo_exemplo.title
    # CORREÇÃO: Compara string com string
    assert str(artigo_recuperado.url) == str(artigo_exemplo.url)

def test_obter_estatisticas(db_memoria: ArticleDB, artigo_exemplo: Article):
    """Testa recuperar estatísticas da base de dados."""
    db_memoria.save_article(artigo_exemplo)
    stats = db_memoria.get_stats()
    assert stats["total"] == 1
    assert stats["pending_vectorization"] == 1
    assert stats["vectorized"] == 0
    
    # CORREÇÃO: Passa URL como string
    id_artigo = db_memoria.get_article_by_url(str(artigo_exemplo.url)).id
    db_memoria.mark_as_vectorized(id_artigo, "chroma_id_123")
    
    stats = db_memoria.get_stats()
    assert stats["vectorized"] == 1
    assert stats["pending_vectorization"] == 0

def test_obter_todos_titulos_e_urls(db_memoria: ArticleDB, artigo_exemplo: Article):
    """Testa recuperar todos os títulos e URLs."""
    db_memoria.save_article(artigo_exemplo)
    titulos_e_urls = db_memoria.get_all_titles_and_urls()
    assert len(titulos_e_urls) == 1
    assert titulos_e_urls[0] == (artigo_exemplo.title, str(artigo_exemplo.url))