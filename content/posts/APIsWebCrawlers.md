---
draft: false
title: 'Estudo: APIs e Web Crawlers'
ShowToc: true
---


## 1. Introdução

Este documento explica os conceitos de **web crawling** e **APIs REST**, compara ferramentas populares para construir crawlers e discute os principais desafios legais e éticos associados à coleta automatizada de dados.

---

## 2. O que é Web Crawling

**Web crawling** é o processo automatizado de navegar por páginas web e coletar (baixar) seu conteúdo para indexação, análise ou extração de dados. Crawlers — também chamados de spiders — visitam URLs, seguem links e armazenam cópias das páginas ou extraem informações específicas.

**Quando usar crawling vs scraping vs APIs:**

* *Crawling* normalmente refere-se ao ato de descobrir páginas (seguir links) em grande escala.
* *Scraping* é a extração de dados de páginas individuais (parsing HTML, extrair campos).
* *APIs* são interfaces fornecidas pelos serviços para acesso estruturado — sempre que disponível, preferir API em vez de scraping.

---

## 3. Como funcionam os Web Crawlers (técnica)

Fluxo básico de um crawler:

1. **Seed list (lista inicial):** começa com um conjunto de URLs.
2. **Fetch (requisição):** faz requisições HTTP das páginas.
3. **Parse:** analisa o HTML para extrair links e conteúdo relevante.
4. **URL queue (fila):** adiciona novos links para visitar (com políticas de prioridade).
5. **Storage/indexação:** salva páginas ou extrai e armazena campos em banco de dados.
6. **Políticas:** politeness (intervalos entre requisições), politeness por host, limites de profundidade, tratamento de duplicatas.

Componentes técnicos importantes:

* **User-agent** — identifica o bot; deve cumprir regras indicadas em `robots.txt` quando aplicável.
* **robots.txt** — protocolo de exclusão usado por sites para indicar quais caminhos os crawlers podem acessar.
* **Sitemaps** — arquivos que listam URLs que o site deseja que sejam indexados.
* **Renderização JavaScript** — muitos sites modernos carregam conteúdo via JS; é preciso renderizar (headless browser) ou usar ferramentas que executem JS.

---

## 4. Principais ferramentas para criação de crawlers — levantamento e comparação

Abaixo há uma visão geral das ferramentas mais usadas (foco em 2024–2025):

| Ferramenta | Tipo | Linguagem | Quando usar | Prós | Contras |
|:-|:-|:-|:-|:-|:-|
| **Scrapy** | Framework crawler | Python | Crawling/scraping em larga escala, pipelines | Projetado para scraping, alto desempenho, extensível, comunidade ativa. | Curva de aprendizado; não executa JS por padrão. |
| **BeautifulSoup** | Parser HTML | Python | Extração simples de páginas estáticas | Fácil para parsing e protótipos. | Não faz requests paralelos nem renderiza JS (usado junto com requests). |
| **Selenium** | Browser automation | Multi (bindings em Python, JS) | Sites com JS complexo; automação de navegador | Executa JS, pode interagir com scripts e formulários. | Mais lento e pesado; consumo de recursos. |
| **Playwright** | Browser automation / scraping | Node.js / Python / .NET | Renderização robusta e headless, multi-browser | Rápido para automação moderna, suporte multi-engine. | Requer gerenciar instâncias de browser; maior complexidade. |
| **Puppeteer / Puppeteer-core** | Headless Chrome control | Node.js | Similar ao Playwright, focado Chrome/Chromium | Bom para páginas JS; API fluída. | Focado no motor Chromium. |
| **Apache Nutch** | Crawler distribuído / search | Java | Crawling em larga escala, integração com Hadoop | Escalável, extensível; pensado para motores de busca. | Mais complexo; stack Java/Hadoop. |
| **Heritrix** | Crawler para arquivamento | Java | Arquivamento web (ex.: bibliotecas, instituições) | Projetado para arquivamento em larga escala. | Complexidade operacional. |
| **Crawlee (Apify SDK)** | Framework de scraping | Node.js | Escalabilidade, integração com Apify | Bom para jobs em nuvem, rotinas reutilizáveis. | Ecossistema mais jovem que Scrapy. |

---

## 5. O que são APIs REST e como funcionam

### Conceito

**API (Application Programming Interface)** é uma interface que permite que aplicações comuniquem entre si. **REST (Representational State Transfer)** é um estilo arquitetural para APIs sobre HTTP que usa recursos (URLs) e operações HTTP (GET, POST, PUT, DELETE, PATCH) para manipular o estado.

### Princípios chave do REST

* **Recursos identificáveis por URIs** (ex.: `/users/123`).
* **Operações via métodos HTTP**: `GET` para leitura, `POST` para criar, `PUT`/`PATCH` para atualizar, `DELETE` para excluir.
* **Statelessness:** cada requisição deve conter informação suficiente para o servidor processá-la (não manter estado no servidor entre requisições).
* **Representação:** os recursos são retornados em formatos padrão (JSON é o mais comum hoje).
* **HATEOAS (hipermídia como o motor do estado da aplicação)** — ideal REST fulness, mas nem sempre implementado.

