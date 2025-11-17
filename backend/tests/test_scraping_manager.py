import pytest
from unittest.mock import Mock, patch
from app.services.scraping_manager import ScrapingManager, ScrapingError
from app.models.article import Article
from pytest_mock import MockerFixture

# --- Fixtures de Teste (Ambiente Controlado) ---

@pytest.fixture
def mock_articledb_class(mocker: MockerFixture):
    """
    Mocka a *classe* ArticleDB *antes* que o ScrapingManager
    tente inicializá-la em seu __init__.
    """
    # Esta parte estava correta e continua igual.
    return mocker.patch("app.services.scraping_manager.ArticleDB")

@pytest.fixture
def mock_scraper_instance(mocker: MockerFixture):
    """
    Cria uma *instância de mock* de um scraper (ex: G1Scraper).
    É este objeto que vamos controlar nos testes.
    """
    return mocker.Mock()

@pytest.fixture
def manager(
    mocker: MockerFixture, 
    mock_articledb_class: Mock, 
    mock_scraper_instance: Mock
) -> ScrapingManager:
    """
    Retorna uma instância do ScrapingManager.
    
    [A GRANDE MUDANÇA]: Nós usamos 'mocker.patch.dict' para
    hackear o dicionário 'ScrapingManager.SCRAPERS' e injetar
    um mock da *classe* do scraper, que por sua vez retorna
    a *instância* do mock que controlamos.
    """
    
    # 1. Cria um mock de "Classe"
    # Quando o código chamar scraper_class(), ele vai retornar nossa instância
    mock_scraper_class = mocker.Mock(return_value=mock_scraper_instance)
    
    # 2. Injeta o mock da classe no dicionário
    mocker.patch.dict(
        ScrapingManager.SCRAPERS, 
        {"g1.globo.com": mock_scraper_class}
    )
    
    # 3. Agora, quando ScrapingManager() for criado, ele usará
    # o mock_articledb_class. E quando scrape_and_save() for chamado,
    # ele usará o mock_scraper_class.
    return ScrapingManager()


@pytest.fixture
def sample_article():
    """Retorna um objeto Article de exemplo para os mocks."""
    return Article(
        id=123,
        url="https://g1.globo.com/artigo-teste",
        title="Título Teste",
        author="Autor Teste",
        content="Conteúdo do artigo."
    )

# --- Testes (Agora corrigidos para usar a fixture correta) ---

def test_scrape_and_save_success_caminho_feliz(
    manager: ScrapingManager,
    mock_articledb_class: Mock,
    mock_scraper_instance: Mock,  # <-- Mudança aqui
    sample_article: Article
):
    """
    Testa o "caminho feliz":
    1. URL é do G1
    2. Artigo não existe no DB
    3. Scraping funciona
    4. Salvar no DB funciona
    """
    # 1. Configuração dos Mocks
    url = "https://g1.globo.com/artigo-teste"
    mock_db = mock_articledb_class.return_value
    
    mock_db.get_article_by_url.return_value = None # Artigo não existe
    # Configura o mock da *instância* que será usada
    mock_scraper_instance.scrape.return_value = sample_article # Scraping funciona
    mock_db.save_article.return_value = 123 # Salvar funciona

    # 2. Execução
    article_id, created = manager.scrape_and_save(url)

    # 3. Verificação
    assert article_id == 123
    assert created is True
    mock_db.get_article_by_url.assert_called_once_with(url)
    mock_scraper_instance.scrape.assert_called_once_with(url) # <-- Mudança aqui
    mock_db.save_article.assert_called_once_with(sample_article)

def test_scrape_and_save_unsupported_url(manager: ScrapingManager):
    """
    Testa se uma URL não suportada (que não está no `SCRAPERS`)
    levanta um ValueError.
    """
    url = "http://fontedesconhecida.com/noticia"
    
    with pytest.raises(ValueError, match="Fonte de URL não suportada"):
        manager.scrape_and_save(url)

