# Guia de Estudo: Testes Automatizados, Cobertura e Integração Contínua

## 1. O Propósito dos Testes Automatizados

O objetivo principal da implementação de uma cultura de testes não é apenas encontrar bugs, mas prevenir que eles ocorram e garantir a manutenibilidade do software a longo prazo. Testes automatizados funcionam como uma rede de segurança que permite ao time adicionar novas funcionalidades e refatorar o código existente com a confiança de que as partes críticas do sistema não foram quebradas.

Eles também servem como uma documentação viva do sistema, demonstrando como cada unidade de código deve se comportar.

## 2. A Estratégia Central: A Pirâmide de Testes

Não é prático ou eficiente testar tudo da mesma maneira. A "Pirâmide de Testes" é o modelo estratégico adotado para classificar os tipos de testes, balanceando velocidade, custo e confiabilidade.

### 2.1. Base: Testes Unitários

- **O que são:** Testam a menor unidade de código (uma função, um método, um componente) de forma completamente isolada de suas dependências (como APIs externas, banco de dados ou outros módulos).
- **Por que usar:** São extremamente rápidos de executar (milissegundos), baratos de escrever e fáceis de manter. A maior parte da lógica de negócio deve ser validada aqui.
- **Isolamento:** Para isolar uma unidade, utilizam-se "Mocks" (dublês), que simulam o comportamento das dependências. Por exemplo, ao testar uma função que chama a API da Gemini, o teste não deve chamar a API real; ele deve usar um mock que retorna uma resposta simulada.

### 2.2. Meio: Testes de Integração

- **O que são:** Verificam a interação e a comunicação entre duas ou mais unidades/módulos do sistema.
- **Por que usar:** Garantem que os diferentes "canos" do sistema estão conectados corretamente.
- **Exemplos no Projeto:**
  - Validar se o App Flutter (front-end) consegue enviar uma requisição e interpretar corretamente a resposta da API (back-end).
  - Validar se a API (back-end) consegue se comunicar com o banco de dados.
  - Validar se a API (back-end) consegue chamar uma API externa real (como a Gemini) e tratar sua resposta.

### 2.3. Topo: Testes End-to-End (E2E)

- **O que são:** Simulam uma jornada completa do usuário através da aplicação, da interface do usuário até o banco de dados e de volta.
- **Por que usar:** Validam o fluxo de negócio completo. São os testes que dão a maior confiança de que o sistema funciona do ponto de vista do usuário.
- **Desvantagem:** São lentos para rodar (minutos), caros para escrever e muito frágeis (quebram facilmente com mudanças na UI). Por isso, devem ser poucos e focar nos "caminhos felizes" mais críticos (ex: fluxo de login, fluxo de consulta principal).

## 3. Análise de Ferramentas e Práticas de Teste

A escolha das ferramentas é ditada pela stack do projeto (Python/FastAPI e Flutter/Dart). Esta seção explora as opções e as recomendações.

### 3.1. Stack Back-end (Python/FastAPI)

**Opção 1: `Pytest` (Recomendado)**

- **O que é:** O framework de testes *de facto* da comunidade Python.
- **Por que usar:**
  - **Sintaxe Simples:** Usa a palavra-chave `assert` nativa do Python, tornando os testes mais limpos e legíveis.
  - **Fixtures:** Possui um sistema poderoso chamado *fixtures* para configurar o estado de um teste (ex: criar um usuário no banco, iniciar um serviço).
  - **Ecossistema:** Gigantesco. Plugins como `pytest-cov` (para cobertura) e `pytest-mock` (para mocks) integram-se perfeitamente.
- **Quando usar:** Quase sempre. É a escolha padrão para projetos novos.

**Opção 2: `Unittest` (Alternativa)**

- **O que é:** O framework de testes nativo do Python (incluído na biblioteca padrão).
- **Por que considerar:** Não requer nenhuma instalação (`pip install`).
- **Por que não é recomendado:** É muito mais verboso. Exige que os testes sejam classes que herdam de `unittest.TestCase` e usa métodos de asserção como `self.assertEqual()` ou `self.assertTrue()`, tornando a escrita mais lenta e a leitura mais poluída.

**Ferramenta de Teste de API: `TestClient` (Recomendado)**

- **O que é:** Uma ferramenta fornecida pelo próprio FastAPI.
- **Por que usar:** É a solução oficial. Ele "roda" a aplicação FastAPI em memória e permite que os testes (escritos com `pytest`) chamem os endpoints diretamente, como se fossem requisições HTTP, mas sem a lentidão da camada de rede.

**Ferramenta de Cobertura: `pytest-cov` (Recomendado)**

- **O que é:** Um plugin para `pytest` que utiliza a ferramenta `Coverage.py` por baixo dos panos.
- **Por que usar:** Integra-se perfeitamente ao fluxo de teste com um simples comando (`pytest --cov`).

### 3.2. Stack Front-end (Flutter/Dart)

O ecossistema Flutter é mais fechado; as ferramentas principais já são fornecidas pelo Google e são as recomendações padrão.

**Testes Unitários: `package:test`**

- **O que é:** O framework padrão para testes unitários em Dart.
- **Foco:** Testar lógica de negócio pura (BLoCs, Cubits, Repositories, ViewModels, funções de formatação).
- **Prática Essencial (Mocking):** Para isolar a lógica, é crucial usar bibliotecas de "mock". As opções mais populares são:
  - `mockito`: A mais antiga e popular, baseada em geração de código.
  - `mocktail`: Uma alternativa mais nova que não requer geração de código, sendo mais simples de configurar.

**Testes de Widget: `package:flutter_test`**

