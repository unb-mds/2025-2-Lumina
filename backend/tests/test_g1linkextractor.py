import pytest
from bs4 import BeautifulSoup
from app.webcrawler.G1.g1linkextractor import G1LinkExtractor

@pytest.fixture
def extractor():
    """Fixture que retorna uma instância do extrator para ser usada nos testes."""
    return G1LinkExtractor()

class TestG1LinkExtractor:

    def test_initialization(self, extractor):
        """Testa se o domínio padrão está correto."""
        assert extractor.allowed_domain == "g1.globo.com"

    # --- Testes de clean_url ---

    def test_clean_url_removes_query_and_fragment(self, extractor):
        """Deve remover ?query e #fragment."""
        raw_url = "https://g1.globo.com/noticia.ghtml?utm_source=fb#comentarios"
        expected = "https://g1.globo.com/noticia.ghtml"
        assert extractor.clean_url(raw_url) == expected

    def test_clean_url_non_string_input(self, extractor, caplog):
        """Deve retornar o input original e logar aviso se não for string."""
        invalid_input = 12345
        result = extractor.clean_url(invalid_input)
        assert result == 12345
        assert "Entrada não é uma string" in caplog.text

    # --- Testes de _is_valid_url (Regras de Negócio) ---

    @pytest.mark.parametrize("url, expected_result, reason", [
        # Casos Válidos (Regra 3: .ghtml ou /)
        ("https://g1.globo.com/economia/noticia/2023/01/01/artigo.ghtml", True, "Artigo padrão .ghtml"),
        ("https://g1.globo.com/politica/", True, "Página de seção terminando em /"),

        # Regra 1: Esquema Inválido
        ("ftp://g1.globo.com/arquivo.ghtml", False, "Esquema FTP não permitido"),
        ("file:///C:/user/docs", False, "Esquema File não permitido"),

        # Regra 2: Domínio Externo
        ("https://www.google.com/search", False, "Domínio externo"),
        ("https://oglobo.globo.com/politica", False, "Outro portal (O Globo != G1)"),

        # Regra 3: Extensão/Caminho Inválido
        ("https://g1.globo.com/politica", False, "Não termina em / nem .ghtml"),
        ("https://g1.globo.com/imagem.jpg", False, "Arquivo de imagem"),
        ("https://g1.globo.com/podcast.mp3", False, "Arquivo de áudio"),
    ])
    def test_is_valid_url_rules(self, extractor, url, expected_result, reason):
        """Testa todas as 3 regras do motor de validação do G1."""
        assert extractor._is_valid_url(url) is expected_result, f"Falha em: {reason}"

    def test_is_valid_url_force_exception(self, extractor, mocker):
        """
        Simula um erro interno (ValueError) no urlparse para garantir que o bloco
        'except ValueError' seja executado.
        """
        # Substitui o urlparse APENAS dentro do módulo do G1LinkExtractor
        mocker.patch("app.webcrawler.G1.g1linkextractor.urlparse", side_effect=ValueError("Erro forçado"))
        
        result = extractor._is_valid_url("http://qualquer-url.com")
        
        assert result is False

    # --- Testes de extract (Integração BeautifulSoup) ---

    def test_extract_links_from_html(self, extractor):
        """Testa a extração, conversão de relativos e filtragem."""
        html_content = """
        <html>
            <body>
                <!-- Link Válido (Relativo) -->
                <a href="/rj/rio-de-janeiro/noticia/2023/artigo.ghtml">Matéria RJ</a>
                
                <!-- Link Válido (Absoluto) -->
                <a href="https://g1.globo.com/sp/sao-paulo/">Seção SP</a>

                <!-- Link Inválido (Externo) -->
                <a href="https://google.com">Google</a>

                <!-- Link Inválido (Extensão errada) -->
                <a href="https://g1.globo.com/foto.jpg">Foto</a>
                
                <!-- Link Inválido (Sem href) -->
                <a>Link quebrado</a>
            </body>
        </html>
        """
        soup = BeautifulSoup(html_content, "html.parser")
        
        extracted_links = extractor.extract(soup)

        expected_links = {
            "https://g1.globo.com/rj/rio-de-janeiro/noticia/2023/artigo.ghtml",
            "https://g1.globo.com/sp/sao-paulo/"
        }

        # Verifica se extraiu exatamente o que esperamos
        assert extracted_links == expected_links
        assert len(extracted_links) == 2