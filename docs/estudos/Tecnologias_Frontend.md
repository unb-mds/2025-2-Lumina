# Os principais frameworks
Quando falamos de desenvolvimento mobile temos algumas opções, mas as que possuem mais destaque são o Flutter e o React Native, isso pois as duas se destacam por trazerem a proposta de serem framework para desenvolvimento de aplicativos **cross-platform**, ou seja, ambos focam em facilitar o desenvolvimento para vários sistemas operacionais, como por exemplo, android e iOS . Ambos facilitam o desenvolvimento utilizando de bibliotecas para abstrair as diferenças entre as plataformas, permitindo que em grande maioria as coisas sejam feitas com apenas um código.
Esse estudo tem o intuito de comparar os pontos fortes e fracos entre eles para ajudar na decisão de qual deles será utilizado. Primeiramente precisamos entender sobre os dois frameworks em questão, como já há um estudo dedicado sobre Flutter, o próximo tópico será dedicado a apresentar o React Native antes de citar os prós e contras de cada framework.

---

# React Native
O React Native é uma Framework baseada na linguagem JavaScript, que permite criar aplicativos móveis que são renderizados nativamente para android e iOS, assim como o flutter, ele permite criar um aplicativo para varias plataformas usando a mesma base do código, trazendo uma grande economia de tempo e recursos.
Ele é construído com base no React, uma biblioteca JavaScript que já era bastante popular quando esse Framework foi lançado, o que facilita um pouco na hora do aprendizado, visto que, caso você já tenha tido contato com a linguagem de JavaScript a curva de aprendizado seria relativamente menor do que a do flutter que utiliza a linguagem Dart.
A arquitetura do React Native pode ser resumida da seguinte forma:
* O **código React** que o desenvolvedor escreve o app
* O **JavaScript** que é eventualmente interpretado a partir do código escrito pelo desenvolvedor
* Uma serie de elementos conhecidos como **The bridge**, que serve como uma ponte entre o código em JavaScript e a parte nativa do código do aparelho
* O lado nativo do aparelho

Para uma melhor compreensão sobre React Native, recomendo o video do canal [Código Fonte TV](https://www.youtube.com/watch?v=mqltv3kFdgE),  que serve como uma boa introdução, e também o artigo do site da [Alura](https://www.alura.com.br/artigos/react-native?srsltid=AfmBOorYpDZu78HiYNCDcp3ziPz0z3Z9kiA2wIJUO_Q-E_Qn526lIDzy), que além de explicar sobre o Framework, dita algumas vantagens e desvantagens, que serão discutidas no próximo tópico

---

# As vantagens e desvantagens de cada Framework
Abaixo esta uma tabela com as vantagens e desvantagens tanto do Flutter quanto do React Native
|Framework|Vantagens|Desvantagens|
|---------|-----------|--------------|
|Flutter| - Linguagem orientada a objetos; <br>-Documentação de qualidade; <br> - Visualização em tempo real das mudanças em testes (stateful hot reload);<br>- UI altamente personalizável devido aos widgets;<br> - Melhor compatibilidade com IDE| -Comunidade ainda em crescimento, devido ao tempo de vida curto;<br> - Arquivos potencialmente podem ocupar mais espaço; |
|React Native|-Grande comunidade; <br> - Visualização em tempo real das mudanças (hot reload, praticamente igual ao do Flutter);<br> - Excelente experiência de usuário; <br> - Carregamento rápido de aplicativos;<br> - Comunidade grande e ativa; |- Documentação Ruim; <br>- Problemas de compatibilidade de pacotes e ferramentas de debug;|

Seguem algumas recomendações para melhor entendimento dos prós e contras de cada framework:
Artigos da Alura sobre [Flutter](https://www.alura.com.br/artigos/flutter?srsltid=AfmBOoqP4RfRwBt2ioDMYAEiRzptlPAlprnhF7GBM5DzIsiWl0Ga9UKT) e [React Native](https://www.alura.com.br/artigos/react-native?srsltid=AfmBOorYpDZu78HiYNCDcp3ziPz0z3Z9kiA2wIJUO_Q-E_Qn526lIDzy) (o segundo é o mesmo link citado no topico anterior)
Um [Blog](https://uds.com.br/blog/flutter-react-native) que cita as vantagens e desvantagens além de comparar os dois Frameworks

---
# Comparações
Abaixo está uma tabela comparando alguns aspectos das duas frameworks, baseada na tabela do [Blog](https://uds.com.br/blog/flutter-react-native) citado no tópico anterior

| Característica|Flutter|React Native|
|--------------|-------|-------------|
|Linguagem| Dart| JavaScript|
|Componentes GUI|Widgets proprietarios|Componentes OS nativos|
|Hot reloading| sim|sim|
|Documentação| Melhor | Pior|
|Reutilização do código|90-100%|90%|
|Popularidade [(segundo o google trends e Stack Overflow)](https://www.nomtek.com/blog/flutter-vs-react-native)|Ligeira vantagem| Ligeiramente atras|
|comunidade| Crescente e ativa(porém relativamente nova)|Grande e ativa|
|Performance| Renderiza a propria tela mantendo consistência visual e evitando problemas com atualizações nativas. Com o novo motor gráfico Impeller, Flutter otimiza o uso de GPU, oferecendo melhor performance|com o módulo JSI, melhora a comunicação entre componentes JavaScript e nativos, reduzindo a latência|
|Facilidade de uso| Dart, é considerado mais fácil de aprender e utilizar, especialmente para desenvolvedores com experiência em desenvolvimento móvel nativo. A CLI do Flutter e o Flutter Doctor facilitam a configuração do ambiente| React Native, usando JavaScript, pode ser mais complexo, mas ferramentas como Expo simplificam o desenvolvimento|

---
# Recomendação
Baseado nas informações desse estudo, é perceptível que ambas as Frameworks são bastante competentes no que se propõem,  tendo diferenças mínimas. Então após uma analise sobre os prós e contras, recomendaria o trabalho com o Flutter, devido aos fatores como widgets bem customizáveis, além de um grande catalogo de widgets já prontos, sendo possível também criar um caso desejado, outro fator importante considerado é a documentação, já que a [documentação oficial do flutter](https://docs.flutter.dev) é mais clara e profunda segundo os usuários. A pesar de Dart ser uma linguagem nova e diferente, ela é dita simples de aprender, além de aprender por sua semelhança com outras linguagens baseadas em C, assim como o JavaScript .Por último, a pesar de precisar de algumas ferramentas a mais, como o Android Studio para compilação do projeto além de um emulador para os testes, a compatibilidade do flutter com a grande maioria dos IDEs também é um fator que facilita bastante tanto por praticidade quanto por conforto.
