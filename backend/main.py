import os
from functools import lru_cache
from typing import List, Optional

from app.ai.gemini import GeminiModel
from app.ai.rag.google_embedder import GoogleEmbedder
from app.ai.rag.retriever import NewsRetriever
from app.ai.rag.text_splitter import TextSplitter
from app.db.vectordb import VectorDB
from app.services.chat_service import ChatService
from app.services.scraping_manager import ScrapingError, ScrapingManager

# --- NOVAS IMPORTAÇÕES PARA O CRUD ---
from app.db.articledb import ArticleDB
from app.models.article import Article  # Importa o *novo* modelo Pydantic

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

# --- NOVOS MODELOS PYDANTIC PARA O CRUD ---
class ArticleUpdateRequest(BaseModel):
    """Campos permitidos para atualização de um artigo."""
    title: Optional[str] = None
    author: Optional[str] = None
    content: Optional[str] = None

class DeleteResponse(BaseModel):
    """Resposta padrão para deleção bem-sucedida."""
    message: str
    article_id: int


# --- Endpoints da API (RAG e Chat) ---
@app.post(
    "/chat",
    summary="Envia uma pergunta para o chat e obtém uma resposta com base em RAG.",
    response_model=ChatResponse,
    tags=["RAG Chat"],
)
def handle_chat(
    request: ChatRequest, chat_service: ChatService = Depends(get_chat_service)
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


@app.get("/prompt/{prompt}", tags=["RAG Chat"])
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

# --- Endpoints CRUD de Artigos ---

@app.post(
    "/article/add",
    summary="Adiciona e processa um novo artigo a partir de uma URL.",
    status_code=status.HTTP_201_CREATED,
    tags=["Article CRUD"], # Adiciona uma tag para organizar a documentação
)
def add_article(request: AddArticleRequest):
    """
    (CREATE) Recebe uma URL, faz scraping, processa e salva no banco.
    """
    # NOTA: Assume-se que o ScrapingManager agora está
    # usando o PageScraper corrigido (com o Downloader).
    manager = ScrapingManager()

    try:
        # Passa a URL como string, pois o Pydantic já validou
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
        # Erro inesperado
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro inesperado ao adicionar o artigo.",
        )


@app.get(
    "/articles/",
    summary="Lista todos os artigos do banco de dados SQL.",
    response_model=List[Article], # Retorna uma Lista de Artigos Pydantic
    tags=["Article CRUD"],
)
def get_all_articles():
    """
    (READ-All) Retorna todos os artigos salvos no banco de dados SQL.
    """
    db = ArticleDB()
    try:
        articles = db.get_all_articles()
        return articles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar artigos: {e}",
        )
    finally:
        db.close()


@app.get(
    "/article/{article_id}",
    summary="Busca um artigo específico pelo ID.",
    response_model=Article, # Retorna um único Artigo Pydantic
    tags=["Article CRUD"],
)
def get_article(article_id: int):
    """
    (READ-One) Retorna um artigo específico salvo no banco de dados SQL.
    """
    db = ArticleDB()
    try:
        article = db.get_article_by_id(article_id)
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artigo não encontrado.",
            )
        return article
    except HTTPException as e:
        raise e # Re-levanta o 404
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar artigo: {e}",
        )
    finally:
        db.close()


@app.put(
    "/article/{article_id}",
    summary="Atualiza um artigo existente.",
    response_model=Article,
    tags=["Article CRUD"],
)
def update_article(article_id: int, request: ArticleUpdateRequest):
    """
    (UPDATE) Atualiza os campos (title, author, content) de um artigo.
    """
    db = ArticleDB()
    try:
        # Converte o request Pydantic em um dicionário,
        # removendo campos que não foram enviados (None)
        data_to_update = request.dict(exclude_unset=True)

        if not data_to_update:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nenhum campo fornecido para atualização.",
            )

        updated_article = db.update_article(article_id, data_to_update)

        if not updated_article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artigo não encontrado para atualizar.",
            )
        
        return updated_article
    except HTTPException as e:
        raise e # Re-levanta o 404 ou 400
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar artigo: {e}",
        )
    finally:
        db.close()


@app.delete(
    "/article/{article_id}",
    summary="Deleta um artigo.",
    response_model=DeleteResponse,
    tags=["Article CRUD"],
)
def delete_article(article_id: int):
    """
    (DELETE) Remove um artigo do banco de dados SQL.
    """
    db = ArticleDB()
    try:
        success = db.delete_article(article_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artigo não encontrado para deletar.",
            )
        return DeleteResponse(
            message="Artigo deletado com sucesso", article_id=article_id
        )
    except HTTPException as e:
        raise e # Re-levanta o 404
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar artigo: {e}",
        )
    finally:
        db.close()

# --- Endpoint Raiz ---
@app.get("/")
def root():
    return {"message": "The API is working!"}