- **O que é:** O framework padrão para testar componentes (Widgets) de UI.
- **Foco:** Permite construir um único widget (ou uma tela) em um ambiente de teste, simular interações (toques, digitação) e verificar o estado da UI (ex: `expect(find.text('Olá'), findsOneWidget);`).
- **Prática Essencial (Padrão AAA):** Testes de widget devem seguir o padrão *Arrange, Act, Assert*:
  - **Arrange (Organizar):** Construir o widget (`await tester.pumpWidget(...)`).
  - **Act (Agir):** Simular a interação do usuário (`await tester.tap(...)`).
  - **Assert (Verificar):** Checar se a UI reagiu como esperado (`expect(...)`).

**Testes de Integração/E2E: `package:integration_test`**

- **O que é:** O framework oficial do Flutter para testes E2E.
- **Por que usar:** Ele "dirige" o aplicativo real em um emulador ou dispositivo. Por ser escrito em Dart, integra-se totalmente ao projeto.
- **Alternativas (Externas):** Ferramentas como Appium ou Maestro permitem testes E2E "caixa-preta". No entanto, são mais complexas, lentas e não são escritas em Dart, o que introduz outra linguagem/ferramenta ao projeto. A recomendação é manter-se no ecossistema Flutter com `integration_test`.

### 3.3. Práticas de Escrita de Testes (Princípios FIRST)

Independentemente da ferramenta, para que os testes sejam eficazes, eles devem seguir os princípios FIRST:

- **F (Fast / Rápido):** Testes lentos são ignorados pelo time.
- **I (Isolated / Isolado):** Um teste não deve depender do estado deixado por outro.
- **R (Repeatable / Repetível):** Deve passar consistentemente em qualquer ambiente.
- **S (Self-Validating / Auto-Validado):** O teste deve retornar "Passou" ou "Falhou" sem intervenção humana.
- **T (Timely / Oportuno):** Devem ser escritos no momento certo.

### 3.4. Práticas de Desenvolvimento: TDD vs. BDD

**TDD (Test-Driven Development / Desenvolvimento Orientado a Testes):**

- **O que é:** Uma prática de desenvolvimento (popularizada pelo XP - Extreme Programming) onde o ciclo é:
  1. **Red:** Escrever um teste que falha (porque a funcionalidade não existe).
  2. **Green:** Escrever o código mínimo para o teste passar.
  3. **Refactor:** Refatorar o código (limpar, otimizar) com a segurança do teste.
- **Por que usar:** Garante 100% de cobertura e que o código escrito serve a um propósito testável.

**BDD (Behavior-Driven Development / Desenvolvimento Orientado a Comportamento):**

- **O que é:** Uma evolução do TDD. Foca em escrever os testes em linguagem natural, descrevendo o comportamento do sistema.
- **Sintaxe (Gherkin):** `Dado` (um estado inicial), `Quando` (uma ação ocorre), `Então` (um resultado é esperado).
- **Por que usar:** Alinha os testes diretamente com as Histórias de Usuário e critérios de aceitação. É muito usado para testes E2E.
- **Ferramentas:** `pytest-bdd` (Python), `flutter_gherkin` (Flutter).

## 4. Métrica de Qualidade: Cobertura de 90%

A "Cobertura de Teste" é uma métrica que indica qual porcentagem do código-fonte foi executada pelos testes automatizados.

- **Por que 90%?** É uma meta alta que força a disciplina de testes. Não garante a ausência de bugs (um teste pode "cobrir" uma linha sem validar a lógica corretamente), mas assegura que o código foi, no mínimo, executado e verificado. É um forte indicador de "pontos cegos" no código.
- **Como Medir:**
  - **Back-end:** `pytest --cov` (usando `pytest-cov`).
  - **Front-end:** `flutter test --coverage`.
- **"Coverall":** O termo (como o serviço `Coveralls.io`) refere-se a ferramentas que monitoram essa métrica ao longo do tempo, mostrando relatórios visuais e falhando o *build* se a cobertura diminuir.

## 5. Automação: O Pipeline de CI/CD

O objetivo final é automatizar essa verificação de qualidade. Isso é feito através de um Pipeline de Integração Contínua (CI).

### 5.1. Linters: A Primeira Linha de Defesa

- **O que são:** Ferramentas de análise estática. Elas leem o código sem executá-lo e apontam erros de sintaxe, bugs comuns e, principalmente, problemas de estilo.
- **Por que usar:** Garantem que todo o código enviado ao repositório siga o mesmo padrão, tornando-o mais legível e fácil de manter.
- **Ferramentas Recomendadas:**
  - **Back-end (Python):** `Ruff` (extremamente rápido e moderno, substitui Flake8 e isort).
  - **Front-end (Flutter):** `flutter analyze` (nativo, configurado no arquivo `analysis_options.yaml`).

### 5.2. GitHub Actions: O Pipeline Automatizado

- **O que é:** É a ferramenta de CI/CD nativa do GitHub. Ela permite definir um fluxo de trabalho (em um arquivo `.yml`) que será executado automaticamente em eventos do repositório (ex: a cada *push* ou *pull request*).
- **O que o pipeline fará (Obrigatório):**
  1. **Gatilho:** Iniciar quando um novo código é enviado.
  2. **Passo 1 (Linter):** Rodar o linter (`ruff` e `flutter analyze`). Se o código estiver fora do padrão, o pipeline falha.
  3. **Passo 2 (Testes):** Rodar todos os testes automatizados (`pytest` e `flutter test`). Se qualquer teste falhar, o pipeline falha.
  4. **Passo 3 (Cobertura):** Verificar se a cobertura de testes atingiu a meta (ex: 90%). Se for menor, o pipeline falha.
- **Por que usar:** Isso protege a *branch* principal (*main*). Nenhum código que quebre a aplicação, falhe nos testes ou diminua a qualidade pode ser integrado.