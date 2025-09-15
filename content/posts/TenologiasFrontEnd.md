---
draft: false
title: 'Análise de Tecnologias para o FRONTEND'
ShowToc: true
---

## 1. Os Principais Frameworks
Quando falamos de desenvolvimento mobile, temos algumas opções, mas as que possuem mais destaque são o Flutter e o React Native. Isso ocorre pois as duas se destacam por trazerem a proposta de serem frameworks para o desenvolvimento de aplicativos **cross-platform**, ou seja, ambos focam em facilitar o desenvolvimento para vários sistemas operacionais, como Android e iOS. Ambos facilitam o desenvolvimento utilizando bibliotecas para abstrair as diferenças entre as plataformas, permitindo que, na grande maioria das vezes, as coisas sejam feitas com apenas um código.

Este estudo tem o intuito de comparar os pontos fortes e fracos entre eles para ajudar na decisão de qual será utilizado. Primeiramente, precisamos entender sobre os dois frameworks em questão. Como já há um estudo dedicado sobre Flutter, o próximo tópico será dedicado a apresentar o React Native antes de citar os prós e contras de cada um.

## 2. React Native
O React Native é um framework baseado na linguagem JavaScript que permite criar aplicativos móveis renderizados nativamente para Android e iOS. Assim como o Flutter, ele permite criar um aplicativo para várias plataformas usando a mesma base de código, trazendo uma grande economia de tempo e recursos.

Ele é construído com base no React, uma biblioteca JavaScript que já era bastante popular quando o framework foi lançado, o que facilita um pouco na hora do aprendizado, visto que, caso você já tenha tido contato com a linguagem JavaScript, a curva de aprendizado seria relativamente menor do que a do Flutter, que utiliza a linguagem Dart.

A arquitetura do React Native pode ser resumida da seguinte forma:
* O **código React** que o desenvolvedor escreve para o app.
* O **JavaScript** que é eventualmente interpretado a partir do código escrito pelo desenvolvedor.
* Uma série de elementos conhecidos como **The Bridge**, que serve como uma ponte entre o código em JavaScript e a parte nativa do código do aparelho.
* O lado nativo do aparelho.

## 3. Vantagens e Desvantagens de Cada Framework
Abaixo está uma tabela com as vantagens e desvantagens tanto do Flutter quanto do React Native.

| Framework    | Vantagens                                                                                                                              | Desvantagens                                                                 |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| **Flutter** | - Linguagem orientada a objetos;<br>- Documentação de qualidade;<br>- Visualização em tempo real das mudanças (Stateful Hot Reload);<br>- UI altamente personalizável devido aos widgets;<br>- Melhor compatibilidade com IDEs. | - Comunidade ainda em crescimento;<br>- Arquivos podem ocupar mais espaço.         |
| **React Native** | - Grande comunidade;<br>- Visualização em tempo real das mudanças (Hot Reload);<br>- Excelente experiência de usuário;<br>- Carregamento rápido de aplicativos;<br>- Comunidade grande e ativa. | - Documentação ruim;<br>- Problemas de compatibilidade e ferramentas de debug. |

## 4. Comparações
Abaixo está uma tabela comparando alguns aspectos dos dois frameworks.

| Característica         | Flutter                                                                                                                          | React Native                                                                                                   |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|
| **Linguagem** | Dart                                                                                                                             | JavaScript                                                                                                     |
| **Componentes GUI** | Widgets proprietários                                                                                                            | Componentes nativos do SO                                                                                      |
| **Hot Reloading** | Sim                                                                                                                              | Sim                                                                                                            |
| **Documentação** | Melhor                                                                                                                           | Pior                                                                                                           |
| **Reutilização do Código** | 90-100%                                                                                                                          | 90%                                                                                                            |
| **Popularidade** | Ligeira vantagem                                                                                                                 | Ligeiramente atrás                                                                                             |
| **Comunidade** | Crescente e ativa (porém relativamente nova)                                                                                     | Grande e ativa                                                                                                 |
| **Performance** | Renderiza a própria tela, mantendo consistência visual. Com o novo motor gráfico Impeller, otimiza o uso de GPU para melhor performance. | Com o módulo JSI, melhora a comunicação entre componentes JavaScript e nativos, reduzindo a latência.          |
| **Facilidade de Uso** | Dart é considerado mais fácil de aprender. A CLI do Flutter e o Flutter Doctor facilitam a configuração do ambiente.              | JavaScript pode ser mais complexo, mas ferramentas como Expo simplificam o desenvolvimento.                  |

## 5. Recomendação
Baseado nas informações deste estudo, é perceptível que ambos os frameworks são bastante competentes no que se propõem, tendo diferenças mínimas. Após uma análise sobre os prós e contras, recomendaria o trabalho com o **Flutter**.

Os principais motivos são seus widgets altamente customizáveis, um grande catálogo de componentes prontos, e uma documentação oficial considerada mais clara e profunda pelos usuários. Apesar de Dart ser uma linguagem nova, ela é dita como simples de aprender, com semelhanças a outras linguagens baseadas em C. Por último, a compatibilidade do Flutter com a grande maioria dos IDEs é um fator que facilita bastante, tanto por praticidade quanto por conforto.

## 6. Referências
* **Vídeo:** *O que é React Native?* - [Código Fonte TV](https://www.youtube.com/watch?v=mqltv3kFdgE)
* **Artigo:** *O que é React Native e como funciona essa tecnologia?* - [Alura](https://www.alura.com.br/artigos/react-native)
* **Artigo:** *O que é Flutter?* - [Alura](https://www.alura.com.br/artigos/flutter)
* **Blog:** *Flutter ou React Native: qual é a melhor opção?* - [UDS](https://uds.com.br/blog/flutter-react-native)
* **Blog:** *Flutter vs React Native in 2024* - [Nomtek](https://www.nomtek.com/blog/flutter-vs-react-native)
* **Documentação Oficial do Flutter:** [https://docs.flutter.dev](https://docs.flutter.dev)