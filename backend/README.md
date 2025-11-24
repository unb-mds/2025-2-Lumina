# 📋 Requisitos Prévios

Certifique-se de que os seguintes requisitos estão instalados no seu sistema:

1. **Python**: Versão 3.10 ou superior.
2. **pip**: O gerenciador de pacotes do Python, que geralmente é instalado junto com o Python.

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

O servidor estará rodando, geralmente, em `http://127.0.0.1:8000` (ou `http://localhost:8000`).

ip do servidor na nuvem: 152.67.59.120

## 6. Estrutura do Projeto

### Backend

A estrutura de pastas do backend foi organizada para separar as responsabilidades e facilitar a manutenção.

```
backend/
├── app/
│   ├── ai/
│   │   ├── ai_models/
│   │   ├── rag/
│   │   └── system_prompts/
│   ├── db/
│   ├── models/
│   ├── services/
│   └── webcrawler/
│       ├── G1/
│       └── Metropoles/
├── tests/
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


