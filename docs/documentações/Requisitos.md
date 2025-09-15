## *Requisitos Funcionais*

---

### Dentro desse tópico vou esclarecer o que o sistema ira ter e quais são as funcionalidades tecnicas que ele obrigatoriamente deve ter para funcionar de forma adequada ao projeto

#### Irei separar por alguns topicos para que no futuro fique de melhor entendimento, lembrando que caso prefira algo mais visual, futuramente (Caso ainda não implementado enquanto você estiver lendo), existe um campo no Figma para requisitos.

#### Primeiramente irei explicar a jornada do usuario ao usar o aplicativo depois irei detalhar individualmente os processos necessarios para que isso aconteça.

---

### Para que fique claro o que foi apresentado, dentro da idealização da interface e desing do aplicativo, foi acordado que seria algo com uma tématica clean e esteticamente parecida com a página de buscas inicial do google.

Explicando como funcionará a ordem de ação do usuario (Para melhor explicação irei criar uma pessoa ficticia e ela sera o usuario)

1- Carla é uma professora universitaria que se encontra diariamente debatendo com seus alunos em classe. Dentro desses debates Carla constantemente se encontra com infomações que seus alunos trazem a ela, tais como constações absurdas ou mesmo noticias que ela não tem o conhecimento de sua veracidade.

2- Por ser uma pessoa ligada nas redes sociais, Carla para se previnir da desinformação na internet escolheu uma forma de se inteirar sobre o que #ÉFake, baixando assim o aplicativo mobile em seu Android. (Unica opção devido ao aplicativo não existir para IOS) 

3- Ao instalar o aplicativo sem dificuldades, Carla depois de poucos segundos (no maximo 3) se depara com uma interface clara e intuitiva, contendo uma caixa de buscas, uma interface interresante que comunica bem a ideia do projeto e algumas outras funcionalidades, como: configurações, historico de conversas*, saiba mais e uma caixa de login. (Não foi discutido se o login será obrigatorio ainda)

4- Carla logo que visualizou a caixa de buscas entendeu que ali deve ser o local aonde irá anexar seu link de noticia ou mesmo digitar o que quer verificar sua verossimilidade.

5- Ao anexar uma notícia que um aluno comentou com ela em sala de aula dentro da caixa de texto, carla cola o link dento da caixa de textos e agora espera ansiosamente por uma resposta desse aplicativo detector de mentiras.

6- Após alguns segundos (10 a 15), a professora Universitaria se surpreende com a resposta clara e conclusiva oriunda do aplicativo (Podendo ser Verdadeira, Falsa ou Inconclusivo), com uma resposa rápida escrita em destaque, agora em outra tela, avisando-a a resposta sobre sua pesquisa.

7- Carla tem curiosiadade de saber mais sobre sua pesquisa, não apenas se algo e verdadeiro ou falso, então se surpreende novamente ao perceber que junto a resposta de sua pesquisa, encontra-se a fonte de onde o fato foi buscado, junto de um texto breve e explicativo sobre o tema.

8- Por ter conhecimento previo, ela reconhece que esse procedimento foi feito por um agente de IA, que com um webcrawiling usando de jornais e fontes confiaveis buscou e fez o link para trazer uma resposta.

9- Contente com o conteudo de sua resposta, ela suspira de alivio com a nova informação adiquirida e em outra oportunidade irá novemente usar esse canal confiavel e rapido de buscas.


---

### (1) Interface e Fluxo de Busca
####	Estes critérios focam na experiência do usuário e no fluxo principal da aplicação, desde a entrada de dados até a exibição dos resultados.


#### Interface de Entrada de Busca: 

- A tela inicial do aplicativo deve conter um campo de texto principal para o usuário digitar ou colar a informação a ser verificada. A interface deve ser simples e limpa, similar a uma barra de busca do Google.

#### Botão de Ação: 

- Deve haver um botão claro e visível (por exemplo, "Verificar" ou um ícone de lupa) ao lado do campo de busca que inicie o processo de análise quando pressionado.

#### Tela de Carregamento: 

- Após o usuário iniciar a busca, o aplicativo deve exibir uma tela de carregamento ou uma animação de progresso para indicar que a análise está em andamento. Essa tela deve ser mantida até que o resultado seja processado, com a meta de tempo de resposta do agente de IA em 10 segundos, aceitável em até 15 segundos.

#### Tela de Resultados:

- A tela de resultados deve ser distinta da tela de busca e deve apresentar a resposta de forma clara e organizada. Ela deve conter as seguintes informações:

	O veredito final (por exemplo, "Verdadeiro", "Falso" ou "Inconclusivo").

	Uma justificativa detalhada, em texto, sobre a conclusão.

	Fontes e links para os jornais ou artigos usados na análise.

#### Navegação de Volta:

- O usuário deve ser capaz de retornar facilmente da tela de resultados para a tela de busca inicial para realizar uma nova verificação.

##### Para que fique claro o que foi apresentado, dentro da idealização da interface e desing do aplicativo, foi acordado que seria algo com uma tématica clean e esteticamente parecida com a página de buscas inicial do google.

---

### (2) Processamento e Conteúdo
#### 	Esses critérios se concentram na lógica interna do aplicativo, garantindo que o processamento e a apresentação da informação sejam precisos e relevantes.


#### Análise do Agente de IA:

- O agente de IA deve ser capaz de realizar um web crawling em uma lista de jornais pré-selecionados para buscar informações relevantes sobre o conteúdo inserido pelo usuário.

#### Verificação de Conteúdo:

- O sistema deve comparar a informação do usuário com o conteúdo obtido dos jornais confiáveis e, com base nessa análise, determinar se a informação é verdadeira ou falsa. O sistema deve ser intuitivo de usar.

