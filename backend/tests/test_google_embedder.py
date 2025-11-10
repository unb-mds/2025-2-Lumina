import os
import pytest
from dotenv import load_dotenv
from app.ai.ai_models.google_embedder import GoogleEmbedder

# Carrega as variáveis de ambiente (ex: GOOGLE_API_KEY) do .env
# Isso é crucial para o teste de integração funcionar.
load_dotenv()

# Pula os testes se a API key não estiver configurada no ambiente
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
pytestmark = pytest.mark.skipif(
    not GOOGLE_API_KEY,
    reason="GOOGLE_API_KEY não encontrada no .env. Pulando testes de integração.",
)

# Dimensão esperada dos vetores do modelo "models/embedding-001"
EXPECTED_DIMENSION = 768


@pytest.fixture(scope="module")
def embedder() -> GoogleEmbedder:
    """Fixture que inicializa o Embedder uma vez por módulo."""
    try:
        return GoogleEmbedder(api_key=GOOGLE_API_KEY)
    except Exception as e:
        pytest.fail(f"Falha ao inicializar GoogleEmbedder: {e}")


def test_embedder_inicializacao(embedder: GoogleEmbedder):
    """Testa se o embedder foi inicializado corretamente."""
    assert embedder is not None
    assert embedder.model_name == "models/embedding-001"
    assert embedloc.client is not None


def test_embed_document_retorna_vetor_correto(embedder: GoogleEmbedder):
    """
    Testa (Regra 2) se a vetorização de um único texto
    retorna um vetor (List[float]) com a dimensão correta.
    """
    texto = "Olá, mundo!"
    vetor = embedder.embed_document(texto)

    # 1. Deve ser uma lista
    assert isinstance(vetor, list)
    # 2. Não deve estar vazia
    assert len(vetor) > 0
    # 3. Deve ter a dimensão correta (768 para 'models/embedding-001')
    assert len(vetor) == EXPECTED_DIMENSION
    # 4. Todos os itens devem ser números (float)
    assert all(isinstance(item, float) for item in vetor)


def test_embed_documents_retorna_lista_de_vetores(embedder: GoogleEmbedder):
    """
    Testa a vetorização em lote (batch) de múltiplos textos.
    """
    textos = ["Isto é o primeiro texto.", "Este é o segundo."]
    vetores = embedder.embed_documents(textos)

    # 1. Deve ser uma lista
    assert isinstance(vetores, list)
    # 2. Deve ter o mesmo número de vetores que de textos
    assert len(vetores) == len(textos)

    # 3. Verifica o primeiro vetor
    vetor_1 = vetores[0]
    assert isinstance(vetor_1, list)
    assert len(vetor_1) == EXPECTED_DIMENSION
    assert all(isinstance(item, float) for item in vetor_1)

    # 4. Verifica o segundo vetor
    vetor_2 = vetores[1]
    assert isinstance(vetor_2, list)
    assert len(vetor_2) == EXPECTED_DIMENSION
    assert all(isinstance(item, float) for item in vetor_2)


def test_embed_documentos_lista_vazia(embedder: GoogleEmbedder):
    """
    Testa (Regra 4 - Caso de Borda) o comportamento ao
    passar uma lista vazia.
    """
    textos_vazios = []
    vetores = embedder.embed_documents(textos_vazios)

    # Deve retornar uma lista vazia sem chamar a API ou quebrar
    assert vetores == []


def test_embed_document_texto_vazio(embedder: GoogleEmbedder):
    """
    Testa (Regra 4 - Caso de Borda) o comportamento
    ao passar uma string vazia.
    """
    texto_vazio = ""
    vetor = embedder.embed_document(texto_vazio)

    # O embedding de um texto vazio deve retornar um vetor válido
    assert isinstance(vetor, list)
    assert len(vetor) == EXPECTED_DIMENSION