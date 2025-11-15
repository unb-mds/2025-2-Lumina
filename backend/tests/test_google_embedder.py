import pytest
from backend.app.ai.rag.google_embedder import GoogleEmbedder

# Dimensão esperada dos vetores do modelo "models/embedding-001"
EXPECTED_DIMENSION = 768


@pytest.fixture
def mock_google_embeddings_client(mocker):
    """Mocks the GoogleGenerativeAIEmbeddings client from LangChain."""
    mock_client = mocker.patch(
        "langchain_google_genai.GoogleGenerativeAIEmbeddings",
    ).return_value
    
    mock_client.embed_query.return_value = [0.1] * EXPECTED_DIMENSION
    
    # Configure the mock to return a number of embeddings equal to the input length
    def embed_documents_side_effect(texts):
        return [[0.1] * EXPECTED_DIMENSION for _ in texts]
    
    mock_client.embed_documents.side_effect = embed_documents_side_effect
    
    return mock_client


@pytest.fixture
def embedder(mock_google_embeddings_client) -> GoogleEmbedder:
    """Fixture que inicializa o Embedder com um cliente mockado."""
    instance = GoogleEmbedder(api_key="fake-key")
    instance.client = mock_google_embeddings_client
    return instance


def test_embedder_inicializacao(embedder: GoogleEmbedder, mock_google_embeddings_client):
    """Testa se o embedder foi inicializado corretamente com o mock."""
    assert embedder is not None
    assert embedder.model_name == "models/embedding-001"
    assert embedder.client == mock_google_embeddings_client


def test_embed_document_retorna_vetor_correto(embedder: GoogleEmbedder):
    """
    Testa se a vetorização de um único texto retorna um vetor com a dimensão correta.
    """
    texto = "Olá, mundo!"
    vetor = embedder.embed_document(texto)

    assert isinstance(vetor, list)
    assert len(vetor) == EXPECTED_DIMENSION
    assert all(isinstance(item, float) for item in vetor)
    embedder.client.embed_query.assert_called_once_with(texto)


def test_embed_documents_small_batch(embedder: GoogleEmbedder, mocker):
    """
    Testa a vetorização de um lote pequeno (menor que o BATCH_SIZE),
    verificando se a API é chamada apenas uma vez e sem sleep.
    """
    mock_sleep = mocker.patch("time.sleep")
    textos = ["Texto 1", "Texto 2"]
    vetores = embedder.embed_documents(textos)

    assert len(vetores) == len(textos)
    assert len(vetores[0]) == EXPECTED_DIMENSION
    embedder.client.embed_documents.assert_called_once_with(textos)
    mock_sleep.assert_called_once() # Should be called once after the single batch


def test_embed_documents_throttling_large_batch(embedder: GoogleEmbedder, mocker):
    """
    Testa a vetorização de um lote grande, verificando o throttling.
    """
    mock_sleep = mocker.patch("time.sleep")
    # Cria uma lista com mais textos que o tamanho do lote
    textos = [f"Texto {i}" for i in range(GoogleEmbedder.EMBEDDING_BATCH_SIZE + 5)] # 20 textos
    
    vetores = embedder.embed_documents(textos)

    # 1. Verifica se todos os embeddings foram retornados
    assert len(vetores) == len(textos)
    
    # 2. Verifica se a API foi chamada o número correto de vezes (2 vezes)
    assert embedder.client.embed_documents.call_count == 2
    
    # 3. Verifica as chamadas individuais
    first_call_args = embedder.client.embed_documents.call_args_list[0].args[0]
    second_call_args = embedder.client.embed_documents.call_args_list[1].args[0]
    assert len(first_call_args) == GoogleEmbedder.EMBEDDING_BATCH_SIZE
    assert len(second_call_args) == 5

    # 4. Verifica se o sleep foi chamado o número correto de vezes (2 vezes)
    assert mock_sleep.call_count == 2
    mock_sleep.assert_called_with(1)


def test_embed_documentos_lista_vazia(embedder: GoogleEmbedder):
    """
    Testa o comportamento ao passar uma lista vazia.
    """
    textos_vazios = []
    vetores = embedder.embed_documents(textos_vazios)

    assert vetores == []
    embedder.client.embed_documents.assert_not_called()


def test_embed_document_texto_vazio(embedder: GoogleEmbedder):
    """
    Testa o comportamento ao passar uma string vazia.
    """
    texto_vazio = ""
    vetor = embedder.embed_document(texto_vazio)

    assert isinstance(vetor, list)
    assert len(vetor) == EXPECTED_DIMENSION
    embedder.client.embed_query.assert_called_once_with(texto_vazio)

def test_embed_document_api_failure(embedder: GoogleEmbedder):
    """Testa o que acontece se a API falhar ao vetorizar um documento."""
    embedder.client.embed_query.side_effect = Exception("API Error")
    embedder.client.embed_query.return_value = None # Reset return value
    
    vetor = embedder.embed_document("texto qualquer")
    
    assert vetor == []

def test_embed_documents_api_failure_in_batch(embedder: GoogleEmbedder, mocker):
    """Testa o que acontece se a API falhar no meio de um lote."""
    mock_sleep = mocker.patch("time.sleep")
    embedder.client.embed_documents.side_effect = Exception("API Error")

    vetores = embedder.embed_documents(["texto 1", "texto 2"])

    # Deve retornar uma lista vazia pois a exceção interrompe o loop
    assert vetores == []
    # A API foi chamada uma vez (na primeira tentativa de lote)
    embedder.client.embed_documents.assert_called_once()
    # O sleep não deve ser chamado se a chamada da API falhar
    mock_sleep.assert_not_called()