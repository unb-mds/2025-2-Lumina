import pytest
from app.models.article import Article
from app.ai.rag.text_splitter import TextSplitter
from langchain_core.documents import Document

# -- Fixtures (Ambiente de Teste) --


@pytest.fixture
def splitter_teste():
    """Retorna uma instância do TextSplitter com
    configurações fáceis de testar (chunk_size pequeno)."""
    # Usar um chunk_size pequeno para forçar a quebra
    return TextSplitter(chunk_size=100, chunk_overlap=20)


@pytest.fixture
def sample_article():
    """Retorna um artigo de exemplo padrão."""
    return Article(
        id=1,
        title="Este é o Título",
        author="Autor Teste",
        url="https://example.com/noticia",
        content=(
            "Parágrafo um. Este é o primeiro parágrafo do texto. "  # 56 chars
            "Ele é usado para testar a divisão de chunks.\n\n"  # 49 chars
            "Parágrafo dois. Este é o segundo parágrafo. "  # 47 chars
            "O splitter deve priorizar a quebra aqui. "  # 44 chars
            "Vamos adicionar mais texto para forçar a quebra. "  # 51 chars
            "Mais e mais e mais texto."  # 26 chars
        ),
        # Total: ~273 caracteres
    )


# -- Testes --


def test_splitter_cria_chunks(
    splitter_teste: TextSplitter, sample_article: Article
):
    """
    Testa se o splitter divide um artigo em múltiplos chunks (Documents).
    Com chunk_size=100, o texto de ~273 chars deve ser dividido.
    """
    chunks = splitter_teste.split_article(sample_article)

    # 1. Deve retornar uma lista
    assert isinstance(chunks, list)
    # 2. O texto de ~273 chars com chunk_size=100 deve quebrar (em 4 chunks)
    assert len(chunks) == 3
    # 3. Os itens da lista devem ser 'Documents' do LangChain
    assert isinstance(chunks[0], Document)


def test_splitter_mantem_metadados_em_todos_chunks(
    splitter_teste: TextSplitter, sample_article: Article
):
    """
    Testa (Regra 4 - Dúvida 4) se os metadados (id, url, title)
    estão corretos em TODOS os chunks gerados.
    """
    chunks = splitter_teste.split_article(sample_article)

    assert len(chunks) > 0
    for chunk in chunks:
        assert chunk.metadata["article_id"] == 1
        assert chunk.metadata["url"] == "https://example.com/noticia"
        assert chunk.metadata["title"] == "Este é o Título"


def test_splitter_artigo_sem_conteudo_retorna_lista_vazia(
    splitter_teste: TextSplitter,
):
    """
    Testa se um artigo com 'content' vazio ou None
    retorna uma lista vazia, sem erros.
    """
    article_sem_conteudo = Article(
        id=2,
        title="Sem Conteúdo",
        author="Autor",
        url="https://example.com/sem-conteudo",
        content="",  # Conteúdo vazio
    )
    chunks = splitter_teste.split_article(article_sem_conteudo)
    assert chunks == []


def test_splitter_artigo_sem_id_lanca_erro(splitter_teste: TextSplitter):
    """
    Testa (Regra 2) se um artigo sem 'id' (essencial para RAG)
    impede a execução e lança um ValueError.
    """
    article_sem_id = Article(
        id=None,  # ID nulo
        title="Sem ID",
        author="Autor",
        url="https://example.com/sem-id",
        content="Texto de conteúdo que não importa.",
    )

    # Verifica se um ValueError é lançado
    with pytest.raises(ValueError) as e_info:
        splitter_teste.split_article(article_sem_id)

    # Verifica se a mensagem de erro é a esperada
    assert "não possui um ID" in str(e_info.value)


def test_splitter_overlap_funciona(splitter_teste: TextSplitter):
    """
    Testa se a sobreposição (chunk_overlap=20) está funcionando.

    [TESTE ROBUSTO] Em vez de verificar um 'slice' exato (que é quebradiço),
    verificamos se o *início* do próximo chunk está *contido* no
    *final* do chunk anterior.
    """
    # Texto longo o suficiente para garantir a sobreposição
    texto_longo = (
        "Este é um texto bem longo feito apenas para testar a sobreposição. "
        "Vamos escrever mais de 100 caracteres para ter certeza que quebra. "
        "O final do primeiro chunk deve ser o começo do segundo chunk. "
        "Esta é a última parte."
    )  # ~235 caracteres

    article = Article(
        id=3,
        title="Teste Overlap",
        author="Autor",
        url="httpss://example.com/overlap",
        content=texto_longo,
    )

    chunks = splitter_teste.split_article(article)

    # 1. Verifica se dividiu no número esperado de chunks (isso passou, está ok)
    assert len(chunks) == 3

    # 2. Teste de Overlap (Robusto) para Chunk 0 -> Chunk 1
    # Pega os primeiros 10 caracteres do chunk 1 (ex: "mais de 10")
    inicio_chunk_1 = chunks[1].page_content[:10]
    # Pega os últimos 30 caracteres (margem de segurança) do chunk 0
    final_chunk_0 = chunks[0].page_content[-30:]

    # O início do chunk 1 DEVE estar contido no final do chunk 0
    assert inicio_chunk_1 in final_chunk_0, (
        f"O início do chunk 1 ('{inicio_chunk_1}') "
        f"não foi encontrado no final do chunk 0 ('{final_chunk_0}')"
    )

    # 3. Teste de Overlap (Robusto) para Chunk 1 -> Chunk 2
    # Pega os primeiros 10 caracteres do chunk 2 (ex: "o começo d")
    inicio_chunk_2 = chunks[2].page_content[:10]
    # Pega os últimos 30 caracteres (margem de segurança) do chunk 1
    final_chunk_1 = chunks[1].page_content[-30:]

    # O início do chunk 2 DEVE estar contido no final do chunk 1
    assert inicio_chunk_2 in final_chunk_1, (
        f"O início do chunk 2 ('{inicio_chunk_2}') "
        f"não foi encontrado no final do chunk 1 ('{final_chunk_1}')"
    )