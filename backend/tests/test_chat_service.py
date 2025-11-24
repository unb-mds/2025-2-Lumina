import pytest
from unittest.mock import MagicMock
from langchain_core.documents import Document
from app.services.chat_service import ChatService

# --- Fixtures para simular as dependências ---

@pytest.fixture
def mock_retriever():
    """Cria um Mock para o NewsRetriever."""
    return MagicMock()

@pytest.fixture
def mock_llm():
    """Cria um Mock para o GeminiModel."""
    return MagicMock()

@pytest.fixture
def chat_service(mock_retriever, mock_llm):
    """
    Instancia o ChatService injetando os mocks.
    Assim testamos o serviço isoladamente.
    """
    return ChatService(retriever=mock_retriever, llm=mock_llm)

class TestChatService:

    # --- Testes do método auxiliar _format_docs_for_prompt ---

    def test_format_docs_standard(self, chat_service):
        """
        Testa a formatação padrão com documentos que possuem título e conteúdo.
        """
        docs = [
            Document(page_content="O Brasil cresceu.", metadata={"title": "Economia Hoje"}),
            Document(page_content="Novo vírus descoberto.", metadata={"title": "Saúde Global"}),
        ]

        formatted_text = chat_service._format_docs_for_prompt(docs)

        # Verificações
        assert "Artigo 1 (Título: Economia Hoje):" in formatted_text
        assert "O Brasil cresceu." in formatted_text
        assert "Artigo 2 (Título: Saúde Global):" in formatted_text
        assert "Novo vírus descoberto." in formatted_text
        # Verifica o separador
        assert "\n\n---\n\n" in formatted_text

    def test_format_docs_missing_title_metadata(self, chat_service):
        """
        Testa se o código lida bem com documentos sem o metadado 'title' (fallback para 'N/A').
        """
        docs = [
            Document(page_content="Texto sem título.", metadata={}) # Dicionário vazio
        ]

        formatted_text = chat_service._format_docs_for_prompt(docs)

        assert "Artigo 1 (Título: N/A):" in formatted_text
        assert "Texto sem título." in formatted_text

    def test_format_docs_empty_list(self, chat_service):
        """
        Testa se retorna string vazia caso não haja documentos.
        """
        formatted_text = chat_service._format_docs_for_prompt([])
        assert formatted_text == ""

    # --- Testes do fluxo principal generate_response ---

    def test_generate_response_success(self, chat_service, mock_retriever, mock_llm):
        """
        Testa o fluxo completo:
        1. Chama o retriever com a query.
        2. Formata os documentos retornados.
        3. Monta o prompt final.
        4. Chama o LLM.
        5. Retorna a resposta.
        """
        user_query = "Como está a economia?"
        
        # Configura o comportamento simulado do Retriever
        mock_docs = [
            Document(page_content="PIB subiu 2%.", metadata={"title": "Notícia Economia"})
        ]
        mock_retriever._get_relevant_documents.return_value = mock_docs

        # Configura o comportamento simulado do LLM
        expected_ai_response = "A economia vai bem, o PIB subiu."
        mock_llm.chat.return_value = expected_ai_response

        # Executa o método
        response = chat_service.generate_response(user_query)

        # 1. Verifica se o retriever foi chamado com a pergunta do usuário
        mock_retriever._get_relevant_documents.assert_called_once_with(user_query)

        # 2. Verifica se o prompt enviado ao LLM contém os elementos essenciais
        #    (Não comparamos a string inteira rigidamente para não quebrar com espaços extras,
        #     mas verificamos se as partes críticas estão lá).
        args, _ = mock_llm.chat.call_args
        prompt_sent = args[0]

        assert "Com base nos artigos abaixo" in prompt_sent
        assert "Artigo 1 (Título: Notícia Economia):" in prompt_sent # Contexto formatado
        assert "PIB subiu 2%." in prompt_sent
        assert f"--- Pergunta ---\n{user_query}" in prompt_sent

        # 3. Verifica se a resposta final é a que veio do LLM
        assert response == expected_ai_response

    def test_generate_response_no_docs_found(self, chat_service, mock_retriever, mock_llm):
        """
        Testa o comportamento quando o retriever não encontra nada (lista vazia).
        O prompt deve ir vazio na parte de artigos, mas não deve quebrar.
        """
        user_query = "Pergunta difícil"
        mock_retriever._get_relevant_documents.return_value = [] # Nenhum artigo
        mock_llm.chat.return_value = "Não sei responder."

        response = chat_service.generate_response(user_query)

        # Verifica o prompt enviado
        args, _ = mock_llm.chat.call_args
        prompt_sent = args[0]

        # A seção de artigos deve estar vazia (ou só os headers)
        assert "--- Artigos ---\n\n" in prompt_sent or "--- Artigos ---\n\n--- Pergunta" in prompt_sent
        assert response == "Não sei responder."