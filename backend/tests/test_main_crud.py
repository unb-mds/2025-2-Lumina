import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

# Importe o 'app' e os modelos/exceções necessários.
# Assumimos que o pytest é rodado da pasta 'backend/'.
from main import app
from app.models.article import Article
from app.services.scraping_manager import ScrapingError

# --- Fixtures (Configuração) ---

@pytest.fixture
def client():
    """Cria uma instância do TestClient para nossos testes."""
    return TestClient(app)

@pytest.fixture
def mock_article():
    """Retorna um objeto Article Pydantic padrão para usar nos testes."""
    return Article(
        id=1,
        title="Artigo de Teste",
        author="Autor Teste",
        url="http://example.com/teste",
        content="Conteúdo do teste...",
    )

# --- Testes CREATE (POST /article/add) ---
# Estes testes simulam o ScrapingManager, pois é ele que o endpoint chama.

def test_add_article_success_created(client, mocker):
    """Testa o (C)CREATE: Criação de um novo artigo (201 Created)"""
    # ARRANGE
    mock_manager = MagicMock()
    mock_manager.scrape_and_save.return_value = (1, True) # (article_id=1, created=True)
    # O patch é em 'main.ScrapingManager' pois é onde 'main.py' o importa
    mocker.patch("main.ScrapingManager", return_value=mock_manager)

    # ACT
    response = client.post("/article/add", json={"url": "http://example.com"})

    # ASSERT
    assert response.status_code == 201
    assert response.json() == {
        "message": "Artigo adicionado com sucesso!",
        "article_id": 1,
    }
    mock_manager.scrape_and_save.assert_called_with("http://example.com/")


def test_add_article_success_already_exists(client, mocker):
    """Testa o (C)CREATE: Artigo já existe (200 OK)"""
    # ARRANGE
    mock_manager = MagicMock()
    mock_manager.scrape_and_save.return_value = (2, False) # (article_id=2, created=False)
    mocker.patch("main.ScrapingManager", return_value=mock_manager)

    # ACT
    response = client.post("/article/add", json={"url": "http://example.com/2"})

    # ASSERT
    assert response.status_code == 200
    assert response.json() == {
        "message": "O artigo já existe no banco de dados.",
        "article_id": 2,
    }


def test_add_article_unsupported_url(client, mocker):
    """Testa o (C)CREATE: Erro de fonte não suportada (422)"""
    # ARRANGE
    mock_manager = MagicMock()
    mock_manager.scrape_and_save.side_effect = ValueError("Fonte de URL não suportada.")
    mocker.patch("main.ScrapingManager", return_value=mock_manager)

    # ACT
    response = client.post("/article/add", json={"url": "http://unsupported.com"})

    # ASSERT
    assert response.status_code == 422
    assert response.json() == {"detail": "Fonte de URL não suportada."}


def test_add_article_scraping_error(client, mocker):
    """Testa o (C)CREATE: Erro genérico de scraping (500)"""
    # ARRANGE
    mock_manager = MagicMock()
    mock_manager.scrape_and_save.side_effect = ScrapingError("Falha ao baixar")
    mocker.patch("main.ScrapingManager", return_value=mock_manager)

    # ACT
    response = client.post("/article/add", json={"url": "http://example.com"})

    # ASSERT
    assert response.status_code == 500
    assert response.json() == {"detail": "Falha ao processar o artigo: Falha ao baixar"}


# --- Testes READ-All (GET /articles/) ---
# Estes testes simulam o ArticleDB

def test_get_all_articles_success(client, mock_article, mocker):
    """Testa o (R)READ-All: Retorna uma lista de artigos (200 OK)"""
    # ARRANGE
    mock_db = MagicMock()
    mock_db.get_all_articles.return_value = [mock_article, mock_article]
    mock_db.close.return_value = None
    mocker.patch("main.ArticleDB", return_value=mock_db) # Patch em 'main.ArticleDB'

    # ACT
    response = client.get("/articles/")

    # ASSERT
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["title"] == "Artigo de Teste"
    mock_db.get_all_articles.assert_called_once()
    mock_db.close.assert_called_once()


def test_get_all_articles_empty(client, mocker):
    """Testa o (R)READ-All: Retorna uma lista vazia (200 OK)"""
    # ARRANGE
    mock_db = MagicMock()
    mock_db.get_all_articles.return_value = [] # Lista vazia
    mock_db.close.return_value = None
    mocker.patch("main.ArticleDB", return_value=mock_db)

    # ACT
    response = client.get("/articles/")

    # ASSERT
    assert response.status_code == 200
    assert response.json() == []
    mock_db.get_all_articles.assert_called_once()
    mock_db.close.assert_called_once()


# --- Testes READ-One (GET /article/{id}) ---

