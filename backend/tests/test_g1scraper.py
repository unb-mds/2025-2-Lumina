import pytest
from bs4 import BeautifulSoup
from app.webcrawler.G1.g1scraper import G1Scraper

@pytest.fixture
def scraper():
    """Fixture que retorna uma instância do scraper para ser usada nos testes."""
    return G1Scraper()

class TestG1Scraper:

    # --- Testes de _extract_body_text ---

    def test_extract_body_text_with_paragraphs(self, scraper):
        """
        Testa a extração quando existem tags <p> com a classe específica 'content-text__container'.
        Deve ignorar parágrafos vazios ou sem a classe correta.
        """
        html = """
        <div class="mc-article-body">
            <p class="content-text__container">Parágrafo 1.</p>
            <p class="outra-classe">Ignorar este.</p>
            <p class="content-text__container"></p> <!-- Vazio, deve ignorar -->
            <p class="content-text__container">Parágrafo 2.</p>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        container = soup.find("div")
        
        expected = "Parágrafo 1.\n\nParágrafo 2."
        assert scraper._extract_body_text(container) == expected

    def test_extract_body_text_fallback(self, scraper):
        """
        Testa o fallback: quando não encontra os <p> específicos, 
        deve retornar todo o texto do container.
        """
        html = """
        <div class="mc-article-body">
            Texto solto sem parágrafos estruturados.
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        container = soup.find("div")
        
        assert scraper._extract_body_text(container) == "Texto solto sem parágrafos estruturados."

    # --- Testes de scrape_article ---

    def test_scrape_article_success_full(self, scraper):
        """
        Cenário feliz: Título, Autor e Corpo presentes.
        """
        html = """
        <html>
            <body>
                <h1 class="content-head__title">Título da Notícia</h1>
                <div class="content-publication-data__from">Por Redação G1</div>
                <div class="mc-article-body">
                    <p class="content-text__container">Conteúdo do texto.</p>
                </div>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        url = "https://g1.globo.com/teste.ghtml"
        
        article = scraper.scrape_article(url, soup)
        
        assert article is not None
        assert article.title == "Título da Notícia"
        assert article.author == "Por Redação G1"
        assert article.content == "Conteúdo do texto."
        # Normaliza URL para comparação (Pydantic adiciona / no final do domínio)
        assert str(article.url).rstrip("/") == url.rstrip("/")

    def test_scrape_article_success_missing_author(self, scraper, caplog):
        """
        Cenário feliz parcial: Título e Corpo presentes, mas Autor faltando.
        Deve criar o artigo com autor vazio e logar DEBUG.
        """
        html = """
        <html>
            <body>
                <h1 class="content-head__title">Título Sem Autor</h1>
                <!-- Autor faltando -->
                <div class="mc-article-body">Texto</div>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        
        with caplog.at_level("DEBUG"):
            # CORREÇÃO: Usar URL válida para passar na validação do Pydantic
            article = scraper.scrape_article("http://fake.url", soup)
        
        assert article is not None
        assert article.title == "Título Sem Autor"
        assert article.author == "" # Autor vazio
        
        # Verifica se o log de debug foi acionado para o elemento faltante
        assert "Elemento 'author'" in caplog.text
        assert "não encontrado" in caplog.text

    def test_scrape_article_failure_missing_title(self, scraper, caplog):
        """
        Falha crítica: Corpo presente, mas Título faltando.
        Deve retornar None e logar ERROR.
        """
        html = """
        <html>
            <body>
                <!-- Título faltando -->
                <div class="mc-article-body">Texto</div>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        
        # CORREÇÃO: Usar URL válida
        article = scraper.scrape_article("http://fake.url", soup)
        
        assert article is None
        assert "Elemento crítico faltando: title" in caplog.text

    def test_scrape_article_failure_missing_body(self, scraper, caplog):
        """
        Falha crítica: Título presente, mas Corpo faltando.
        Deve retornar None e logar ERROR.
        """
        html = """
        <html>
            <body>
                <h1 class="content-head__title">Título</h1>
                <!-- Corpo faltando -->
            </body>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        
        # CORREÇÃO: Usar URL válida
        article = scraper.scrape_article("http://fake.url", soup)
        
        assert article is None
        assert "Elemento crítico faltando: body" in caplog.text