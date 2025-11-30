# Documento de Estudo: Ferramentas para Análise de Métricas Ágeis no GitHub

---

### 1. Introdução

Com o objetivo de aprimorar a previsibilidade, a eficiência e a transparência do nosso processo de desenvolvimento no projeto Lumina, este documento apresenta um estudo sobre a adoção de métricas ágeis. O foco é pesquisar e analisar ferramentas que se integrem ao nosso ambiente de desenvolvimento no GitHub para gerar, de forma automatizada, gráficos de **Burndown** e **Velocity**, auxiliando o time a visualizar o progresso e a entender sua capacidade de entrega a cada Sprint.

### 2. Definição e Relevância das Métricas Ágeis

Antes de analisar as ferramentas, é crucial compreender o valor que estas métricas agregam ao time.

* **Gráfico de Burndown:**
    * **O que é?** Uma representação visual do trabalho *restante* versus o tempo *disponível*. O eixo vertical mostra a quantidade de esforço (em Story Points) e o horizontal mostra os dias da Sprint.
    * **Utilidade Prática:** Permite ao time responder rapidamente à pergunta: "Estamos no caminho certo para entregar o que planejamos?". Uma linha de progresso que se desvia muito da linha ideal sinaliza a necessidade de discutir impedimentos ou replanejar.

* **Gráfico de Velocity (Velocidade):**
    * **O que é?** Mede a quantidade média de trabalho (Story Points) que o time consegue concluir por Sprint.
    * **Utilidade Prática:** É uma métrica fundamental para o planejamento. Com base na velocidade histórica, o Product Owner pode prever com mais segurança o escopo da próxima Sprint e estimar o prazo para entregas maiores (como Epics ou versões do produto).

### 3. Análise de Ferramentas

A pesquisa avaliou soluções nativas do GitHub e ferramentas de terceiros disponíveis no GitHub Marketplace.

#### 3.1. Solução Nativa: GitHub Projects & Insights

* **Descrição:** O GitHub oferece funcionalidades de gerenciamento de projetos através do "GitHub Projects" e visualizações de dados na aba "Insights".
* **Análise:**
    * **Vantagens:** É uma solução 100% gratuita e já integrada ao nosso ambiente. Permite a criação de gráficos customizados que podem simular um gráfico de Burnup (trabalho concluído ao longo do tempo).
    * **Desvantagens:** Não oferece gráficos de Burndown e Velocity de forma nativa. A configuração manual para criar visualizações similares é pouco prática e o resultado não é tão claro quanto o de ferramentas especializadas. A ausência de um sistema formal de "Sprints" e "Story Points" dificulta a aplicação direta de metodologias ágeis.
* **Conclusão:** Insuficiente para uma análise ágil robusta e automatizada.

#### 3.2. Ferramenta de Terceiros: Zenhub

* **Descrição:** Uma plataforma de gerenciamento de projetos que se integra diretamente à interface do usuário (UI) do GitHub, adicionando funcionalidades ágeis que não existem nativamente.
* **Análise:**
    * **Vantagens:**
        * **Integração Total:** Funciona dentro do GitHub, evitando a troca de contexto entre ferramentas.
        * **Métricas Automatizadas:** Gera automaticamente relatórios de Burndown, Velocity e Cumulative Flow.
        * **Funcionalidades Ágeis:** Adiciona suporte a Sprints, estimativas em Story Points, Epics e Roadmaps.
        * **Custo:** Oferece um plano gratuito para repositórios públicos e times pequenos, com planos pagos acessíveis.
    * **Desvantagens:** Para repositórios privados e times maiores, possui um custo por usuário.
* **Conclusão:** Uma solução completa que transforma o GitHub em uma ferramenta de gerenciamento ágil poderosa e centralizada.

#### 3.3. Ferramenta de Terceiros: Screenful

* **Descrição:** Um serviço especializado em criar dashboards e relatórios visuais a partir de dados de plataformas de desenvolvimento, incluindo o GitHub.
* **Análise:**
    * **Vantagens:**
        * **Dashboards de Alta Qualidade:** Os gráficos são visualmente bem-acabados, ideais para apresentações a stakeholders.
        * **Métricas Avançadas:** Além de Burndown e Velocity, oferece métricas como Lead Time e Cycle Time, que medem o fluxo de trabalho.
    * **Desvantagens:**
        * **Ferramenta Externa:** A análise e a visualização ocorrem em um dashboard fora do GitHub.
        * **Foco em Análise, Não em Gestão:** Não auxilia no gerenciamento do dia a dia das tarefas, apenas na visualização dos dados.
        * **Custo:** O modelo de preço é por time, o que pode ser mais caro que o Zenhub para equipes pequenas.
* **Conclusão:** Excelente para times focados em análise de dados e que precisam compartilhar relatórios, mas menos prático para a gestão integrada do dia a dia.

### 4. Tabela Comparativa

| Critério                  | GitHub Nativo                                              | Zenhub                                                        | Screenful                                    |
| :------------------------ | :--------------------------------------------------------- | :------------------------------------------------------------ | :------------------------------------------- |
| **Gráficos (Burndown/Velocity)** | ❌ Não nativos                                           | ✅ Automáticos e integrados                                   | ✅ Automáticos e de alta qualidade           |
| **Integração com UI do GitHub** | ✅ Total                                                   | ✅ Total (adiciona novas abas)                                | ❌ Externa (dashboard separado)              |
| **Facilidade de Uso** | ⚠️ Moderada                                                | ✅ Alta                                                       | ✅ Alta                                      |
| **Ecossistema Ágil** | Básico (Issues)                                            | Completo (Sprints, Points, Epics)                             | Focado em relatórios                         |
| **Custo (Plano de Entrada)** | Gratuito                                                   | Gratuito (para repositórios públicos) ou ~$8/usuário/mês      | ~$39/mês (para o time)                       |

### 5. Próximos Passos

1.  **Escolha da Ferramenta:** Apresentar este estudo ao time para decidir qual ferramenta será adotada.
2.  **Instalação e Configuração:** Configurar a ferramenta escolhida no repositório "Lumina".
3.  **Sessão de Treinamento:** Realizar uma breve reunião com o time para demonstrar o uso da nova ferramenta.
4.  **Execução e Reavaliação:** Utilizar a ferramenta na próxima Sprint e, ao final, discutir os resultados e a experiência na reunião de retrospectiva.

### 6. Referências e Leitura Adicional

* [Scrum Guide](https://scrumguides.org/scrum-guide.html) - O guia definitivo sobre o framework Scrum.
* [What is a Burndown Chart?](https://www.atlassian.com/agile/project-management/charts/burndown-chart) - Artigo da Atlassian sobre o uso e interpretação de gráficos de Burndown.
* [Velocity - Agile Alliance](https://www.agilealliance.org/glossary/velocity/) - Definição e boas práticas para o uso da métrica de velocidade.
* [Documentação Oficial do Zenhub](https://help.zenhub.com/)
* [Documentação Oficial do Screenful](https://screenful.com/guide)

```
