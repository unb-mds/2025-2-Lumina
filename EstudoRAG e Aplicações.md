# Geração Aumentada por Recuperação (RAG)

RAG (Retrieval-Augmented Generation) é uma técnica que combina modelos de linguagem pré-treinados com sistemas de recuperação de informação. Ela faz com que o LLM “busque” dados externos relevantes (uma base de conhecimento) antes de gerar respostas[\[1\]](https://aws.amazon.com/what-is/retrieval-augmented-generation/#:~:text=Retrieval,and%20useful%20in%20various%20contexts)[\[2\]](https://www.couchbase.com/blog/pt/an-overview-of-retrieval-augmented-generation/#:~:text=Muitas%20equipes%20t%C3%A9cnicas%20est%C3%A3o%20trabalhando,tenha%20acesso%20a%20fatos%20externos). Em vez de confiar apenas no conhecimento embutido no modelo, o RAG recupera documentos ou trechos de texto relevantes (via embeddings e pesquisa semântica) e usa esses dados como contexto para a geração da resposta[\[3\]](https://aws.amazon.com/what-is/retrieval-augmented-generation/#:~:text=Without%20RAG%2C%20the%20LLM%20takes,an%20overview%20of%20the%20process)[\[2\]](https://www.couchbase.com/blog/pt/an-overview-of-retrieval-augmented-generation/#:~:text=Muitas%20equipes%20t%C3%A9cnicas%20est%C3%A3o%20trabalhando,tenha%20acesso%20a%20fatos%20externos). Isso otimiza a precisão e atualidade dos resultados, principalmente em domínios específicos, sem precisar retreinar o modelo completo[\[1\]](https://aws.amazon.com/what-is/retrieval-augmented-generation/#:~:text=Retrieval,and%20useful%20in%20various%20contexts)[\[4\]](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/#:~:text=Retrieval,specific%20and%20relevant%20data%20sources).

## Arquitetura e Pipeline

Uma aplicação típica de RAG envolve duas fases principais: **indexação** e **recuperação/geração**[\[5\]](https://python.langchain.com/docs/tutorials/rag/#:~:text=1,and%20%20179%20model)[\[6\]](https://python.langchain.com/docs/tutorials/rag/#:~:text=4,question%20with%20the%20retrieved%20data).

- **Indexação (pré-processamento):** carrega-se a base de dados (por exemplo, documentos, PDFs ou páginas web) usando _loaders_ adequados[\[5\]](https://python.langchain.com/docs/tutorials/rag/#:~:text=1,and%20%20179%20model). Em seguida, o texto é fragmentado em pedaços menores (usando um _TextSplitter_) para facilitar a busca[\[5\]](https://python.langchain.com/docs/tutorials/rag/#:~:text=1,and%20%20179%20model). Cada pedaço de texto é então convertido em vetor numérico por meio de um modelo de embedding (como o _OpenAIEmbeddings_) e armazenado num banco vetorial (_VectorStore_)[\[5\]](https://python.langchain.com/docs/tutorials/rag/#:~:text=1,and%20%20179%20model). Essa etapa estrutura o conhecimento, permitindo pesquisas semânticas eficientes.
- **Recuperação e geração (runtime):** dada uma consulta do usuário, o sistema converte a pergunta em embedding e usa um _retriever_ para encontrar os fragmentos mais relevantes no índice pré-computado[\[6\]](https://python.langchain.com/docs/tutorials/rag/#:~:text=4,question%20with%20the%20retrieved%20data)[\[3\]](https://aws.amazon.com/what-is/retrieval-augmented-generation/#:~:text=Without%20RAG%2C%20the%20LLM%20takes,an%20overview%20of%20the%20process). Por fim, um modelo de linguagem (por exemplo, GPT ou outro LLM) recebe a pergunta junto com os trechos recuperados e gera uma resposta contextualizada[\[6\]](https://python.langchain.com/docs/tutorials/rag/#:~:text=4,question%20with%20the%20retrieved%20data)[\[7\]](https://www.anaconda.com/blog/how-to-build-a-retrieval-augmented-generation-chatbot#:~:text=Are%20you%20interested%20in%20making,based%20on%20that%20retrieved%20information). Ou seja, o modelo lê o material recuperado e produz uma resposta factual e precisa em vez de depender apenas do seu conhecimento interno[\[6\]](https://python.langchain.com/docs/tutorials/rag/#:~:text=4,question%20with%20the%20retrieved%20data)[\[7\]](https://www.anaconda.com/blog/how-to-build-a-retrieval-augmented-generation-chatbot#:~:text=Are%20you%20interested%20in%20making,based%20on%20that%20retrieved%20information).

Esse fluxo — documentos carregados ➔ fragmentados ➔ indexados em vetor store ➔ consulta do usuário ➔ busca semântica ➔ geração com contexto — é a essência da RAG[\[5\]](https://python.langchain.com/docs/tutorials/rag/#:~:text=1,and%20%20179%20model)[\[6\]](https://python.langchain.com/docs/tutorials/rag/#:~:text=4,question%20with%20the%20retrieved%20data). Bibliotecas como o LangChain facilitam essa arquitetura, oferecendo _document loaders_, _text splitters_, modelos de _embeddings_, vetores e cadeias (chains) de RAG prontas para uso.

## Casos de Uso

RAG é especialmente útil em aplicações que exigem respostas precisas e baseadas em dados específicos. Entre os casos de uso mais comuns estão:

- **Sistemas de Perguntas e Respostas (Q&A):** RAG permite usuários fazerem perguntas e receber respostas detalhadas e relevantes baseadas em documentos de referência. Em comparação com sistemas tradicionais, ele oferece maior precisão e profundidade de conhecimento[\[8\]](https://www.couchbase.com/blog/pt/an-overview-of-retrieval-augmented-generation/#:~:text=Cria%C3%A7%C3%A3o%20de%20um%20sistema%20de,Q%26A).
- **Chatbots e assistentes virtuais:** Ao criar chatbots de atendimento ou suporte, RAG ajuda a fornecer respostas variadas e informativas mesmo em conversas complexas. Por exemplo, um chatbot no setor de seguros pode acessar políticas e manuais para responder dúvidas sobre benefícios e sinistros[\[9\]](https://www.couchbase.com/blog/pt/an-overview-of-retrieval-augmented-generation/#:~:text=Sistemas%20de%20conversa%C3%A7%C3%A3o).
- **Aplicações educacionais:** Em plataformas de ensino, RAG pode não só responder perguntas de alunos como também explicar as etapas de resolução ou gerar material de estudo com base em livros-texto e artigos relevantes[\[10\]](https://www.couchbase.com/blog/pt/an-overview-of-retrieval-augmented-generation/#:~:text=Sistemas%20educacionais). Isso enriquece a experiência de aprendizado em todos os níveis educacionais[\[10\]](https://www.couchbase.com/blog/pt/an-overview-of-retrieval-augmented-generation/#:~:text=Sistemas%20educacionais).
- **Geração de conteúdo e relatórios:** Para marketing, jornalismo ou análise de dados, RAG pode recuperar informações atuais e gerar relatórios resumidos ou conteúdos criativos (artigos, postagens em rede social, roteiros) de forma automatizada[\[11\]](https://www.couchbase.com/blog/pt/an-overview-of-retrieval-augmented-generation/#:~:text=Gera%C3%A7%C3%A3o%20de%20conte%C3%BAdo%20e%20relat%C3%B3rios). Isso acelera a pesquisa e aumenta a produtividade de quem cria conteúdo.
- **Conhecimento corporativo:** Quase qualquer empresa pode transformar manuais, políticas e logs internos em bases de conhecimento que alimentam assistentes internos. Esses assistentes podem ajudar em **suporte ao cliente**, treinamento de funcionários ou aumento de produtividade de desenvolvedores[\[12\]](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/#:~:text=For%20example%2C%20a%20generative%20AI,assistant%20linked%20to%20market%20data). Em suma, RAG viabiliza “conversas” com repositórios de dados em linguagem natural, abrindo amplos usos em diversos setores[\[13\]](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/#:~:text=With%20retrieval,the%20number%20of%20available%20datasets)[\[8\]](https://www.couchbase.com/blog/pt/an-overview-of-retrieval-augmented-generation/#:~:text=Cria%C3%A7%C3%A3o%20de%20um%20sistema%20de,Q%26A).

## Benefícios

A RAG traz diversas vantagens sobre o uso de LLMs isoladamente:

- **Atualização constante:** Um LLM pré-treinado tem base de conhecimento fixa (até uma certa data de corte). Com RAG, conectamos o modelo a dados atualizados em tempo real (ex.: notícias, repositórios internos), mantendo as respostas relevantes[\[14\]](https://aws.amazon.com/what-is/retrieval-augmented-generation/#:~:text=Current%20information)[\[15\]](https://www.ibm.com/think/topics/retrieval-augmented-generation#:~:text=Access%20to%20current%20and%20domain,data). Isso evita respostas obsoletas ou genéricas.
- **Maior precisão e menor risco de “alucinação”:** Ao fundamentar as respostas em fontes externas confiáveis, RAG reduz a tendência do modelo de inventar informações. O modelo “ancora” suas respostas em fatos existentes, aumentando a confiabilidade[\[16\]](https://www.ibm.com/think/topics/retrieval-augmented-generation#:~:text=Lower%20risk%20of%20AI%20hallucinations)[\[17\]](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/#:~:text=Retrieval,That%20builds%20trust). Além disso, é possível incluir citações das fontes usadas, o que permite ao usuário verificar as informações[\[17\]](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/#:~:text=Retrieval,That%20builds%20trust)[\[18\]](https://www.ibm.com/think/topics/retrieval-augmented-generation#:~:text=Increased%20user%20trust).
- **Custo-efetividade:** Introduzir novos dados via RAG é muito mais econômico do que retreinar ou ajustar finamente o modelo com grandes quantidades de texto. Em vez de pagar pelo pesado fine-tuning, a empresa simplesmente indexa os dados relevantes e deixa que o LLM os consulte[\[19\]](https://aws.amazon.com/what-is/retrieval-augmented-generation/#:~:text=Cost)[\[20\]](https://www.ibm.com/think/topics/retrieval-augmented-generation#:~:text=RAG%20empowers%20organizations%20to%20avoid,it%20can%20provide%20better%20answers). Isso facilita escalar aplicações de IA sem altos custos de processamento.
- **Controle do desenvolvedor:** RAG dá ao desenvolvedor controle sobre as fontes de informação. É possível adicionar, atualizar ou restringir os documentos usados sem mudar o modelo em si[\[21\]](https://aws.amazon.com/what-is/retrieval-augmented-generation/#:~:text=More%20developer%20control)[\[18\]](https://www.ibm.com/think/topics/retrieval-augmented-generation#:~:text=Increased%20user%20trust). Dados sensíveis podem ficar protegidos “on-premise” enquanto apenas trechos autorizados são disponibilizados ao LLM[\[21\]](https://aws.amazon.com/what-is/retrieval-augmented-generation/#:~:text=More%20developer%20control)[\[22\]](https://www.redhat.com/pt-br/topics/ai/what-is-retrieval-augmented-generation#:~:text=Privacidade%20e%20soberania%20de%20dados,de%20permiss%C3%A3o%20de%20seguran%C3%A7a%20deles). Isso melhora a segurança e conformidade do sistema.
- **Experiência do usuário:** Por apresentar respostas com fontes e mais contextuais, RAG aumenta a confiança dos usuários no chatbot ou sistema de IA[\[23\]](https://aws.amazon.com/what-is/retrieval-augmented-generation/#:~:text=Enhanced%20user%20trust)[\[17\]](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/#:~:text=Retrieval,That%20builds%20trust). Saber que as respostas vêm de documentos reais (que podem ser checados) evita o ceticismo típico de saídas dos LLMs não referenciadas.

Em resumo, RAG combina o melhor de dois mundos: a fluência dos grandes modelos de linguagem com a precisão de bases de conhecimento específicas[\[1\]](https://aws.amazon.com/what-is/retrieval-augmented-generation/#:~:text=Retrieval,and%20useful%20in%20various%20contexts)[\[4\]](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/#:~:text=Retrieval,specific%20and%20relevant%20data%20sources).

## Implementação em Código (usando LangChain)

Uma implementação básica de RAG em Python segue estas etapas principais (exemplificadas com o framework LangChain):

- **Instalar bibliotecas:** certifique-se de instalar o LangChain e dependências de vetorização, por exemplo: pip install langchain langchain-text-splitters langchain-embeddings chromadb.
- **Carregar documentos:** use um _DocumentLoader_ para importar seus dados. Por exemplo, para PDFs:  
```
from langchain.document_loaders import PyPDFLoader  
    loader = PyPDFLoader("documento.pdf")  
    documentos = loader.load()
```
- (LangChain oferece vários loaders, incluindo _WebBaseLoader_, _CSVLoader_ etc.)[\[24\]](https://www.anaconda.com/blog/how-to-build-a-retrieval-augmented-generation-chatbot#:~:text=,are%20then%20translated%20into%20numerical).
- **Fragmentar texto:** quebre cada documento em pedaços menores (chunks) para melhorar a busca. Por exemplo:  
```
from langchain.text_splitter import CharacterTextSplitter  
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)  
    fragmentos = splitter.split_documents(documentos)
```
- Isso facilita encontrar as partes relevantes sem ultrapassar o limite de contexto do LLM[\[5\]](https://python.langchain.com/docs/tutorials/rag/#:~:text=1,and%20%20179%20model)[\[24\]](https://www.anaconda.com/blog/how-to-build-a-retrieval-augmented-generation-chatbot#:~:text=,are%20then%20translated%20into%20numerical).
- **Gerar embeddings:** converta os fragmentos em vetores numéricos usando um modelo de embedding. Exemplo com OpenAI:  
```
from langchain.embeddings import OpenAIEmbeddings  
    embeddings = OpenAIEmbeddings() # requer OPENAI_API_KEY
 ```   
- Cada fragmento agora é representado por um vetor que captura seu conteúdo semântico[\[25\]](https://www.anaconda.com/blog/how-to-build-a-retrieval-augmented-generation-chatbot#:~:text=,are%20then%20translated%20into%20numerical).
- **Criar VectorStore:** armazene os vetores em um banco vetorial (como Chroma, FAISS, Pinecone etc.) para permitir buscas por similaridade. Exemplo usando Chroma:  
```
from langchain.vectorstores import Chroma  
    db = Chroma.from_documents(fragmentos, embeddings)
```
- Isso cria um índice onde podemos fazer consultas similares à consulta do usuário[\[26\]](https://www.anaconda.com/blog/how-to-build-a-retrieval-augmented-generation-chatbot#:~:text=,questions%3A%C2%A0A%20RetrievalQA%20chain%20chains%20a).
- **Configurar retriever:** exponha o VectorStore através de um _retriever_, especificando tipo de busca (geralmente similaridade). Por exemplo:  
```
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
```
- Isso fará com que, dado um embedding de pergunta, sejam retornados os 3 fragmentos mais relevantes do índice[\[26\]](https://www.anaconda.com/blog/how-to-build-a-retrieval-augmented-generation-chatbot#:~:text=,questions%3A%C2%A0A%20RetrievalQA%20chain%20chains%20a).
- **Encadear com LLM (RAG):** finalmente, crie uma cadeia de RAG que combina o LLM com o retriever. Por exemplo:  
```
from langchain.chains import RetrievalQA  
    from langchain.llms import OpenAI  
    rag_chain = RetrievalQA.from_chain_type(  
    llm=OpenAI(model_name="gpt-4"),  
    retriever=retriever,  
    return_source_documents=True  
    )  
    resposta = rag_chain.run("Qual é a sua pergunta aqui?")  
    print(resposta)
```
- Isso faz com que o LLM gere uma resposta considerando os fragmentos recuperados. (Em modo verbose, também pode retornar as fontes usadas.)

Veja abaixo um exemplo completo resumido em código:
```
from langchain.document_loaders import PyPDFLoader  
from langchain.text_splitter import CharacterTextSplitter  
from langchain.embeddings import OpenAIEmbeddings  
from langchain.vectorstores import Chroma  
from langchain.chains import RetrievalQA  
from langchain.llms import OpenAI  
# 1. Carrega documento  
loader = PyPDFLoader("documento.pdf")  
docs = loader.load()  
# 2. Divide em fragmentos  
splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)  
chunks = splitter.split_documents(docs)  
# 3. Gera embeddings  
embeddings = OpenAIEmbeddings()  
# 4. Cria o VectorStore (índice vetorial)  
db = Chroma.from_documents(chunks, embeddings)  
# 5. Configura o retriever  
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 2})  
# 6. Cria a cadeia RAG de QA  
qa = RetrievalQA.from_chain_type(llm=OpenAI(model_name="gpt-4"), retriever=retriever)  
# 7. Executa uma consulta  
answer = qa.run("Qual é o tema principal deste documento?")  
print(answer)
```

Nesse exemplo, o PDF é dividido, indexado e utilizado para responder perguntas. A função RetrievalQA (cadeia de RAG do LangChain) interna faz a recuperação dos fragmentos relevantes e passa tudo ao LLM para formar a resposta[\[27\]](https://www.anaconda.com/blog/how-to-build-a-retrieval-augmented-generation-chatbot#:~:text=os.environ%5B,to%20use%20embeddings%20%3D%20OpenAIEmbeddings)[\[28\]](https://www.anaconda.com/blog/how-to-build-a-retrieval-augmented-generation-chatbot#:~:text=retriever%20%3D%20db.as_retriever%28%20search_type%3D,retriever%3Dretriever%2C%20return_source_documents%3DTrue).

## Considerações Finais

A geração aumentada por recuperação (RAG) é uma técnica poderosa para criar aplicações de IA mais precisas e confiáveis. Ao integrar busca de informações e modelos de linguagem, ela permite que chatbots e sistemas de QA funcionem com dados atuais e específicos, sem exigirem modelos caros e estáticos. O uso de frameworks como LangChain simplifica essa implementação, fornecendo abstrações de loaders, vetores e _chains_ prontas. Em resumo, o RAG amplia significativamente as capacidades dos LLMs, tornando-os capazes de responder com base em conhecimentos reais e atualizados[\[1\]](https://aws.amazon.com/what-is/retrieval-augmented-generation/#:~:text=Retrieval,and%20useful%20in%20various%20contexts)[\[4\]](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/#:~:text=Retrieval,specific%20and%20relevant%20data%20sources).

**Fontes:** As informações acima foram compiladas de documentos oficiais e artigos especializados sobre RAG, incluindo materiais da LangChain[\[5\]](https://python.langchain.com/docs/tutorials/rag/#:~:text=1,and%20%20179%20model)[\[6\]](https://python.langchain.com/docs/tutorials/rag/#:~:text=4,question%20with%20the%20retrieved%20data), AWS[\[1\]](https://aws.amazon.com/what-is/retrieval-augmented-generation/#:~:text=Retrieval,and%20useful%20in%20various%20contexts)[\[19\]](https://aws.amazon.com/what-is/retrieval-augmented-generation/#:~:text=Cost), NVIDIA[\[4\]](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/#:~:text=Retrieval,specific%20and%20relevant%20data%20sources)[\[17\]](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/#:~:text=Retrieval,That%20builds%20trust), IBM[\[20\]](https://www.ibm.com/think/topics/retrieval-augmented-generation#:~:text=RAG%20empowers%20organizations%20to%20avoid,it%20can%20provide%20better%20answers)[\[29\]](https://www.ibm.com/think/topics/retrieval-augmented-generation#:~:text=RAG%20anchors%20LLMs%20in%20specific,proof) e publicações técnicas relevantes[\[30\]](https://www.couchbase.com/blog/pt/an-overview-of-retrieval-augmented-generation/#:~:text=Cria%C3%A7%C3%A3o%20de%20um%20sistema%20de,Q%26A)[\[11\]](https://www.couchbase.com/blog/pt/an-overview-of-retrieval-augmented-generation/#:~:text=Gera%C3%A7%C3%A3o%20de%20conte%C3%BAdo%20e%20relat%C3%B3rios). Cada afirmação está embasada nas referências indicadas.

[\[1\]](https://aws.amazon.com/what-is/retrieval-augmented-generation/#:~:text=Retrieval,and%20useful%20in%20various%20contexts) [\[3\]](https://aws.amazon.com/what-is/retrieval-augmented-generation/#:~:text=Without%20RAG%2C%20the%20LLM%20takes,an%20overview%20of%20the%20process) [\[14\]](https://aws.amazon.com/what-is/retrieval-augmented-generation/#:~:text=Current%20information) [\[19\]](https://aws.amazon.com/what-is/retrieval-augmented-generation/#:~:text=Cost) [\[21\]](https://aws.amazon.com/what-is/retrieval-augmented-generation/#:~:text=More%20developer%20control) [\[23\]](https://aws.amazon.com/what-is/retrieval-augmented-generation/#:~:text=Enhanced%20user%20trust) What is RAG? - Retrieval-Augmented Generation AI Explained - AWS

<https://aws.amazon.com/what-is/retrieval-augmented-generation/>

[\[2\]](https://www.couchbase.com/blog/pt/an-overview-of-retrieval-augmented-generation/#:~:text=Muitas%20equipes%20t%C3%A9cnicas%20est%C3%A3o%20trabalhando,tenha%20acesso%20a%20fatos%20externos) [\[8\]](https://www.couchbase.com/blog/pt/an-overview-of-retrieval-augmented-generation/#:~:text=Cria%C3%A7%C3%A3o%20de%20um%20sistema%20de,Q%26A) [\[9\]](https://www.couchbase.com/blog/pt/an-overview-of-retrieval-augmented-generation/#:~:text=Sistemas%20de%20conversa%C3%A7%C3%A3o) [\[10\]](https://www.couchbase.com/blog/pt/an-overview-of-retrieval-augmented-generation/#:~:text=Sistemas%20educacionais) [\[11\]](https://www.couchbase.com/blog/pt/an-overview-of-retrieval-augmented-generation/#:~:text=Gera%C3%A7%C3%A3o%20de%20conte%C3%BAdo%20e%20relat%C3%B3rios) [\[30\]](https://www.couchbase.com/blog/pt/an-overview-of-retrieval-augmented-generation/#:~:text=Cria%C3%A7%C3%A3o%20de%20um%20sistema%20de,Q%26A) What Is Retrieval Augmented Generation (RAG)? An Overview

<https://www.couchbase.com/blog/pt/an-overview-of-retrieval-augmented-generation/>

[\[4\]](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/#:~:text=Retrieval,specific%20and%20relevant%20data%20sources) [\[12\]](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/#:~:text=For%20example%2C%20a%20generative%20AI,assistant%20linked%20to%20market%20data) [\[13\]](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/#:~:text=With%20retrieval,the%20number%20of%20available%20datasets) [\[17\]](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/#:~:text=Retrieval,That%20builds%20trust) What Is Retrieval-Augmented Generation aka RAG | NVIDIA Blogs

<https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/>

[\[5\]](https://python.langchain.com/docs/tutorials/rag/#:~:text=1,and%20%20179%20model) [\[6\]](https://python.langchain.com/docs/tutorials/rag/#:~:text=4,question%20with%20the%20retrieved%20data) Build a Retrieval Augmented Generation (RAG) App: Part 1 | ️ LangChain

<https://python.langchain.com/docs/tutorials/rag/>

[\[7\]](https://www.anaconda.com/blog/how-to-build-a-retrieval-augmented-generation-chatbot#:~:text=Are%20you%20interested%20in%20making,based%20on%20that%20retrieved%20information) [\[24\]](https://www.anaconda.com/blog/how-to-build-a-retrieval-augmented-generation-chatbot#:~:text=,are%20then%20translated%20into%20numerical) [\[25\]](https://www.anaconda.com/blog/how-to-build-a-retrieval-augmented-generation-chatbot#:~:text=,are%20then%20translated%20into%20numerical) [\[26\]](https://www.anaconda.com/blog/how-to-build-a-retrieval-augmented-generation-chatbot#:~:text=,questions%3A%C2%A0A%20RetrievalQA%20chain%20chains%20a) [\[27\]](https://www.anaconda.com/blog/how-to-build-a-retrieval-augmented-generation-chatbot#:~:text=os.environ%5B,to%20use%20embeddings%20%3D%20OpenAIEmbeddings) [\[28\]](https://www.anaconda.com/blog/how-to-build-a-retrieval-augmented-generation-chatbot#:~:text=retriever%20%3D%20db.as_retriever%28%20search_type%3D,retriever%3Dretriever%2C%20return_source_documents%3DTrue) How to Build a Retrieval-Augmented Generation Chatbot | Anaconda

<https://www.anaconda.com/blog/how-to-build-a-retrieval-augmented-generation-chatbot>

[\[15\]](https://www.ibm.com/think/topics/retrieval-augmented-generation#:~:text=Access%20to%20current%20and%20domain,data) [\[16\]](https://www.ibm.com/think/topics/retrieval-augmented-generation#:~:text=Lower%20risk%20of%20AI%20hallucinations) [\[18\]](https://www.ibm.com/think/topics/retrieval-augmented-generation#:~:text=Increased%20user%20trust) [\[20\]](https://www.ibm.com/think/topics/retrieval-augmented-generation#:~:text=RAG%20empowers%20organizations%20to%20avoid,it%20can%20provide%20better%20answers) [\[29\]](https://www.ibm.com/think/topics/retrieval-augmented-generation#:~:text=RAG%20anchors%20LLMs%20in%20specific,proof) What is RAG (Retrieval Augmented Generation)? | IBM

<https://www.ibm.com/think/topics/retrieval-augmented-generation>

[\[22\]](https://www.redhat.com/pt-br/topics/ai/what-is-retrieval-augmented-generation#:~:text=Privacidade%20e%20soberania%20de%20dados,de%20permiss%C3%A3o%20de%20seguran%C3%A7a%20deles) O que é geração aumentada de recuperação (RAG)?

<https://www.redhat.com/pt-br/topics/ai/what-is-retrieval-augmented-generation>
