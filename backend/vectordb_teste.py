from app.webcrawler.G1.g1scraper import G1Scraper
from app.webcrawler.dowloader import Downloader
from app.db.vectordb import VectorDB
from app.ai.rag.text_splitter import TextSplitter
from app.ai.rag.google_embedder import GoogleEmbedder
def test_g1_scraper(url: str):
    scraper = G1Scraper()
    downloader = Downloader()

    html_data = downloader.fetch(url)
    article = scraper.scrape_article(url,html_data)
    
    if article:
        print("- Título do artigo:", article.title)
        print("- Autor do artigo:", article.author)
        print("- URL do artigo:", article.url)
        print("- Conteúdo do artigo:", article.content)
    else:
        print("Falha ao raspar o artigo.")
    
    print("Todos os testes passaram com sucesso.")
    return article

if __name__ == "__main__":
    test_url = "https://g1.globo.com/tecnologia/noticia/2022/12/08/chatgpt-conheca-o-robo-conversador-que-viralizou-por-ter-resposta-para-quase-tudo.ghtml"
    article = test_g1_scraper(test_url)
    article.id = "14474756"  # Atribuindo um ID fictício para o artigo
    api_key = "AIzaSyAxVj7YVDBEAm0eF25JnYTnyVhBNl17_Mw"
    vectorDB = VectorDB(text_splitter=TextSplitter(), embedding_platform=GoogleEmbedder(api_key=api_key))
    vectorDB.vectorize_article(article)

