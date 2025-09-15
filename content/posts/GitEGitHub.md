---
draft: false
title: 'Guia Completo de Git e GitHub'
ShowToc: true
---

Este guia oferece um passo a passo detalhado sobre como utilizar Git e GitHub de forma colaborativa. O material aborda desde a configuração inicial até fluxos de trabalho avançados, explicando os conceitos, os comandos essenciais e o "porquê" de cada processo para garantir a eficiência da equipe.

## 1. Conceitos Fundamentais: Git vs. GitHub

É crucial entender a diferença entre as ferramentas:

* **Git:** É o sistema de controle de versão distribuído instalado em sua máquina. Ele é responsável por rastrear todas as alterações nos arquivos do projeto, criando um histórico detalhado.
* **GitHub:** É a plataforma online que hospeda repositórios Git. Ele funciona como o servidor central onde a equipe sincroniza seu trabalho.

Basicamente, o fluxo de trabalho consiste em manter seu repositório local (em sua máquina) sincronizado com o repositório remoto (no GitHub).

## 2. Configuração Inicial do Projeto

Existem duas maneiras de começar um projeto: criando um novo ou clonando um existente.

### Criando e Conectando um Novo Repositório

Este processo é ideal para projetos que estão começando do zero.

**Instruções (Linux e Windows):**

1. Crie um repositório remoto no GitHub.
2. Na pasta do seu projeto em sua máquina, abra o terminal (Terminal/Bash no Linux, PowerShell/CMD/Git Bash no Windows).
3. Inicie um repositório Git local:
   ```bash
   git init
   ```
   Este comando inicia um repositório local.
4. Renomeie a branch principal para `main` (uma prática moderna):
   ```bash
   git branch -M main
   ```
   Este comando cria a "gaveta principal" do projeto.
5. Conecte seu repositório local ao repositório remoto que você criou no GitHub:
   ```bash
   git remote add origin [URL_DO_SEU_REPOSITORIO.GIT]
   ```
   Este passo conecta os dois repositórios.

### Clonando um Repositório Existente

Para trabalhar em um projeto que já está no GitHub, o primeiro passo é "clonar" o repositório. Isso cria uma cópia local completa do projeto em sua máquina.

**Instruções (Linux e Windows):**
```bash
git clone [URL_DO_REPOSITORIO]
```

## 3. O Fluxo de Trabalho Essencial: Salvando e Sincronizando

O ciclo diário de trabalho envolve salvar suas alterações (commits) e sincronizá-las com a equipe.

### Passo 1: Verificar o Status das Alterações

Verifique quais arquivos foram modificados. Arquivos que não estão no repositório ou não foram atualizados aparecerão marcados.

**Comando (Linux e Windows):**
```bash
git status
```
Este comando mostra os arquivos que ainda não foram adicionados ao próximo commit (geralmente em vermelho).

### Passo 2: Adicionar Alterações à Área de Preparação

Para incluir as alterações no próximo commit, você precisa adicioná-las à "área de preparação" (Staging Area).

**Comando (Linux e Windows):**
```bash
git add .
```
Este comando encaminha todos os arquivos modificados para o repositório local, preparando-os para o commit.

### Passo 3: "Comitar" as Alterações

O commit salva um "pacote" de alterações no histórico do repositório local. É fundamental que a mensagem do commit resuma o que foi feito.

**Comando (Linux e Windows):**
```bash
git commit -m "Sua mensagem descritiva aqui"
```
Para visualizar o registro de commits, você pode usar o comando `git log`.

### Passo 4: Sincronizar com o Repositório Remoto

* **Baixar alterações (Pull):** Antes de enviar suas mudanças, sempre baixe as atualizações feitas por outros membros da equipe para evitar conflitos.

    **Comando (Linux e Windows):**
    ```bash
    git pull origin main
    ```
    Este comando atualiza seu repositório local com as mudanças que estão no repositório remoto.

