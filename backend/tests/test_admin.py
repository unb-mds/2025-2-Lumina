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
        follow_redirects=False # Não segue o redirect para verificarmos o status 302
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
def test_dashboard_content_render(MockArticleDB):
    """
    Acessa o dashboard logado e verifica se os dados do banco 
    estão sendo exibidos na tela HTML.
    """
    # Configura o Mock do Banco
    mock_instance = MockArticleDB.return_value
    
    # Simula dois artigos retornados pelo get_all_articles
    mock_instance.get_all_articles.return_value = [
        MagicMock(id=1, title="Notícia Fake G1", url="http://g1.com/1", author="G1 Bot"),
        MagicMock(id=2, title="Notícia Fake Metro", url="http://metro.com/2", author="Metro Bot")
    ]
    
    # Loga manualmente
    client.cookies.set("admin_logged_in", "true")

    # Faz a requisição
    response = client.get("/admin/dashboard")

    # Asserções
    assert response.status_code == 200
    assert "Notícia Fake G1" in response.text
    assert "Notícia Fake Metro" in response.text
    # Como o dashboard chama o banco duas vezes (uma pra cada DB), verificamos se foi chamado
    assert mock_instance.get_all_articles.call_count >= 1

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

    # --- CORREÇÃO AQUI: Usar a nova rota com source_db ---
    # Simulamos deletar do banco 'articles.db' o ID 50
    response = client.get(
        "/admin/article/delete/articles.db/50", 
        follow_redirects=False
    )

    assert response.status_code == 302 # Deve redirecionar para atualizar a página
    mock_instance.delete_article.assert_called_with(50)