from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND

from app.db.articledb import ArticleDB
from app.services.scraping_manager import ScrapingManager
from app.models.article import Article

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

ADMIN_PASSWORD = "admin" 

# --- Dependências Auxiliares ---
def verify_admin_login(request: Request):
    return request.cookies.get("admin_logged_in") is not None

# --- Rotas ---

@router.get("/admin", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return templates.TemplateResponse("admin_login.html", {
        "request": request,
        "now": datetime.now()
    })

@router.post("/admin/login", response_class=RedirectResponse)
async def admin_login_action(request: Request, password: str = Form(...)):
    if password == ADMIN_PASSWORD:
        response = RedirectResponse(url=router.url_path_for("admin_dashboard"), status_code=HTTP_302_FOUND)
        response.set_cookie(key="admin_logged_in", value="true", httponly=True)
        return response
    
    return templates.TemplateResponse(
        "admin_login.html", 
        {"request": request, "messages": [("error", "Senha incorreta")], "now": datetime.now()}
    )

@router.get("/admin/logout")
async def admin_logout():
    response = RedirectResponse(url="/admin", status_code=HTTP_302_FOUND)
    response.delete_cookie("admin_logged_in")
    return response

@router.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request, search: Optional[str] = None):
    if not verify_admin_login(request):
        return RedirectResponse(url="/admin", status_code=HTTP_302_FOUND)
    
    todos_artigos: List[Article] = []

    # 1. Carrega G1
    try:
        db_g1 = ArticleDB(db_name="articles.db")
        g1_list = db_g1.get_all_articles()
        for art in g1_list:
            art.source_db = "articles.db"
            art.source_label = "G1"
        todos_artigos.extend(g1_list)
        db_g1.close()
    except Exception as e:
        print(f"Erro ao ler G1: {e}")

    # 2. Carrega Metrópoles
    try:
        db_metro = ArticleDB(db_name="metroarticles.db")
        metro_list = db_metro.get_all_articles()
        for art in metro_list:
            art.source_db = "metroarticles.db"
            art.source_label = "Metrópoles"
        todos_artigos.extend(metro_list)
        db_metro.close()
    except Exception as e:
        print(f"Erro ao ler Metrópoles: {e}")

    # 3. Ordenação (Do mais novo para o mais antigo, assumindo ID alto = novo)
    # Como os IDs se repetem entre bancos, isso mistura eles de forma justa
    todos_artigos.sort(key=lambda x: x.id if x.id else 0, reverse=True)

    # 4. Filtro de Busca
    artigos_filtrados = todos_artigos
    if search:
        s = search.lower()
        artigos_filtrados = [
            art for art in todos_artigos 
            if s in art.title.lower() or s in str(art.url).lower()
        ]

    return templates.TemplateResponse("lumina_admin.html", {
        "request": request,
        "usuario_nome": "Administrador",
        "artigos": artigos_filtrados,
        "now": datetime.now(), 
        "search_term": search
    })

@router.post("/admin/article/add", response_class=RedirectResponse)
async def admin_add_article(request: Request, link_artigo: str = Form(...)):
    if not verify_admin_login(request):
        return RedirectResponse(url="/admin", status_code=HTTP_302_FOUND)

    manager = ScrapingManager()
    try:
        manager.scrape_and_save(link_artigo)
    except Exception as e:
        print(f"Erro ao adicionar: {e}")
        
    return RedirectResponse(url=router.url_path_for("admin_dashboard"), status_code=HTTP_302_FOUND)

@router.get("/admin/article/delete/{source_db}/{article_id}", response_class=RedirectResponse)
async def admin_delete_article(source_db: str, article_id: int, request: Request):
    if not verify_admin_login(request):
        return RedirectResponse(url="/admin", status_code=HTTP_302_FOUND)
    
    if source_db in ["articles.db", "metroarticles.db"]:
        try:
            db = ArticleDB(db_name=source_db)
            db.delete_article(article_id)
            db.close()
        except Exception as e:
            print(f"Erro ao deletar: {e}")
    
    return RedirectResponse(url=router.url_path_for("admin_dashboard"), status_code=HTTP_302_FOUND)