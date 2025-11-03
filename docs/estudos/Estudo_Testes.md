# Guia Prático de Testes Automatizados

Este guia ensina como escrever testes unitários para a classe `Article`, medir cobertura de código e automatizar testes de forma prática usando Python e pytest.

---

## 1. Por que testar

Testes automatizados garantem que o código funciona corretamente e ajudam a prevenir bugs. Eles facilitam a refatoração do código e servem como documentação viva, mostrando como cada função ou classe deve se comportar. Para serem eficazes, os testes devem ser rápidos, isolados, repetíveis e auto-validados, ou seja, devem informar se passaram ou falharam sem intervenção manual.

---

## 2. Tipos de testes

Existem três tipos principais de testes que podem ser aplicados a um projeto:

1. **Testes Unitários**: Testam funções ou métodos isolados, sem depender de outras partes do sistema. Mocks podem ser usados para simular dependências externas, como APIs ou banco de dados. São rápidos, baratos e fáceis de manter.

2. **Testes de Integração**: Verificam se diferentes módulos do sistema funcionam bem juntos, por exemplo, se a API consegue se comunicar com o banco de dados ou com outra API externa.

3. **Testes End-to-End (E2E)**: Simulam o fluxo completo do usuário, desde a interface até o banco de dados e de volta. São mais lentos e frágeis, então devem ser usados apenas para os fluxos mais críticos.

---

## 3. Estrutura do projeto

Uma organização mínima para o projeto seria:

* `app/models/article.py`: classe `Article`.
* `tests/test_article.py`: testes unitários do `Article`.
* `pytest.ini`: configuração do pytest.

Exemplo de arquivo `pytest.ini`:

```
[pytest]
pythonpath = .
testpaths = tests
python_files = test_*.py
```

---

## 4. Instalação das dependências

Para instalar pytest e o plugin de cobertura, execute:

```
python -m pip install pytest pytest-cov
```

---

## 5. Criando testes unitários para Article

Você pode criar testes que validem a criação de objetos `Article` e seus atributos. Use o recurso de parametrização do pytest para testar múltiplos casos automaticamente.

Exemplo:

```python
import pytest
from app.models.article import Article

test_articles = [
    {"title": "Python", "author": "Alice", "url": "https://exemplo.com/python", "content": "Linguagem poderosa."},
    {"title": "Notícia", "author": "Bob", "url": "https://exemplo.com/news", "content": ""},
]

@pytest.mark.parametrize("data", test_articles)
def test_article_creation(data):
    article = Article(**data)
    assert article.title == data["title"]
    assert article.author == data["author"]
    assert article.url.startswith("https://")
    assert isinstance(article.content, str)
```

Não é necessário usar artigos reais. Dados fictícios já permitem testar se a criação do objeto funciona corretamente.

---

## 6. Rodando os testes e cobrindo o código

Para executar os testes e medir a cobertura:

```
python -m pytest -v --cov=app.models.article --cov-report=term-missing
```

* `-v` mostra detalhes dos testes.
* `--cov` calcula a cobertura.
* `--cov-report=term-missing` mostra as linhas do código que não foram testadas.

---

## 7. Automatizando os testes com GitHub Actions

Você pode configurar o GitHub Actions para rodar os testes automaticamente a cada push ou pull request. Um workflow mínimo seria:

```
name: Run Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: python -m pip install --upgrade pip
      - run: pip install pytest pytest-cov
      - run: python -m pytest -v --cov=app.models.article --cov-report=term-missing
```

Dessa forma, todos os testes são executados automaticamente e qualquer erro ou redução de cobertura será detectado imediatamente.

---

## 8. Resumo prático

1. Escreva testes unitários usando pytest e dados fictícios.
2. Use `@pytest.mark.parametrize` para testar múltiplos casos de forma automática.
3. Meça a cobertura de código com pytest-cov.
4. Configure CI/CD com GitHub Actions para automatizar os testes em cada push.

