# Prompt de Contextualização de LLM para o Projeto "Lumina"

Você é um assistente de IA especialista e desenvolvedor Python. Sua tarefa é trabalhar em um projeto chamado **"Lumina"**, um serviço de agregação e sumarização de notícias.  
Abaixo está uma visão detalhada da arquitetura, tecnologias e principais fluxos de trabalho do projeto.

---

## 1. Objetivo Geral do Projeto

O projeto é um sistema backend baseado em **Python**, projetado para:

a. Rastrear sites de notícias específicos (iniciando com **G1** e preparado para **Metrópoles**).  
b. Fazer **scraping** e extrair conteúdo de notícias individuais.  
c. Armazenar os dados estruturados dos artigos em um banco de dados **SQLite** local.  
d. Fazer um processo de embedding para transformar os artigos em vetores numericos
e. Utilizar o **Google Gemini LLM** para gerar resumos ou outros insights a partir do conteúdo das notícias atravez de RAG
f. Expor esses dados e funcionalidades por meio de um servidor web **FastAPI**.

---

## 2. Tecnologias Principais

- **Framework Backend:** FastAPI (em `main.py`) — usado para construir e servir a API web.  
- **Web Crawling/Scraping:** `requests` e `BeautifulSoup4` — bibliotecas principais para buscar e analisar conteúdo HTML.  
- **Banco de Dados:** SQLite (identificado por `articles.db`, provavelmente usando o módulo padrão `sqlite3` em `app/db/articledb.py`).  
- **Integração com IA:** Google Gemini (via biblioteca `google-generativeai`, configurada em `app/ai/gemini.py`).  
- **Testes:** Pytest (configurado em `pytest.ini`, com testes no diretório `tests/`).  
- **Estilo de Código e Linting:** Ruff (inferido pelo diretório `.ruff_cache`).

---

## 3. Módulos-Chave e Interações entre Classes

O projeto segue uma estrutura modular dentro do diretório `app/`.

### **Pontos de Entrada**
- **`main.py`**: Ponto principal de execução do servidor FastAPI. Orquestra as rotas da API.  
- **`run_crawler.py`**: Script dedicado para iniciar o processo de rastreamento e scraping de notícias.

### **`app.webcrawler` (Ingestão de Dados)**
- Módulo central de coleta de dados, projetado para ser extensível a múltiplas fontes de notícias.  
- **`app.webcrawler.G1`**: Contém a lógica específica para o portal de notícias G1.  
  - `g1linkextractor.py`: Localiza e extrai URLs de artigos individuais nas páginas do G1.  
  - `g1scraper.py`: Baixa e analisa páginas HTML para extrair informações principais (título, autor, data, conteúdo, etc.), preenchendo um modelo `Article`.  
  - `g1webcrawler.py`: Orquestra o processo do G1, utilizando o extrator de links e o scraper para processar múltiplos artigos.  
- **`app.webcrawler.Metropoles`**: Um módulo semelhante iniciado para o site Metrópoles, evidenciando uma arquitetura “plug-and-play” para novas fontes.

### **`app.models` (Estruturas de Dados)**
- **`article.py`**: Define o modelo central de dados para um artigo de notícia.  
  - Provavelmente um modelo **Pydantic** ou **dataclass**, contendo campos como `url`, `title`, `content`, `publication_date`, entre outros.

### **`app.db` (Camada de Persistência)**
- **`articledb.py`**: Gerencia todas as operações com o banco de dados.  
  - Contém funções como `add_article()`, `get_article()`, `list_articles()`, etc.  
  - Recebe objetos `Article` do módulo `models` e os salva no banco `articles.db`.  
  - Responsável por executar todas as consultas SQL.

### **`app.ai` (Camada de Inteligência)**
- **`gemini.py`**: Responsável por todas as interações com a API do **Google Gemini**.  
  - Possui funções como `summarize_text(text: str)` que recebem o conteúdo de um artigo.  
  - Lê um prompt base em `app/ai/system_prompts/system_prompt.md`, que define o tom, formato e tarefa do LLM (ex: “Você é um sumarizador de notícias útil…”).  
- **`ai_models/responses.py`**: Provavelmente define a estrutura de dados para as respostas geradas pela IA.

---

## 4. Fluxo Principal (Crawler → Banco de Dados)

1. O script `run_crawler.py` é executado.  
2. Ele instancia e executa o `g1webcrawler` do módulo `app.webcrawler.G1.g1webcrawler`.  
3. O `g1webcrawler` utiliza o `g1linkextractor` para obter uma lista de URLs de artigos.  
4. Para cada URL, o `g1scraper` busca a página e a converte em um objeto `Article` estruturado (de `app.models.article`).  
5. O scraper chama uma função em `app.db.articledb` (ex: `add_article`) para salvar o objeto `Article` no banco de dados `articles.db`.

---

## 5. Sua Tarefa

Seu principal objetivo é **auxiliar no desenvolvimento e manutenção do projeto "Lumina"**.  
Ao adicionar funcionalidades, corrigir bugs ou responder perguntas, siga rigorosamente a arquitetura e tecnologias existentes.

Exemplos de boas práticas:

- Ao adicionar uma nova fonte de notícias, crie um novo subdiretório em `app/webcrawler/`, imitando a estrutura de `G1/` ou `Metropoles/`.  
- Ao modificar interações com o banco de dados, edite `app/db/articledb.py`.  
- Ao alterar o comportamento da API, modifique `main.py`.  
- Sempre utilize os modelos definidos em `app/models/`.  
- Garanta que o novo código seja testável e, quando apropriado, adicione novos testes no diretório `tests/`.

---
