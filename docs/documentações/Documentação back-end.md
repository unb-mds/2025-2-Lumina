
# Documentação: Tecnologia Back-End

## 1. Escolha da tecnologia

A tecnologia back-end escolhida para o projeto é a linguagem de programação Python, utilizando o framework FastAPI.

Essa escolha se justifica pela alta performance do FastAPI (baseado em Starlette e Pydantic), pela facilidade de criação de APIs assíncronas e pela vasta disponibilidade de bibliotecas para Inteligência Artificial (LangChain, Google Generative AI) e Web Scraping (BeautifulSoup, Requests), que são o coração do projeto Lumina.

## 2. Estrutura do Backend

```
backend/
├── app/                  # Código fonte principal
│   ├── ai/               # Módulos de Inteligência Artificial
│   ├── db/               # Camada de Banco de Dados
│   ├── models/           # Modelos de Dados (Schemas)
│   ├── routers/          # Definição de Rotas da API
│   ├── services/         # Regras de Negócio
│   ├── static/           # Arquivos Estáticos (CSS/JS)
│   ├── templates/        # Templates HTML (Jinja2)
│   └── webcrawler/       # Robôs de Coleta de Dados
├── scripts/              # Scripts de Execução e Manutenção
├── tests/                # Testes Automatizados (Unitários e E2E)
├── main.py               # Ponto de Entrada da Aplicação
└── requirements.txt      # Lista de Dependências
```

## 3. Descrição dos diretórios

* `app`/
Pasta responsável por conter toda a lógica da aplicação. É o núcleo do sistema, dividindo-se em sub-módulos para garantir a separação de responsabilidades.
* `app/webcrawler`/
Pasta responsável pelos robôs de coleta de dados. Aqui residem as implementações específicas para cada portal de notícias (G1, Metrópoles), incluindo extratores de links e analisadores de HTML (scrapers).
* `app/ai`/
Módulo dedicado à integração com Inteligência Artificial. Contém a configuração do modelo Gemini e a lógica de RAG (Retrieval-Augmented Generation) para gerar respostas contextualizadas.
* `app/db`/
Camada de persistência. Gerencia as conexões com os bancos de dados relacionais (SQLite) para armazenamento de artigos brutos e com o banco vetorial (ChromaDB) para busca semântica.
* `app/routers/ e app/templates`/
Responsáveis pela interface web administrativa. routers define os endpoints (URLs) e templates contém os arquivos HTML renderizados pelo Jinja2 para o Painel Admin.
* `tests`/
Pasta relacionada aos testes automatizados. O projeto utiliza Pytest para testes unitários de backend e Playwright para testes End-to-End (E2E) da interface administrativa, garantindo a robustez do sistema.
* `requirements.txt`
Arquivo responsável pelas dependências do projeto. Ele lista todas as bibliotecas Python necessárias (FastAPI, Uvicorn, LangChain, etc.) para que o ambiente possa ser replicado em qualquer máquina com o comando pip install -r requirements.txt.

## 4. Deploy

A aplicação backend é construída para ser containerizável (Docker) e pode ser implantada em qualquer serviço de nuvem que suporte Python/FastAPI (AWS, Google Cloud Run, Heroku ou DigitalOcean). Atualmente, o servidor de produção está acessível no IP 152.67.59.120.