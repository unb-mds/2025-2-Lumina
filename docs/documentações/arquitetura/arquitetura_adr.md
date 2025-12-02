# ADR 001: Estratégia de Implantação (Banco de Dados Acoplado)

* **Status:** Aceito
* **Projeto:** Lumina

## Contexto
Estamos desenvolvendo uma aplicação que utiliza RAG (Retrieval-Augmented Generation). No estágio atual do projeto, a prioridade é a velocidade de desenvolvimento ("Time to Market"), simplicidade operacional e redução de custos de infraestrutura.

Precisamos decidir a topologia da infraestrutura: se teremos servidores de banco de dados dedicados (ex: RDS, instâncias separadas na nuvem) ou se manteremos os dados acoplados à instância da API (FastAPI).

## Decisão
Decidimos **hospedar o banco de dados relacional e o armazenamento vetorial na mesma instância (servidor) que gerencia a API**.

A arquitetura será monolítica no sentido de implantação, onde o armazenamento reside no mesmo sistema de arquivos do processo da aplicação.

## Consequências

### Positivas
* **Simplificação de DevOps:** Não há necessidade de gerenciar redes complexas (VPCs), regras de firewall entre serviços ou orquestração de containers múltiplos. O deploy é atômico.
* **Latência Zero:** A comunicação entre a API e o banco de dados ocorre via I/O de disco ou memória local, eliminando latência de rede.
* **Custo Reduzido:** Apenas uma máquina/container é necessária para rodar toda a stack.

### Negativas
* **Escalonamento Horizontal:** Adicionar mais servidores de API torna-se complexo, pois o estado (dados) está acoplado a uma única máquina.
* **Ponto Único de Falha:** Se o servidor cair ou o disco corromper, tanto a API quanto os dados ficam inacessíveis.

---

# ADR 002: Armazenamento de Artigos com SQLite

* **Status:** Aceito
* **Relacionado a:** [ADR 001: Estratégia de Implantação]

## Contexto
Precisamos de um armazenamento persistente e confiável para os textos brutos dos artigos que serão processados pelo sistema. O volume de dados esperado é compatível com armazenamento em disco local e não requer, neste momento, concorrência massiva de escrita distribuída. Precisamos de uma solução que se alinhe com a decisão de manter a infraestrutura simples.

## Decisão
Utilizaremos **SQLite** como banco de dados relacional para salvar o conteúdo textual e metadados dos artigos.

## Consequências

### Positivas
* **Serverless:** Configuração zero; o banco de dados é apenas um arquivo (`.db`) no disco.
* **Portabilidade:** Backups e migrações são feitos copiando um único arquivo.
* **Performance de Leitura:** Excelente velocidade para recuperar o texto completo de um artigo após a busca vetorial identificar os IDs relevantes.

### Negativas
* **Concorrência de Escrita:** O SQLite trava o arquivo durante a escrita (database locking). Embora o modo WAL (Write-Ahead Logging) mitigue isso, ele exige cuidado ao ser usado com servidores assíncronos (FastAPI) para evitar gargalos de I/O bloqueante.
* **Tipagem:** A tipagem dinâmica exige validação rigorosa na camada de aplicação (via Pydantic ou SQLAlchemy).

---

# ADR 003: Motor de Busca Vetorial com ChromaDB

* **Status:** Aceito
* **Relacionado a:** [ADR 001: Estratégia de Implantação]

## Contexto
Para implementar a funcionalidade de RAG, precisamos armazenar os *embeddings* (representações vetoriais) gerados a partir dos artigos e realizar buscas por similaridade semântica. O sistema precisa interagir eficientemente com o ecossistema Python de Inteligência Artificial.

## Decisão
Utilizaremos o **ChromaDB** rodando em modo persistente local para o armazenamento e recuperação de vetores.

## Consequências

### Positivas
* **Alinhamento Arquitetural:** O ChromaDB funciona nativamente em modo persistente local (usando DuckDB/Parquet internamente), alinhado com a nossa estratégia de "banco de dados junto da API".
* **Developer Experience (DX):** API simples e integração nativa com as principais bibliotecas de IA (LangChain, LlamaIndex).
* **Busca Híbrida:** Permite filtrar resultados por metadados antes ou depois da busca vetorial.

### Negativas
* **Consumo de Memória:** O carregamento de índices vetoriais (HNSW) consome memória RAM da instância da API. À medida que o número de vetores cresce, pode ser necessário aumentar a RAM do servidor.
* **Migração Futura:** Caso o projeto escale para milhões de vetores, a migração para uma instância Cliente-Servidor do Chroma será necessária.
