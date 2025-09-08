# Relatório: Análise e Uso do Hugo

## 1. Sites Estáticos vs. Dinâmicos

---

[cite_start]**Sites estáticos** são construídos com HTML e contêm um conteúdo pré-definido e imutável[cite: 2]. [cite_start]Eles não oferecem interatividade para o usuário e carregam uma página "crua"[cite: 3]. [cite_start]Um exemplo comum é um portfólio online ou um projeto de faculdade sem muitas funcionalidades específicas para cada usuário[cite: 4].

[cite_start]**Sites dinâmicos**, por outro lado, utilizam bancos de dados para carregar informações externas, o que os torna mais complexos[cite: 5]. [cite_start]Eles permitem interatividade com o usuário[cite: 6]. [cite_start]A grande maioria dos sites da internet são dinâmicos, e nosso projeto também será[cite: 6].

## 2. O Que é o Hugo?

---

[cite_start]Hugo é uma ferramenta que converte arquivos de texto simples, como **Markdown**, em sites completos com HTML, CSS e JavaScript, prontos para serem publicados[cite: 7]. [cite_start]Em vez de criar cada página manualmente, você pode focar em escrever o conteúdo em arquivos de texto, e o Hugo se encarrega da parte de design e estrutura[cite: 8].

[cite_start]Hugo é ideal para sites que precisam ser leves, como sites de documentação, e que tenham uma estrutura base estática[cite: 9].

### Como Instalar o Hugo (Windows)

A instalação do Hugo no Windows é simples. [cite_start]Basta abrir o CMD e digitar `winget install Hugo.Hugo.Extended`[cite: 10]. [cite_start]Durante a instalação, você precisará concordar com os termos e, em seguida, reiniciar o PowerShell[cite: 10].

* [cite_start]**Observação:** Para usuários de Windows, é recomendado usar o PowerShell, WSL (Windows Subsystem for Linux) ou Git Bash em vez do Command Prompt tradicional[cite: 12].

## 3. Tutorial do Hugo "Quick Start"

---

[cite_start]O tutorial "Quick Start" no site oficial da GoHugo promete ensinar como criar, adicionar conteúdo, configurar e publicar um site[cite: 11]. [cite_start]É necessário ter o Hugo e o Git instalados na máquina antes de começar[cite: 12].

[cite_start]Embora o tutorial seja intuitivo e simples de seguir, a leitura no site oficial é altamente recomendada: [https://gohugo.io/getting-started/quick-start/](https://gohugo.io/getting-started/quick-start/)[cite: 12].

[cite_start]Se você seguiu o tutorial corretamente, o arquivo do seu projeto, chamado "quickstart," estará na sua pasta de usuário principal[cite: 12].

## 4. Sintaxe do Markdown

---

O Hugo utiliza a linguagem Markdown, que se assemelha ao HTML. A sintaxe básica é simples e fácil de aprender.

* **Títulos**: Use o caractere `#` para criar títulos. [cite_start]Quanto mais `#` você usar, menor o título será[cite: 15].
    * `# Título Principal`
    * `## Subtítulo`
    * `### Sub-subtítulo`

* [cite_start]**Ênfase (Negrito e Itálico)**: Use asteriscos (`*`) ou underscores (`_`) para dar ênfase[cite: 16].
    * `Este texto é **negrito** e este é *itálico*.`

* [cite_start]**Listas**: Use `*` ou `-` para listas não ordenadas, e números para listas ordenadas[cite: 17].
    * `* Item 1`
    * `* Item 2`
        * `* Subitem`
    * `1. Primeiro item`
    * `2. Segundo item`

* [cite_start]**Links**: Use colchetes para o texto e parênteses para a URL[cite: 18].
    * `Este é um [link para o Google](https://www.google.com).`

* [cite_start]**Imagens**: Similar aos links, mas com um ponto de exclamação (`!`) no início[cite: 19].
    * `![Texto alternativo para a imagem](caminho/para/imagem.jpg)`

## 5. Publicando um Site com Hugo no GitHub Pages

---

[cite_start]Gerar arquivos estáticos com Hugo é muito simples; basta digitar o comando `hugo` no terminal, e o site será gerado localmente[cite: 20].

Para publicá-lo no GitHub Pages, siga estes passos:

1.  [cite_start]Crie um novo repositório no GitHub[cite: 20].
2.  [cite_start]Configure o Git na sua pasta `public`[cite: 21]:
    * [cite_start]Inicialize o repositório Git localmente: `git init`[cite: 21].
    * [cite_start]Adicione todos os arquivos gerados ao controle de versão: `git add .`[cite: 21, 22].
    * [cite_start]Faça o primeiro commit: `git commit -m "Primeira publicação do site com Hugo"`[cite: 21, 22].
    * [cite_start]Conecte o repositório local ao seu repositório do GitHub: `git remote add origin https://github.com/seu-nome-de-usuario/seu-nome-de-usuario.github.io.git`[cite: 21, 22].
3.  [cite_start]Publique os arquivos do seu repositório local para o GitHub: `git push -u origin main`[cite: 23].

[cite_start]Após a conclusão, os arquivos deverão estar disponíveis em seu repositório no GitHub[cite: 23].

## 6. Considerações Finais

---

[cite_start]A experiência de criar um site estático com Hugo é simples e intuitiva[cite: 24]. [cite_start]A ferramenta Go (na qual Hugo é baseado) foi a escolhida para este projeto, mas existem outras linguagens como Ruby, JavaScript, e React, que também são usadas para criar sites estáticos[cite: 23].

[cite_start]O processo de "deploy" (publicação) é muito simples, bastando apenas o comando `hugo`[cite: 26]. [cite_start]Embora a ferramenta seja menos estilizada e não ofereça uma estrutura com orientação a objetos como o Flask, ela é extremamente funcional para o que se propõe[cite: 25].