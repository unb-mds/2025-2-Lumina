# Estudo sobre Arquitetura e Implementação de Agentes de IA

---
## O que é um Agente de IA e seus principais padrões de arquitetura


Um agente de IA é um sistema que percebe um ambiente, decide (planeja) e atua para atingir objetivos. No contexto de aplicações web, é um software que recebe entradas (URL, texto, prompt), usa modelos/algoritmos e ferramentas externas (buscas, DBs) e devolve ações/decisões (resposta, veredito, execução de tarefas).

#### Componentes essenciais:

1. **Percepção / Input** - Captura dados: texto do usuário, páginas web, feeds de notícias, APIs.



2. **Módulo de Planejamento / Raciocínio** - Decide os passos a seguir (ex.: “buscar fontes → comparar → sintetizar”).
Geralmente implementado com um LLM(Large Language Model) + lógica de controle.



3. **Uso de Ferramentas (Tooling)** - Ferramentas externas chamadas pelo agente: web crawler, base de fatos, classificadores, tradutores.


4. **Memória**
>- **Curto prazo:** histórico da sessão, contexto atual.
>- **Longo prazo:** fatos verificados, perfis de usuário.


5. **Execução / Ação (Output)** -  Geração de relatórios, atualizações no banco de dados.

---

#### Principais padrões de arquitetura de agentes de IA


**A — Planner–Executor (Planejador + Executor**)

O que é: um módulo “planejador” gera um plano de alto nível (lista de passos/subtarefas); o “executor” implementa cada passo chamando ferramentas e retornando resultados.

Vantagens: facilita decomposição de tarefas complexas e paralelização de passos (ex.: paralelizar buscas em fontes).

Desvantagens: requer componente adicional para reconciliar resultados.


**B — Multi-agent / Orquestração (subagentes especializados)**

O que é: vários agentes especializados (pesquisador, extrator, verificador, sintetizador) colaboram, pode haver um “orquestrador” que coordena.

Vantagens: modularidade, independência de responsabilidades, fácil teste e substituição de componentes (ex.: trocar o extrator por outro melhor).

Desvantagens: complexidade operacional e de comunicação entre agentes; necessidade de mecanismos de consenso/merge de evidências.

Exemplo prático e framework que suporta multi-agent: AutoGen (Microsoft). 

---
#### RAG (Retrieval-Augmented Generation)


RAG é uma arquitetura de IA que aprimora os LLMs ao permitir que eles acessem e utilizem informações de fontes de dados externas para gerar respostas mais precisas e contextualmente ricas. Em vez de depender apenas do seu conhecimento de treinamento, um sistema RAG primeiro recupera dados relevantes de bancos de dados, documentos e da web e depois os usa para melhorar a geração de texto, garantindo que as respostas sejam mais atualizadas. 

---

#### Principais frameworks e bibliotecas para construir agentes


**LangChain**

é um framework que simplifica o desenvolvimento de aplicações baseadas em LLMs. Ele fornece "blocos de construção" prontos e ferramentas que permitem aos desenvolvedores conectar LLMs a fontes de dados, criar cadeias de processos e agentes de IA, possibilitando aplicações mais complexas e inteligentes como chatbots.

Propósito: orquestração de LLMs, RAG, agentes (tool-calling) e integração com vector DBs.

Pontos fortes: grande ecossistema, documentação, integração com provedores (OpenAI, Anthropic), suporte a agents e RAG; migração para LangGraph para execução mais sofisticada. 



**AutoGen (Microsoft)**

AutoGen é uma estrutura de código aberto projetada para criar aplicativos de IA com vários agentes que podem operar de forma semiautônoma e totalmente autônoma

Propósito: framework para construir aplicações multi-agent e workflows event-driven com LLMs.

Pontos fortes: pensado para cenários multi-agent, streaming e colaboração; suporte de pesquisa/produção da Microsoft. 



**LlamaIndex (GPT Index)**

LlamaIndex é um framework de código aberto que conecta modelos de LLMs com os seus próprios dados, permitindo a criação de aplicações de IA generativa mais precisas e contextualizadas.

Propósito: camada de ingestão e indexação de dados para agentes/assistentes (document parsing, RAG).

Pontos fortes: facilita construir "knowledge bases" sobre documentos, integra com vector DBs e agentes. Útil para extrair evidências de fontes de dados baseadas em texto. 

---
#### Intenção de um Web Crawler com um Agente de IA

**O que é um Web Crawler**

Um web crawler é um programa que Navega automaticamente pela web, visitando links e coletando informações. É usado por motores de busca (Googlebot, Bingbot) para indexar páginas.

**Interação do web crawler com o agente**

1. Agente (IA) recebe a intenção → “preciso verificar essa notícia”.

2. Crawler é acionado para coletar conteúdo atualizado em sites confiáveis.

3. O crawler retorna os dados para o agente.

4. O agente interpreta o conteúdo (NLP, embeddings, classificação).

5. O agente decide a resposta final e comunica ao usuário.

---

#### Proposta de aplicação de um agente no projeto

Vou esboçar uma funcionalidade de um agente de IA para o projeto usando o fluxo do projeto e as interações do agente.

**Objetivo da funcionalidade**

Permitir que um usuário submeta uma URL/texto e receba um relatório de verificação com veredito (Verdadeiro / Falso / Impreciso / Não Verificado), evidências citadas, score de confiança e explicação.

**Fluxo**

1. Recebe input (URL/texto) na UI.


2. Classificação de intenção → “checagem factual”.


3. Planejamento (planner) → passos: retrieve-sources, extract-claims, verify-claim, synthesize-report.


4. Tooling:

>Crawler: busca a URL submetida + extrai texto; paralelamente aciona crawler para fontes confiáveis relacionadas ao tema.

>RAG: busca de artigos verificados e no banco de dados de notícias. Usar LlamaIndex para coletar, carregar e análise de dados.

>Classificador/Comparador: modelos que comparam claims extraídos vs. evidência.


>Synthesis: LLM gera relatório explicável com citações diretas (trechos curtos), score e limitações.



5. Resposta: retorna relatório ao usuário.





**Interações do agente**

1. Busca: buscar artigos relacionados (crawler + search).

2. Extração: extrair claims/entidades/datas do texto submetido.

3. Comparação: para cada claim, recuperar evidências e checar correspondência (factualidade/tempo/contexto).

4. Sintetizar: gerar laudo com: veredito, evidências (links + trechos de artigos) e índice de confiança.




