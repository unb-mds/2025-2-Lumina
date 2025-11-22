import pytest
from bs4 import BeautifulSoup
from unittest.mock import MagicMock
from app.webcrawler.Metropoles.metroscraper import MetroScraper

@pytest.fixture
def scraper():
    return MetroScraper()

class TestMetroScraper:

    # --- Testes de is_article_page ---

    def test_is_article_page_true(self, scraper):
        """Deve retornar True se a meta tag article:section existir."""
        html = '<html><head><meta property="article:section" content="Brasil"></head></html>'
        soup = BeautifulSoup(html, "html.parser")
        assert scraper.is_article_page(soup) is True

    def test_is_article_page_false(self, scraper):
        """Deve retornar False se a meta tag não existir."""
        html = '<html><head><meta name="description" content="Site"></head></html>'
        soup = BeautifulSoup(html, "html.parser")
        assert scraper.is_article_page(soup) is False

    def test_is_article_page_exception(self, scraper, mocker):
        """Deve capturar exceção e retornar False."""
        mock_soup = MagicMock()
        # Simula erro ao chamar .find()
        mock_soup.find.side_effect = Exception("Erro de parse")
        
        assert scraper.is_article_page(mock_soup) is False

    # --- Testes de _extract_title ---

    def test_extract_title_strategy_1_wrapper(self, scraper):
        """Tentativa 1: HeaderNoticiaWrapper com H1 e H2."""
        html = """
        <div class="HeaderNoticiaWrapper__Categoria-sc-123">
            <h1>Título Principal</h1>
            <h2>Subtítulo</h2>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        assert scraper._extract_title(soup) == "Título Principal - Subtítulo"

    def test_extract_title_strategy_1_wrapper_h1_only(self, scraper):
        """Tentativa 1: HeaderNoticiaWrapper apenas com H1."""
        html = """
        <div class="HeaderNoticiaWrapper__Categoria-sc-123">
            <h1>Título Sozinho</h1>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        assert scraper._extract_title(soup) == "Título Sozinho"

    def test_extract_title_strategy_1_wrapper_h2_only(self, scraper):
        """
        Tentativa 1: HeaderNoticiaWrapper apenas com H2 (sem H1).
        Cobre o 'elif subtitle_text:' (linhas 66-67).
        """
        html = """
        <div class="HeaderNoticiaWrapper__Categoria-sc-123">
            <h2>Subtítulo vira Título</h2>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        assert scraper._extract_title(soup) == "Subtítulo vira Título"

    def test_extract_title_strategy_2_og_title(self, scraper):
        """Tentativa 2: Meta og:title (quando a tentativa 1 falha)."""
        html = """
        <html>
            <head><meta property="og:title" content="Título via Meta"></head>
            <body><div>Nada aqui</div></body>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        assert scraper._extract_title(soup) == "Título via Meta"

    def test_extract_title_strategy_3_title_tag(self, scraper):
        """Tentativa 3: Tag <title> (limpando o sufixo)."""
        html = """
        <html>
            <head><title>Título da Tag | Metrópoles</title></head>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        assert scraper._extract_title(soup) == "Título da Tag"

    def test_extract_title_failure(self, scraper):
        """Nenhuma estratégia funciona."""
        html = "<html><body></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        assert scraper._extract_title(soup) == ""

    # --- Testes de _extract_authors ---

    def test_extract_authors_strategy_1_wrapper_links(self, scraper):
        """Tentativa 1: HeaderNoticiaWrapper com links <a>."""
        html = """
        <div class="HeaderNoticiaWrapper__Autor-sc-123">
            <a href="#">Autor 1</a>
            <a href="#">Autor 2</a>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        assert scraper._extract_authors(soup) == "Autor 1, Autor 2"

    def test_extract_authors_strategy_1_wrapper_text(self, scraper):
        """Tentativa 1: HeaderNoticiaWrapper apenas texto."""
        html = """
        <div class="HeaderNoticiaWrapper__Autor-sc-123">
            Texto do Autor
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        assert scraper._extract_authors(soup) == "Texto do Autor"

    def test_extract_authors_strategy_2_meta(self, scraper):
        """Tentativa 2: Meta author."""
        html = '<meta name="author" content="Meta Autor">'
        soup = BeautifulSoup(html, "html.parser")
        assert scraper._extract_authors(soup) == "Meta Autor"

    def test_extract_authors_strategy_3_generic(self, scraper):
        """Tentativa 3: Classe genérica (testando limpeza do 'Por ')."""
        html = '<div class="author-name">Por Redação</div>'
        soup = BeautifulSoup(html, "html.parser")
        assert scraper._extract_authors(soup) == "Redação"

    def test_extract_authors_failure(self, scraper):
        html = "<html></html>"
        soup = BeautifulSoup(html, "html.parser")
        assert scraper._extract_authors(soup) == ""

    # --- Testes de _extract_body ---

    def test_extract_body_strategy_1_wrapper(self, scraper):
        """Tentativa 1: ConteudoNoticiaWrapper."""
        html = """
        <div class="ConteudoNoticiaWrapper__Artigo-sc-123">
            <p>Parágrafo 1.</p>
            <p>Parágrafo 2.</p>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        expected = "Parágrafo 1.\n\nParágrafo 2."
        assert scraper._extract_body(soup) == expected

    def test_extract_body_strategy_2_article_tag(self, scraper):
        """Tentativa 2: Tag <article>."""
        html = """
        <article>
            <p>Texto Article.</p>
        </article>
        """
        soup = BeautifulSoup(html, "html.parser")
        assert scraper._extract_body(soup) == "Texto Article."

    def test_extract_body_strategy_3_generic(self, scraper):
        """Tentativa 3: Classe genérica 'materia'."""
        html = """
        <div class="materia-body">
            <p>Texto Genérico.</p>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        assert scraper._extract_body(soup) == "Texto Genérico."

    def test_extract_body_fallback_no_paragraphs(self, scraper):
        """Fallback: Container encontrado mas sem <p>, usa get_text."""
        html = """
        <article>
            Texto solto sem parágrafo.
        </article>
        """
        soup = BeautifulSoup(html, "html.parser")
        assert scraper._extract_body(soup) == "Texto solto sem parágrafo."

    def test_extract_body_failure(self, scraper):
        html = "<html></html>"
        soup = BeautifulSoup(html, "html.parser")
        assert scraper._extract_body(soup) == ""

    def test_extract_body_exception_inside_extraction(self, scraper, mocker):
        """
        Simula erro durante a extração dos parágrafos (find_all falhando)
        após ter encontrado o container.
        """
        html = "<article><p>teste</p></article>"
        soup = BeautifulSoup(html, "html.parser")
        
        # Mockando find_all do elemento article encontrado
        # O find retorna um objeto, precisamos mockar esse objeto
        mock_element = MagicMock()
        mock_element.find_all.side_effect = Exception("Erro ao buscar P")
        
        # Forçamos o find("article") a retornar nosso mock
        mocker.patch.object(soup, 'find', return_value=mock_element)
        
        # Como estamos testando a lógica interna, precisamos garantir que o find("article") seja chamado
        # A estratégia 1 vai falhar (não tem wrapper), a 2 vai achar nosso mock
        assert scraper._extract_body(soup) == ""


    # --- Teste de Integração: scrape_article ---

    def test_scrape_article_success(self, scraper):
        """Testa o fluxo completo com sucesso."""
        html = """
        <html>
            <head><meta property="og:title" content="Título Completo"></head>
            <body>
                <div class="author">João</div>
                <article><p>Conteúdo Real.</p></article>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        # Usamos HTTPS para evitar redirecionamentos ou normalizações extras, 
        # mas o ponto chave é converter para string na assertiva.
        url = "https://fake.url"
        
        article = scraper.scrape_article(url, soup)
        
        assert article is not None
        assert article.title == "Título Completo"
        assert article.author == "João"
        assert article.content == "Conteúdo Real."
        # CORREÇÃO: Converter o HttpUrl para string antes de comparar
        # E normalizar a barra final que o Pydantic adiciona
        assert str(article.url).rstrip("/") == url.rstrip("/")

    def test_scrape_article_missing_title(self, scraper):
        """Deve retornar None se não achar título (campo obrigatório)."""
        html = "<html><body><article><p>Tem corpo mas não tem título</p></article></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        
        assert scraper.scrape_article("url", soup) is None

    def test_scrape_article_missing_content(self, scraper):
        """Deve retornar None se não achar corpo (campo obrigatório)."""
        html = "<html><head><title>Tem Título</title></head><body></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        
        assert scraper.scrape_article("url", soup) is None

    # --- Testes de Cobertura de Exceções (Forçando erros nos Try/Except) ---
    
    def test_extract_title_exceptions(self, scraper, mocker):
        """Força exceções em todas as tentativas de título para cobrir os logs de warning."""
        mock_soup = MagicMock()
        mock_soup.find.side_effect = Exception("Boom!")
        
        # O resultado deve ser vazio, mas o log deve registrar os warnings (testado implicitamente pela cobertura)
        assert scraper._extract_title(mock_soup) == ""

    def test_extract_authors_exceptions(self, scraper, mocker):
        """Força exceções em todas as tentativas de autor."""
        mock_soup = MagicMock()
        mock_soup.find.side_effect = Exception("Boom!")
        assert scraper._extract_authors(mock_soup) == ""

    def test_extract_body_exceptions(self, scraper, mocker):
        """Força exceções em todas as tentativas de corpo."""
        mock_soup = MagicMock()
        mock_soup.find.side_effect = Exception("Boom!")
        assert scraper._extract_body(mock_soup) == ""