# Lumina

### Combate às fake news com inteligência artificial conversacional.

---

## 📄 Sobre o Projeto

Projeto desenvolvido para a disciplina de **Métodos de Desenvolvimento de Software (MDS) - 2025/2** da **Universidade de Brasília (UnB)**.

O objetivo do Lumina é combater a desinformação crescente. Nossa solução é um chatbot inteligente que permite a verificação rápida de fatos e notícias. Diferente dos mecanismos de busca tradicionais, o Lumina oferece uma interface conversacional intuitiva, utilizando IA Generativa para analisar e sintetizar informações de fontes confiáveis em tempo real.

## 🛠️ Tecnologias Utilizadas

O ecossistema do Lumina é robusto e utiliza as seguintes tecnologias:

* **📱 Frontend (App Mobile):** Flutter (Android/iOS).
* **⚙️ Backend (API):** Python com FastAPI.
* **🤖 Inteligência Artificial:** Google Gemini API via LangChain para RAG.
* **🗄️ Banco de Dados:**
    * **SQLite:** Para armazenamento relacional de artigos e metadados.
    * **ChromaDB:** Banco de dados vetorial para busca semântica e embeddings.

## 🏗️ Estrutura do Repositório

O projeto adota uma arquitetura de monorepo, contendo frontend e backend no mesmo local.

```
Lumina/
├── .github/                 # Configurações de CI/CD e Templates
│   ├── workflows/           # Pipelines do GitHub Actions
│   └── ...
│
├── backend/                 # API, IA e Lógica de Servidor
│   ├── app/                 # Código fonte Python
│   ├── tests/               # Testes automatizados (Pytest)
│   └── main.py              # Ponto de entrada do servidor
│
├── frontend/                # Aplicativo Mobile (Flutter)
│   ├── lib/                 # Código fonte Dart
│   ├── android              #Integração do aplicativo para a plataforma   
│   └── pubspec.yaml         # Dependências do Flutter
│
├── docs/                    # Documentação do Projeto
│   ├── documentações/       # Documentos técnicos
│   ├── estudos/             # Pesquisas e provas de conceito
│   └── planejamentos/       # Gestão do projeto (Atas, Sprints)
│
├── .gitignore               # Arquivos ignorados pelo Git
├── CONTRIBUTING.md          # Guia para contribuir
├── LICENSE                  # Licença MIT
├── README.md                # Visão geral do projeto
└── pytest.ini               # Configuração de testes
```

## 🤝 Como Contribuir
Ficamos felizes com o interesse em contribuir! Para detalhes sobre como submeter Pull Requests, padrões de código e nossa política de conduta, leia nosso guia:[CONTRIBUTING.md](CONTRIBUTING.md)

## 👥 Autores
O projeto é desenvolvido pelas seguintes pessoas

|Nome|Função|Github|
|-----|-----|------|
| Cecília Costa Rebelo Cunha |Scrum Master (Líder de projeto)| [CeciliaCunha](https://github.com/CeciliaCunha) |
|Arthur Luiz Silva Guedes|Product Manager (PO)| [ArthurLuizUnB](https://github.com/ArthurLuizUnB)|
|Átila Sobral de Oliveira|Developer| [Atila05](https://github.com/Atila05)|
|Nathan Pontes Romão|Developer (Líder)| [nathanpromao](https://github.com/nathanpromao)|
|João Pedro Ferreira Gomes |Designer|[Joao-PFG](https://github.com/Joao-PFG)|
|Tiago Geovane da Silva Sousa|Arquitetura/DevOps|[TiagoUNB](https://github.com/TiagoUNB)|
------------

# 🔗 Links importantes
- Nosso [Git Pages](https://unb-mds.github.io/2025-2-Lumina)

- Nosso [Figma](https://www.figma.com/design/WAbCYuadSmQjoSXwQu2FZa/Squad-07--MDS?node-id=1-3188&t=jXbDeQuQQlIQOL1h-0)

