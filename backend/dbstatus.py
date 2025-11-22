from app.db.articledb import ArticleDB

article_db = ArticleDB(db_path=r"C:\Users\Tiago\2025-2-Lumina\backend\app\db\articles.db")

    
stats = article_db.get_stats()


print("Status do Banco de Dados de Artigos:")
print(f"Total de artigos: {stats['total']}")
print(f"Artigos pendentes de vetorização: {stats['pending_vectorization']}")
print(f"Artigos vetorizados: {stats['vectorized']}")
