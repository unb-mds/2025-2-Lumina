# Documento de Requisitos de Software (DRS): Chatbot Anti-Fake News  
**Versão:** 2.0 
**Data:** 17 de Setembro de 2025  

---

## 1. Introdução  


### 1.1 Problema
A disseminação de **notícias falsas (fake news)** é um dos maiores desafios da sociedade conectada. Com a velocidade da informação em redes sociais e aplicativos de mensagens, conteúdos enganosos ou manipulados podem se espalhar rapidamente, impactando negativamente áreas como saúde, política, economia e segurança pública.  

Atualmente, usuários comuns têm dificuldade em identificar a veracidade das informações que recebem, pois a checagem de fatos exige tempo, acesso a fontes confiáveis e habilidades específicas de análise crítica. Além disso, ferramentas tradicionais de busca não oferecem, de forma simples e imediata, uma validação contextualizada das notícias.  

O problema central, portanto, é a **falta de uma solução acessível e confiável** que auxilie usuários a verificarem, em tempo real, a credibilidade de informações recebidas, reduzindo a propagação de fake news e fortalecendo o consumo consciente de conteúdo digital.  

### 1.2. Propósito  
O propósito deste documento é descrever de forma clara e detalhada todos os requisitos funcionais, não-funcionais e de interface para o aplicativo móvel de chatbot anti-fake news. Este DRS servirá como guia para a equipe de desenvolvimento, base para o planejamento de testes e como um acordo formal entre os stakeholders do projeto.  
### 1.3. Escopo do Produto  
O produto será um aplicativo móvel para a plataforma **Android**. Sua função principal é permitir que usuários conversem com um chatbot inteligente para obter informações precisas e verificadas sobre notícias e eventos atuais.  

Utilizando uma arquitetura de **Geração Aumentada por Recuperação (RAG)**, o sistema consultará uma base de dados curada de jornais e artigos confiáveis para formular respostas, combatendo a desinformação e as *fake news*.  

**Estarão fora do escopo desta versão:**  
- Autenticação de usuários com login e senha em nuvem.  
- Sincronização de histórico de chat entre múltiplos dispositivos.  
- Funcionalidades de chat em grupo ou social.  
- Monetização ou sistemas de assinatura.  

### 1.4. Definições, Acrônimos e Abreviações  
- **DRS:** Documento de Requisitos de Software.  
- **App:** Aplicativo móvel.  
- **LLM (Large Language Model):** Modelo de Linguagem de Grande Porte, a tecnologia de IA que potencializa o chatbot.  
- **RAG (Retrieval-Augmented Generation):** Geração Aumentada por Recuperação. Arquitetura que combina um LLM com uma base de dados externa para gerar respostas mais precisas e baseadas em fatos.  
- **API (Application Programming Interface):** Interface de Programação de Aplicação.  
- **UI (User Interface):** Interface do Usuário.  

---

## 2. Descrição Geral  

### 2.1. Perspectiva do Produto  
O aplicativo é um produto independente e autocontido. Ele se posiciona como uma ferramenta de verificação de fatos e informação rápida, competindo com mecanismos de busca tradicionais e outras plataformas de checagem de notícias, com o diferencial de uma interface conversacional intuitiva.  

### 2.2. Características dos Usuários  
O público-alvo do aplicativo são usuários de smartphones em geral, preocupados com a veracidade das informações que consomem. Isso inclui:  

- **Usuário Geral:** Pessoas com pouca afinidade tecnológica que buscam respostas rápidas e confiáveis para suas dúvidas.  
- **Estudantes e Pesquisadores:** Utilizarão o app como ponto de partida para obter informações de fontes seguras.  
- **Profissionais de Comunicação:** Jornalistas e criadores de conteúdo que necessitam de uma ferramenta ágil para checagem de fatos.  

### 2.3. Restrições Gerais  
- O sistema dependerá de uma conexão ativa com a internet para se comunicar com a API da LLM.  
- Toda a curadoria de conteúdo para o banco de dados deve seguir princípios éticos de jornalismo e imparcialidade.  

