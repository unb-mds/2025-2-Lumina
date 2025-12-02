import pytest
from playwright.sync_api import Page, expect

# URL base do seu site local
BASE_URL = "http://127.0.0.1:8000"

def test_admin_login_flow(page: Page):
    """
    Testa o fluxo completo de login:
    1. Acessa a página
    2. Tenta senha errada
    3. Tenta senha certa
    4. Verifica redirecionamento
    """
    # 1. Acessar a página de login
    page.goto(f"{BASE_URL}/admin")
    
    # Verifica se o título está correto
    expect(page).to_have_title("Lumina Admin Page")
    expect(page.locator("h2")).to_contain_text("Login de Administrador")

    # 2. Tentar senha errada
    page.fill("input[name='password']", "senha_errada_123")
    page.click("button[type='submit']")
    
    # Espera ver a mensagem de erro
    expect(page.locator(".error-message")).to_be_visible()
    expect(page.locator(".error-message")).to_contain_text("Senha incorreta")

    # 3. Tentar senha certa (admin)
    page.fill("input[name='password']", "admin")
    page.click("button[type='submit']")

    # 4. Verificar se entrou no Dashboard
    # Espera a URL mudar ou um elemento exclusivo do dashboard aparecer
    expect(page).to_have_url(f"{BASE_URL}/admin/dashboard")
    expect(page.locator(".welcome-text")).to_contain_text("Bem-vindo")

def test_dashboard_visual_elements(page: Page):
    """
    Testa se os elementos visuais (Cards, Badges, Tabela) estão carregando.
    Precisa estar logado.
    """
    # --- Setup de Login Rápido ---
    page.goto(f"{BASE_URL}/admin")
    page.fill("input[name='password']", "admin")
    page.click("button[type='submit']")
    # -----------------------------

    # 1. Verifica se os Cards de Estatística estão lá
    expect(page.locator(".stats-container")).to_be_visible()
    
    # Verifica se temos os 3 cards (Total, G1, Metro)
    cards = page.locator(".stat-card")
    expect(cards).to_have_count(3)
    
    # Verifica cores (classes CSS)
    expect(page.locator(".card-g1")).to_be_visible()
    expect(page.locator(".card-metro")).to_be_visible()

    # 2. Verifica a Tabela com Scroll
    expect(page.locator(".table-wrapper")).to_be_visible()
    
    # 3. Verifica se as Badges (Etiquetas) estão aparecendo
    # Nota: Isso depende de ter dados no banco. Se tiver vazio, este teste pode falhar.
    # Vamos verificar se a tabela existe, pelo menos.
    expect(page.locator("table.artigos-table")).to_be_visible()

def test_add_article_interaction(page: Page):
    """
    Testa a interação com o formulário de adicionar artigo.
    Não vamos submeter de verdade para não sujar o banco, mas vamos testar os campos.
    """
    # --- Setup de Login ---
    page.goto(f"{BASE_URL}/admin")
    page.fill("input[name='password']", "admin")
    page.click("button[type='submit']")
    # ---------------------

    # Localiza o input de URL
    input_url = page.locator("input#link_artigo")
    
    # Verifica se está visível e vazio
    expect(input_url).to_be_visible()
    expect(input_url).to_be_empty()

    # Digita algo
    input_url.fill("https://teste.com")
    
    # Verifica se o valor foi preenchido
    expect(input_url).to_have_value("https://teste.com")
    
    # Verifica se o botão tem o emoji e o texto correto
    btn = page.locator(".btn-add-source")
    expect(btn).to_contain_text("Adicionar Fonte")