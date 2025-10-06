# 📋 Requisitos Prévios

Certifique-se de que os seguintes requisitos estão instalados no seu sistema:

1. **Python**: Versão 3.10 ou superior.
2. **pip**: O gerenciador de pacotes do Python, que geralmente é instalado junto com o Python.

---

## 🛠️ Configuração do Ambiente

### 1. Instalação de Dependências

Todas as bibliotecas necessárias para o projeto estão listadas no arquivo `requirements.txt`.

Para instalá-las, abra o seu terminal no diretório raiz do projeto e execute o comando:

```bash
pip install -r requirements.txt
```

### 2. Configuração da Chave API do Gemini

O projeto requer uma chave de API para interagir com o modelo Gemini. Você precisa criar um arquivo chamado `.env` na raiz do seu projeto e adicionar sua chave nele.

O conteúdo do seu arquivo `.env` deve seguir este formato:

```
GEMINI_API_KEY="SUA_CHAVE_DE_API_DO_GEMINI_AQUI"
```

* Substitua `"SUA_CHAVE_DE_API_DO_GEMINI_AQUI"` pela sua chave real.

---

## 🚀 Como Rodar o Servidor

Após instalar as dependências e configurar a chave API, você pode iniciar o servidor localmente usando Uvicorn.

Execute o seguinte comando no terminal (ainda no diretório raiz do projeto):

```bash
uvicorn main:app --reload
```

### Detalhes do Comando

* `uvicorn`: O servidor ASGI rápido que estamos usando.
* `main:app`: Indica ao Uvicorn para procurar a aplicação (variável `app`) dentro do módulo (`main.py`).
* `--reload`: Ativa o modo de recarga automática. O servidor será reiniciado automaticamente sempre que você salvar alterações no seu código-fonte, o que é ótimo para o desenvolvimento.

O servidor estará rodando, geralmente, em `http://127.0.0.1:8000` (ou `http://localhost:8000`).
