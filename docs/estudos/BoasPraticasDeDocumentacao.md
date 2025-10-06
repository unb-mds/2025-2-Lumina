# Estudo: Boas Práticas de Documentação de Software

## 1. O que é documentação de software?

A documentação de software se refere a todo o material textual que os profissionais de engenharia, testes, produtos e outros usam para realizar seu trabalho. No entanto, isso vai além de simples instruções: é uma descrição precisa de um sistema de software, que atua como referência e fonte de evidências nos processos de desenvolvimento e uso do produto.

Portanto, uma boa documentação tem um propósito claro: abstrair a complexidade técnica de um sistema e focar no que é essencial para o usuário. Isso inclui explicações de implementações, configurações e funcionalidades, garantindo que as informações estejam completas e permitam que objetivos específicos sejam alcançados.

Além disso, seu valor está em:

* Apoiar a equipe de desenvolvimento durante as fases de criação, compreensão e manutenção do código.
* Facilitar o uso do software para usuários finais e outras partes interessadas.
* Estabelecer autoridade, pois um documento preciso e bem elaborado pode servir como evidência de decisões e processos.
* Facilitar o trabalho em equipe, garantindo que os desenvolvedores tenham acesso a informações precisas e claras, o que reduz mal-entendidos e melhora a colaboração.
* Minimizar erros e retrabalho, que geram altos custos.

Para isso, é fundamental definir o tipo de documentação necessária de acordo com as características do projeto e o perfil de quem consultará os documentos.

## 2. Quais são os tipos de documentação de software?

### 2.1. Documentação do usuário

Inclui:

* **Guia de introdução:** visão geral do software, ajudando novos usuários a se familiarizarem com os principais recursos e interface.
* **Manual do usuário:** instruções detalhadas sobre todos os recursos do software.
* **Perguntas frequentes (FAQ):** respostas às perguntas mais comuns de forma concisa e direta.
* **Tutoriais (How-to):** etapas claras e visuais para executar tarefas específicas.

### 2.2. Documentação técnica

Inclui:

* **Documentação API:** como interagir com APIs do software.
* **Comentários de código e explicações de algoritmos:** notas dentro do código que explicam a lógica de implementações complexas.
* **Guia de migração e integração:** etapas para migrar dados, configurações ou sistemas existentes.
* **Guia de implantação e instalação:** instruções para instalar e configurar o software em diferentes ambientes.
* **Notas da versão (changelog):** resumo de modificações, novos recursos e correções.

### 2.3. Documentação da plataforma

Inclui:

* **Especificações da arquitetura do sistema:** diagramas e descrições da estrutura.
* **Requisitos de hardware e software:** recursos mínimos e recomendados, incluindo dependências externas.
* **Configuração e personalização do ambiente:** instruções para adaptar a plataforma.
* **Protocolos de recuperação de desastres e backup:** procedimentos de proteção de dados.
* **Compatibilidade e suporte da plataforma:** versões suportadas e ciclos de suporte.

### 2.4. Documentação de marketing e publicidade

Inclui:

* **Páginas de apresentação de produtos:** descrição clara e atrativa para clientes potenciais.
* **Análise de mercado e estratégias de marketing:** pesquisas sobre necessidades de clientes e tendências.
* **Casos de sucesso e estudos de caso:** exemplos reais de uso do software com resultados positivos.

## 3. Quais são as melhores práticas para documentação de software?

* **Comentários objetivos:** claros, focados no porquê da ação.
* **Funções e métodos detalhados:** descrevendo finalidade, parâmetros e retornos.
* **Padronização de estilo:** consistência em toda a documentação.
* **Atualizações e testes frequentes:** revisar após mudanças significativas no código.
* **Automação de documentação:** uso de ferramentas como Swagger (APIs) ou Doxygen (C++).

## 4. Perspectivas sobre Documentação

### 4.1. A frustração com a documentação

Problemas comuns incluem efeitos colaterais de métodos, erros em etapas e documentos desatualizados.

### 4.2. Responsabilidade e Desafios

A maior parte da documentação é feita por engenheiros. No entanto, a escrita é muitas vezes vista como separada da programação, uma carga extra, e há uma percepção de falta de habilidade ou de ferramentas integradas.

### 4.3. Importância e Benefícios

* **Para o projeto:** Facilita o entendimento de código e APIs, clareza de objetivos e onboarding mais eficiente.
* **Para o autor:** Ajuda a clarificar APIs, manter um histórico, evitar a repetição de explicações e demonstra profissionalismo.
* **Para o leitor:** Documentar pensando no leitor amplia o impacto positivo ao longo do tempo.

### 4.4. Documentação como código

A abordagem moderna trata a documentação como parte do código, com regras, estilo, clareza, proprietários definidos, versionamento e revisão. Um exemplo de solução para problemas como ausência de donos e obsolescência é manter documentos versionados junto ao código, usando Markdown.

### 4.5. Conhecer o público

É fundamental identificar o público-alvo e escrever focando na clareza para ele.

## 5. Referências

* [Documentação de Software: o que é, tipos e boas práticas - Sydle](https://www.sydle.com/br/blog/documentacao-de-software-67607a278f7ac06b8fb6bbcc)
* [Software Engineering at Google, Chapter 10: Documentation - Abseil](https://abseil.io/resources/swe-book/html/ch10.html)
* [Vídeo: Como documentar código? Dicas para entrevista e projetos profissionais/pessoais - YouTube](https://youtu.be/lTjwm1CghDY)