#### Justificativa da IA:

- A resposta do sistema deve incluir uma justificativa para o veredito, explicando por que a informação foi classificada daquela forma. A IA terá acesso a jornais de notícia e páginas confiáveis para essa análise.

#### Tratamento de Inconclusividade:

- Se o sistema não conseguir chegar a uma conclusão clara sobre a veracidade da informação, ele deve indicar que o resultado é inconclusivo e explicar o motivo.

#### Coleta de Fontes:

- As fontes utilizadas pelo agente de IA para a verificação devem ser listadas na tela de resultados para que o usuário possa consultá-las diretamente. A forma de produzir escalabilidade no projeto é trazer cada vez mais artigos para fazer o web crawling


##### Essa será as funções que terão a implementação com inteligencia artificial, serão o grande show da peça

---

### (3) Funções de Usuabilidade, Dados e Segurança
#### Esses critérios se concentram em recursos que vão além da funcionalidade principal de busca, melhorando a experiência do usuário e a segurança do aplicativo.

#### Cadastro de Usuário: 

- O sistema deve permitir que o usuário crie uma conta usando seu e-mail e uma senha.

#### Login e Autenticação:

- Deve ser possível que o usuário faça login na aplicação. Uma vez logado, o usuário deve permanecer assim até que ele decida sair. O sistema também deve ter um serviço de autenticação por dois fatores.

#### Proteção de Dados:

- Ao cadastrar uma conta, os dados do usuário devem ser protegidos com criptografia básica. O sistema também deve garantir a segurança dos dados armazenados sobre o uso do usuário dentro da aplicação, podendo usar criptografia ou salvá-los fora do servidor que o aplicativo roda.

#### Histórico de Buscas:

- O aplicativo deve armazenar o histórico de buscas do usuário. Essa funcionalidade permitirá que o usuário revisite verificações anteriores sem ter que digitar a informação novamente.

#### Exclusão de Histórico:

- O usuário deve ter a opção de limpar seu histórico de buscas a qualquer momento nas configurações do aplicativo.

##### Essas adições ajudam a construir um projeto mais robusto e completo, considerando tanto a usabilidade quanto a segurança dos dados do usuário.

---

### (4) Requisito Funcional Adicional: Coleta de Dados

#### Coleta de Dados para Análise (Opcional):

- O sistema pode ser projetado para, em uma futura iteração, coletar de forma anônima e agregada os dados de busca dos usuários. O objetivo principal dessa coleta seria refinar o algoritmo de busca e a precisão do agente de IA. Esta funcionalidade deve ser implementada de forma a proteger a privacidade do usuário, garantindo que nenhum dado pessoal seja armazenado sem consentimento explícito.



---



## *Requisitos Não Funcionais*

---

#### Desempenho: 
- Não demorar mais que três segundos para fazer as funções básicas como login, cadastro, acessar as configurações, refresh na página. (recomendação da professora sobre tempo que um site deve demorar para funcionar).

- Tempo de resposta para o agente de IA, META DE 10 SEGUNDOS   porém caso fique na média de 15 ainda vai ser aceitável ao projeto.
		
#### Segurança:  (Ter a certeza do grau de complexidade de segurança que nosso projeto precisa)
- Criptografia básica para proteção de dados dos usuários ao cadastrar uma conta à aplicação.

- Serviço de autenticação por dois fatores ao fazer login no aplicativo. *Não fazer com que o usuário tenha que realizar login diversas vezes para entrar no aplicativo, deixando o usuário logado nele caso não tenha se desconectado*

- Segurança com os dados que serão armazenados dos usuários sobre o seu uso dentro da aplicação, criptografia seria uma saída ou salva-los fora do servidor que a aplicação roda.

#### Capacidade: 
- A capacidade de armazenamento e processamento são importantes ao projeto devido ao banco de dados do projeto ser extenso e todos os processos dele tambem serem pesados. (Devido a ser um projeto de faculdade, não precisa ser tão robusto assim, porém e bom dar uma estudada melhor para ter certeza de quanto será o mínimo para o projeto rodar).

- Um sistema capaz de suportar no seu pico de acessos 20 usuários.

- A possibilidade de um escalonamento horizontal pode ser útil, ter esse conhecimento prévio.
 
#### Confiabilidade e Disponibilidade:
- Falando sobre quanto tempo o aplicativo deve ficar no ar, durante o período do semestre e durante mais algum tempo, caso seja válido e não tão custoso.

- Em caso de falha dentro do aplicativo por ser praticamente um sistema de buscas, acho viável o aplicativo ter uma tela apenas para avisar que ele está fora do ar para manutenção.

- Durante o período que a aplicação estiver no ar, manutenções quinzenais serão mais que do que necessárias.

#### Escalabilidade:
- O aplicativo por ter uma tema muito ambicioso e atual ao momento presente da internet pode ser escalável a algo maior, como um aplicativo de verificação de vídeos e coisas mais complexas.

- Uma forma de produzir escabilidade ao projeto é trazer cada vez mais artigos para fazer o webcrawling.

#### Usabilidade: 
- O sistema tem que ser intuitivo ao uso, tendo em sua interface claramente como utilizar o aplicativo.

#### Compatibilidade:
- O aplicativo será compatível apenas com o sistema operacional Android.


---

#### Referencias:

##### Artigo sobre requisitos funcionais
- https://www.perforce.com/blog/alm/what-are-functional-requirements-examples

##### Artigo sobre requisitos não funcionais

- https://www.perforce.com/blog/alm/what-are-non-functional-requirements-examples