### 2.4. Suposições e Dependências  
- **Dependência de API Externa:** O funcionamento do chatbot depende diretamente da disponibilidade e dos termos de serviço da API da LLM escolhida (ex: Gemini, OpenAI API).  
- **Qualidade do Banco de Dados:** A precisão das respostas do chatbot é proporcional à qualidade e atualização do banco de dados vetorial.  

---

## 3. Requisitos Funcionais  

### RF-001: Configuração Inicial do Usuário  
**Descrição:** Na primeira vez que abrir o aplicativo, o usuário será apresentado a uma tela inicial.  

**Componentes:**  
- **RF-001.1:** A tela deve exibir o logo e o nome do aplicativo.
- **RF-001.2:** O tutorial deve ser exibido apenas na primeira utilização do aplicativo.
- **RF-001.3:** A landing page deve ter telas que explicam o propósito do aplicativo e como ele funciona.
- **RF-001.4:** Uma das telas deve conter um campo de texto para que o usuário insira um nome ou apelido.
- **RF-001.5:** Um botão "Entrar" ou similar deve persistir o nome do usuário localmente no dispositivo e direcioná-lo para a tela principal do chat.
- **RF-001.6:** O usuário deve ser capaz de revisitar a landing page/tutorial a qualquer momento através de um botão específico na tela de configurações (RF-004-1.6). 

### RF-002: Interface de Chat  
**Descrição:** A tela principal do aplicativo será uma interface de chat interativa.  

**Componentes:**  
- **RF-002.1:** Exibir mensagens do usuário e do chatbot em formato cronológico.  
- **RF-002.2:** Campo de texto para digitação de mensagens.  
- **RF-002.3:** Botão "Enviar" para enviar mensagens ao chatbot.  
- **RF-002.4:** Exibir o logo do aplicativo na parte superior da tela.  
- **RF-002.5:** A interface do chat deve exibir um nome ou identificador claro para o chatbot (ex: "Nome do Agente"), diferenciando-o das mensagens do usuário.

### RF-003: Menu Lateral e Histórico  
**Descrição:** A tela de chat deve conter um menu lateral para acesso a outras funcionalidades.  

**Componentes:**  
- **RF-003.1:** Ícone (três barras horizontais) abre o menu lateral.  
- **RF-003.2:** O menu lateral deve conter lista de chats anteriores armazenados localmente.  
- **RF-003.3:** Botão para acessar a pagina de configurações
- **RF-003.4:** O menu deve incluir um botão "Nova Conversa" que limpa a interface e permite iniciar uma nova sessão.
- **RF-003.5:** A lista de chats deve ser organizada sob um título como "Conversas Recentes" para clareza.

### RF-004-1: Tela de Configuração 

**Componentes:**  
- **RF-004-1.1:** Botão de edição do nome de usuário.
- **RF-004-1.2:** Dentro a opção app: Idioma, botão para mudar a linguagem em que a LLM responde e do app.
- **RF-004-1.3:** Dentro a opção app: Aparência, botão para trocar o tema do aplicativo para claro ou escuro, começa pelo padrão do sistema
- **RF-004-1.4:** Dentro a opção app: Tamanho da Fonte, botão para trocar o tamanho da fonte
- **RF-004-1.5:** Dentro da opção sobre: Um botão "Saiba Mais" que redireciona ao github pages.
- **RF-004-1.6:** Dentro da opção sobre: Um botão de "Tutorial" que redireciona o usuário a landing page.
- **RF-004-1.7:** Dentro da opção sobre: Um botão de Termos de Serviço.
- **RF-004-1.8:** Botão de volta a tela principal.

### RF-004-2: Tela de Configuração em Janela
- **RF-004-2.1:** Tanto o botão "Idioma" quanto o "Aparência" irão redirecionar a uma tela em janela que será aberta dentro das configurações, aplicando um filtro para escurecer tudo fora da janela.
- **RF-004-2.2:** Essa configuração em janela tem opções de escolha a esqueda que podem ser selecionadas a direita.
- **RF-004-2.3:** Um botão que irá voltar a tela de configurações. 

