# Estudo: Flutter e Linguagem Dart

## 1. O que é Flutter?

O Flutter é um framework que funciona com a linguagem de programação Dart e é capaz de criar aplicações híbridas, que funcionam em plataformas diferentes com apenas um código. Isso significa que uma aplicação poderia, por exemplo, rodar em Android, iOS ou até mesmo em um navegador, mantendo a performance nativa nos dispositivos. O grande diferencial desse framework são os widgets, que serão aprofundados no próximo tópico.

## 2. Widgets

Widgets são ferramentas usadas no Flutter como **"blocos de montar"** da interface do usuário (UI) de uma aplicação. Eles servem tanto para controlar aspectos de outros widgets (alinhamento, linha/coluna, padding, etc.), quanto para compor a parte visual e interativa (textos, botões, imagens, ícones, etc.).

O Flutter introduz duas classes principais de widgets:

### 2.1. Stateless Widget

São widgets que não possuem estados mutáveis, ou seja, eles permanecem os mesmos independentemente da interação com o usuário. Um widget de texto ou um ícone, por exemplo, seriam **stateless**, pois suas propriedades não mudam com o tempo.

### 2.2. Stateful Widget

Estes, por outro lado, têm a característica de mudar com base na interação do usuário ou outros fatores. Por exemplo, um widget que exibe um contador que é incrementado toda vez que um botão é apertado. Nesse caso, o valor do contador é o "estado" do widget. Como o valor a ser exibido muda, o widget precisa ser reconstruído para atualizar sua parte na UI.

## 3. Linguagem Dart

Dart é uma linguagem de programação orientada a objetos, assim como Java e C++. Sua sintaxe é bem semelhante a linguagens baseadas em C, então a declaração e inicialização de variáveis são feitas de forma parecida.

Uma pequena diferença é que, em Dart, as variáveis não podem ser nulas, a menos que você as declare explicitamente dessa forma, graças a um sistema interno feito para evitar *Null Exceptions*. Além disso, é possível declarar variáveis sem especificar seu tipo usando a palavra-chave `var`, onde o tipo da variável será determinado pelo seu valor inicial (*Type Inference*).

## 4. Referências

* Vídeo: O que é Flutter? - Código Fonte TV
* Documentação: Uma introdução aos widgets - Flutter Docs
* Documentação: Uma introdução ao Dart - Flutter Docs
* Guia: Um tour pela linguagem Dart