### Elementos práticos

* **Autenticação/Autorização:** API keys, OAuth 2.0, JWT.
* **Rate limiting:** para evitar abuso e proteger recursos do servidor.
* **Versionamento:** `/v1/` ou versionamento via cabeçalhos.
* **Códigos de status HTTP:** 200, 201, 204, 400, 401, 403, 404, 429, 500 etc.

### Exemplo simples (curl)

```bash
# Requisição GET para obter um recurso
curl -X GET "https://api.exemplo.com/v1/users/123" -H "Accept: application/json"

# Requisição POST para criar
curl -X POST "https://api.exemplo.com/v1/users" \
  -H "Content-Type: application/json" \
  -d '{"name":"Maria","email":"maria@ex.com"}'
```

---

## 6. APIs públicas úteis

> Repositórios e coleções úteis de APIs públicas:
>
> * **Public APIs (GitHub)** — lista colaborativa de APIs gratuitas e públicas.

Exemplos de APIs públicas que costumam ser úteis em estudos e projetos:

- **GitHub API**: metadados de repositórios, usuários, issues.
- **OpenStreetMap / Nominatim**: geocodificação e dados cartográficos abertos.
- **APIs de dados governamentais**: muitos países oferecem portais de dados abertos (open data).
- **NewsAPI.org**: Fornece artigos de várias fontes jornalísticas internacionais.
- **Mediastack API**: Similar ao NewsAPI, fornece notícias globais em tempo real.
- **GNews API**: Focado em notícias recentes, com endpoints simples e suporte a várias línguas.
- **Portal de Dados Abertos**: Encontre dados publicados pelo governo federal e por governos locais para realizar pesquisas, desenvolver aplicativos e criar novos serviços.

---

## 7. Desafios legais e éticos na coleta de dados

### Principais aspectos legais

* **Terms of Service (ToS):** muitos sites proíbem scraping em seus termos. Romper ToS pode levar a ações civis ou bloqueios técnicos.
* **Robots.txt:** não é lei, mas é considerado uma convenção de boa conduta; ignorá-lo aumenta risco reputacional e técnico.
* **Leis de proteção de dados (ex.: GDPR, LGPD):** coleta de dados pessoais requer bases legais, transparência, e cumprimento de direitos dos titulares.
* **CFAA e jurisprudência:** em alguns países (ex.: EUA) a legislação sobre acesso não autorizado (CFAA) foi usada em disputas. Um caso famoso é *hiQ v. LinkedIn*, que envolveu scraping de perfis públicos e gerou decisões e recursos que influenciaram o entendimento jurídico — essa área continua em evolução e depende da jurisdição.

### Questões éticas

* **Privacidade:** mesmo dados “públicos” podem afetar privacidade quando agregados e reidentificados.
* **Impacto econômico:** crawlers que geram tráfego massivo podem impor custos ao dono do site.
* **Consentimento e transparência:** ser transparente sobre coleta e uso de dados é prática ética recomendada.
* **Uso justo e direitos autorais:** reutilizar conteúdo sem autorização para fins comerciais pode infringir direitos.

---

## 8. Boas práticas ao coletar dados (crawling e via APIs)

* **Prefira APIs oficiais** quando existirem.
* **Respeite `robots.txt`** e políticas do site.
* **Implemente rate limiting** e backoff exponencial para reduzir carga no servidor.
* **Use User-Agent claro** e informações de contato (quando apropriado).
* **Cache e incremental crawling** para evitar downloads redundantes.
* **Proteja dados pessoais** e cumpra leis de proteção de dados.
* **Documente seu pipeline** e mantenha logs de acesso para auditoria.
* **Negocie acesso** com provedores de conteúdo quando for coletar em larga escala (parcerias, contratos).

---

## 9. Conclusão

Web crawling e APIs REST são ferramentas poderosas para obter dados da web. Enquanto APIs oferecem acesso estruturado e seguro quando disponíveis, crawlers permitem descobrir conteúdo onde APIs não existem, mas trazem complexidade técnica e riscos legais/éticos. 

Adote sempre práticas responsáveis: prefira APIs, seja transparente, e respeite limites técnicos e legais.

---

## 10. Referências

* Cloudflare — *What is a web crawler?* — [https://www.cloudflare.com/learning/bots/what-is-a-web-crawler/](https://www.cloudflare.com/learning/bots/what-is-a-web-crawler/)
* AWS — *What is RESTful API?* — [https://aws.amazon.com/what-is/restful-api/](https://aws.amazon.com/what-is/restful-api/)
* GitHub — *public-apis (lista de APIs públicas)* — [https://github.com/public-apis/public-apis](https://github.com/public-apis/public-apis)
* ScrapeHero / Apify — comparativos e listas de ferramentas (2024–2025).

  * [https://www.scrapehero.com/open-source-web-scraping-frameworks-and-tools/](https://www.scrapehero.com/open-source-web-scraping-frameworks-and-tools/)
  * [https://blog.apify.com/top-11-open-source-web-crawlers-and-one-powerful-web-scraper/](https://blog.apify.com/top-11-open-source-web-crawlers-and-one-powerful-web-scraper/)


---