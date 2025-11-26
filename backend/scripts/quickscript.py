import sys
import logging



import os
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, "..")
sys.path.append(project_root)

from app.db.articledb import ArticleDB

articledb = ArticleDB(db_name="metroarticles.db")

def main():
    articles = articledb.get_all_titles_and_urls()
    for title, url in articles:
        print(f"Title: {title}\nURL: {url}\n")
if __name__ == "__main__":
    main()