### RF-004-3: Tela de Configuração de Fonte
- **RF-004-3.1:** Uma tela separada de configurações com um texto explicativo mostrando o tamanho da fonte atual que está sendo ultilizado pelo chatbot.
- **RF-004-3.2:** Caixa interativa na parte inferior da tela com opções de diminuir e aumentar a fonte, mudando em tempo real o texto explicativo.
- **RF-004-3.3:** Botão de volta a página de configurações. 

### RF-004-4: Tela de Configuração de Termos de Serviço
- **RF-004-4.1:** Quando clicado, irá redirecionar a uma tela com duas opções: Termos de Uso e Política de Privacidade.
- **RF-004-4.2:** Botão em ambas as opções que ira redirecionar o usuario até a tela especifica a isso. 
- **RF-004-4.3:** Tela contendo de forma crua os termos de serviço e política de privacidade, com botão de volta a tela de termos de seviço.
- **RF-004-4.4:** Botão de volta a configurações.

### RF-005: Sistema de Interação com o Chatbot (RAG)  
**Descrição:** Núcleo do sistema que processa as perguntas e gera respostas.  

**Componentes:**  
- **RF-005.1:** Receber pergunta do usuário.  
- **RF-005.2:** Consultar banco de dados vetorial para artigos relevantes.  
- **RF-005.3:** Enviar dados para a LLM.  
- **RF-005.4:** Receber resposta e exibir na interface de chat.  
- **RF-005.5:** Analisar se entrada é um link. Caso não confiável, retornar mensagem:  
  > "Desculpe, só posso analisar informações de fontes confiáveis que fazem parte do meu conhecimento."  

### RF-006: Sistema de Administração de Conteúdo  
**Descrição:** Interface web para administradores controlarem quais reportagems estão sendo colocadas no banco de dados.  

**Componentes:**  
- **RF-006.1:** Permitir envio e remoção de novos artigos (link ou upload).  
- **RF-006.2:** Mostrar quais reportagens e a fonte da mesma estão armazenadas no banco de dados.

---

## 4. Requisitos Não-Funcionais  

- **RNF-001: Desempenho**  
  Tempo de resposta deve ser < **10 segundos** em média.  

- **RNF-002: Segurança**  
  Comunicação via **HTTPS**. Dados de usuário armazenados apenas localmente.  

- **RNF-003: Confiabilidade**  
  Se não houver dados relevantes, chatbot deve responder:  
  > "Não encontrei informações sobre este tópico em minha base de dados para fornecer uma resposta confiável."  

- **RNF-004: Usabilidade**  
  Interface deve seguir padrões de apps de mensagens populares (WhatsApp, Telegram, ChatGPT, Gemini).  

- **RNF-005: Escalabilidade**  
  Suporte estável para até **100 usuários simultâneos**.  

---

## 5. Requisitos de Interface Externa  

### 5.1. Interfaces de Usuário (UI)  
- UI deve ser limpa, moderna e intuitiva.  
- Adaptar-se a diferentes tamanhos de tela.  
- Exibir feedback visual quando o chatbot estiver "digitando".  

### 5.2. Interfaces de Software  
- **API da LLM:** Comunicação via **HTTP RESTful**.  
- **Banco de Dados Vetorial:** Backend conectado a serviço de vetores (ex: ChromaDB).  

### 6. Impacto Esperado  

O aplicativo de chatbot anti-fake news pretende gerar um impacto positivo em diferentes níveis:  

- **Social:** reduzir a disseminação de desinformação, promovendo um consumo mais consciente e responsável de notícias.  
- **Educacional:** oferecer uma ferramenta de apoio para estudantes, pesquisadores e cidadãos em geral, facilitando o acesso a informações verificadas.  
- **Tecnológico:** demonstrar o uso prático de arquiteturas baseadas em **LLM** e **RAG**, aplicadas a um problema real de relevância global.  
- **Comunicacional:** apoiar profissionais de mídia e criadores de conteúdo na checagem rápida de fatos, fortalecendo a credibilidade das informações divulgadas.  

Com isso, espera-se contribuir para um ambiente digital mais confiável, onde usuários possam tomar decisões melhor informadas e reduzir os efeitos nocivos das fake news na sociedade.  






