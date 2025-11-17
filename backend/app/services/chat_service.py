from typing import List

from langchain_core.documents import Document
from app.ai.gemini import GeminiModel
from app.ai.rag.retriever import NewsRetriever


class ChatService:
    def __init__(self, retriever: NewsRetriever, llm: GeminiModel):
        self.retriever = retriever
        self.llm = llm

    def _format_docs_for_prompt(self, docs: List[Document]) -> str:
        """
        Formata os documentos recuperados em uma string para o prompt.
        """
        formatted_docs = []
        for i, doc in enumerate(docs):
            # Usando o metadado 'title' que você já tem
            doc_str = f"Artigo {i + 1} (Título: {doc.metadata.get('title', 'N/A')}):\n{doc.page_content}"
            formatted_docs.append(doc_str)

        return "\n\n---\n\n".join(formatted_docs)

    def generate_response(self, query: str) -> str:
        """
        Orquestra o processo de RAG.
        """
        # 1. Retrieval: Busca os documentos relevantes
        # Usando a versão síncrona por simplicidade, mas pode ser aget_relevant_documents
        relevant_docs = self.retriever._get_relevant_documents(query)

        # 2. Augmentation: Formata o prompt para o LLM
        context = self._format_docs_for_prompt(relevant_docs)

        # Este é o prompt que será enviado para o GeminiModel.chat()
        # Ele combina a pergunta do usuário com o contexto dos artigos.
        final_prompt = f"Com base nos artigos abaixo, responda à seguinte pergunta.\n\n--- Artigos ---\n{context}\n\n--- Pergunta ---\n{query}"

        # 3. Generation: Chama o LLM para gerar a resposta
        response = self.llm.chat(final_prompt)

        return response
