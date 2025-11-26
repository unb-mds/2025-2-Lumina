import pytest
from bs4 import BeautifulSoup
from app.webcrawler.Metropoles.metrolinkextractor import MetroLinkExtractor

@pytest.fixture
def extractor():
    """Fixture que retorna uma instância do extrator para ser usada nos testes."""
    return MetroLinkExtractor()

class TestMetroLinkExtractor:

    def test_initialization(self, extractor):
        """Testa se as configurações iniciais e listas de ignorados estão corretas."""
        assert extractor.allowed_domain == "www.metropoles.com"
        assert extractor.base_url == "https://www.metropoles.com"
        assert "/sobre" in extractor.IGNORED_PREFIXES
        assert ".jpg" in extractor.IGNORED_SUFFIXES
        assert "/" in extractor.IGNORED_PATHS

    # --- Testes de clean_url ---

    def test_clean_url_removes_query_and_fragment(self, extractor):
        """Deve remover ?query e #fragment."""
        raw_url = "https://www.metropoles.com/noticia?utm_source=fb#comentarios"
        expected = "https://www.metropoles.com/noticia"
        assert extractor.clean_url(raw_url) == expected

    def test_clean_url_non_string_input(self, extractor, caplog):
        """Deve retornar o input original e logar aviso se não for string."""
        invalid_input = 12345
        result = extractor.clean_url(invalid_input)
        assert result == 12345
        assert "Entrada não é uma string" in caplog.text

    # --- Testes de _is_valid_url (Regras de Negócio) ---

    @pytest.mark.parametrize("url, expected_result, reason", [
        # Casos Válidos (Regra 6: Pelo menos 2 barras no path)
        ("https://www.metropoles.com/brasil/politica/noticia-1", True, "URL válida profunda"),
        ("https://www.metropoles.com/mundo/guerra", True, "URL válida"),

        # Regra 1: Esquema Inválido
        ("ftp://www.metropoles.com/brasil/noticia", False, "Esquema FTP não permitido"),
        ("file:///C:/user/docs", False, "Esquema File não permitido"),

        # Regra 2: Domínio Externo
        ("https://www.google.com/search", False, "Domínio externo"),
        ("https://g1.globo.com/politica", False, "Outro portal de notícia"),

        # Regra 3: Caminhos Exatos Ignorados
        ("https://www.metropoles.com/", False, "Homepage exata ignorada"),
        ("https://www.metropoles.com", False, "Homepage sem barra (path vazio/raiz)"),

        # Regra 4: Prefixos Ignorados
        ("https://www.metropoles.com/sobre", False, "Página Sobre"),
        ("https://www.metropoles.com/fale-conosco/envie", False, "Subpágina de serviço"),
        ("https://www.metropoles.com/autores/joao-silva", False, "Página de autor"),

        # Regra 5: Sufixos de Arquivo Ignorados
        ("https://www.metropoles.com/imagem.jpg", False, "Imagem JPG"),
        ("https://www.metropoles.com/documento.pdf", False, "Documento PDF"),

        # Regra 6: Profundidade do Caminho (path.count('/') < 2)
        ("https://www.metropoles.com/brasil", False, "Caminho muito curto (seção)"),
        ("https://www.metropoles.com/mundo", False, "Caminho muito curto (seção)"),
        
        # Caso de URL Malformada (Cai no except ValueError)
        ("http://[::1]:80", False, "URL IPv6 malformada ou estranha para o parser"),
    ])
    def test_is_valid_url_rules(self, extractor, url, expected_result, reason):
        """Testa todas as 6 regras do motor de validação."""
        assert extractor._is_valid_url(url) is expected_result, f"Falha em: {reason}"

    def test_is_valid_url_force_exception(self, extractor, mocker):
        """
        Simula um erro interno (ValueError) no urlparse para garantir que o bloco
        'except ValueError' seja executado e coberto pelos testes.
        """
        # Substitui a função urlparse importada no módulo alvo por um Mock que sempre falha
        mocker.patch("app.webcrawler.Metropoles.metrolinkextractor.urlparse", side_effect=ValueError("Erro forçado"))
        
        result = extractor._is_valid_url("http://qualquer-url.com")
        
        # O método deve capturar o erro, logar e retornar False
        assert result is False

    # --- Testes de extract (Integração BeautifulSoup) ---

    def test_extract_links_from_html(self, extractor):
        """Testa a extração, conversão de relativos e filtragem."""
        html_content = """
        <html>
            <body>
                <!-- Link Válido (Relativo) -->
                <a href="/brasil/politica/artigo-importante">Matéria 1</a>
                
                <!-- Link Válido (Absoluto) -->
                <a href="https://www.metropoles.com/mundo/guerra/artigo-2">Matéria 2</a>

                <!-- Link Inválido (Externo) -->
                <a href="https://google.com">Google</a>

                <!-- Link Inválido (Serviço/Ignorado) -->
                <a href="/sobre/nos">Sobre</a>

                <!-- Link Inválido (Arquivo) -->
                <a href="/images/foto.jpg">Foto</a>
                
                <!-- Link Inválido (Sem href) -->
                <a>Link quebrado</a>
            </body>
        </html>
        """
        soup = BeautifulSoup(html_content, "html.parser")
        
        extracted_links = extractor.extract(soup)

        expected_links = {
            "https://www.metropoles.com/brasil/politica/artigo-importante",
            "https://www.metropoles.com/mundo/guerra/artigo-2"
        }

        # Verifica se extraiu exatamente o que esperamos
        assert extracted_links == expected_links
        assert len(extracted_links) == 2