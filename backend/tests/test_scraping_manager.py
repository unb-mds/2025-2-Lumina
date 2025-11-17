import pytest
from unittest.mock import MagicMock, patch
from backend.app.services.scraping_manager import ScrapingManager, ScrapingError
from backend.app.models.article import Article
from bs4 import BeautifulSoup

@pytest.fixture
def mock_articledb():
    """Fixture to mock ArticleDB."""
    with patch('backend.app.services.scraping_manager.ArticleDB') as mock_db:
        yield mock_db.return_value

@pytest.fixture
def mock_downloader():
    """Fixture to mock Downloader."""
    with patch('backend.app.services.scraping_manager.Downloader') as mock_downloader:
        yield mock_downloader.return_value

@pytest.fixture
def sample_article():
    """Fixture to provide a sample article."""
    return Article(
        id=1,
        title="Test Title",
        author="Test Author",
        url="http://g1.globo.com/test",
        content="Test content."
    )

@pytest.fixture
def mock_html():
    """Fixture to provide a mock HTML content."""
    html = """
    <html>
        <body>
            <h1 class="content-head__title">Test Title</h1>
            <p class="content-publication-data__from">Test Author</p>
            <div class="mc-article-body">
                <p class="content-text__container">Test content.</p>
            </div>
        </body>
    </html>
    """
    return BeautifulSoup(html, "html.parser")

def test_scrape_and_save_new_article(mock_articledb: MagicMock, mock_downloader: MagicMock, sample_article: Article, mock_html: BeautifulSoup):
    """Test scraping and saving a new article."""
    mock_articledb.get_article_by_url.return_value = None
    mock_downloader.fetch.return_value = mock_html
    
    mock_scraper = MagicMock()
    mock_scraper.scrape_article.return_value = sample_article
    
    mock_articledb.save_article.return_value = 1

    manager = ScrapingManager()
    manager.db = mock_articledb
    manager.downloader = mock_downloader
    manager.SCRAPERS = {"g1.globo.com": lambda: mock_scraper}
    
    article_id, created = manager.scrape_and_save(sample_article.url)

    assert article_id == 1
    assert created is True
    mock_articledb.get_article_by_url.assert_called_once_with(sample_article.url)
    mock_downloader.fetch.assert_called_once_with(sample_article.url)
    mock_scraper.scrape_article.assert_called_once_with(sample_article.url, mock_html)
    mock_articledb.save_article.assert_called_once_with(sample_article)

def test_scrape_and_save_existing_article(mock_articledb: MagicMock, mock_downloader: MagicMock, sample_article: Article):
    """Test scraping an existing article."""
    mock_articledb.get_article_by_url.return_value = sample_article

    manager = ScrapingManager()
    manager.db = mock_articledb
    manager.downloader = mock_downloader
    
    article_id, created = manager.scrape_and_save(sample_article.url)

    assert article_id == sample_article.id
    assert created is False
    mock_articledb.get_article_by_url.assert_called_once_with(sample_article.url)
    mock_downloader.fetch.assert_not_called()
    mock_articledb.save_article.assert_not_called()

def test_scrape_and_save_unsupported_url(mock_articledb: MagicMock):
    """Test scraping an unsupported URL."""
    manager = ScrapingManager()
    manager.db = mock_articledb
    with pytest.raises(ValueError, match="Fonte de URL não suportada."):
        manager.scrape_and_save("http://unsupported.com/test")

def test_scrape_and_save_scraper_fails(mock_articledb: MagicMock, mock_downloader: MagicMock, sample_article: Article, mock_html: BeautifulSoup):
    """Test scraping when the scraper fails."""
    mock_articledb.get_article_by_url.return_value = None
    mock_downloader.fetch.return_value = mock_html
    
    mock_scraper = MagicMock()
    mock_scraper.scrape_article.return_value = None

    manager = ScrapingManager()
    manager.db = mock_articledb
    manager.downloader = mock_downloader
    manager.SCRAPERS = {"g1.globo.com": lambda: mock_scraper}

    with pytest.raises(ScrapingError, match="Não foi possível extrair o conteúdo do artigo da URL."):
        manager.scrape_and_save(sample_article.url)

def test_scrape_and_save_db_fails(mock_articledb: MagicMock, mock_downloader: MagicMock, sample_article: Article, mock_html: BeautifulSoup):
    """Test scraping when saving to the database fails."""
    mock_articledb.get_article_by_url.return_value = None
    mock_downloader.fetch.return_value = mock_html
    
    mock_scraper = MagicMock()
    mock_scraper.scrape_article.return_value = sample_article
    
    mock_articledb.save_article.return_value = None
    # To trigger the final error, the second get_article_by_url must also return None
    mock_articledb.get_article_by_url.side_effect = [None, None]


    manager = ScrapingManager()
    manager.db = mock_articledb
    manager.downloader = mock_downloader
    manager.SCRAPERS = {"g1.globo.com": lambda: mock_scraper}

    with pytest.raises(ScrapingError, match="Falha ao salvar o artigo no banco de dados após o scraping."):
        manager.scrape_and_save(sample_article.url)
