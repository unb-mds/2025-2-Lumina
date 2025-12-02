import uuid
import os
from unittest.mock import patch

import pytest
from langchain_core.documents import Document

from app.ai.rag.google_embedder import GoogleEmbedder
from app.ai.rag.text_splitter import TextSplitter
from app.db.vectordb import VectorDB
from app.models.article import Article

# --- Fixtures (Configuração de Dependências) ---

@pytest.fixture
def mock_google_embedder(mocker):
    """
    Fixture que fornece uma instância do GoogleEmbedder com o cliente interno mockado.
    Isso evita chamadas reais à API do Google Generative AI.
    """
    # Mock do cliente interno dentro do GoogleEmbedder
    mock_client = mocker.patch(
        "langchain_google_genai.GoogleGenerativeAIEmbeddings",
    ).return_value

    # Simula o retorno de vetores (embeddings) para dois chunks
    mock_client.embed_documents.return_value = [[0.1] * 768, [0.2] * 768]

    # Cria a instância real mas substitui o cliente pelo mock
    embedder = GoogleEmbedder(api_key="fake_api_key")
    embedder.client = mock_client
    return embedder


@pytest.fixture
def mock_text_splitter(mocker):
    """
    Fixture que mocka o TextSplitter para controlar como o texto é dividido.
    Retorna dois chunks fixos para facilitar a validação.
    """
    mock_splitter = mocker.MagicMock(spec=TextSplitter)
    mock_splitter.split_article.return_value = [
        Document(
            page_content="chunk 1",
            metadata={
                "article_id": 1,
                "url": "http://example.com/1",
                "title": "Title 1",
            },
        ),
        Document(
            page_content="chunk 2",
            metadata={
                "article_id": 1,
                "url": "http://example.com/1",
                "title": "Title 1",
            },
        ),
    ]
    return mock_splitter


@pytest.fixture
def mock_chroma_collection(mocker):
    """Fixture que mocka o objeto de coleção (Collection) do ChromaDB."""
    return mocker.MagicMock()


@pytest.fixture
def mock_chroma_client(mocker, mock_chroma_collection):
    """
    Fixture que mocka o PersistentClient do ChromaDB.
    Garante que 'get_or_create_collection' retorne o mock da coleção acima.
    """
    with patch("chromadb.PersistentClient") as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.get_or_create_collection.return_value = mock_chroma_collection
        yield MockClient  # Retorna a classe mockada para verificações de instanciação


@pytest.fixture
def sample_article():
    """Fixture que fornece um objeto Article válido com conteúdo."""
    return Article(
        id=1,
        title="Sample Article Title",
        author="Test Author",
        url="http://example.com/sample-article",
        content="This is the content of the sample article. It is long enough to be split into multiple chunks.",
    )


@pytest.fixture
def article_no_content():
    """Fixture que fornece um objeto Article vazio (sem conteúdo)."""
    return Article(
        id=2,
        title="No Content Article",
        author="Test Author",
        url="http://example.com/no-content",
        content="",
    )


@pytest.fixture
def article_no_id():
    """Fixture que fornece um objeto Article sem ID (Inválido para vetorização)."""
    return Article(
        id=None,
        title="No ID Article",
        author="Test Author",
        url="http://example.com/no-id",
        content="Content for article with no ID.",
    )


# --- Testes de Inicialização ---

def test_vectordb_init_success(
    mock_google_embedder, mock_text_splitter, mock_chroma_client
):
    """
    Testa a inicialização bem-sucedida do VectorDB.
    Verifica se o cliente ChromaDB é instanciado no diretório correto e a coleção é criada.
    """
    # Execução
    vectordb = VectorDB(
        embedding_platform=mock_google_embedder,
        text_splitter=mock_text_splitter,
        db_directory_name="chroma_db"
    )

    # Verificação
    # Checa se PersistentClient foi chamado com um caminho terminando em 'chroma_db'
    args, kwargs = mock_chroma_client.call_args
    assert "path" in kwargs
    assert kwargs["path"].endswith("chroma_db")

    # Verifica se a coleção correta foi acessada/criada
    mock_chroma_client.return_value.get_or_create_collection.assert_called_once_with(
        name="lumina_articles"
    )
    
    # Verifica a injeção de dependências
    assert vectordb.embedding_platform == mock_google_embedder
    assert vectordb.splitter == mock_text_splitter
    assert vectordb.client is not None
    assert vectordb.collection is not None


def test_vectordb_init_failure_chroma(mock_google_embedder, mock_text_splitter, mocker):
    """Testa a falha na inicialização quando o cliente ChromaDB lança uma exceção."""
    # Configuração: Simula erro de conexão no Chroma
    mocker.patch(
        "chromadb.PersistentClient", side_effect=Exception("ChromaDB connection error")
    )
    
    # Execução e Verificação
    with pytest.raises(Exception, match="ChromaDB connection error"):
        VectorDB(
            embedding_platform=mock_google_embedder,
            text_splitter=mock_text_splitter,
            db_directory_name="chroma_db"
        )


# --- Testes de Vetorização (Core Logic) ---

