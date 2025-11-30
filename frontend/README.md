# 📋 Requisitos Prévios
Certifique-se de que os seguintes requisitos estão instalados no seu sistema:
- flutter SDK: Versão 3.35.4 ou superior


## 🛠️ Configurações do ambiente
### Para rodar o Aplicativo é necessario dos seguintes requerimentos


- Flutter instalado 

- Ter um arquivo .env com a URL da sua API com a seguinte formatação
    ```
    API_BASE_URL=Minha_URL
    ```
    - Substitua "Minha_URL" pela URL do seu servidor local
    - Caso queira rodar no android emulator use a URL http://10.0.2.2:8000
    - Não deixe espaço no texto
    - O arquivo .env deve estar na pasta frontend

- Baixar os pacotes do flutter necessarios para esse projeto
  - Para baixar basta rodar
    ```
    flutter pub get
    ```

- para rodar basta: 
    1. rodar o servidor local, encontrado no [backend](/backend/) para que a comunicação com a API de IA seja feita

    2. selecionar o dispositivo desejado para rodar o aplicativo

    3. rodar o main.dart no dispositivo desejado usando o commando
        ```
        flutter run
        ```` 
---

## 🏗️ Estrutura do Frontend

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