def test_get_article_success(client, mock_article, mocker):
    """Testa o (R)READ-One: Artigo encontrado (200 OK)"""
    # ARRANGE
    mock_db = MagicMock()
    mock_db.get_article_by_id.return_value = mock_article
    mock_db.close.return_value = None
    mocker.patch("main.ArticleDB", return_value=mock_db)

    # ACT
    response = client.get("/article/1")

    # ASSERT
    assert response.status_code == 200
    data = response.json()
    # Verificamos se o Pydantic serializou corretamente
    assert data["id"] == 1 
    assert data["title"] == "Artigo de Teste"
    assert data["url"] == "http://example.com/teste"
    mock_db.get_article_by_id.assert_called_with(1)
    mock_db.close.assert_called_once()


def test_get_article_not_found(client, mocker):
    """Testa o (R)READ-One: Artigo não encontrado (404)"""
    # ARRANGE
    mock_db = MagicMock()
    mock_db.get_article_by_id.return_value = None # Não achou
    mock_db.close.return_value = None
    mocker.patch("main.ArticleDB", return_value=mock_db)

    # ACT
    response = client.get("/article/999")

    # ASSERT
    assert response.status_code == 404
    assert response.json() == {"detail": "Artigo não encontrado."}
    mock_db.get_article_by_id.assert_called_with(999)
    mock_db.close.assert_called_once()


# --- Testes UPDATE (PUT /article/{id}) ---

def test_update_article_success(client, mock_article, mocker):
    """Testa o (U)UPDATE: Atualização bem-sucedida (200 OK)"""
    # ARRANGE
    payload = {"title": "Novo Título", "author": "Novo Autor"}
    
    # Criamos uma cópia do mock e aplicamos a mudança
    updated_article = mock_article.model_copy(update=payload)

    mock_db = MagicMock()
    mock_db.update_article.return_value = updated_article
    mock_db.close.return_value = None
    mocker.patch("main.ArticleDB", return_value=mock_db)

    # ACT
    response = client.put("/article/1", json=payload)

    # ASSERT
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Novo Título" # Verifica o dado atualizado
    assert data["author"] == "Novo Autor"  # Verifica o dado atualizado
    
    # Verifica se o método do DB foi chamado com os dados corretos
    mock_db.update_article.assert_called_with(1, payload)
    mock_db.close.assert_called_once()


def test_update_article_not_found(client, mocker):
    """Testa o (U)UPDATE: Artigo não encontrado para atualizar (404)"""
    # ARRANGE
    payload = {"title": "Novo Título"}
    mock_db = MagicMock()
    mock_db.update_article.return_value = None # Não achou
    mock_db.close.return_value = None
    mocker.patch("main.ArticleDB", return_value=mock_db)

    # ACT
    response = client.put("/article/999", json=payload)

    # ASSERT
    assert response.status_code == 404
    assert response.json() == {"detail": "Artigo não encontrado para atualizar."}
    mock_db.update_article.assert_called_with(999, payload)
    mock_db.close.assert_called_once()


def test_update_article_bad_request_empty(client):
    """Testa o (U)UPDATE: Payload de atualização vazio (400)"""
    # ARRANGE
    payload = {} # Vazio, ou com campos "None"

    # ACT
    response = client.put("/article/1", json=payload)

    # ASSERT
    assert response.status_code == 400
    assert response.json() == {"detail": "Nenhum campo fornecido para atualização."}


# --- Testes DELETE (DELETE /article/{id}) ---

def test_delete_article_success(client, mocker):
    """Testa o (D)DELETE: Deleção bem-sucedida (200 OK)"""
    # ARRANGE
    mock_db = MagicMock()
    mock_db.delete_article.return_value = True # Sucesso
    mock_db.close.return_value = None
    mocker.patch("main.ArticleDB", return_value=mock_db)

    # ACT
    response = client.delete("/article/1")

    # ASSERT
    assert response.status_code == 200
    assert response.json() == {
        "message": "Artigo deletado com sucesso",
        "article_id": 1
    }
    mock_db.delete_article.assert_called_with(1)
    mock_db.close.assert_called_once()


def test_delete_article_not_found(client, mocker):
    """Testa o (D)DELETE: Artigo não encontrado para deletar (404)"""
    # ARRANGE
    mock_db = MagicMock()
    mock_db.delete_article.return_value = False # Não achou
    mock_db.close.return_value = None
    mocker.patch("main.ArticleDB", return_value=mock_db)

    # ACT
    response = client.delete("/article/999")

    # ASSERT
    assert response.status_code == 404
    assert response.json() == {"detail": "Artigo não encontrado para deletar."}
    mock_db.delete_article.assert_called_with(999)
    mock_db.close.assert_called_once()