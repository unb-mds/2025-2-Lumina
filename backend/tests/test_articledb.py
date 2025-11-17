import sqlite3

import pytest

from backend.app.db.articledb import ArticleDB
from backend.app.models.article import Article


@pytest.fixture
def memory_db():
    """Fixture to set up an in-memory SQLite database for tests."""
    conn = sqlite3.connect(":memory:")
    db = ArticleDB(db_path=":memory:")
    db.conn = conn
    db.create_table()
    yield db
    db.close()


@pytest.fixture
def sample_article():
    """Fixture to provide a sample article."""
    return Article(
        title="Test Title",
        author="Test Author",
        url="http://example.com/test",
        content="Test content.",
    )


def test_create_table(memory_db: ArticleDB):
    """Test if the articles table is created correctly."""
    cursor = memory_db.conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='articles';"
    )
    assert cursor.fetchone() is not None


def test_save_article(memory_db: ArticleDB, sample_article: Article):
    """Test saving an article to the database."""
    article_id = memory_db.save_article(sample_article)
    assert article_id is not None

    cursor = memory_db.conn.cursor()
    cursor.execute("SELECT * FROM articles WHERE id=?", (article_id,))
    row = cursor.fetchone()
    assert row is not None
    assert row[1] == sample_article.title
    assert row[3] == sample_article.url


def test_get_articles_pending_vectorization(
    memory_db: ArticleDB, sample_article: Article
):
    """Test retrieving articles that are pending vectorization."""
    memory_db.save_article(sample_article)
    articles = memory_db.get_articles_pending_vectorization()
    assert len(articles) == 1
    assert articles[0].title == sample_article.title


def test_mark_as_vectorized(memory_db: ArticleDB, sample_article: Article):
    """Test marking an article as vectorized."""
    article_id = memory_db.save_article(sample_article)
    vector_db_id = "test_vector_id"
    memory_db.mark_as_vectorized(article_id, vector_db_id)

    cursor = memory_db.conn.cursor()
    cursor.execute(
        "SELECT vectorized_at, vector_db_id FROM articles WHERE id=?", (article_id,)
    )
    row = cursor.fetchone()
    assert row is not None
    assert row[0] is not None
    assert row[1] == vector_db_id


def test_get_article_by_url(memory_db: ArticleDB, sample_article: Article):
    """Test retrieving an article by its URL."""
    memory_db.save_article(sample_article)
    retrieved_article = memory_db.get_article_by_url(sample_article.url)
    assert retrieved_article is not None
    assert retrieved_article.title == sample_article.title


def test_get_article_by_id(memory_db: ArticleDB, sample_article: Article):
    """Test retrieving an article by its ID."""
    article_id = memory_db.save_article(sample_article)
    retrieved_article = memory_db.get_article_by_id(article_id)
    assert retrieved_article is not None
    assert retrieved_article.title == sample_article.title


def test_get_stats(memory_db: ArticleDB, sample_article: Article):
    """Test retrieving database statistics."""
    memory_db.save_article(sample_article)
    stats = memory_db.get_stats()
    assert stats["total"] == 1
    assert stats["pending_vectorization"] == 1
    assert stats["vectorized"] == 0

    article_id = memory_db.get_article_by_url(sample_article.url).id
    memory_db.mark_as_vectorized(article_id, "test_vector_id")
    stats = memory_db.get_stats()
    assert stats["total"] == 1
    assert stats["pending_vectorization"] == 0
    assert stats["vectorized"] == 1


def test_get_all_titles_and_urls(memory_db: ArticleDB, sample_article: Article):
    """Test retrieving all titles and URLs."""
    memory_db.save_article(sample_article)
    titles_and_urls = memory_db.get_all_titles_and_urls()
    assert len(titles_and_urls) == 1
    assert titles_and_urls[0] == (sample_article.title, sample_article.url)


def test_close_connection(memory_db: ArticleDB):
    """Test closing the database connection."""
    memory_db.close()
    with pytest.raises(sqlite3.ProgrammingError):
        memory_db.conn.execute("SELECT 1")
