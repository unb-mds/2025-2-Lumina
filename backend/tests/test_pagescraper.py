import pytest
from backend.app.models.pagescraper import PageScraper
from backend.app.models.article import Article

def test_pagescraper_is_abstract_and_cannot_be_instantiated():
    """
    Testa a regra principal da Classe Abstrata (ABC).
    Tentar instanciar PageScraper diretamente deve
    levantar um TypeError, pois ela tem métodos abstratos
    (@abstractmethod) que não foram implementados.
    """
    # 'with pytest.raises(TypeError)' verifica se o código
    # dentro dele *realmente* levanta o erro esperado.
    # Se não levantar o erro, o teste falha.
    with pytest.raises(TypeError):
        PageScraper()

def test_pagescraper_implementation_can_be_instantiated():
    """
    Testa se uma classe "filha" (uma implementação concreta)
    que implementa o método abstrato *pode* ser instanciada.
    Isso garante que nosso teste anterior não foi um falso positivo.
    """

    # 1. Criamos uma classe "falsa" (mock) que herda de PageScraper
    #    apenas para este teste.
    class ConcreteScraper(PageScraper):
        # 2. Nós implementamos o método abstrato 'scrape_article'
        def scrape_article(self, url: str, html_str: str) -> Article | None:
            # A lógica aqui não importa para o teste
            pass

    # 3. Tentar instanciar a classe "concreta" NÃO deve
    #    levantar TypeError.
    try:
        scraper = ConcreteScraper()
        assert isinstance(scraper, PageScraper)
    except TypeError:
        pytest.fail("Falha ao instanciar uma implementação concreta do PageScraper.")