def test_scrape_and_save_article_already_exists(
    manager: ScrapingManager,
    mock_articledb_class: Mock,
    mock_scraper_instance: Mock, # <-- Mudança aqui
    sample_article: Article
):
    """
    Testa se o manager retorna (ID, False) se o artigo já
    existe no banco, sem tentar o scraping.
    """
    # 1. Configuração
    url = "https://g1.globo.com/artigo-teste"
    mock_db = mock_articledb_class.return_value

    # Simula que o artigo JÁ EXISTE no DB
    mock_db.get_article_by_url.return_value = sample_article

    # 2. Execução
    article_id, created = manager.scrape_and_save(url)

    # 3. Verificação
    assert article_id == 123
    assert created is False
    mock_db.get_article_by_url.assert_called_once_with(url)
    # Garante que NENHUM scraping ou save foi tentado
    mock_scraper_instance.scrape.assert_not_called() # <-- Mudança aqui
    mock_db.save_article.assert_not_called()

def test_scrape_and_save_scraping_fails_returns_none(
    manager: ScrapingManager,
    mock_articledb_class: Mock,
    mock_scraper_instance: Mock # <-- Mudança aqui
):
    """
    Testa se o scraper.scrape() falhar (retornando None),
    uma ScrapingError é levantada.
    """
    # 1. Configuração
    url = "https://g1.globo.com/artigo-quebrado"
    mock_db = mock_articledb_class.return_value
    
    mock_db.get_article_by_url.return_value = None # Artigo não existe
    mock_scraper_instance.scrape.return_value = None # Scraping FALHA

    # 2. Execução & Verificação
    with pytest.raises(ScrapingError, match="Não foi possível extrair"):
        manager.scrape_and_save(url)

def test_scrape_and_save_scraping_raises_exception(
    manager: ScrapingManager,
    mock_articledb_class: Mock,
    mock_scraper_instance: Mock # <-- Mudança aqui
):
    """
    Testa se o scraper.scrape() levantar uma exceção,
    ela é capturada e re-levantada como ScrapingError.
    """
    # 1. Configuração
    url = "https://g1.globo.com/artigo-quebrado"
    mock_db = mock_articledb_class.return_value
    
    mock_db.get_article_by_url.return_value = None # Artigo não existe
    # Simula o scraper levantando um erro (ex: falha de rede)
    mock_scraper_instance.scrape.side_effect = Exception("Falha de rede simulada")

    # 2. Execução & Verificação
    with pytest.raises(ScrapingError, match="Falha no scraping: Falha de rede"):
        manager.scrape_and_save(url)

def test_scrape_and_save_fails_on_save_race_condition(
    manager: ScrapingManager,
    mock_articledb_class: Mock,
    mock_scraper_instance: Mock, # <-- Mudança aqui
    sample_article: Article
):
    """
    Testa o caso de falha obscuro:
    1. Artigo não existe
    2. Scraping funciona
    3. `save_article` falha (retorna None)
    4. `get_article_by_url` (2ª chamada) AINDA não encontra (None)
    5. Deve levantar ScrapingError
    """
    # 1. Configuração
    url = "https://g1.globo.com/artigo-teste"
    mock_db = mock_articledb_class.return_value
    
    mock_db.get_article_by_url.return_value = None # 1ª chamada (não existe)
    mock_scraper_instance.scrape.return_value = sample_article # Scraping funciona
    mock_db.save_article.return_value = None # Salvar FALHA
    # A 2ª chamada ao get_article_by_url (verificação) também falha
    # (o mock já está configurado para retornar None)

    # 2. Execução & Verificação
    with pytest.raises(ScrapingError, match="Falha ao salvar o artigo no banco"):
        manager.scrape_and_save(url)
    
    # Garante que o get_article_by_url foi chamado DUAS VEZES
    assert mock_db.get_article_by_url.call_count == 2