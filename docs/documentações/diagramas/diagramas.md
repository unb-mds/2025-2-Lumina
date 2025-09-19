## Diagramas da Arquitetura do Sistema
- Stack Tecnologica
  - Backend: Python com Fast API
  - Frontend Mobile: Flutter
  - Frontend Web: HTML, JS E CSS no git pages
  - Banco de Dados: Chroma DB e SQLite

## Contexto
``` mermaid
---
config:
  theme: forest
---
graph TD
    subgraph " "
        direction LR
        User["Usuário Final"]
        Admin["Administrador"]
    end
    subgraph " "
        direction LR
        LLM_API["API Externa do Gemini"]
        NewsSources["Fontes de Notícias"]
    end
    System["Sistema de Chatbot Anti-Fake News"]
    User -- "Verifica notícias e faz perguntas [via App Móvel]" --> System
    Admin -- "Gerencia a base de notícias [via Interface Web de Admin]" --> System
    System -- "Envia prompts com contexto para gerar respostas [HTTPS/JSON]" --> LLM_API
    System -- "Coleta artigos para a base de dados [via Web Crawler]" --> NewsSources 
```
## Conteineres
``` mermaid
---
config:
  theme: forest
---
flowchart TD
 subgraph subGraph0["Sistema de Chatbot Anti-Fake News"]
    direction LR
        MobileApp["Aplicativo Móvel (Flutter, Android)"]
        API["API do Chatbot (Python, FastAPI)"]
        VectorDB["Banco de Dados Vetorial (ChromaDB)"]
        AdminWeb["Interface Web de Admin (HTML/JS/CSS)"]
        IngestionPipeline["Pipeline de Ingestão (Web Crawler - Python Script)"]
        LocalDB["Banco de Dados Local (SQLite)"]
  end
    User["Usuário Final"] -- Usa --> MobileApp
    MobileApp -- Armazena histórico/usuário --> LocalDB
    MobileApp -- Envia perguntas, recebe respostas [HTTPS/JSON] --> API
    Admin["Administrador"] -- Usa --> AdminWeb
    AdminWeb -- Adiciona/Remove fontes, visualiza dados [HTTPS/JSON] --> API
    API -- Busca por similaridade de texto --> VectorDB
    API -- Envia prompt com contexto [HTTPS/JSON] --> LLM_API["API Externa do Gemini"]
    IngestionPipeline -- Coleta artigos --> NewsSources["Fontes de Notícias (Portais Online)"]
    IngestionPipeline -- Processa e insere vetores de artigos --> VectorDB
     MobileApp:::containerStyle
     API:::containerStyle
     VectorDB:::containerStyle
     AdminWeb:::containerStyle
     IngestionPipeline:::containerStyle
     LocalDB:::databaseStyle
     User:::actorStyle
     Admin:::actorStyle
     LLM_API:::systemStyle
     NewsSources:::systemStyle
    classDef actorStyle fill:#f9f,stroke:#333,stroke-width:2px
    classDef systemStyle fill:#bbf,stroke:#333,stroke-width:2px
    classDef containerStyle fill:#ffc,stroke:#333,stroke-width:2px
    classDef databaseStyle fill:#cfc,stroke:#333,stroke-width:2px
    style MobileApp fill:#FFFFFF,stroke:#000000
    style API fill:#FFFFFF
    style VectorDB fill:#FFFFFF
    style AdminWeb fill:#FFFFFF
    style IngestionPipeline fill:#FFFFFF
    style LocalDB fill:#FFFFFF
    style User fill:#00C853,stroke:#00C853
    style Admin stroke:#00C853,fill:#00C853
    style LLM_API stroke:#2962FF,fill:#2962FF
```

## Componentes
``` mermaid
---
config:
  theme: forest
  layout: dagre
---
flowchart TD
    A[WebCrawler<br><br>Acessa sites relevantes de artigos e informações para obter o conteúdo dentro deles e minerar para dentro do sistema] --> B[Splitter e Embedder<br><br>Separa o conteúdo minerado em chunks para guardar melhor no banco de dados, e utiliza um algoritmo de embedding para transformá-los em vetores numéricos]
    B --> C[Retriever<br><br>Após uma pergunta do Usuário usa um algoritmo para buscar informações relevantes no banco de dados e retorna a pergunta junto com o contexto relevante]
    A --> D[LLM<br><br>Recebe o contexto, um prompt e a pergunta do usuário para retornar uma mensagem com maior precisão de acordo com o que foi perguntado]
    C --> D

```
