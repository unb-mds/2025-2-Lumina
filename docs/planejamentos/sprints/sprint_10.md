# Relatório da Sprint — Projeto Lumina

## 1. Informações Gerais

- **Sprint:** 10
- **Duração:** 03/11/2025 a 09/11/2025
- **Product Owner:** Arthur Luiz Silva Guedes
- **Scrum Master:** Cecília Costa Rebelo Cunha
- **Time de Desenvolvimento:** Átila Sobral de Oliveira, João Pedro Ferreira Gomes, Nathan Pontes Romão, Tiago Geovane da Silva Sousa

## 2. Objetivos da Sprint

Sprint focada em um avanço massivo no desenvolvimento do back-end (scrapers, splitters, embedders), implementação do banco de dados vetorial e em destravar a suíte de testes do projeto.

- Implementar todo o pipeline de extração e processamento de dados (Scraper Metrópoles, Splitter, Embedder).
- Configurar o banco de dados vetorial e o CronJob para automatizar o processo.
- Corrigir e implementar a suíte de testes do back-end para permitir o aumento da cobertura de testes.
- Avançar em features e pesquisas do front-end, incluindo o tutorial do app.

## 3. Backlog da Sprint

| Item | Tarefa                                             | Responsável(eis) | Status    |
| :--- | :------------------------------------------------- | :--------------- | :-------- |
| 1    | Pesquisar persistência do histórico dos chats no frontend | Nathan           | Concluído |
| 2    | Pesquisar sobre teste unitário no flutter            | Nathan           | Concluído |
| 3    | Implementar o tutorial no app                      | João Pedro       | Concluído |
| 4    | Continuar o desenvolvimento dos testes unitários   | Cecília          | Concluído |
| 5    | Pesquisar/Implementar o CronJob de rodar o webcrawler | Tiago            | Concluído |
| 6    | Analisar e implementar o webcrawler do Metrópoles  | Arthur, Átila    | Concluído |
| 7    | Implementar o Splitter                             | Arthur, Átila    | Concluído |
| 8    | Implementar o Embedder                             | Arthur, Átila    | Concluído |
| 9    | Implementar o Banco de dados Vetorial              | Tiago            | Concluído |

## 4. Entregas (Review)

- **Qualidade e Testes (PR de Cecília):** Foi entregue um PR crucial que destravou a suíte de testes (pytest) do back-end. Foram corrigidos NameErrors e adicionadas dependências faltantes (langchain-text-splitters, beautifulsoup4, pytest-mock). Foram implementados novos testes para TextSplitter (100% de cobertura), PageScraper (88%) e LinkExtractor (93%), aumentando a cobertura total do projeto de 10% para 15%.
- **Back-end:** A equipe reportou um "grande desenvolvimento no backend", concluindo as tarefas de implementação dos scrapers (Metrópoles), do Splitter e do Embedder.
- **Infraestrutura:** Foi implementado o Banco de Dados Vetorial e o CronJob para a automação do webcrawler.
- **Front-end:** Foram concluídas as pesquisas sobre persistência de histórico e testes unitários no Flutter, e o tutorial do app foi implementado.

## 5. Métricas da Sprint

- **Velocity (story points concluídos):** Não foram utilizados Story Points.
- **Burn-down Chart:** Gráfico não disponível.
- **Qtd. de tarefas concluídas / planejadas:** 9 / 9

## 6. Retrospectiva

### O que funcionou bem

- **Produtividade do Back-end:** O time destacou o "Grande desenvolvimento no backend" como um ponto muito positivo.
- **Qualidade da Entrega:** Houve uma "Melhoria nas entregas" gerais.
- **Colaboração:** A equipe trabalhou de forma cooperativa, proativa e dedicada (Kudos Sprint 10).

### O que pode melhorar

- **Gestão do Tempo:** O time apontou a necessidade de melhorar a "Pontualidade nas entregas", mesmo que a qualidade esteja boa.

### Ações de melhoria (Plano para Sprint 11)

- **Pontualidade:** Focar em aprimorar a pontualidade da conclusão das tarefas.