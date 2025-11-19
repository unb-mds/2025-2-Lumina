import uuid
from unittest.mock import patch

import pytest
from langchain_core.documents import Document

from app.ai.rag.google_embedder import GoogleEmbedder
from app.ai.rag.text_splitter import TextSplitter
from app.db.vectordb import VectorDB
from app.models.article import Article

# --- Fixtures ---


@pytest.fixture
def mock_google_embedder(mocker):
    """Provides a GoogleEmbedder instance with its internal client fully mocked."""
    # Mock the client inside the GoogleEmbedder
    mock_client = mocker.patch(
        "langchain_google_genai.GoogleGenerativeAIEmbeddings",
    ).return_value

    mock_client.embed_documents.return_value = [[0.1] * 768, [0.2] * 768]

    # Create a real embedder but replace its client with our mock
    embedder = GoogleEmbedder(api_key="fake_api_key")
    embedder.client = mock_client
    return embedder


@pytest.fixture
def mock_text_splitter(mocker):
    """Mocks the TextSplitter to control chunking behavior."""
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
    """Mocks the ChromaDB collection object."""
    return mocker.MagicMock()


@pytest.fixture
def mock_chroma_client(mocker, mock_chroma_collection):
    """Mocks the ChromaDB PersistentClient and its get_or_create_collection method."""
    with patch("chromadb.PersistentClient") as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.get_or_create_collection.return_value = mock_chroma_collection
        yield MockClient  # Yield the class mock itself


@pytest.fixture
def sample_article():
    """Provides a sample Article object for testing."""
    return Article(
        id=1,
        title="Sample Article Title",
        author="Test Author",
        url="http://example.com/sample-article",
        content="This is the content of the sample article. It is long enough to be split into multiple chunks.",
    )


@pytest.fixture
def article_no_content():
    """Provides an Article object with no content."""
    return Article(
        id=2,
        title="No Content Article",
        author="Test Author",
        url="http://example.com/no-content",
        content="",
    )


@pytest.fixture
def article_no_id():
    """Provides an Article object with no ID."""
    return Article(
        id=None,
        title="No ID Article",
        author="Test Author",
        url="http://example.com/no-id",
        content="Content for article with no ID.",
    )


# --- Tests ---


def test_vectordb_init_success(
    mock_google_embedder, mock_text_splitter, mock_chroma_client
):
    """Tests successful initialization of VectorDB."""
    vectordb = VectorDB(
        embedding_platform=mock_google_embedder, text_splitter=mock_text_splitter
    )

    mock_chroma_client.assert_called_once_with(path="app/db/chroma_db")
    mock_chroma_client.return_value.get_or_create_collection.assert_called_once_with(
        name="lumina_articles"
    )
    assert vectordb.embedding_platform == mock_google_embedder
    assert vectordb.splitter == mock_text_splitter
    assert vectordb.client is not None
    assert vectordb.collection is not None


def test_vectordb_init_failure_chroma(mock_google_embedder, mock_text_splitter, mocker):
    """Tests VectorDB initialization failure if ChromaDB client raises an exception."""
    mocker.patch(
        "chromadb.PersistentClient", side_effect=Exception("ChromaDB connection error")
    )
    with pytest.raises(Exception, match="ChromaDB connection error"):
        VectorDB(
            embedding_platform=mock_google_embedder, text_splitter=mock_text_splitter
        )


def test_vectorize_article_success(
    mock_google_embedder, mock_text_splitter, mock_chroma_collection, sample_article
):
    """Tests successful vectorization of an article."""
    vectordb = VectorDB(
        embedding_platform=mock_google_embedder, text_splitter=mock_text_splitter
    )
    vectordb.collection = mock_chroma_collection

    with patch(
        "uuid.uuid4", return_value=uuid.UUID("12345678-1234-5678-1234-567812345678")
    ):
        batch_id = vectordb.vectorize_article(sample_article)

        assert batch_id == "12345678-1234-5678-1234-567812345678"
        mock_text_splitter.split_article.assert_called_once_with(sample_article)
        mock_google_embedder.client.embed_documents.assert_called_once_with(
            ["chunk 1", "chunk 2"]
        )
        mock_chroma_collection.add.assert_called_once_with(
            documents=["chunk 1", "chunk 2"],
            metadatas=[
                {"article_id": 1, "url": "http://example.com/1", "title": "Title 1"},
                {"article_id": 1, "url": "http://example.com/1", "title": "Title 1"},
            ],
            ids=["1_0", "1_1"],
            embeddings=[[0.1] * 768, [0.2] * 768],
        )


