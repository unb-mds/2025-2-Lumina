import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app

# Cria o cliente de teste
client = TestClient(app)

# Credencial definida no código (admin.py)
ADMIN_PASSWORD = "admin"

# --- Testes de Interface (Login) ---

def test_admin_login_page_load():
    """Testa se a página de login carrega corretamente (GET)."""
    response = client.get("/admin")
    assert response.status_code == 200
    assert "Login de Administrador" in response.text

def test_admin_login_success():
    """Testa o login com senha correta."""
    response = client.post(
        "/admin/login", 
        data={"password": ADMIN_PASSWORD},
        follow_redirects=False 
    )
    assert response.status_code == 302
    assert "/admin/dashboard" in response.headers["location"]
    assert "admin_logged_in" in response.cookies

def test_admin_login_failure():
    """Testa o login com senha incorreta."""
    response = client.post(
        "/admin/login", 
        data={"password": "senhaerrada"}
    )
    assert response.status_code == 200 
    assert "Senha incorreta" in response.text

def test_admin_logout():
    """Testa se o logout remove o cookie."""
    client.post("/admin/login", data={"password": ADMIN_PASSWORD})
    response = client.get("/admin/logout", follow_redirects=False)
    assert response.status_code == 302
    assert "/admin" in response.headers["location"]

# --- Testes do Dashboard ---

def test_dashboard_access_denied_without_cookie():
    """Tenta acessar o dashboard sem estar logado."""
    client.cookies.clear() 
    response = client.get("/admin/dashboard", follow_redirects=False)
    assert response.status_code == 302
    assert "/admin" in response.headers["location"]

@patch("app.routers.admin.ArticleDB")
def test_dashboard_content_and_stats(MockArticleDB):
    """
    Testa se o dashboard exibe:
    1. A lista de artigos.
    2. Os Cards de Estatística (KPIs).
    """
    # Configura o Mock do Banco
    mock_instance = MockArticleDB.return_value
    
    # O admin.py chama o banco duas vezes (uma para G1, outra para Metrópoles)
    # Vamos simular que o primeiro banco retorna 2 artigos e o segundo retorna 1
    # Total esperado: 3
    mock_instance.get_all_articles.side_effect = [
        [
            MagicMock(id=1, title="Notícia G1 A", url="http://g1.com/1", author="Bot G1"),
            MagicMock(id=2, title="Notícia G1 B", url="http://g1.com/2", author="Bot G1")
        ],
        [
            MagicMock(id=3, title="Notícia Metro", url="http://metro.com/3", author="Bot Metro")
        ]
    ]
    
    # Loga manualmente
    client.cookies.set("admin_logged_in", "true")

    # Faz a requisição
    response = client.get("/admin/dashboard")

    # Asserções de Status
    assert response.status_code == 200
    
    # Asserções de Conteúdo (Tabela)
    assert "Notícia G1 A" in response.text
    assert "Notícia Metro" in response.text
    
    # Asserções dos Novos Cards (Visual Check)
    assert "Total de Artigos" in response.text
    assert "Fonte: G1" in response.text
    assert "Fonte: Metrópoles" in response.text
    
    # Verifica se os números dos cards estão corretos (2 do G1 + 1 do Metro = 3 Total)
    # O HTML deve conter os números soltos dentro das tags <p>
    assert ">3</p>" in response.text # Total
    assert ">2</p>" in response.text # G1
    assert ">1</p>" in response.text # Metro

# --- Testes de Ações (Adicionar/Remover) ---

@patch("app.routers.admin.ScrapingManager")
def test_admin_add_article_flow(MockScrapingManager):
    """Testa o fluxo de adicionar artigo via formulário Admin."""
    mock_instance = MockScrapingManager.return_value
    mock_instance.scrape_and_save.return_value = (10, True)

    client.cookies.set("admin_logged_in", "true")

    response = client.post(
        "/admin/article/add",
        data={"link_artigo": "http://g1.globo.com/teste-mock"},
        follow_redirects=False
    )

    assert response.status_code == 302 
    mock_instance.scrape_and_save.assert_called_with("http://g1.globo.com/teste-mock")

@patch("app.routers.admin.ArticleDB")
def test_admin_delete_article_flow(MockDB):
    """Testa o botão de 'Excluir' (X) na tabela."""
    mock_instance = MockDB.return_value
    
    client.cookies.set("admin_logged_in", "true")

    # Simulamos deletar do banco 'articles.db' o ID 50
    response = client.get(
        "/admin/article/delete/articles.db/50", 
        follow_redirects=False
    )

    assert response.status_code == 302 # Deve redirecionar
    # Verifica se instanciou o banco com o nome certo e chamou delete
    MockDB.assert_called_with(db_name="articles.db")
    mock_instance.delete_article.assert_called_with(50)