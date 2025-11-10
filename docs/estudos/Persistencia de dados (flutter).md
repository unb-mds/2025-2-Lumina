


# Estudo: Persistência de dados para o frontend

## 1. opções para persistência

Sobre as opções existentes para persistência de dados, e como trata-las, no frontend temos que considerar os tipos de informações que podem ser guardados em cada tipo de opção.
Abaixo serão citadas algumas opções e os diferentes tipos de dados que eles tratam:
- Shared preferences: ideal pra tratar dados em pequenos volumes e não estruturados, como o ID da sessão/usuário, configurações de preferencias (tema, tamanho da fonte, etc). Não sendo ideal pra armazenar listas longas ou objetos complexos
- Hive: modelo de banco de dados NoSQL rápido, leve e orientado a objetos, nativo do dart e otimizado para Flutter, que armazena dados em "caixas" (_Boxes_) de pares chave-valor. Ideal para Histórico de mensagens e dados de contexto local, tendo uma alta performance e relativamente fácil de usar
- Drift: Alternativa moderna que tem uma integração um pouco melhor. Ideal para um grande volume de dados que precisam de relacionamentos e consultas complexas, como armazenar históricos de prazos muito longos, e se o chatbot for integrado com outras funções complexas (ex: lista de contatos, catálogo de produtos, etc), porém possui uma complexidade muito alta em comparação com as outras.
## 2. Tabela comparativa das opções
Considerando que o aplicativo já esta utilizando do shared preferences para salvar as configurações do usuário, abaixo está uma tabela comparando Hive e Drift

| opções   | Vantagens                                                                                                                              | Desvantagens                                                                 |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| **Hive** | - Alta performance;<br>- Relativamente fácil de utilizar;<br>-armazena objetos tipados nativamente(ideal para historico de conversas);       | -Não é o melhor para consultas complexas (como JOINs)
| **Drift** | - Integração com Dart;<br>-  Oferece uma camada de abstração sobre o SQL, simplificando operações comuns de banco de dados e reduzindo a complexidade do código.;<br>- 1.  Type Safety: Garante a segurança de tipos em tempo de compilação, ajudando a evitar erros comuns de tipo que podem ocorrer com SQL puro; | - Curva de aprendizado <br>-   Desempenho: A camada adicional de abstração pode introduzir uma leve sobrecarga de desempenho em comparação com consultas SQL diretas.<br> -Complexidade inicial |

## 3. Considerações finais
Considerando o escopo do projeto e a ideia do que vai ser trabalhado com a persistência de dados, a sugestão é que seja trabalhado com o Hive, visto que a ideia é manter um histórico de chat e o contexto da conversa do bot

## 4. Referencias
**Artigo**: [**Flutter: como persistir dados e quais ferramentas usar** - Alura](https://www.alura.com.br/artigos/alternativas-de-persistencia-de-dados-com-flutter?srsltid=AfmBOopAJHEvA128YUL8QzBZnKSPEEU9a9RUOABYXerKkkUef03wqmTk)
