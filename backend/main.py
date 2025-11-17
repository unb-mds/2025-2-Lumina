import os
from functools import lru_cache

from app.ai.gemini import GeminiModel
from app.ai.rag.google_embedder import GoogleEmbedder
from app.ai.rag.retriever import NewsRetriever
from app.ai.rag.text_splitter import TextSplitter
from app.db.vectordb import VectorDB
from app.services.chat_service import ChatService
from app.services.scraping_manager import ScrapingError, ScrapingManager

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl

load_dotenv()

# --- Configuração de API e Modelos ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("A variável de ambiente GOOGLE_API_KEY não foi definida.")


# --- Inicialização da Aplicação FastAPI ---
app = FastAPI(
    title="Lumina API",
    description="API para processamento e sumarização de notícias.",
    version="1.0.0",
)


# --- Factories Singleton com Cache ---
@lru_cache
def get_llm() -> GeminiModel:
    """Instância única do modelo LLM."""
    return GeminiModel(api_key=GOOGLE_API_KEY)


@lru_cache
def get_chat_service() -> ChatService:
    """
    Cria e retorna uma instância singleton do ChatService,
    inicializando todas as suas dependências.
    """
    embedding_platform = GoogleEmbedder(api_key=GOOGLE_API_KEY)
    text_splitter = TextSplitter(chunk_size=1000, chunk_overlap=200)

    vector_db = VectorDB(
        embedding_platform=embedding_platform,
        text_splitter=text_splitter,
        db_path="app/db/chroma_db",
    )

    retriever = NewsRetriever(vectordb=vector_db, search_k=5)
    llm = get_llm()

    return ChatService(retriever=retriever, llm=llm)


# --- Modelos Pydantic ---
class AddArticleRequest(BaseModel):
    url: HttpUrl


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    response: str


# --- Endpoints da API ---
@app.post(
    "/chat",
    summary="Envia uma pergunta para o chat e obtém uma resposta com base em RAG.",
    response_model=ChatResponse,
)
def handle_chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Recebe uma pergunta do usuário, busca artigos relevantes no banco vetorial
    e usa um LLM para gerar uma resposta fundamentada nesses artigos.
    """
    try:
        response = chat_service.generate_response(request.query)
        return ChatResponse(response=response)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro inesperado ao gerar a resposta.",
        )


@app.get("/prompt/{prompt}")
def prompt_response(prompt: str):
    """
    Endpoint simples para enviar prompts diretos ao modelo (sem RAG).
    """
    llm = get_llm()
    try:
        return {"response": llm.chat(prompt)}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar o prompt.",
        )


@app.post(
    "/article/add",
    summary="Adiciona e processa um novo artigo a partir de uma URL.",
    status_code=status.HTTP_201_CREATED,
)
def add_article(request: AddArticleRequest):
    """
    Recebe uma URL, faz scraping, processa e salva no banco vetorial.

    Retornos:
    - 201: Artigo criado.
    - 200: Artigo já existia.
    - 422: Fonte não suportada.
    - 500: Erro interno.
    """
    manager = ScrapingManager()

    try:
        article_id, created = manager.scrape_and_save(str(request.url))

        # Artigo novo
        if created:
            return {
                "message": "Artigo adicionado com sucesso!",
                "article_id": article_id,
            }

        # Artigo já existe → 200 OK
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "O artigo já existe no banco de dados.",
                "article_id": article_id,
            },
        )

    except ValueError as e:
        # URL de fonte não suportada
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )

    except ScrapingError as e:
        # Erro durante scraping
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha ao processar o artigo: {e}",
        )

    except Exception:
        # Erro inesperado sem vazar stacktrace
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro inesperado ao adicionar o artigo.",
        )


@app.get("/")
def root():
    return {"message": "The API is working!"}
