# Estudo: Análise e Uso do Hugo

## 1. Sites Estáticos vs. Dinâmicos

Sites estáticos são construídos com HTML e contêm um conteúdo pré-definido e imutável. Eles não oferecem interatividade para o usuário e carregam uma página "crua". Um exemplo comum é um portfólio online ou um projeto de faculdade sem muitas funcionalidades específicas para cada usuário.

Sites dinâmicos, por outro lado, utilizam bancos de dados para carregar informações externas, o que os torna mais complexos. Eles permitem interatividade com o usuário. A grande maioria dos sites da internet são dinâmicos, e nosso projeto também será.

## 2. O Que é o Hugo?

Hugo é uma ferramenta que converte arquivos de texto simples, como Markdown, em sites completos com HTML, CSS e JavaScript, prontos para serem publicados. Em vez de criar cada página manualmente, você pode focar em escrever o conteúdo em arquivos de texto, e o Hugo se encarrega da parte de design e estrutura.

Hugo é ideal para sites que precisam ser leves, como sites de documentação, e que tenham uma estrutura base estática.

### 2.1. Como Instalar o Hugo (Windows)

A instalação do Hugo no Windows é simples. Basta abrir o CMD e digitar `winget install Hugo.Hugo.Extended`. Durante a instalação, você precisará concordar com os termos e, em seguida, reiniciar o PowerShell.

> **Observação:** Para usuários de Windows, é recomendado usar o PowerShell, WSL (Windows Subsystem for Linux) ou Git Bash em vez do Command Prompt tradicional.

## 3. Tutorial do Hugo "Quick Start"

O tutorial "Quick Start" no site oficial da GoHugo promete ensinar como criar, adicionar conteúdo, configurar e publicar um site. É necessário ter o Hugo e o Git instalados na máquina antes de começar.

Embora o tutorial seja intuitivo e simples de seguir, a leitura no site oficial é altamente recomendada.

Se você seguiu o tutorial corretamente, o arquivo do seu projeto, chamado `quickstart`, estará na sua pasta de usuário principal.

## 4. Sintaxe do Markdown

O Hugo utiliza a linguagem Markdown, que se assemelha ao HTML. A sintaxe básica é simples e fácil de aprender.

* **Títulos:** Use o caractere `#` para criar títulos. Quanto mais `#` você usar, menor o título será.
    ```markdown
    # Título Principal
    ## Subtítulo
    ### Sub-subtítulo
    ```
* **Ênfase (Negrito e Itálico):** Use asteriscos (`*`) ou underscores (`_`) para dar ênfase.
    ```markdown
    Este texto é **negrito** e este é *itálico*.
    ```
* **Listas:** Use `*` ou `-` para listas não ordenadas, e números para listas ordenadas.
    ```markdown
    * Item 1
    * Item 2
      * Subitem

    1. Primeiro item
    2. Segundo item
    ```
* **Links:** Use colchetes para o texto e parênteses para a URL.
    ```markdown
    Este é um [link para o Google](https://www.google.com).
    ```
* **Imagens:** Similar aos links, mas com um ponto de exclamação (`!`) no início.
    ```markdown
    ![Texto alternativo para a imagem](caminho/para/imagem.jpg)
    ```

## 5. Publicando um Site com Hugo no GitHub Pages

Gerar arquivos estáticos com Hugo é muito simples; basta digitar o comando `hugo` no terminal, e o site será gerado localmente.

Para publicá-lo no GitHub Pages, siga estes passos:

1.  Crie um novo repositório no GitHub.
2.  Configure o Git na sua pasta `public`:
    * Inicialize o repositório Git localmente: `git init`.
    * Adicione todos os arquivos gerados ao controle de versão: `git add .`.
    * Faça o primeiro commit: `git commit -m "Primeira publicação do site com Hugo"`.
    * Conecte o repositório local ao seu repositório do GitHub: `git remote add origin https://github.com/seu-nome-de-usuario/seu-nome-de-usuario.github.io.git`.
    * Publique os arquivos do seu repositório local para o GitHub: `git push -u origin main`.

Após a conclusão, os arquivos deverão estar disponíveis em seu repositório no GitHub.

## 6. Considerações Finais

A experiência de criar um site estático com Hugo é simples e intuitiva. A ferramenta Go (na qual Hugo é baseado) foi a escolhida para este projeto, mas existem outras linguagens como Ruby, JavaScript, e React, que também são usadas para criar sites estáticos.

O processo de "deploy" (publicação) é muito simples, bastando apenas o comando `hugo`. Embora a ferramenta seja menos estilizada e não ofereça uma estrutura com orientação a objetos como o Flask, ela é extremamente funcional para o que se propõe.

## 7. Referências

* [Guia de Início Rápido do Hugo](https://gohugo.io/getting-started/quick-start/)
* [Product Manager: o que faz, quanto ganha e como se destacar - Alura](https://www.alura.com.br/artigos/product-manager-o-que-faz-quanto-ganha-como-se-destacar)
