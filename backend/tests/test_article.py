import pytest

from app.models.article import Article

# Dados de teste variados
test_articles = [
    {
        "title": "Artigo sobre Python",
        "author": "Alice",
        "url": "https://exemplo.com/python",
        "content": "Python é uma linguagem poderosa.",
    },
    {
        "title": "Notícia de Tecnologia",
        "author": "Bob",
        "url": "https://exemplo.com/tech",
        "content": "Novas tecnologias estão surgindo.",
    },
    {
        "title": "Artigo Vazio",
        "author": "Carol",
        "url": "https://exemplo.com/vazio",
        "content": "",
    },
]


@pytest.mark.parametrize("data", test_articles)
def test_article_creation(data):
    """Testa a criação de objetos Article com diferentes dados."""
    article = Article(**data)

    assert article.title == data["title"]
    assert article.author == data["author"]
    assert article.url.startswith("https://")
    assert isinstance(article.content, str)
