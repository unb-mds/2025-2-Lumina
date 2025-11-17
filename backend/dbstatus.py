from app.db.articledb import ArticleDB

db = ArticleDB(db_path="backend/app/db/articles.db")

stats = db.get_stats()

print("Status do Banco de Dados de Artigos:")
print(f"Total de artigos: {stats['total']}")
print(f"Artigos pendentes de vetorização: {stats['pending_vectorization']}")
print(f"Artigos vetorizados: {stats['vectorized']}")