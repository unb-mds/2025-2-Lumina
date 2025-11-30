# Guia Prático para o GitHub Insights: Resumo Estratégico

## 1. Sumário Executivo

> **GitHub Insights** é um conjunto de painéis de análise que fornece dados sobre a saúde do repositório, o progresso do projeto e o engajamento da comunidade. Não se trata de uma ferramenta única, mas de uma suíte de funcionalidades distintas.

O uso eficaz desses dados permite identificar gargalos, otimizar a alocação de recursos e melhorar continuamente os fluxos de trabalho de desenvolvimento. Este guia detalha os três principais painéis do Insights — **Repositório**, **Projetos** e **Comunidade** — explicando suas métricas-chave e fornecendo estratégias para transformar dados em melhorias de processo.

---

## 2. Visão Geral Estrutural

GitHub Insights refere-se às várias ferramentas de análise nativas da plataforma. O objetivo é fornecer dados quantitativos para entender a performance e a atividade de um projeto. A análise é dividida em três áreas principais:

* **Insights do Repositório:** Focado na atividade do código-fonte (*Commits*, Contribuidores e Tráfego).
* **Insights de Projetos:** Integrado ao *GitHub Projects*, permite o acompanhamento visual do trabalho (ex: gráficos de *burn-up*).
* **Insights da Comunidade:** Específico para repositórios com *GitHub Discussions*, mede o engajamento e o crescimento da comunidade.

**Nota:** Não há um "dashboard mestre" nativo. Para obter uma visão completa, as equipes precisam consultar painéis diferentes e sintetizar as informações. O acesso geralmente requer permissões de *push* ou *maintain*.

---

## 3. Análise de Repositórios

Os Insights do Repositório fornecem uma visão geral da atividade de desenvolvimento e da interação do público com o código.

### 3.1. Pulse: O Eletrocardiograma do Projeto
O painel **Pulse** oferece um resumo da atividade do repositório em um período selecionado (padrão de 7 dias), exibindo dados sobre *pull requests* (PRs), *issues* e atividade de *commits*. É útil para uma verificação rápida do ritmo da equipe.

### 3.2. Contributors: O Mapa de Esforço da Equipe
Este gráfico visualiza os 100 principais contribuidores, detalhando o número de *commits* e as linhas de código adicionadas/removidas. É usado para identificar os membros mais ativos e detectar desequilíbrios na carga de trabalho.

> **Atenção:** Disponível apenas para repositórios com menos de 10.000 *commits*.

### 3.3. Commits & Code Frequency
* **Commits:** Mostra a frequência de *commits* por semana e dia, identificando padrões de trabalho.
* **Code Frequency:** Exibe adições e deleções de código por semana. Um alto volume de deleções pode sinalizar esforços de refatoração.

### 3.4. Traffic: Alcance e Popularidade
Rastreia a interação com a página do repositório nos últimos 14 dias.
* **Views & Unique Visitors:** Interesse geral e alcance.
* **Clones & Unique Cloners:** Interesse profundo e intenção de uso do código.
* **Referring Sites:** Origem do tráfego.

---

## 4. Insights de Projetos

Integrados ao *GitHub Projects*, permitem a criação de gráficos personalizáveis para visualizar dados como *issues* e *pull requests*.

### 4.1. Gráficos Atuais vs. Históricos
* **Atuais (Current):** Snapshot do estado atual, ideais para *status report*.
* **Históricos (Historical):** Evolução ao longo do tempo, essenciais para identificar tendências.

### 4.2. Análise do Gráfico "Burn Up"
O gráfico de **"Burn Up"** é uma ferramenta visual poderosa que compara o trabalho concluído com o escopo total. Uma linha de "Escopo Total" que sobe constantemente é sinal de *scope creep* (aumento de escopo não planejado), colocando o prazo em risco.

### 4.3. Criação de Gráficos Personalizados
A qualidade dos insights depende dos metadados definidos pela equipe.
* *Exemplo:* um gráfico de barras mostrando a contagem de *issues* por responsável (*Assignee*) ajuda a balancear a carga de trabalho em tempo real.

---

## 5. Insights da Comunidade

Painel específico para repositórios que utilizam o *GitHub Discussions*.

* **Atividade de Contribuição:** Compara o volume de Discussões vs. Issues vs. PRs.
* **Novos Contribuidores:** Mede a capacidade do projeto de atrair novos membros. Para projetos *open source*, métricas crescentes aqui indicam saúde e adoção do projeto.

---

## 6. Aplicações Práticas

Como transformar dados em ações concretas:

1.  **Otimização do Fluxo:** Se o *Burn Up* mostra platôs, ou se *issues* ficam muito tempo em "In Review", há gargalos. A solução pode ser definir SLAs para revisões ou incentivar PRs menores.
2.  **Melhoria da Produtividade:** Monitore a frequência de *commits* e volume de PRs mesclados ao introduzir novas ferramentas (como Copilot) para medir impacto.
3.  **Crescimento Open Source:** Use a análise de tráfego para focar a divulgação e o monitoramento de novos contribuidores para validar iniciativas de engajamento.

---

## 7. Limitações e Extensões

As ferramentas nativas possuem restrições importantes:

* **Limite de Commits:** Vários gráficos somem após 10.000 *commits*.
* **Métricas de Fluxo:** Faltam métricas ágeis cruciais como *Cycle Time* e *Lead Time for Changes*.
* **Dados Arquivados:** Itens arquivados não aparecem nos Insights de Projetos.

**Solução:** Para análises sofisticadas (ex: métricas DORA), recomenda-se usar a API do GitHub para dashboards personalizados ou ferramentas de terceiros do Marketplace.

---

## 8. Tabela de Referência Rápida

| Métrica | Painel | Definição Concisa | Pergunta que Responde |
| :--- | :--- | :--- | :--- |
| **Pulse** | Repositório | Resumo semanal de PRs, issues e commits. | "Qual foi o ritmo da equipe na última semana?" |
| **Code Frequency** | Repositório | Linhas de código adicionadas/removidas. | "Estamos criando features ou refatorando?" |
| **Contributors** | Repositório | Lista de contribuidores por atividade. | "Quem são os especialistas e como o trabalho está distribuído?" |
| **Unique Visitors** | Repositório | Pessoas distintas que viram a página. | "Qual é o alcance real do projeto?" |
| **Unique Cloners** | Repositório | Usuários que clonaram o repo. | "Quantas pessoas têm intenção de usar o código?" |
| **Burn Up Chart** | Projetos | Trabalho concluído vs. escopo total. | "Vamos entregar no prazo? O escopo aumentou?" |
| **Current Chart** | Projetos | Itens por status do kanban. | "Onde estão os gargalos agora?" |
| **New Contributors** | Comunidade | Novos usuários nas Discussões. | "Nossa comunidade está crescendo?" |

---

## 9. Referências

### 9.1. Documentação Oficial do GitHub
* About repository graphs
* Using Pulse to view repository activity
* Viewing traffic to a repository
* Viewing insights from your project
* Viewing insights for your discussions

### 9.2. Guias e Artigos de Análise
* **Graphite:** A deep dive into GitHub statistics and analytics
* **Keypup:** Master GitHub Analytics
* **Open Source Guides:** Open Source Metrics
* **Axify:** Git Analytics: What Works, What Doesn't
* **Neosync:** The Official Guide to Github Metrics for Open Source Projects
