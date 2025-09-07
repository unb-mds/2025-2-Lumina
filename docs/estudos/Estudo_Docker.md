# Roteiro de Estudo: Docker para Padronização de Ambientes

## 1. Objetivo

Este roteiro organiza nosso estudo sobre Docker. O objetivo é aprender a usar contêineres para padronizar nossos ambientes de desenvolvimento, eliminando o problema de "na minha máquina funciona". Com o Docker, garantimos que a aplicação se comporte da mesma forma em qualquer máquina, desde o desenvolvimento até a produção.

---

## 2. Conceitos Fundamentais

Antes de começar, é crucial entender a diferença entre **Contêineres e Máquinas Virtuais (VMs)**.
* Uma **VM** virtualiza o hardware para rodar um sistema operacional completo, o que a torna pesada e lenta para iniciar.
* Um **Contêiner** virtualiza o sistema operacional, compartilhando o mesmo kernel do sistema hospedeiro. Isso o torna extremamente leve, rápido e portátil.

Os quatro pilares do Docker que precisamos dominar são:

* **Imagem (Image):** É o "molde" ou "pacote" estático e imutável que contém tudo o que a aplicação precisa para rodar: o código, as bibliotecas, as variáveis de ambiente e os arquivos de configuração. Imagens são construídas a partir de um Dockerfile.

* **Contêiner (Container):** É a instância em execução de uma imagem. É o ambiente isolado e executável onde a aplicação realmente vive. Podemos criar, iniciar, parar e remover múltiplos contêineres a partir da mesma imagem.

* **Dockerfile:** É um arquivo de texto que contém um script com comandos, passo a passo, para construir uma imagem Docker. É a nossa "receita de bolo" para criar o ambiente perfeito para a aplicação.

* **Volume:** É o mecanismo para persistir dados gerados por um contêiner. Ele mapeia um diretório do contêiner para um diretório na máquina hospedeira (host), garantindo que os dados (como arquivos de um banco de dados) não sejam perdidos quando o contêiner for removido.

---

## 3. Módulos de Aprendizagem Prática

Vamos dividir a parte prática em etapas lógicas para construir o conhecimento progressivamente.

### Módulo 1: Primeiros Passos e Comandos Essenciais

* **Foco:** Familiarizar-se com a instalação do Docker e executar um contêiner a partir de uma imagem pública do Docker Hub (o repositório oficial de imagens).
* **Comandos Chave:** `docker run`, `docker ps`, `docker images`, `docker pull`.
* **Resultado Esperado:** Ser capaz de baixar e executar a imagem do `nginx` e acessá-la pelo navegador, entendendo o conceito de mapeamento de portas (`-p 8080:80`).

### Módulo 2: Criando Nossa Própria Imagem com Dockerfile

* **Foco:** Aprender a escrever um `Dockerfile` para empacotar uma aplicação simples (ex: um "Hello World" em Python ou Node.js).
* **Comandos Chave:** `docker build`, `docker tag`.
* **Resultado Esperado:** Criar um `Dockerfile` que copie os arquivos da nossa aplicação, instale suas dependências e defina o comando para executá-la. Construir uma imagem a partir deste arquivo.

### Módulo 3: Orquestrando Serviços com Docker Compose

* **Foco:** Entender como gerenciar aplicações que dependem de múltiplos serviços (como uma API e um banco de dados) de forma simples e declarativa.
* **Conceito Chave:** O arquivo `docker-compose.yml`, que descreve todos os serviços, redes e volumes necessários para a aplicação.
* **Comandos Chave:** `docker-compose up`, `docker-compose down`.
* **Resultado Esperado:** Criar um arquivo `docker-compose.yml` que defina dois serviços: nossa aplicação customizada (do Módulo 2) e um banco de dados (ex: `postgres` ou `mysql`), e fazê-los se comunicarem.

---

## 4. Plano de Ação

Para atingir os objetivos, seguiremos os seguintes passos:

1.  **Instalação e Ambiente:** Instalar o Docker Desktop em nossas máquinas e executar os primeiros comandos (`docker run hello-world`) para verificar se tudo está funcionando.
2.  **Estudo Conceitual:** Pesquisar e documentar em poucas linhas a diferença prática entre Contêineres e VMs.
3.  **Prática com Dockerfile:** Seguir um tutorial para criar um `Dockerfile` para uma aplicação simples. Durante o processo, praticar o mapeamento de portas (`-p`) e o uso de volumes (`-v`) para injetar arquivos de configuração ou salvar logs.
4.  **Prática com Docker Compose:** Desenvolver um arquivo `docker-compose.yml` que orquestre a aplicação criada no passo anterior junto com um serviço de banco de dados público (ex: a imagem oficial do `postgres`).

---

## 5. Recursos Recomendados

* **Documentação Oficial (Get Started):** O melhor lugar para começar. É direto e cobre todos os conceitos essenciais. [Docker Get Started Guide](https://docs.docker.com/get-started/)
* **Docker Hub:** Para pesquisar e encontrar imagens públicas para quase qualquer serviço que precisarmos. [Docker Hub](https://hub.docker.com/)
* **Awesome Docker (GitHub):** Uma lista curada de excelentes recursos, tutoriais e ferramentas sobre Docker. [Link para a Lista](https://github.com/veggiemonk/awesome-docker)