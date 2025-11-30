<div align="center">

# Lumina
### Combate às fake news com inteligência artificial conversacional.

![GitHub repo size](https://img.shields.io/github/repo-size/unb-mds/2025-2-Lumina?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/unb-mds/2025-2-Lumina?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/unb-mds/2025-2-Lumina?style=for-the-badge)
![Bitbucket open issues](https://img.shields.io/github/issues/unb-mds/2025-2-Lumina?style=for-the-badge)
![GitHub license](https://img.shields.io/github/license/unb-mds/2025-2-Lumina?style=for-the-badge)

</div>

---

## 📄 Sobre o Projeto

Projeto desenvolvido para a disciplina de **Métodos de Desenvolvimento de Software (MDS) - 2025/2** da **Universidade de Brasília (UnB)**.

O objetivo do Lumina é combater a desinformação crescente. Nossa solução é um chatbot inteligente que permite a verificação rápida de fatos e notícias. Diferente dos mecanismos de busca tradicionais, o Lumina oferece uma interface conversacional intuitiva, utilizando IA Generativa para analisar e sintetizar informações de fontes confiáveis em tempo real.

## 🚦 Status de Qualidade e Testes

Aqui você acompanha a saúde atual do projeto:

| Tipo | Status |
|------|--------|
| **Integração Contínua (CI)** | ![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/unb-mds/2025-2-Lumina/main.yml?style=for-the-badge&label=Build%20%26%20Test) |
| **Testes Backend** | ![Tests](https://img.shields.io/badge/Pytest-Passing-success?style=for-the-badge&logo=pytest) |
| **Testes Frontend** | ![Tests](https://img.shields.io/badge/Flutter%20Test-Passing-success?style=for-the-badge&logo=flutter) |

## 🛠️ Tecnologias Utilizadas

O ecossistema do Lumina é composto pelas seguintes tecnologias:

| Categoria | Tecnologias |
|-----------|-------------|
| **Frontend (Mobile)** | ![Flutter](https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white) ![Dart](https://img.shields.io/badge/Dart-0175C2?style=for-the-badge&logo=dart&logoColor=white) |
| **Backend (API)** | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) |
| **Banco de Dados** | ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white) ![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6F00?style=for-the-badge&logo=database&logoColor=white) |
| **DevOps & Testes** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) |

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

## 🚀 Como Executar

Siga os passos abaixo para configurar o ambiente de desenvolvimento na sua máquina.

### 📋 Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina:
* **Git** (instalado e configurado).
* **Python 3.10+** instalado.
* **Flutter SDK** instalado e configurado.
* Uma chave de API do **Google Gemini** (obtenha no [Google AI Studio](https://aistudio.google.com/)).

---

### 1. ⚙️ Backend (API Python)

1. Navegue até a pasta do backend:
    ```bash
    cd Oncomap/backend
    ```

2. Crie um ambiente virtual para isolar as dependências:
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Instale as dependências do projeto:
    ```bash
    pip install -r requirements.txt
    ```

4. Configure as variáveis de ambiente:

* Crie um arquivo chamado .env na raiz da pasta backend.

* Adicione a sua chave de API dentro dele:
    ```bash
    GOOGLE_API_KEY=sua_chave_aqui
    ```

5. Execute o servidor de desenvolvimento:
    ```bash
    fastapi dev main.py
    ```

### 2. 📱 Frontend (App Mobile)

1. Em outro terminal, acesse a pasta do frontend:
    ```bash
    cd frontend
    ```

2. Instale as dependências do Flutter:

    ```bash
    flutter pub get
    ```

3. Execute o aplicativo: (Nota: É necessário um emulador Android/iOS aberto ou um dispositivo físico conectado via USB)
    ```bash
    flutter run
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
  