def test_vectorize_article_success(
    mock_google_embedder, mock_text_splitter, mock_chroma_collection, sample_article
):
    """
    Testa o fluxo feliz de vetorização de um artigo.
    
    Etapas verificadas:
    1. O artigo é dividido em chunks (TextSplitter).
    2. Os chunks são convertidos em vetores (GoogleEmbedder).
    3. Dados e vetores são salvos na coleção (ChromaDB).
    """
    # Configuração
    vectordb = VectorDB(
        embedding_platform=mock_google_embedder,
        text_splitter=mock_text_splitter,
        db_directory_name="chroma_db"
    )
    vectordb.collection = mock_chroma_collection

    # Execução
    # Mockamos o UUID para garantir que o ID do batch seja previsível no teste
    with patch(
        "uuid.uuid4", return_value=uuid.UUID("12345678-1234-5678-1234-567812345678")
    ):
        batch_id = vectordb.vectorize_article(sample_article)

        # Verificação
        assert batch_id == "12345678-1234-5678-1234-567812345678"
        
        # 1. Verifica split
        mock_text_splitter.split_article.assert_called_once_with(sample_article)
        
        # 2. Verifica embedding
        mock_google_embedder.client.embed_documents.assert_called_once_with(
            ["chunk 1", "chunk 2"]
        )
        
        # 3. Verifica salvamento no Chroma com metadados e IDs corretos
        mock_chroma_collection.add.assert_called_once_with(
            documents=["chunk 1", "chunk 2"],
            metadatas=[
                {"article_id": 1, "url": "http://example.com/1", "title": "Title 1"},
                {"article_id": 1, "url": "http://example.com/1", "title": "Title 1"},
            ],
            ids=["1_0", "1_1"], # IDs compostos: {article_id}_{index}
            embeddings=[[0.1] * 768, [0.2] * 768],
        )


def test_vectorize_article_no_content(
    mock_google_embedder, mock_text_splitter, mock_chroma_collection, article_no_content
):
    """
    Testa a vetorização de um artigo sem conteúdo.
    Deve retornar None e não chamar o embedder nem o banco.
    """
    # Configuração
    vectordb = VectorDB(
        embedding_platform=mock_google_embedder,
        text_splitter=mock_text_splitter,
        db_directory_name="chroma_db"
    )
    vectordb.collection = mock_chroma_collection
    # O splitter retorna lista vazia pois não há conteúdo
    mock_text_splitter.split_article.return_value = []

    # Execução
    batch_id = vectordb.vectorize_article(article_no_content)

    # Verificação
    assert batch_id is None
    mock_text_splitter.split_article.assert_called_once_with(article_no_content)
    # Garante que processos caros não foram executados
    mock_google_embedder.client.embed_documents.assert_not_called()
    mock_chroma_collection.add.assert_not_called()


def test_vectorize_article_no_id(
    mock_google_embedder, mock_text_splitter, mock_chroma_collection, article_no_id
):
    """
    Testa a validação de artigo sem ID.
    Deve lançar ValueError, pois o ID é necessário para metadados e controle.
    """
    vectordb = VectorDB(
        embedding_platform=mock_google_embedder,
        text_splitter=mock_text_splitter,
        db_directory_name="chroma_db"
    )
    vectordb.collection = mock_chroma_collection

    # Execução e Verificação
    with pytest.raises(
        ValueError, match="Artigo precisa de um ID para ser vetorizado."
    ):
        vectordb.vectorize_article(article_no_id)

    # Garante que nada foi processado
    mock_text_splitter.split_article.assert_not_called()
    mock_google_embedder.client.embed_documents.assert_not_called()
    mock_chroma_collection.add.assert_not_called()


def test_vectorize_article_embedding_failure(
    mock_google_embedder, mock_text_splitter, mock_chroma_collection, sample_article
):
    """
    Testa o comportamento quando a geração de embeddings falha (retorna vazio).
    O processo deve ser abortado e nada deve ser salvo no banco.
    """
    # Configuração
    vectordb = VectorDB(
        embedding_platform=mock_google_embedder,
        text_splitter=mock_text_splitter,
        db_directory_name="chroma_db"
    )
    vectordb.collection = mock_chroma_collection
    
    # Simula falha silenciosa ou retorno vazio da API de embedding
    mock_google_embedder.client.embed_documents.return_value = []

    # Execução
    batch_id = vectordb.vectorize_article(sample_article)

    # Verificação
    assert batch_id is None
    mock_text_splitter.split_article.assert_called_once_with(sample_article)
    mock_google_embedder.client.embed_documents.assert_called_once_with(
        ["chunk 1", "chunk 2"]
    )
    # Não deve salvar no banco se não temos vetores
    mock_chroma_collection.add.assert_not_called()


def test_vectorize_article_chroma_add_failure(
    mock_google_embedder, mock_text_splitter, mock_chroma_collection, sample_article
):
    """
    Testa o tratamento de exceção durante a adição ao ChromaDB.
    Deve capturar a exceção, logar (implícito) e retornar None.
    """
    # Configuração
    vectordb = VectorDB(
        embedding_platform=mock_google_embedder,
        text_splitter=mock_text_splitter,
        db_directory_name="chroma_db"
    )
    vectordb.collection = mock_chroma_collection
    
    # Simula erro crítico ao tentar adicionar ao banco
    mock_chroma_collection.add.side_effect = Exception("ChromaDB add error")

    # Execução
    batch_id = vectordb.vectorize_article(sample_article)

    # Verificação
    assert batch_id is None
    mock_text_splitter.split_article.assert_called_once_with(sample_article)
    mock_google_embedder.client.embed_documents.assert_called_once_with(
        ["chunk 1", "chunk 2"]
    )
    mock_chroma_collection.add.assert_called_once()


# --- Testes de Remoção ---

def test_delete_article_by_url(
    mock_google_embedder, mock_text_splitter, mock_chroma_collection
):
    """Testa a funcionalidade de deletar vetores de um artigo baseado na URL."""
    # Configuração
    vectordb = VectorDB(
        embedding_platform=mock_google_embedder,
        text_splitter=mock_text_splitter,
        db_directory_name="chroma_db"
    )
    vectordb.collection = mock_chroma_collection
    url_to_delete = "http://example.com/to-delete"

    # Execução
    vectordb.delete_article_by_url(url_to_delete)

    # Verificação
    mock_chroma_collection.delete.assert_called_once_with(where={"url": url_to_delete})