def test_vectorize_article_no_content(
    mock_google_embedder, mock_text_splitter, mock_chroma_collection, article_no_content
):
    """Tests vectorization of an article with no content."""
    vectordb = VectorDB(
        embedding_platform=mock_google_embedder, text_splitter=mock_text_splitter
    )
    vectordb.collection = mock_chroma_collection
    mock_text_splitter.split_article.return_value = []

    batch_id = vectordb.vectorize_article(article_no_content)

    assert batch_id is None
    mock_text_splitter.split_article.assert_called_once_with(article_no_content)
    mock_google_embedder.client.embed_documents.assert_not_called()
    mock_chroma_collection.add.assert_not_called()


def test_vectorize_article_no_id(
    mock_google_embedder, mock_text_splitter, mock_chroma_collection, article_no_id
):
    """Tests vectorization of an article with no ID (should raise ValueError)."""
    vectordb = VectorDB(
        embedding_platform=mock_google_embedder, text_splitter=mock_text_splitter
    )
    vectordb.collection = mock_chroma_collection

    with pytest.raises(
        ValueError, match="Artigo precisa de um ID para ser vetorizado."
    ):
        vectordb.vectorize_article(article_no_id)

    mock_text_splitter.split_article.assert_not_called()
    mock_google_embedder.client.embed_documents.assert_not_called()
    mock_chroma_collection.add.assert_not_called()


def test_vectorize_article_embedding_failure(
    mock_google_embedder, mock_text_splitter, mock_chroma_collection, sample_article
):
    """Tests failure during embedding generation."""
    vectordb = VectorDB(
        embedding_platform=mock_google_embedder, text_splitter=mock_text_splitter
    )
    vectordb.collection = mock_chroma_collection
    mock_google_embedder.client.embed_documents.return_value = []

    batch_id = vectordb.vectorize_article(sample_article)

    assert batch_id is None
    mock_text_splitter.split_article.assert_called_once_with(sample_article)
    mock_google_embedder.client.embed_documents.assert_called_once_with(
        ["chunk 1", "chunk 2"]
    )
    mock_chroma_collection.add.assert_not_called()


def test_vectorize_article_chroma_add_failure(
    mock_google_embedder, mock_text_splitter, mock_chroma_collection, sample_article
):
    """Tests failure during chromadb.add operation."""
    vectordb = VectorDB(
        embedding_platform=mock_google_embedder, text_splitter=mock_text_splitter
    )
    vectordb.collection = mock_chroma_collection
    mock_chroma_collection.add.side_effect = Exception("ChromaDB add error")

    batch_id = vectordb.vectorize_article(sample_article)

    assert batch_id is None
    mock_text_splitter.split_article.assert_called_once_with(sample_article)
    mock_google_embedder.client.embed_documents.assert_called_once_with(
        ["chunk 1", "chunk 2"]
    )
    mock_chroma_collection.add.assert_called_once()


def test_delete_article_by_url(
    mock_google_embedder, mock_text_splitter, mock_chroma_collection
):
    """Tests deleting an article by URL."""
    vectordb = VectorDB(
        embedding_platform=mock_google_embedder, text_splitter=mock_text_splitter
    )
    vectordb.collection = mock_chroma_collection
    url_to_delete = "http://example.com/to-delete"

    vectordb.delete_article_by_url(url_to_delete)

    mock_chroma_collection.delete.assert_called_once_with(where={"url": url_to_delete})
