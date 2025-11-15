import pytest
from typing import Set
from bs4 import BeautifulSoup
from app.models.linkextractor import BaseLinkExtractor

# 1. Teste da Regra Abstrata
def test_base_link_extractor_is_abstract():
    """
    Testa a regra principal da ABC (Classe Abstrata):
    BaseLinkExtractor não pode ser instanciado diretamente
    porque possui métodos abstratos.
    """
    # Usamos 'with pytest.raises(TypeError)' para *esperar*
    # que um TypeError aconteça. Se não acontecer, o teste falha.
    with pytest.raises(TypeError) as e_info:
        # Tentar instanciar a classe base deve falhar
        BaseLinkExtractor(allowed_domain="example.com")
    
    # Verificamos se a mensagem de erro é a esperada
    assert "abstract methods" in str(e_info.value)


# 2. Teste da Lógica Concreta (__init__)
def test_concrete_extractor_implementation_works():
    """
    Testa se uma classe "filha" (concreta) que implementa
    todos os métodos abstratos pode ser instanciada e,
    principalmente, se o __init__ (que é da classe base)
    funciona e salva o 'allowed_domain'.
    """

    # --- Setup: Criação da Classe "Dummy" ---
    # Precisamos criar uma classe "falsa" que implementa
    # os métodos abstratos, apenas para este teste.
    class DummyExtractor(BaseLinkExtractor):
        
        # Implementação "falsa" (dummy) do método 1
        def extract(self, base_url: str, html_soup: BeautifulSoup) -> Set[str]:
            return {"http://test.com/link1"}

        # Implementação "falsa" (dummy) do método 2
        def _is_valid_url(self, url: str) -> bool:
            return True

        # Implementação "falsa" (dummy) do método 3
        def clean_url(self, url: str) -> str:
            return url
    # --- Fim do Setup ---

    # --- Execução e Verificação ---
    try:
        # 1. Tenta instanciar a classe "concreta"
        extractor = DummyExtractor(allowed_domain="test.com")
        
        # 2. Verifica se a instância foi criada
        assert isinstance(extractor, BaseLinkExtractor)
        
        # 3. [O TESTE REAL] Verifica se o __init__ funcionou
        assert extractor.allowed_domain == "test.com"
        
    except TypeError as e:
        # Se um TypeError for levantado, o teste falha,
        # pois nossa implementação "dummy" deveria ser válida.
        pytest.fail(f"Falha ao instanciar DummyExtractor: {e}")