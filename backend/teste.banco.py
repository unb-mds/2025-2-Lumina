from app.db.articledb import ArticleDB

db = ArticleDB()

stats = db.get_stats()
print(f"Estatísticas do banco de dados: {stats}")

db.close()