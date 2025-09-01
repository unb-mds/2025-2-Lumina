# Flutter e linguagem Dart 

## O que é Flutter? 
Flutter é um framework que funciona na linguagem de programação Dart, e capaz de criar aplicações hibridas, que funcionam em plataformas diferentes com apenas um código, ou seja, a aplicação poderia, por exemplo, rodar em android, iOS ou até navegador, mantendo a performance nativa da aplicação nos dispositivos em que irão rodar. Além disso, o diferencial desse framework são os widgets, que serão aprofundados no próximo tópico.
Um bom video **introdutório**  sobre Flutter é esse do [Código fonte TV](https://www.youtube.com/watch?v=XkEA4xT34jg), explicando bem sobre o que é o Flutter.

## Widgets

Widgets são ferramentas usadas no Flutter como "blocos de montar" da UI de uma aplicação, servindo tanto pra controlar aspectos de outras widgets (alinhamento, linha/coluna, padding, etc.), e também para compor a parte visual e interativa (textos, botões, imagens, ícones, etc.)

O flutter introduz duas classes maiores de widgets, são esses:

* ### Stateless Widget:
São widgets que não possuem status mutáveis(não possuem uma propriedade de classe que muda com o tempo) , ou seja, eles permanecem o mesmo independente da interação com o usuário, como por exemplo um widget de texto ou ícone seriam stateless

* ### Stateful Widget:
Esse por outro lado tem a característica única de mudar com base na interação de usuário ou outros fatores que façam com que ele mude, por exemplo, um widget que tem um contador incrementado toda vez que um botão é apertado, nesse caso, o valor do contador é o estado do widget, então como o valor a ser representado muda, o widget precisa ser reconstruído pra atualizar sua parte na UI

## Linguagem Dart
É uma linguagem de programação orientada a objetos, assim como java e C++. Essa linguagem possui uma sintaxe bem semelhante a linguagens baseadas em C, então declarar e inicializar uma variável é feito como nessas linguagens, com uma pequena diferença que em Dart as variáveis não podem ser nulas a menos que você as declare assim, por conta de um sistema interno feito pra evitar Null Exceptions. Além disso é possível declarar variáveis sem especificar seu tipo explicitamente, devido ao Type-safe code do dart usando "var" antes da declaração, onde o tipo da variável vai ser determinado pelos seus valores iniciais.
Segue um guia recomendado para [introdução à Dart](https://dart.dev/language#imports), explicando sobre as variáveis
