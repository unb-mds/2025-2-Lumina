# Boas práticas de documentação de Software

[referência
1](https://www.sydle.com/br/blog/documentacao-de-software-67607a278f7ac06b8fb6bbcc)

No desenvolvimento de software, a documentação de software não é apenas
um complemento, mas uma ferramenta essencial para garantir a
compreensão, manutenção e evolução de um projeto.

## O que é documentação de software?

A **documentação de software** se refere a todo o **material textual** que os
profissionais de engenharia, testes, produtos e outros **usam para realizar seu trabalho**. No entanto, isso vai além de simples instruções:
é uma **descrição precisa** de um sistema de software, que **atua como referência** e fonte de evidências nos processos de desenvolvimento e uso
do produto.

Portanto, uma boa documentação tem um **propósito** claro: abstrair a
complexidade técnica de um sistema e **focar no que é essencial** para o
usuário. Isso inclui explicações de implementações, configurações e
funcionalidades, garantindo que as informações estejam completas e
permitam que objetivos específicos sejam alcançados.

Além disso, seu valor está em: 
- **Apoiar a equipe de desenvolvimento durante as fases de criação**, compreensão e manutenção do código. 
- **Facilitar o uso do software** para usuários finais e outras partes
interessadas. 
- **Estabelecer autoridade**, pois um documento preciso e bem
elaborado pode servir como evidência de decisões e processos. 
- **Facilitar o trabalho em equipe**, garantindo que os desenvolvedores tenham
acesso a informações precisas e claras, o que reduz mal-entendidos e
melhora a colaboração. 
- **Minimizar erros e retrabalho**, que geram altos
custos.

Para isso, é fundamental definir o **tipo de documentação** necessária de
acordo com as características do projeto e o perfil de quem consultará
os documentos.

## Quais são os tipos de documentação de software?

### 1. Documentação do usuário

Inclui: 
- **Guia de introdução**: visão geral do software, ajudando
novos usuários a se familiarizarem com os principais recursos e
interface. 
- **Manual do usuário**: instruções detalhadas sobre todos os
recursos do software. 
- **Perguntas frequentes (FAQ)**: respostas às
perguntas mais comuns de forma concisa e direta. 
- **Tutoriais (How-to)**: etapas claras e visuais para executar tarefas específicas.

### 2. Documentação técnica

Inclui: 
- **Documentação API**: como interagir com APIs do software. 
- **Comentários de código e explicações de algoritmos**: notas dentro do
código que explicam a lógica de implementações complexas. 
- **Guia de migração e integração**: etapas para migrar dados, configurações ou
sistemas existentes. 
- **Guia de implantação e instalação**: instruções
para instalar e configurar o software em diferentes ambientes. 
- **Notas da versão (changelog)**: resumo de modificações, novos recursos e
correções.

### 3. Documentação da plataforma

Inclui: 
- **Especificações da arquitetura do sistema**: diagramas e descrições da estrutura. 
- **Requisitos de hardware e software**: recursos mínimos e recomendados, incluindo dependências externas. 
- **Configuração e personalização do ambiente**: instruções para adaptar a
plataforma. 
- **Protocolos de recuperação de desastres e backup**: procedimentos de proteção de dados. 
- **Compatibilidade e suporte da plataforma**: versões suportadas e ciclos de suporte.

### 4. Documentação de marketing e publicidade

Inclui: 
- **Páginas de apresentação de produtos**: descrição clara e
atrativa para clientes potenciais. 
- **Análise de mercado e estratégias de marketing**: pesquisas sobre necessidades de clientes e tendências. 
- **Casos de sucesso e estudos de caso**: exemplos reais de uso do
software com resultados positivos.

## Quais são as melhores práticas para documentação de software?

-   **Comentários objetivos**: claros, focados no porquê da ação.
-   **Funções e métodos detalhados**: descrevendo finalidade, parâmetros
    e retornos.
-   **Padronização de estilo**: consistência em toda a documentação.
-   **Atualizações e testes frequentes**: revisar após mudanças
    significativas no código.
-   **Automação de documentação**: uso de ferramentas como Swagger
    (APIs) ou Doxygen (C++).

[Referência 2](https://abseil.io/resources/swe-book/html/ch10.html)

Um resumo por ChatGPT do livro: *Software Engineering at Google*.

### 1. Introdução -- A frustração com a documentação

Problemas comuns: efeitos colaterais de métodos, erros em etapas,
documentos desatualizados.

### 2. Responsabilidade dos engenheiros

Maior parte da documentação é feita por engenheiros, com suporte
necessário.

### 3. Comparativo com testes

Documentação ainda não reconhecida institucionalmente, mas ganhando
importância.

### 4. O que constitui documentação?

Engloba qualquer texto essencial, desde documentos até comentários no
código.

### 5. Por que é importante?

-   Entendimento de código e APIs.
-   Clareza de objetivos do projeto.
-   Onboarding mais eficiente.
-   Benefícios de longo prazo.

### 6. Desafios

-   Escrita vista como separada de programação.
-   Percepção de falta de habilidade.
-   Falta de ferramentas integradas.
-   Vista como carga extra.

### 7. Benefícios ao autor

-   Clarificação de APIs.
-   Histórico e manutenção.
-   Profissionalismo e melhor manutenção.
-   Evita repetição de explicações.

### 8. Benefícios ao leitor

Documentar pensando no leitor amplia impacto ao longo do tempo.

### 9. Documentação como código

-   Regras, estilo, clareza.
-   Proprietários definidos.
-   Versionamento e revisão.

#### Caso GooWiki

-   Problemas: ausência de donos, duplicidade, obsolescência.
-   Solução: documentos versionados junto ao código, usando Markdown e
    g3doc.

### 10. Conhecer o público

-   Identificar público-alvo.
-   Escrever focando na clareza para ele.

[Vídeo Suporte: Como documentar código? Dicas para entrevista e projetos profissionais/pessoais](https://youtu.be/lTjwm1CghDY?si=FkzLHYYmXIJXAIzC)
