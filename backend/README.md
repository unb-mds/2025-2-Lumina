# 🧠 Backend Lumina (API & Crawler)

O núcleo de processamento do Lumina, responsável pela coleta de notícias, armazenamento vetorial, processamento de IA e gerenciamento de conteúdo via Painel Administrativo.

# 📋 Requisitos Prévios

Certifique-se de que os seguintes requisitos estão instalados no seu sistema:

1. **Python**: Versão 3.10 ou superior.
2. **pip**: O gerenciador de pacotes do Python, que geralmente é instalado junto com o Python.
3. **Navegadores(Opcional)**: Para rodar os testes de interface (E2E): eles são relativamente pesados, por isso foram colocados no gitignore. Portanto, será necessário instalar os binários do Playwright (instruções abaixo).

---

## 🛠️ Configuração do Ambiente

### 1. Instalação de Dependências

Todas as bibliotecas necessárias para o projeto estão listadas no arquivo `requirements.txt`.

Para instalá-las, abra o seu terminal no diretório raiz do projeto e execute o comando:

```bash
pip install -r requirements.txt
```

### 2. Configuração da Chave API do Gemini

O projeto requer uma chave de API para interagir com o modelo Gemini. Você precisa criar um arquivo chamado `.env` na raiz do seu projeto e adicionar sua chave nele.

O conteúdo do seu arquivo `.env` deve seguir este formato:

```
GOOGLE_API_KEY="SUA_CHAVE_DE_API_DO_GEMINI_AQUI"
```

* Substitua `"SUA_CHAVE_DE_API_DO_GEMINI_AQUI"` pela sua chave real.

### 3. Instalação do Playwright (Para Testes E2E)

Se você pretende rodar os testes de interface (frontend do admin), instale os navegadores necessários:

```
python -m playwright install chromium
```



---

## 🚀 Como Rodar o Servidor

Após instalar as dependências e configurar a chave API, você pode iniciar o servidor localmente usando Uvicorn.

Execute o seguinte comando no terminal (ainda no diretório raiz do projeto):

```bash
uvicorn main:app --reload
```

### Detalhes do Comando

* `uvicorn`: O servidor ASGI rápido que estamos usando.
* `main:app`: Indica ao Uvicorn para procurar a aplicação (variável `app`) dentro do módulo (`main.py`).
* `--reload`: Ativa o modo de recarga automática. O servidor será reiniciado automaticamente sempre que você salvar alterações no seu código-fonte, o que é ótimo para o desenvolvimento.

O servidor estará rodando `http://127.0.0.1:8000`.
- API Docs (Swagger): `http://127.0.0.1:8000/docs`
- Painel Admin: `http://127.0.0.1:8000/admin`

ip do servidor na nuvem: 152.67.59.120

## 📰 Painel Administrativo (Lumina Admin)

O sistema possui uma interface web para gerenciamento das notícias coletadas.

Após instalar as dependências e configurar a chave API, você pode iniciar o servidor localmente usando Uvicorn.

Execute o seguinte comando no terminal (dentro da pasta backend):

```bash
uvicorn main:app --reload
```

* `uvicorn`: O servidor ASGI rápido que estamos usando.
* `main:app`: Indica ao Uvicorn para procurar a aplicação (variável `app`) dentro do módulo (`main.py`).
* `--reload`: Ativa o modo de recarga automática. O servidor será reiniciado automaticamente sempre que você salvar alterações no seu código-fonte, o que é ótimo para o desenvolvimento.

O servidor estará rodando em `http://127.0.0.1:8000/admin`
Faça login com a senha de administrador configurada (Padrão: admin).

**Funcionalidades**
- Dashboard Unificado: Visualiza notícias de múltiplas fontes (G1 e Metrópoles) em uma única tabela.
- Estatísticas (KPIs): Cards informativos com o total de artigos coletados por fonte.
- Adicionar Notícia: Permite inserir manualmente um link de notícia para ser processado pelo Crawler.
- Exclusão: Remove artigos indesejados do banco de dados.

