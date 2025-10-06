# Estudo de Métricas Open Source

A saúde de projetos open source (OSS) tornou-se uma disciplina crucial. A viabilidade e sustentabilidade de um projeto dependem da vitalidade da sua comunidade e da eficácia dos seus processos.

## 1. A Saúde do Projeto como Terceiro Pilar Estratégico

A gestão de risco em OSS tradicionalmente foca em:
- Conformidade de licenças
- Segurança de vulnerabilidades

Estes são pilares reativos. A **saúde do projeto** emerge como um terceiro pilar proativo que avalia o bem-estar social e a resiliência de um projeto.

Em vez de procurar falhas no código, esta abordagem foca na dinâmica da comunidade de contribuidores e na eficiência das atividades de desenvolvimento. OSS é um artefacto sociotécnico: o código é o esqueleto, mas a comunidade é o motor.

## 2. Estrutura de Análise: Quatro Dimensões

### 2.1. Vitalidade da Comunidade
Avalia o capital humano do projeto. Uma comunidade vibrante, com fluxo de novos contribuidores e diversidade organizacional, indica sustentabilidade.

### 2.2. Velocidade de Desenvolvimento
Mede o pulso operacional. Refere-se à eficiência do ciclo de desenvolvimento, desde a resposta a contribuições até a entrega de versões. Resposta rápida sinaliza mantenedores engajados.

### 2.3. Governança e Manutenibilidade
Examina a estrutura organizacional e processos. Boa governança proporciona clareza e transparência. Documentação de qualidade reduz a barreira para novos contribuidores.

### 2.4. Resiliência e Influência no Ecossistema
Avalia o impacto e posição do projeto no ecossistema de software. Quantifica adoção, popularidade e importância para outras tecnologias.

Estas dimensões funcionam em ciclo de feedback contínuo.

## 3. Principais Métricas

### 3.1. Vitalidade da Comunidade

* **Bus Factor:** O menor número de pessoas responsáveis por 50% das contribuições. Bus factor baixo (1 ou 2) é sinal de alerta de dependência de indivíduos-chave.
* **Diversidade Organizacional:** Número de empresas cujos funcionários contribuem. Reduz o risco de abandono por uma única entidade.

### 3.2. Velocidade de Desenvolvimento

* **Tempo para Primeira Resposta:** Tempo mediano para resposta humana a nova issue ou pull request. Impacta diretamente a retenção de novos contribuidores.
* **Rácio de Fecho de Issues/PRs:** Relação entre issues/PRs abertos e fechados. Backlog crescente indica equipa sobrecarregada.

### 3.3. Governança e Manutenibilidade

* **Qualidade da Documentação:** Presença de README, CONTRIBUTING.md e Código de Conduta. Indica projeto acolhedor e bem gerido.

### 3.4. Resiliência e Influência

* **Dependentes do Projeto:** Número de outros projetos que dependem deste. Número elevado indica infraestrutura crítica.

## 4. Ferramentas de Análise

### 4.1. Framework CHAOSS
Iniciativa da Linux Foundation que cria padrão universal para saúde de comunidades open source. Oferece catálogo de métricas e "Modelos de Métricas" para análise estratégica profunda.

### 4.2. GitHub Insights
Ferramentas de análise nativas do GitHub, acessível no separador "Insights". Fornece dados em tempo real sobre tráfego, contribuidores e commits. Perfeito para monitorização tática diária.

**As ferramentas são complementares:** GitHub Insights oferece visão tática do "agora", CHAOSS fornece lente estratégica para análise de risco.

## 5. Aplicação Prática

### 5.1. Casos de Uso

* **Avaliação de Dependências Externas:** Use lista de verificação de devida diligência para avaliar risco de nova dependência. Inclui verificação de documentação, análise de atividade no GitHub Insights e avaliação de risco da comunidade.
* **Monitorização de Projetos Internos:** Crie painel de saúde para monitorização contínua. Balance indicadores antecipados (preveem saúde futura) e indicadores atrasados (relatam desempenho passado).

### 5.2. Painel Inicial Recomendado

* **Para avaliação de dependências:**
    * Bus Factor
    * Frequência de Lançamentos
    * Diversidade Organizacional
* **Para gestão de projetos internos:**
    * Tempo para Primeira Resposta
    * Contagem de Novos Contribuidores
    * Tempo Médio para Merge de PRs

## 6. Conclusão

As métricas não são alvo, mas ferramenta para iniciar conversas e orientar estratégia. O contexto de cada projeto é fundamental. Use os dados para tomar medidas informadas que melhorem a saúde e sustentabilidade do ecossistema open source.

## 7. Referências

* **CHAOSS (Community Health Analytics in Open Source Software):** [https://chaoss.community/](https://chaoss.community/)
* **Guia de Métricas de Código Aberto:** [https://opensource.guide/metrics/](https://opensource.guide/metrics/)
* **Project Health as the Third Pillar of Open Source Strategy:** [https://bitergia.com/blog/project-health-is-the-third-pillar-of-open-source-strategy/](https://bitergia.com/blog/project-health-is-the-third-pillar-of-open-source-strategy/)
* **GitHub Insights:** [https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository](https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository)
* **Guia Conciso OpenSSF para Avaliação de Software Open Source:** [https://best.openssf.org/Concise-Guide-for-Evaluating-Open-Source-Software.html](https://best.openssf.org/Concise-Guide-for-Evaluating-Open-Source-Software.html)
