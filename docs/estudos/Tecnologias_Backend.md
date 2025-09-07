# Análise da Linguagem para o BACKEND

A decisão mais crítica é a escolha da linguagem de programação.  
A funcionalidade principal do projeto se divide em duas tarefas:

- **Web scraping** → tarefa intensiva em **I/O (entrada/saída)**  
- **Processamento de Linguagem Natural** → tarefa intensiva em **CPU**

---

## Python vs. Node.js

### Node.js
- Se destaca em tarefas **I/O-bound** 

Obs : tarefas **I/O-bound** (**input**/**output** bound) são tarefas que o fator limitante de desempenho é a velocidade de leitura ou escrita de dados.  

- Arquitetura orientada a eventos e motor V8 tornam-no rápido para scraping.  
- Excelente em **sites dinâmicos** com uso de **JavaScript**, com bibliotecas como **Puppeteer** e **Cheerio**.  

### Python
- **Padrão da indústria** para ciência de dados, machine learning e Processamento de Linguagem Natural (PLN).  
- A proposta central do projeto é **detecção de fake news**, que depende de modelos avançados como **BERT** e **RoBERTa**. 

O BERT (Bidirectional Encoder Representations from Transformers) é um modelo de inteligência artificial desenvolvido pelo Google que faz com que entende o significado das palavras com base no contexto ao redor delas, tanto antes quanto depois. Isso faz com que o processamento de linguagem natural (NLP) fique muito mais próximo da maneira como os humanos realmente entendem um texto.

- Ecossistema rico, com bibliotecas como **spaCy** e acesso a modelos de ponta via **Hugging Face**.  
- Embora Node.js seja mais rápido para coleta de dados, a **análise de PLN** é a parte mais crítica e complexa.  
- O pipeline unificado em Python (ingestão de dados → análise → API) simplifica a arquitetura e acelera o desenvolvimento.  

✅ **Conclusão:** Python é a escolha lógica e inegociável para este projeto.  

---

# Seleção do Framework de API: Produtividade com Django e DRF

Com Python definido, a escolha do framework de API se resume a **Django** e **Flask**.

### Flask
- Micro-framework flexível, ideal para projetos pequenos ou com forte personalização.  
- Exige integração manual de componentes para autenticação, ORM e banco de dados.  

### Django
- Filosofia de **“baterias inclusas”**, oferecendo solução completa: ORM, autenticação e painel administrativo.  
- Com o **Django REST Framework (DRF)**, ganha-se:
  - Serialização robusta.  
  - Autenticação integrada.  
  - **API navegável automática**, acelerando testes e exploração de endpoints.  

✅ **Conclusão:** A complexidade do projeto está no pipeline de PLN, não na API.  
O Django com DRF permite focar na análise de dados sem reinventar funcionalidades básicas.  


## Referências Principais
- [Comparativo Python vs. Node.js para Web Scraping](https://scrape.do/blog/web-scraping-python-vs-nodejs/)  
- [Comparativo Django vs. Flask para APIs REST](https://www.excella.com/insights/creating-a-restful-api-django-rest-framework-vs-flask)  
-[BERT: o que é, como funciona e como implementar com Python?](https://hub.asimov.academy/blog/bert-o-que-e-como-funciona)  


