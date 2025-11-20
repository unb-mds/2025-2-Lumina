import pytest
from app.models.article import Article

test_articles = [
    {
        "url": "https://exemplo.com/python",
        "title": "Artigo sobre Python",
        "author": "Alice",
        "content": "Python é uma linguagem poderosa.",
    },
    {
        "url": "https://exemplo.com/tech",
        "title": "Notícia de Tecnologia",
        "author": "Bob",
        "content": "Novas tecnologias estão surgindo.",
    },
    {
        "url": "https://exemplo.com/vazio",
        "title": "Artigo Vazio",
        "author": "Carol",
        "content": "",
    },
]


@pytest.mark.parametrize("data", test_articles)
def test_article_creation(data):
    """Testa a criação de objetos Article com diferentes dados."""
    article = Article(**data)

    assert article.title == data["title"]
    assert article.author == data["author"]
    assert str(article.url).startswith("https://")
    assert article.content == data["content"]