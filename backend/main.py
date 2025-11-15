from fastapi import FastAPI, HTTPException, status
from app.services.scraping_manager import ScrapingManager, ScrapingError
from app.ai.gemini import GeminiModel
from dotenv import load_dotenv
from pydantic import BaseModel, HttpUrl
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = GeminiModel(api_key=GOOGLE_API_KEY)

app = FastAPI(
    title="Lumina API",
    description="API para processamento e sumarização de notícias.",
    version="1.0.0",
)

# Modelo Pydantic para validação da URL de entrada
class AddArticleRequest(BaseModel):
    url: HttpUrl

@app.post(
    "/article/add",
    summary="Adiciona e processa um novo artigo a partir de uma URL",
    status_code=status.HTTP_201_CREATED,
)
def add_article(request: AddArticleRequest):
    """
    Recebe uma URL, faz o scraping do conteúdo, salva no banco de dados e retorna o ID do artigo.

    - **Validação**: A URL deve ser válida.
    - **Sucesso (201)**: Retorna o ID do artigo e uma mensagem de sucesso se o artigo for novo.
    - **Conflito (200)**: Retorna o ID e uma mensagem indicando que o artigo já existe.
    - **Erro de Cliente (422)**: Se a URL não for de uma fonte suportada.
    - **Erro de Servidor (500)**: Se o scraping falhar por um problema inesperado.
    """
    manager = ScrapingManager()
    try:
        article_id, created = manager.scrape_and_save(request.url)

        if created:
            return {
                "message": "Artigo adicionado com sucesso!",
                "article_id": article_id,
            }
        else:
            # Se o artigo já existe, retornamos 200 OK em vez de 409 Conflict
            # para simplificar o tratamento no cliente.
            return status.HTTP_200_OK, {
                "message": "O artigo já existe no banco de dados.",
                "article_id": article_id,
            }

    except ValueError as e:
        # Erro de URL não suportada
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
    except ScrapingError as e:
        # Erro durante o scraping
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha ao processar o artigo: {e}",
        )
    except Exception as e:
        # Outros erros inesperados
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro inesperado: {e}",
        )

@app.get("/")
def root():
    return {"message": "The API is working!"}


@app.get("/prompt/{prompt}")
def response(prompt: str):
    return {"response": llm.chat(prompt)}





