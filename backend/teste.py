from urllib.parse import urlparse, urlunparse
import logging

# Configuração opcional de logging para ver avisos ou erros
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_url(url: str) -> str:
    """
    Remove a query string (parte após '?') de uma URL, preservando o fragmento ('#').

    Args:
        url: A string da URL a ser limpa.

    Returns:
        A URL sem a query string. Se a URL não tiver query string ou
        se a entrada for inválida, retorna a URL original.
    """
    if not isinstance(url, str):
        logger.warning(f"Entrada não é uma string, retornando como está: {url}")
        return url

    try:
        # 1. Parseia a URL em seus componentes
        parsed_url = urlparse(url)

        # 2. Reconstrói a URL usando urlunparse, passando uma string vazia
        #    para o componente 'query' (índice 4).
        #    A ordem dos componentes é: (scheme, netloc, path, params, query, fragment)
        cleaned_url = urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            '',  # <--- Remove a query string aqui
            ''
        ))
        return cleaned_url
    except ValueError:
        # Trata erros de parsing, embora urlparse seja robusto
        logger.error(f"Falha ao parsear a URL: {url}")
        return url # Retorna a URL original em caso de erro

# --- Exemplos de Uso ---
urls_to_test = [
    "https://g1.globo.com/sp/page.ghtml?utm_source=facebook&param=value",
    "https://g1.globo.com/no-query.html",
    "https://g1.globo.com/only-fragment.html#section1",
    "https://g1.globo.com/both.ghtml?query=1#fragment2",
    "http://example.com/path?a=1&b=2",
    "/relative/path?query=yes#frag", # urlparse lida bem com caminhos relativos
    "invalid-url-format"
]

for test_url in urls_to_test:
    print(f"Original: {test_url}")
    print(f"Limpada:  {clean_url(test_url)}\n")