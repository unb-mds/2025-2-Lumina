from app.db.articledb import ArticleDB

db = ArticleDB()
#articles = db.get_all_titles_and_urls()

#for title, url in articles:
    #print(f"{title}\n{url}\n")

stats = db.get_stats()
print(f"Estatísticas do banco de dados: {stats}")

url = "https://g1.globo.com/tecnologia/noticia/2022/12/08/chatgpt-conheca-o-robo-conversador-que-viralizou-por-ter-resposta-para-quase-tudo.ghtml"
article = db.get_article_by_url(url)
if article:
    print(f"Artigo encontrado:\nTítulo: {article.title}\nURL: {article.url}\nConteúdo: {article.content}...")
else:
    print("Artigo não encontrado.")


db.close()