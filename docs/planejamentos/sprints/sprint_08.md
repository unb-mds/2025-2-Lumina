# Relatório da Sprint — Projeto Lumina

## 1. Informações Gerais

- **Sprint:** 08
- **Duração:** 20/10/2025 a 26/10/2025
- **Product Owner:** Arthur Luiz Silva Guedes
- **Scrum Master:** Cecília Costa Rebelo Cunha
- **Time de Desenvolvimento:** Átila Sobral de Oliveira, João Pedro Ferreira Gomes, Nathan Pontes Romão, Tiago Geovane da Silva Sousa

## 2. Objetivos da Sprint

Sprint focada em estruturar o back-end (spider, scrapers e BD), implementar os primeiros testes e avançar na persistência de dados do front-end.

- Desenvolver o spider para alimentar os scrapers e refatorar o código existente.
- Criar e organizar a estrutura do banco de dados para receber os dados minerados.
- Implementar a persistência local das configurações de usuário no front-end.
- Iniciar a criação de testes unitários para o back-end.

## 3. Backlog da Sprint

| Item | Tarefa                                                       | Responsável(eis)       | Status    |
| :--- | :----------------------------------------------------------- | :--------------------- | :-------- |
| 1    | Trabalhar no spider para puxar os links para o scraper       | Átila, Arthur, Tiago   | Concluído |
| 2    | Refatorar o código dos scrapers para adotar o padrão         | Átila, Arthur          | Concluído |
| 3    | Criar persistência nas opções de configuração do usuário (frontend) | Nathan, João           | Concluído |
| 4    | Criar testes unitários para o back-end                       | Cecília                | Concluído |
| 5    | Pesquisar persistência do histórico dos chats no frontend    | Nathan, João           | Concluído |
| 6    | Criar/Organizar um banco de dados para o webcrawler          | Tiago                  | Concluído |
| 7    | Pesquisar sobre testes unitários E2E no frontend             | Nathan, João           | Concluído |

## 4. Entregas (Review)

- **Front-end:** Foi entregue a implementação da funcionalidade dos botões das configurações (persistência local).
- **Back-end:** A equipe avançou no desenvolvimento do WebCrawler, incluindo o spider e a refatoração dos scrapers.
- **Infraestrutura:** A estrutura inicial do banco de dados foi montada por Tiago para receber os dados.
- **Qualidade:** Cecília entregou a sua issue referente à implementação dos primeiros testes unitários.

## 5. Métricas da Sprint

- **Velocity (story points concluídos):** Não foram utilizados Story Points.
- **Burn-down Chart:** Gráfico não disponível.
- **Qtd. de tarefas concluídas / planejadas:** 7 / 7

## 6. Retrospectiva

### O que funcionou bem

- **Front-end:** O time destacou o "Bom desenvolvimento do Front".
- **Colaboração:** Houve uma "Melhora do trabalho em equipe", com todos os membros sendo proativos e prestativos (Kudos da Sprint 08).

### O que pode melhorar

- **Qualidade de Código:** Foi identificada a necessidade de ter mais "Atenção ao padrão do código".
- **Processo de Revisão:** A equipe precisa "Informar sobre os PRs e solicitar reviews" de forma mais consistente.

### Ações de melhoria (Plano para Sprint 09)

- **Padronização:** Focar na "Padronização do código".
- **Pull Requests:** "Utilizar melhor os PRs e pedir para revisarem o código" para garantir a qualidade antes do merge.