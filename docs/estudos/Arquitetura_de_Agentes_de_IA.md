# Estudo: Arquitetura e Implementação de Agentes de IA

---

## 1. O que é um Agente de IA e seus principais padrões de arquitetura

Um agente de IA é um sistema que percebe um ambiente, decide (planeja) e atua para atingir objetivos. No contexto de aplicações web, é um software que recebe entradas (URL, texto, prompt), usa modelos/algoritmos e ferramentas externas (buscas, DBs) e devolve ações/decisões (resposta, veredito, execução de tarefas).

### 1.1. Componentes essenciais:

* **Percepção / Input:** Captura dados: texto do usuário, páginas web, feeds de notícias, APIs.
* **Módulo de Planejamento / Raciocínio:** Decide os passos a seguir (ex.: “buscar fontes → comparar → sintetizar”). Geralmente implementado com um LLM (Large Language Model) + lógica de controle.
* **Uso de Ferramentas (Tooling):** Ferramentas externas chamadas pelo agente: web crawler, base de fatos, classificadores, tradutores.
* **Memória:**
    * **Curto prazo:** histórico da sessão, contexto atual.
    * **Longo prazo:** fatos verificados, perfis de usuário.
* **Execução / Ação (Output):** Geração de relatórios, atualizações no banco de dados.

### 1.2. Principais padrões de arquitetura de agentes de IA

#### 1.2.1. Planner–Executor (Planejador + Executor)

* **O que é:** Um módulo “planejador” gera um plano de alto nível (lista de passos/subtarefas); o “executor” implementa cada passo chamando ferramentas e retornando resultados.
* **Vantagens:** Facilita a decomposição de tarefas complexas e a paralelização de passos (ex.: paralelizar buscas em fontes).
* **Desvantagens:** Requer um componente adicional para reconciliar resultados.

#### 1.2.2. Multi-agent / Orquestração (subagentes especializados)

* **O que é:** Vários agentes especializados (pesquisador, extrator, verificador, sintetizador) colaboram; pode haver um “orquestrador” que coordena.
* **Vantagens:** Modularidade, independência de responsabilidades, fácil teste e substituição de componentes (ex.: trocar o extrator por outro melhor).
* **Desvantagens:** Complexidade operacional e de comunicação entre agentes; necessidade de mecanismos de consenso/merge de evidências.

### 1.3. RAG (Retrieval-Augmented Generation)

RAG é uma arquitetura de IA que aprimora os LLMs ao permitir que eles acessem e utilizem informações de fontes de dados externas para gerar respostas mais precisas e contextualmente ricas. Em vez de depender apenas do seu conhecimento de treinamento, um sistema RAG primeiro recupera dados relevantes de bancos de dados, documentos e da web e depois os usa para melhorar a geração de texto, garantindo que as respostas sejam mais atualizadas.

---

## 2. Principais frameworks e bibliotecas para construir agentes

### 2.1. LangChain

É um framework que simplifica o desenvolvimento de aplicações baseadas em LLMs. Ele fornece "blocos de construção" prontos e ferramentas que permitem aos desenvolvedores conectar LLMs a fontes de dados, criar cadeias de processos e agentes de IA, possibilitando aplicações mais complexas e inteligentes como chatbots.

* **Propósito:** Orquestração de LLMs, RAG, agentes (tool-calling) e integração com vector DBs.
* **Pontos fortes:** Grande ecossistema, documentação, integração com provedores (OpenAI, Anthropic), suporte a agents e RAG; migração para LangGraph para execução mais sofisticada.

### 2.2. AutoGen (Microsoft)

AutoGen é uma estrutura de código aberto projetada para criar aplicativos de IA com vários agentes que podem operar de forma semiautônoma e totalmente autônoma.

* **Propósito:** Framework para construir aplicações multi-agent e workflows event-driven com LLMs.
* **Pontos fortes:** Pensado para cenários multi-agent, streaming e colaboração; suporte de pesquisa/produção da Microsoft.

### 2.3. LlamaIndex (GPT Index)

LlamaIndex é um framework de código aberto que conecta modelos de LLMs com os seus próprios dados, permitindo a criação de aplicações de IA generativa mais precisas e contextualizadas.

* **Propósito:** Camada de ingestão e indexação de dados para agentes/assistentes (document parsing, RAG).
* **Pontos fortes:** Facilita construir "knowledge bases" sobre documentos, integra com vector DBs e agentes. Útil para extrair evidências de fontes de dados baseadas em texto.

---

## 3. Intenção de um Web Crawler com um Agente de IA

### 3.1. O que é um Web Crawler

Um web crawler é um programa que navega automaticamente pela web, visitando links e coletando informações. É usado por motores de busca (Googlebot, Bingbot) para indexar páginas.

### 3.2. Interação do web crawler com o agente

1.  Agente (IA) recebe a intenção → “preciso verificar essa notícia”.
2.  Crawler é acionado para coletar conteúdo atualizado em sites confiáveis.
3.  O crawler retorna os dados para o agente.
4.  O agente interpreta o conteúdo (NLP, embeddings, classificação).
5.  O agente decide a resposta final e comunica ao usuário.

---

## 4. Proposta de aplicação de um agente no projeto

### 4.1. Objetivo da funcionalidade

Permitir que um usuário submeta uma URL/texto e receba um relatório de verificação com veredito (Verdadeiro / Falso / Impreciso / Não Verificado), evidências citadas, score de confiança e explicação.

### 4.2. Fluxo

* Recebe input (URL/texto) na UI.
* Classificação de intenção → “checagem factual”.
* Planejamento (planner) → passos: `retrieve-sources`, `extract-claims`, `verify-claim`, `synthesize-report`.
* **Tooling:**
    * **Crawler:** Busca a URL submetida + extrai texto; paralelamente aciona crawler para fontes confiáveis relacionadas ao tema.
    * **RAG:** Busca de artigos verificados e no banco de dados de notícias. Usar LlamaIndex para coletar, carregar e análise de dados.
    * **Classificador/Comparador:** Modelos que comparam claims extraídos vs. evidência.
    * **Synthesis:** LLM gera relatório explicável com citações diretas (trechos curtos), score e limitações.
* Resposta: Retorna relatório ao usuário.

### 4.3. Interações do agente

* **Busca:** Buscar artigos relacionados (crawler + search).
* **Extração:** Extrair claims/entidades/datas do texto submetido.
* **Comparação:** Para cada claim, recuperar evidências e checar correspondência (factualidade/tempo/contexto).
* **Sintetizar:** Gerar laudo com: veredito, evidências (links + trechos de artigos) e índice de confiança.

---

## 5. Referências

* [What are AI agents? - Google Cloud](https://cloud.google.com/discover/what-are-ai-agent)
* [Firecrawl e Web Scraping Inteligente com IA - DSA Blog](https://blog.dsacademy.com.br/firecrawl-e-web-scraping-inteligente-com-ia/)
* [LangChain Documentation](https://langchain.com)
* [LlamaIndex Documentation](https://www.llamaindex.ai)
* [AutoGen Documentation](https://microsoft.github.io/autogen/stable//index.html)