* **Enviar alterações (Push):** Após fazer seus commits, envie suas contribuições para o GitHub.

    **Comando (Linux e Windows):**
    ```bash
    git push origin main
    ```
    Isso envia todas as alterações confirmadas do seu repositório local para o remoto.

## 4. Trabalhando com Branches (Ramificações)

Branches são como cópias independentes do projeto, permitindo desenvolver funcionalidades ou testar ideias de forma isolada. O código só é integrado à branch principal (`main`) depois de aprovado.

> **Por que usar várias branches?**
>
> * **Isolamento e Segurança:** Permite que desenvolvedores trabalhem em tarefas diferentes simultaneamente sem afetar a versão estável do código.
> * **Organização:** Facilita o gerenciamento de funcionalidades, correções e diferentes versões do software.

### Comandos de Branch (Linux e Windows)

* **Listar branches:**
    ```bash
    git branch
    ```
    Este comando mostra todas as ramificações existentes no repositório.

* **Criar uma nova branch e já mudar para ela:**
    ```bash
    git checkout -b nome-da-nova-branch
    ```
    O comando `checkout` altera para a nova branch, e a flag `-b` a cria.

* **Mudar para uma branch existente:**
    ```bash
    git checkout nome-da-branch
    ```
    Este comando apenas muda para a branch especificada.

* **Excluir uma branch:**
    * **Localmente:** `git branch -d nome-da-branch`
    * **Remotamente:** `git push origin --delete nome-da-branch`

### Merge: Integrando Branches

Merge é o processo de integrar as alterações de uma branch em outra.

**Como fazer um merge:**

1.  Primeiro, vá para a branch que vai **receber** as alterações (ex: `main` ou `develop`).
    ```bash
    git checkout main
    ```
2.  Execute o comando `merge`, especificando qual branch você quer integrar:
    ```bash
    git merge nome-da-branch-a-ser-integrada
    ```

## 5. Padrões de Branches: GitFlow

GitFlow é um modelo popular que organiza o fluxo de trabalho em projetos maiores.

#### Branches Principais:
* `main`: Contém o código estável, pronto para produção.
* `develop`: Serve como base para a criação de outras branches e integra todas as novas funcionalidades.

#### Branches de Suporte:
* `feature`: Criadas a partir da `develop` para implementar novas funcionalidades.
* `release`: Usadas para testar o código da `develop` antes de mesclá-lo com a `main` para um novo lançamento.
* `hotfix`: Criadas a partir da `main` para corrigir problemas críticos em produção de forma rápida. As correções são aplicadas tanto na `main` quanto na `develop`.

## 6. Tags para Versionamento de Software

Tags são marcadores usados para identificar pontos específicos no histórico, geralmente para marcar lançamentos de versões (v1.0, v1.1, v2.0).

> **Por que é importante?** Facilita a visualização e o acesso ao código exato de cada versão lançada, o que é fundamental para manutenção e organização.

**Comando (Linux e Windows):**
```bash
git tag -a v1.0 -m "Lançamento da versão 1.0"
```
Com `-a` definimos a versão e com `-m`, a mensagem da tag.

## 7. Colaboração Eficiente

### Pull Requests (PRs)

Um Pull Request (PR) é um mecanismo do GitHub para propor e analisar um merge antes que ele aconteça. É uma prática essencial para o trabalho em equipe, pois permite testar e analisar o código antes da integração.

> **Por que usar Pull Requests?**
>
> * **Revisão de Código:** Permite que a equipe analise o código, sugira melhorias e garanta a qualidade antes da integração.
> * **Discussão e Rastreabilidade:** Cria um registro formal das alterações e das decisões tomadas.
> * **Testes:** Permite a execução de testes automatizados para garantir que as novas mudanças não quebrem o sistema.

O processo envolve abrir um PR, onde as alterações são apontadas, a equipe revisa, e por fim, a branch é mesclada (`merge`).

### Issues

Issues no GitHub são usadas para organizar o projeto, funcionando como um checklist de tarefas. Elas permitem rastrear bugs, documentação, novas funcionalidades e outras demandas, ajudando a equipe a se manter alinhada. É possível usar `tags` (labels) para organizar cada issue.

