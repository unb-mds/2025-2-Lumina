## Resumos do projeto

Um app mobile onde o usuario pode conversar com um chatbot que utiliza de um banco de dados com dados de varios jornais atravez da arquitetura RAG para assim informar o usuario melhor e combater as fake news

Uma LLM ve a pergunta, procura reportagems relevantes a pergunta, analisa elas, e responde o usuario com maior precisão e evitando alucinação.

## Requisitos Funcionais

-  Tela inicial
     - Componentes necessarios na tela
        - Caixa da texto para o usuario colocar seu nome e salvar no sistema localmente
        - Logo e nome do app
- Tela de chat interativa onde o usuario pode ver a suas mensagems enviadas e as mensagems recebidas do bot 
    - Componentes necessarios na tela
        - Caixa de texto para receber mensagems do usuarios
        - Logo do aplicativo em cima
        - Icone de 3 barras horizontais para abrir uma aba lateral
        - Aba Lateral com toggle para abrir ela terá um historico LOCAL de chats e abas explicando sobre o app
- Sistema de RAG para mandar informações precisas para o usuario
    - Componentes do Sistema
        - Sistema para enviar para o chatbot e receber mensagems do chatbot.
        - Banco de dados com vetores sobre informações relevantes e fontes confiaveis para verificação pelo chatbot
        - Sistema para um admin enviar reportagems e artigos confiaveis para o banco de dados
        - Analise de links de reportagems e artigos para analisar confiabilidade do conteudo e da fonte
            - Caso o usuario mande um link fora desse escopo, retornar uma mensagem falando que está fora das opções

## Requisitos Não-Funcionais

- Desempenho
    - O sistema de envio e recebimento de mensagems depende naturalmente do sistema de busca de informações pertinentes com base na pergunta do usuario e do tempo de resposta da api da llm utilizada. Portanto não é possivel tempos de respostas extremamente rapidos (<1s) porem um tempo de espera muito grande para uma resposta maior que 10s prejudica muito a experiencia do usuario, portanto um tempo há uma necessidade de optimização do sistema para atingir tempos menores que 10s,
- Segurança
    - Como o app não salva na nuvem os dados do usuario, segurança não é de maxima prioridade, buscar apenas segurança para não vazar as conversas entre o chat é o usuario é suficiente
- Confiablidade
    - O app deve garantir respostas confiaveis, de maneira em que a confiabiliade é um requisito de alta prioridade, pois caso ele não consiga uma informação no banco de dados para responder o usuario o sistema deve mandar uma resposta indicando que não sabe ao em vez de alucinar e mandar respostas imprecisas.
- Usabilidade
    - O usuario deve conseguir mandar mensagens e receber com bas em padrões de sistemas de chat já implementados na industria (Whatsapp, Gemini, ChatGPT), assim mesmo usuarios com menor afinidade em tecnologia conseguiram utilizar nosso sistema
- Escalabilidade
    - Em primeiro momento, por nosso projeto utilizar API's externas para boa parte do processamento de dados, não há grande necessidade de um alto poder de processamento para conseguir atingir uma quantidade decente de usuarios simultaneos (<100 users)

