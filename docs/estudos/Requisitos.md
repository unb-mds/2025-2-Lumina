# Estudo: Fundamentos de Análise de Requisitos

## 1. Definição

Um **requisito de software** é uma declaração que define **o que o sistema deve fazer** ou **as restrições sob as quais ele deve operar**. Eles são fundamentais na etapa inicial do desenvolvimento de um software, responsável por identificar, analisar, documentar e validar as necessidades do cliente/usuário.
Sem requisitos bem definidos, corre-se o risco de desenvolver um sistema **que não resolve o problema real** ou **não atende às expectativas do cliente**.


## 2. Classificação dos Requisitos

### 2.1. Requisitos Funcionais (RF)

São as **funções e serviços** que o sistema deve oferecer. Normalmente descritos como **interações entre usuários e sistema**.
**Exemplos**:

- O sistema deve permitir que o usuário crie uma conta.

- O sistema deve registrar transações de pagamento.

- O usuário deve poder consultar seu histórico de compras.


### 2.2. Requisitos Não Funcionais (RNF)

Estão relacionados a **atributos de qualidade** do sistema. São restrições ou características globais que não dizem respeito a funções específicas, mas ao comportamento esperado.

**Exemplos**:

- **Desempenho:** o sistema deve responder a consultas em menos de 1 segundo.

- **Segurança:** dados de senha devem ser armazenados criptografados.

- **Confiabilidade:** o sistema deve estar disponível 24/7.

- **Usabilidade:** a interface deve ser intuitiva e acessível.

- **Portabilidade:** o software deve rodar em Windows, Linux e Mac.


## 3. Engenharia de Requisitos

O processo de trabalhar com requisitos passa por várias fases:

1.  **Elicitação (levantamento)**

    - Descobrir o que os clientes/usuários realmente precisam.

    - Técnicas: entrevistas, questionários, observação, análise de documentos, prototipagem.

2.  **Análise**

    - Verificar se os requisitos levantados são **consistentes, viáveis e completos**.

    - Resolver conflitos entre diferentes necessidades dos usuários.

3.  **Especificação**

    - Documentar os requisitos de forma clara e organizada (pode ser em linguagem natural estruturada, casos de uso, histórias de usuário).

4.  **Validação**

    - Confirmar com os clientes/usuários se os requisitos levantados realmente atingem suas expectativas.

5.  **Gerenciamento de Requisitos**

    - Manter os requisitos **sob controle** ao longo do projeto.

    - Permitir que mudanças sejam feitas de forma **rastreável (muito importante, já que requisitos mudam com frequência)**.


## 4. Como Levantar Requisitos de Software

1.  **Identificar os stakeholders**

    - Stakeholders são todas as pessoas ou entidades interessadas no sistema (usuários, clientes, gestores, equipe técnica, órgãos reguladores).

2.  **Definir o contexto do sistema**

    - Entender o problema que será resolvido.

    - Mapear o ambiente onde o software vai funcionar e as interações com outros sistemas.

3.  **Técnicas de elicitação (levantamento)**
    Existem várias maneiras de coletar requisitos. Algumas das principais:

    - Entrevistas.

    - Questionários e pesquisas.

    - Análise de documentos existentes (examinar relatórios, planilhas, sistemas antigos, normas e regulamentos).

4.  **Analisar e priorizar requisitos**

    - Nem todos os requisitos têm a mesma importância. Alguns são essenciais (sem eles o sistema não funciona), outros são apenas desejáveis.

5.  **Documentar os requisitos**

    - Depois de levantar, é preciso registrar de forma clara. Formato comum: lista de requisitos funcionais e não funcionais.

6.  **Validar os requisitos**

    - Revisar os requisitos com os stakeholders para garantir que estão corretos.

    - Técnicas: revisões, protótipos, simulações, reuniões de feedback.


## 5. Características de Bons Requisitos

Para que um requisito seja útil é recomendado que ele seja:

* **Correto:** realmente representa a necessidade do cliente.

* **Completo:** inclui todas as informações necessárias.

* **Consistente:** não entra em conflito com outros requisitos.

* **Não ambíguo:** escrito de forma clara, sem múltiplas interpretações.

* **Verificável:** é possível testar se foi implementado.

* **Viável:** pode ser implementado com os recursos disponíveis.


## 6. Proposta de Requisitos do Projeto 'É Fake'

Estas são algumas ideias para os requisitos do projeto, **não são os requisitos finais**.


### 6.1. Requisitos Funcionais (RF)

Ou seja, o que o sistema deve ou pode fazer:

1.  O sistema pode permitir que o usuário **insira um link, texto ou título de uma notícia** para verificação.

2.  O sistema deve **coletar automaticamente artigos de sites confiáveis** (fontes pré-definidas).

3.  O sistema deve utilizar **algoritmos de IA** para comparar o conteúdo da notícia enviada com informações das fontes confiáveis.

4.  O sistema pode classificar a notícia como:

    * **Verdadeira**,

    * **Falsa**,

    * **Imprecisa / Manipulada**,

    * **Não verificada (sem evidências suficientes)**.

5.  O sistema deve exibir ao usuário um **relatório de checagem**, incluindo:

    * Fontes usadas na análise.

    * Grau de confiança da IA.

    * Trechos de comparação entre a notícia e as fontes.

6.  O sistema pode oferecer **explicação da IA**, ou seja, mostrar de forma compreensível por que uma notícia foi considerada falsa ou verdadeira.

7.  O sistema pode permitir que o usuário **visualize histórico de checagens** (apenas se estiver logado).

8.  O sistema pode oferecer **cadastro e login de usuários** para salvar preferências e histórico.

9.  O sistema pode gerar **estatísticas** (ex.: percentual de notícias falsas detectadas por tema).


### 6.2. Requisitos Não Funcionais (RNF)

Relacionados à qualidade do sistema:

1.  O sistema deve ser **seguro**, garantindo criptografia de dados (HTTPS, senhas criptografadas).

2.  A arquitetura deve ser **escalável**, suportando grande volume de acessos simultâneos.

3.  A interface deve ser **intuitiva e responsiva**, acessível em desktop e dispositivos móveis.

4.  O sistema deve suportar **atualização automática** das fontes confiáveis quando disponível.


5.  O administrador deve conseguir **atualizar a lista de sites confiáveis**.

6.  O sistema pode **considerar contextos linguísticos** (ex.: ironia, sátiras, manchetes sensacionalistas).

7.  O sistema pode permitir **análise multilíngue** (português, inglês pelo menos).


## 7. Resumo

Levantar requisitos significa descobrir, organizar e validar o que o sistema deve fazer e como deve funcionar. Isso é feito ouvindo os clientes e usuários, analisando processos atuais e usando técnicas como entrevistas e análises de relatórios.

O projeto precisará combinar **mineração de dados e checagem automática de fontes confiáveis**. Os requisitos devem garantir não só as funções principais (minerar, verificar, classificar), mas também **qualidade** (segurança, escalabilidade, relatório de checagem).
**Os requisitos definitivos do projeto ainda serão debatidos e definidos.**


## 8. Referências

* **Introdução a Requisitos de Software** - [DevMedia](https://www.devmedia.com.br/introducao-a-requisitos-de-software/29580)

* **Requisitos de Software: Funcionais e Não Funcionais** - [SoftDesign](https://softdesign.com.br/blog/requisitos-de-software-funcionais-e-nao-funcionais/)

* **Engenharia de Software em Destaque: Levantamento de Requisitos** - [Estratégia Concursos](https://www.estrategiaconcursos.com.br/blog/engenharia-software-levantamento-requisitos/)