## 8. Boas Práticas Adicionais

### O Arquivo `.gitignore`

> **O que é?** Um arquivo de texto chamado `.gitignore` que você coloca na raiz do seu projeto.
>
> **Por que é importante?** Nele, você lista arquivos e pastas que o Git deve ignorar completamente. Isso é crucial para evitar que arquivos desnecessários ou sensíveis sejam enviados para o repositório, como:
>
> * Pastas de dependências (ex: `node_modules`).
> * Arquivos de configuração do sistema operacional (ex: `.DS_Store` no macOS).
> * Arquivos com senhas ou chaves de API (ex: `.env`).
> * Arquivos compilados ou gerados automaticamente.

### Padrão para Mensagens de Commit (Conventional Commits)

> **O que é?** É uma convenção simples sobre como escrever as mensagens de commit para torná-las mais claras e padronizadas.
>
> **Por que é importante?** Torna o histórico do projeto muito mais legível e permite a automação de processos. Um formato comum é:
>
> * `feat`: Adiciona modal de login (para novas funcionalidades).
> * `fix`: Corrige validação de e-mail no formulário (para correção de bugs).
> * `docs`: Atualiza documentação do componente de botão (para mudanças na documentação).

## 9. Resolvendo Conflitos

Um conflito ocorre quando o Git não consegue mesclar duas alterações porque elas foram feitas na mesma parte do mesmo arquivo.

**Como resolver:**

1.  Primeiro, execute `git pull origin main` para trazer as alterações remotas e revelar o conflito em sua máquina local.
2.  Abra os arquivos conflitantes. O Git marcará as áreas problemáticas com `<<<<<<< HEAD`, `=======` e `>>>>>>>`.
3.  Edite manualmente o arquivo para manter a versão final correta, removendo as marcações do Git. Você pode manter a versão local, a remota ou uma combinação de ambas.
4.  Após resolver, adicione os arquivos corrigidos com `git add .`.
5.  Faça o commit da resolução. Geralmente, não é preciso escrever uma mensagem, pois o Git cria uma automaticamente.
    ```bash
    git commit
    ```

## 10. Fluxo de Trabalho do Desenvolvedor (Passo a Passo)

Aqui está um resumo prático do fluxo de trabalho para iniciar e concluir uma nova tarefa:

1.  **Sincronize seu ambiente:** Antes de começar, garanta que sua branch principal local está atualizada.
    ```bash
    git checkout main
    git pull origin main
    ```

2.  **Crie uma branch para a tarefa:** Crie uma nova branch a partir da `main` (ou `develop`).
    ```bash
    git checkout -b feature/nome-da-sua-tarefa
    ```

3.  **Desenvolva e faça commits:** Trabalhe no seu código e faça commits pequenos e frequentes com mensagens claras.
    ```bash
    # ... faz alterações no código ...
    git add .
    git commit -m "feat: implementa a lógica inicial do componente X"
    ```

4.  **Envie sua branch para o GitHub:** Ao finalizar a tarefa (ou ao final do dia), envie seu trabalho.
    ```bash
    git push origin feature/nome-da-sua-tarefa
    ```

5.  **Abra um Pull Request:** No GitHub, crie um Pull Request da sua branch para a branch principal (`main` ou `develop`).

6.  **Revise e faça o Merge:** Aguarde a revisão do time. Após a aprovação, o Pull Request será mesclado.

7.  **Limpeza:** Após o merge, você pode excluir sua branch de tarefa localmente.
    ```bash
    git checkout main
    git branch -d feature/nome-da-sua-tarefa
    ```

## 11. Referências:

* [Documentação Oficial do Git](https://git-scm.com/doc)
* [Guias do GitHub (GitHub Docs)](https://docs.github.com/pt)
* [Tutorial sobre o fluxo GitFlow (Atlassian)](https://www.atlassian.com/br/git/tutorials/comparing-workflows/gitflow-workflow)
* [Tutorial Interativo para Aprender Git](https://try.github.io/)