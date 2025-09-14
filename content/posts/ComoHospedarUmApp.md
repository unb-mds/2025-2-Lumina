---
draft: false
title: 'Estudo: Como Hospedar um App na Play Store'
ShowToc: true
---


Este estudo tem como objetivo criar um guia e esclarecer as exigências para a publicação de um app na Play Store.

### 1. Criar uma conta de desenvolvedor do Google Play
Para publicar um aplicativo é necessário uma conta de desenvolvedor.
 * Google Play Console: O Google Play Console é a plataforma web que o Google oferece para desenvolvedores publicarem, gerenciarem e acompanharem o desempenho de seus aplicativos. Para criar uma conta de desenvolvedor é necessário preencher os dados do desenvolvedor e de pagar uma **taxa de registro**.
 * Taxa de registro: A Google cobra uma taxa única de US$ 25 para registrar uma conta de desenvolvedor. Após pagar essa taxa, é possível publicar um número ilimitado de apps sem nenhuma cobrança. A única outra cobrança que o Google aplica é a taxa de serviço (de 15% a 30%) sobre a receita gerada por vendas de produtos ou serviços digitais dentro do aplicativo, caso os tenha. Se o aplicativo for totalmente gratuito e não tiver compras internas, não haverá mais nenhuma cobrança por parte do Google.
### 2. Preparação do aplicativo
Antes de enviar o app, ele precisa estar pronto para o lançamento. Isto é a preparação de arquivos de compilação e da chave de assinatura.
#### AAB e APK
Ambos, APK e AAB, são formatos de arquivo usados para empacotar aplicativos Android, mas eles funcionam de maneiras fundamentalmente diferentes, especialmente em como o aplicativo é entregue aos usuários.

**O que é um Bundle de Aplicativo (AAB)?**

Um Android App Bundle (AAB) é o formato de publicação mais recente e recomendado pelo Google. Ele é um pacote que contém todo o código compilado e os recursos do app, mas de uma forma que permite que a Google Play Store otimize a entrega do aplicativo para cada dispositivo individualmente.
Em vez de criar um único arquivo universal (como o APK) com todos os recursos e configurações para todos os tipos de dispositivos, o AAB separa o conteúdo. Ele pode incluir:
* Múltiplas arquiteturas de CPU: Versões do seu código para chips de 64 bits ou 32 bits, por exemplo.
* Múltiplas densidades de tela: Versões de imagens e layouts para telas de alta e baixa resolução.
* Múltiplos idiomas: Strings de texto para diversos idiomas.

**Diferença entre AAB e APK**

A principal diferença é que o AAB é para o upload para a loja, resultando em downloads menores e mais eficientes para os usuários, já que o dispositivo só recebe os recursos necessários, enquanto o APK é o formato final que o usuário instala. 

#### Chave de assinatura 
A chave de assinatura é um elemento de segurança essencial no processo de publicação de aplicativos Android.


**Para que serve a chave de assinatura?**

A chave de assinatura tem duas funções principais:
 * Garantir a autenticidade: Ela garante aos usuários e à Google Play Store que a versão do aplicativo que eles estão baixando é a versão original, criada e publicada pelo desenvolvedor. Se alguém tentar modificar o app (por exemplo, injetando malware) e enviá-lo com outra chave, o Android vai detectar a fraude e não permitirá a instalação.
 * Permitir atualizações: Para que a Google Play Store permita que um desenvolvedor envie uma atualização para seu app, a nova versão precisa ser assinada com a mesma chave da versão anterior. 

**Como funciona?**

Ao publicar o aplicativo pela primeira vez, ele é assinado com uma chave privada. A partir dessa chave, é gerado um certificado público, que é o que a Google e os dispositivos Android usam para verificar a assinatura.
O Google Play Console oferece uma ferramenta chamada "Assinatura de apps pelo Google Play" (App Signing by Google Play). Essa é a forma mais recomendada de gerenciar a chave. Ao usar esse serviço:
 * Você envia sua chave de assinatura para a Google.
 * A Google armazena sua chave de forma segura.
 * Quando você envia uma nova versão do seu app, a Google a assina com a sua chave antes de publicá-la.
Isso evita o risco de perder a chave. Se a chave privada for perdida, não será possível atualizar o aplicativo, e a única solução seria publicar um novo aplicativo (com outro nome de pacote), o que faria com que todos os usuários perdessem o acesso às atualizações. Por isso, a assinatura de apps pelo Google é a opção mais segura.




 
#### 3. Preparação da ficha do aplicativo
A ficha do app é como uma vitrine na Google Play Store e é necessário preencher os seguintes dados:
 * Título do aplicativo.
 * Descrição: Um resumo sobre as funcionalidades do app.
 * Ícone do aplicativo.
 * Imagens e vídeos da interface do app.
 * Tipo e categoria, por exemplo: "Ferramentas", "Educação".

#### 4. Política de privacidade 
Para cumprir as políticas do Google Play, o aplicativo deve seguir as seguintes diretrizes:
1. Ter uma Política de Privacidade:
* **URL obrigatória:** Um link válido e ativo para uma política de privacidade na página do app no Google Play Console.
* **Conteúdo detalhado:** A política deve explicar de forma clara e completa como o app coleta, usa e compartilha dados dos usuários, e com quem esses dados são compartilhados (por exemplo, serviços de análise, publicidade, etc.).
* **Acessível no app:** Em muitos casos, a política de privacidade também precisa estar facilmente acessível dentro do próprio aplicativo.
2. Transparência e Consentimento:
* **Divulgação clara:** Se o app coleta dados pessoais ou confidenciais, deve avisar o usuário de forma clara e visível.
* **Consentimento explícito:** O usuário deve dar um consentimento ativo e claro para a coleta de dados.






#### 5. Análise e lançamento
Após configurar tudo, a Google fará uma análise do aplicativo para garantir que ele cumpre as Políticas do Google Play.
 * Envie para análise: Quando lançar o app ele será enviado para análise.
 * Aguarde a aprovação: O processo de análise pode levar de algumas horas a vários dias. A Google verifica se o app não contém malware, violações de direitos autorais ou qualquer outro tipo de conteúdo proibido.
 * Publicação: Quando o app for aprovado, ele será publicado na Google Play Store e ficará disponível para os usuários baixarem.


### Referências

Create and set up your app - Play Console Help - https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://support.google.com/googleplay/android-developer/answer/9859152%3Fhl%3Den&ved=2ahUKEwi1w7be3tiPAxVjILkGHfZCEeoQFnoECCMQAQ&usg=AOvVaw15kvOz88ux_SvKYA3y7oTy

What's the difference between AABs and APKs? - https://developer.android.com/guide/app-bundle/faq?hl=pt-br#:~:text=Unity%2C%20and%20Unreal.-,What's%20the%20difference%20between%20AABs%20and%20APKs?,can%20be%20installed%20on%20devices.


Publish your app | Android Studio - https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://developer.android.com/studio/publish&ved=2ahUKEwi1w7be3tiPAxVjILkGHfZCEeoQFnoECF8QAQ&usg=AOvVaw0QvZbEygpJ_BkJ4Mxu7_8l