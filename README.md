# Lumina
## 1. Objetivo
Projeto desenvolvido para a disciplina de **Métodos e Desenvolvimentos de Software - 2025/2**
---
O objetivo do projeto é combater as fake news que vem em constante crescente, fazendo isso por meio de um chatbot para uma verificação de fatos e informação rápida, competindo com mecanismos de busca tradicionais e outras plataformas de checagem de notícias, com o diferencial de uma interface conversacional intuitiva.

## 2. Tecnologias Utilizadas
As seguintes tecnologias foram utilizadas nesse projeto:
- Front-end: Flutter
- Back-end: Python
- APIs: Gemini API
- Frameworks: Fast API

## 3. Como Contribuir
Para contribuir você pode acessar o arquivo [CONTRIBUTING.md](CONTRIBUTING.md)

## 4. Autores
O projeto é desenvolvido pelas seguintes pessoas

|Nome|Função|Github|
|-----|-----|------|
| Cecília Costa Rebelo Cunha |Scrum Master (Líder de projeto)| [CeciliaCunha](https://github.com/CeciliaCunha) |
|Arthur Luiz Silva Guedes|Product Manager (PO)| [ArthurLuizUnB](https://github.com/ArthurLuizUnB)|
|Átila Sobral de Oliveira|Developer| [Atila05](https://github.com/Atila05)|
|Nathan Pontes Romão|Developer (Líder)| [nathanpromao](https://github.com/nathanpromao)|
|João Pedro Ferreira Gomes |Designer|[Joao-PFG](https://github.com/Joao-PFG)|
|Tiago Geovane da Silva Sousa|Arquitetura/DevOps|[TiagoUNB](https://github.com/TiagoUNB)|
------------

# 5. Links importantes
- Nosso [Git Pages](https://unb-mds.github.io/2025-2-Lumina)

- Nosso [Figma](https://www.figma.com/design/WAbCYuadSmQjoSXwQu2FZa/Squad-07--MDS?node-id=1-3188&t=jXbDeQuQQlIQOL1h-0)

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
