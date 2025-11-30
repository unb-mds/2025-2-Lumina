# Estudo: Testes unitários para flutter

## 1. Para que servem?

Assim como no frontend, os testes unitários ajudam a ver se alguma mudança no código ou implementações atrapalham na aplicação ou se ela segue funcionando conforme o esperado, com o diferencial que, por se tratar do front end, os testes também incluem os Widgets, integração (fluxo de telas), resposta de requisição do servidor, além da própria lógica


## 2. Tipos de teste

Existem vários tipos de testes que podem ser aplicados, mas os tipos mais comuns para flutter são:

-   O teste de unidade, que em inglês você verá muito como  _"unit test"_. Esse teste é o mais simples e direto, pois testa uma única função, método ou classe;

-   O teste de widget, que em inglês você verá como  _"widget test"_, e que é conhecido em outras tecnologias que possuem estruturas de interface de usuário como "teste de componente".

-   O teste de integração, o famoso do inglês  _"integration test"_. Esse é o mais robusto dos testes pois testa o aplicativo todo ou, pelo menos, grande parte dele.


## 3. Integração com o GitHub

Em questão da automatização dos testes, é necessário criar um arquivo YAML, onde irão conter as condições em que o teste irá rodar (por exemplo, rodar caso um pull request seja feito), o ambiente de teste, uma ação para pegar as dependências do projeto (flutter pub get) e por fim rodar o teste, depois basta colocar esse arquivo na pasta responsável pelos testes automatizados (.github)

## 4. Referencias

- **Artigo**: [Testes no Flutter: guia completo para iniciantes-Alura](https://www.alura.com.br/artigos/testes-flutter?srsltid=AfmBOoqZNuqrNr3nN3bd-Ag20Wi8KkjKFf_ZQufTvWH-m68Ssfo6FjLN)

- **Artigo**: [Testes unitários — Dart e Flutter - medium (Por Cristiano Raffi Cunha)](https://medium.com/cristiano-cunha/testes-automatizados-dart-cf9df0e741ab)

- **Documentação**: [An introduction to unit testing - Flutter docs](https://docs.flutter.dev/cookbook/testing/unit/introduction)
