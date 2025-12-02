from unittest.mock import MagicMock, patch

import pytest
from bs4 import BeautifulSoup

from app.models.article import Article
from app.services.scraping_manager import ScrapingError, ScrapingManager

# --- Fixtures (Configuração de Testes) ---

@pytest.fixture
def mock_articledb():
    """Fixture para criar um mock do ArticleDB."""
    with patch("app.services.scraping_manager.ArticleDB") as mock_db:
        yield mock_db.return_value

@pytest.fixture
def mock_downloader():
    """Fixture para criar um mock do Downloader."""
    with patch("app.services.scraping_manager.Downloader") as mock_downloader:
        yield mock_downloader.return_value

@pytest.fixture
def sample_article():
    """Fixture que fornece um objeto Article de exemplo para os testes."""
    return Article(
        id=1,
        title="Título de Teste",
        author="Autor de Teste",
        url="http://g1.globo.com/teste",
        content="Conteúdo de teste.",
    )

@pytest.fixture
def mock_html():
    """Fixture que fornece um conteúdo HTML simulado (BeautifulSoup)."""
    html = """
    <html>
        <body>
            <h1 class="content-head__title">Título de Teste</h1>
            <p class="content-publication-data__from">Autor de Teste</p>
            <div class="mc-article-body">
                <p class="content-text__container">Conteúdo de teste.</p>
            </div>
        </body>
    </html>
    """
    return BeautifulSoup(html, "html.parser")

# --- Testes de Fluxo Principal ---

def test_scrape_and_save_new_article(
    mock_articledb: MagicMock,
    mock_downloader: MagicMock,
    sample_article: Article,
    mock_html: BeautifulSoup,
):
    """
    Testa o fluxo completo de scraping e salvamento de um novo artigo.
    
    Verifica se o gerenciador:
    1. Confirma que o artigo não existe no banco.
    2. Baixa o HTML da URL.
    3. Executa o scraper específico.
    4. Salva o artigo no banco.
    """
    # Configuração: O artigo não existe no banco (return_value = None)
    mock_articledb.get_article_by_url.return_value = None
    
    # O download retorna o HTML mockado
    mock_downloader.fetch.return_value = mock_html

    # Configura o scraper específico mockado
    mock_scraper = MagicMock()
    mock_scraper.scrape_article.return_value = sample_article

    # Configura o retorno do salvamento no banco (ID gerado)
    mock_articledb.save_article.return_value = 1

    # Inicializa o Manager com os mocks
    manager = ScrapingManager()
    manager.db = mock_articledb
    manager.downloader = mock_downloader
    manager.SCRAPERS = {"g1.globo.com": lambda: mock_scraper}

    # Executa a ação
    article_id, created = manager.scrape_and_save(sample_article.url)

    # Asserções
    assert article_id == 1
    assert created is True
    
    # Verifica se as chamadas foram feitas corretamente
    mock_articledb.get_article_by_url.assert_called_once_with(sample_article.url)
    mock_downloader.fetch.assert_called_once_with(sample_article.url)
    mock_scraper.scrape_article.assert_called_once_with(sample_article.url, mock_html)
    mock_articledb.save_article.assert_called_once_with(sample_article)

def test_scrape_and_save_existing_article(
    mock_articledb: MagicMock, mock_downloader: MagicMock, sample_article: Article
):
    """
    Testa o comportamento quando o artigo já existe no banco de dados.
    Deve retornar o ID existente e não realizar novo download ou scraping.
    """
    # Configuração: O banco já retorna um artigo existente
    mock_articledb.get_article_by_url.return_value = sample_article

    manager = ScrapingManager()
    manager.db = mock_articledb
    manager.downloader = mock_downloader

    # Executa a ação
    article_id, created = manager.scrape_and_save(sample_article.url)

    # Asserções
    assert article_id == sample_article.id
    assert created is False
    
    # Verifica que o fluxo de download e salvamento NÃO foi acionado
    mock_articledb.get_article_by_url.assert_called_once_with(sample_article.url)
    mock_downloader.fetch.assert_not_called()
    mock_articledb.save_article.assert_not_called()

# --- Testes de Erros e Exceções ---

def test_scrape_and_save_unsupported_url(mock_articledb: MagicMock):
    """Testa a tentativa de scraping com uma URL de domínio não suportado."""
    manager = ScrapingManager()
    manager.db = mock_articledb
    
    # Deve lançar ValueError ao tentar processar um domínio desconhecido
    with pytest.raises(ValueError, match="Fonte de URL não suportada."):
        manager.scrape_and_save("http://unsupported.com/test")

def test_scrape_and_save_scraper_fails(
    mock_articledb: MagicMock,
    mock_downloader: MagicMock,
    sample_article: Article,
    mock_html: BeautifulSoup,
):
    """Testa o cenário onde o scraper específico falha ao extrair dados (retorna None)."""
    mock_articledb.get_article_by_url.return_value = None
    mock_downloader.fetch.return_value = mock_html

    # Configura o scraper para falhar (retornar None)
    mock_scraper = MagicMock()
    mock_scraper.scrape_article.return_value = None

    manager = ScrapingManager()
    manager.db = mock_articledb
    manager.downloader = mock_downloader
    manager.SCRAPERS = {"g1.globo.com": lambda: mock_scraper}

    # Deve lançar ScrapingError
    with pytest.raises(
        ScrapingError, match="Não foi possível extrair o conteúdo do artigo da URL."
    ):
        manager.scrape_and_save(sample_article.url)

def test_scrape_and_save_db_fails(
    mock_articledb: MagicMock,
    mock_downloader: MagicMock,
    sample_article: Article,
    mock_html: BeautifulSoup,
):
    """Testa o cenário de falha ao salvar o artigo no banco de dados."""
    mock_articledb.get_article_by_url.return_value = None
    mock_downloader.fetch.return_value = mock_html

    mock_scraper = MagicMock()
    mock_scraper.scrape_article.return_value = sample_article

    # Simula falha no salvamento (retorna None)
    mock_articledb.save_article.return_value = None
    
    # Para acionar o erro final, a segunda verificação de existência (pós-tentativa de salvar) 
    # também deve retornar None, confirmando que não foi salvo.
    mock_articledb.get_article_by_url.side_effect = [None, None]

    manager = ScrapingManager()
    manager.db = mock_articledb
    manager.downloader = mock_downloader
    manager.SCRAPERS = {"g1.globo.com": lambda: mock_scraper}

    # Deve lançar ScrapingError indicando falha no banco
    with pytest.raises(
        ScrapingError,
        match="Falha ao salvar o artigo no banco de dados após o scraping.",
    ):
        manager.scrape_and_save(sample_article.url)