## 🕷️ Crawlers e Coleta de Dados

O sistema suporta múltiplos crawlers que podem ser executados manualmente para popular o banco de dados.

**Executar Crawler do G1**

```
python -m scripts.run_crawler
```

**Executar Crawler do Metrópoles**

```
python -m scripts.run_metropoles_crawler
```

**Nota:** Os crawlers salvam o estado em arquivos JSON (`crawler_state.json`) para permitir pausar e continuar a coleta posteriormente.

## ✅ Testes Automatizados

O projeto segue uma rigorosa política de testes, cobrindo desde a unidade até a interface do usuário.

1. Testes de Backend (Unidade e Integração)
Testam a lógica do banco de dados, crawlers e endpoints da API.

```
pytest
```

(Ignora automaticamente a pasta tests/e2e para ser mais rápido)

2. Testes de Frontend (End-to-End / E2E)

Testam a interface do Admin simulando um usuário real navegando no Chrome.
**Requisito:** O servidor deve estar rodando em outro terminal (`uvicorn main:app`).

```
python -m pytest tests/e2e --browser chromium
```

Para ver o navegador abrindo na tela, adicione `--headed --slowmo 1000`.



## 📂 Estrutura do Projeto

### Backend

A estrutura de pastas do backend foi organizada para separar as responsabilidades e facilitar a manutenção.

```
backend/
├── app/
│   ├── ai/                 # Lógica de IA (Gemini, RAG, Embeddings)
│   ├── db/                 # Gerenciamento de Banco de Dados (SQLite e ChromaDB)
│   ├── models/             # Modelos de Dados (Pydantic)
│   ├── routers/            # Rotas da API e do Admin
│   ├── services/           # Lógica de Negócio (ChatService, ScrapingManager)
│   ├── static/             # Arquivos CSS/JS do Admin
│   ├── templates/          # Templates HTML (Jinja2) do Admin
│   └── webcrawler/         # Módulos de Coleta de Dados
│       ├── G1/             # Implementação específica G1
│       └── Metropoles/     # Implementação específica Metrópoles
├── scripts/                # Scripts utilitários (Executar crawler, Debug DB)
├── tests/                  # Testes Automatizados
│   ├── e2e/                # Testes de Interface (Playwright)
│   └── ...                 # Testes de Unidade (Pytest)
├── main.py                 # Ponto de entrada da aplicação
└── requirements.txt        # Dependências do projeto
```

### Módulos Principais

*   **`main.py`**: Ponto de entrada do servidor FastAPI. Responsável por orquestrar as rotas da API que expõem as funcionalidades do sistema, como a busca e sumarização de notícias.

*   **`run_crawler.py`**: Script dedicado para iniciar o processo de rastreamento e scraping de notícias. Ele ativa os crawlers específicos para cada fonte de notícia.

*   **`app/webcrawler/`**: Módulo central para a coleta de dados. Contém a lógica para rastrear sites de notícias e extrair links para artigos. É projetado de forma extensível para suportar novas fontes.
    *   **`G1/`** e **`Metropoles/`**: Subdiretórios que contêm a implementação específica para cada portal, incluindo a extração de links e o scraping do conteúdo.

*   **`app/models/`**: Define as estruturas de dados do projeto, como o modelo `Article`, que representa um artigo de notícia com seus atributos (título, conteúdo, data, etc.).

*   **`app/db/`**: Camada de persistência de dados. Gerencia a conexão com o banco de dados SQLite (`articles.db`) e o banco de vetores (`ChromaDB`), sendo responsável por armazenar e consultar os artigos e seus embeddings.

*   **`app/ai/`**: Módulo de inteligência artificial. Integra-se com o Google Gemini para realizar tarefas de processamento de linguagem natural, como a sumarização de textos, utilizando a técnica de RAG (Retrieval-Augmented Generation).

*   **`tests/`**: Contém os testes automatizados do projeto, garantindo a qualidade e o correto funcionamento dos componentes.
