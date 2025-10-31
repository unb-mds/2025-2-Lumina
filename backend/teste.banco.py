from app.db.articledb import ArticleDB

db = ArticleDB()
articles = db.get_all_titles_and_urls()

for title, url in articles:
    print(f"{title}\n{url}\n")

db.close()