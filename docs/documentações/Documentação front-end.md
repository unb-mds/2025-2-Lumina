


# Documentação: Tecnologia frontend

## 1. Escolha da tecnologia

A tecnologia escolhida para o front-end do projeto é a framework **Flutter**, o que garante uma ótima experiência tanto visual quanto interativa para o usuário, além de garantir a compatibilidade com múltiplas plataformas.

## 2. Estrutura do frontend

├── `lib`/Programação do front\
├── `android`/Integração do aplicativo para a plataforma<br>
├── `test`/ Pasta para os testes do front    
└── `pubspec.yaml`/Arquivo dos requisitos do aplicativo

## 3. Descrição dos diretórios

- `lib/`
Pasta responável por conter a parte principal da programação do aplicativo flutter, nela estão presentes todas as telas pelas quais o aplicativo passa, além da main.dart que é responsavel por sua vez pelo ponto de partida do aplicativo e como ele vai manejar as telas, persistências, Etc. 

- `android/`
Pasta responsável por interpretar, buildar e configurar o aplicativo para o sistema android, que foi o sistema operacional escolhido para distribuição do projeto. É uma pasta que necessita de poucas alterações, geralmente sendo de coisas especificas da plataforma e menores em relação ao desenvolvimendo total do projeto.

- `test/`
Pasta relacionada aos testes unitários automatizados do frontend, garantindo a qualidade e o funcionamento dos componentes.

- `pubspec.yaml/`
Arquivo responsável pelas dependências do projeto, ele é acessado quando o comando ```flutter pub get``` é utilizado, pegando todas as bibliotecas e as baixando para o projeto ser interpretado corretamente, além de mostrar os assets (.env,JSON,imgens, etc.) que o aplicativo deve empacotar e utilizar.

## 4. Deploy
O aplicativo sera lançado na **playstore**, para dispositivos **android**, tendo em mente a facil acessibilidade à dispositivos eletrônicos atualmente.