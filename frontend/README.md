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

- Baixar os pacotes do flutter
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
    