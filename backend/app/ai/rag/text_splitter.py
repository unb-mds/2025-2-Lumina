import logging
from typing import List
from app.models.article import Article
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)


class TextSplitter:
    """
    Responsável por dividir o conteúdo de um Artigo em 'chunks' (pedaços)
    de texto menores, prontos para a vetorização, anexando os metadatos
    necessários para o RAG.
    """

    def __init__(self, chunk_size: int = 1500, chunk_overlap: int = 150):
        """
        Inicializa o splitter.

        Args:
            chunk_size (int): O tamanho máximo de cada chunk (em caracteres).
                              (Padrão: 1500)
            chunk_overlap (int): A sobreposição entre chunks (em caracteres).
                                 (Padrão: 150)
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Usamos o RecursiveCharacterTextSplitter por ser mais inteligente
        # na divisão, priorizando parágrafos (\n\n), depois linhas (\n),
        # e só então espaços (" ") ou caracteres ("").
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
        )
        logger.info(
            f"TextSplitter inicializado com chunk_size={chunk_size} e chunk_overlap={chunk_overlap}"
        )

    def split_article(self, article: Article) -> List[Document]:
        """
        Recebe um objeto Article e divide seu 'content' em múltiplos
        objetos Document (do LangChain).

        Cada Document (chunk) conterá o texto e os metadados
        (article_id, url, title) necessários para a citação de fontes no RAG.

        Args:
            article (Article): O artigo a ser dividido.

        Returns:
            List[Document]: Uma lista de 'chunks' como objetos Document.
                            Cada Document tem 'page_content' (o texto) e
                            'metadata' (article_id, url, title).

        Raises:
            ValueError: Se o artigo não tiver um 'id', que é essencial
                        para os metadados do RAG.
        """
        if not article.content:
            logger.warning(
                f"Artigo ID {article.id} ({article.url}) não possui conteúdo. Pulando."
            )
            return []

        # REGRA DE NEGÓCIO (RAG): Um chunk *deve* ter um ID de origem.
        if article.id is None:
            logger.error(
                f"Artigo com URL {article.url} está sem ID. Não é possível splittar sem ID."
            )
            raise ValueError(
                f"Artigo com URL {article.url} não possui um ID do banco de dados."
            )

        # 1. Define os metadados que serão *comuns* a todos os chunks
        metadata = {
            "article_id": article.id,
            "url": article.url,
            "title": article.title,
        }

        # 2. Divide o 'content' e cria os Documentos.
        # O método 'create_documents' aplica os metadados a todos
        # os chunks criados a partir daquele texto.
        try:
            chunks = self.splitter.create_documents(
                [article.content],  # Lista de textos a serem divididos
                metadatas=[metadata],  # Lista de metadados correspondentes
            )

            logger.info(
                f"Artigo ID {article.id} ({article.url}) dividido em {len(chunks)} chunks."
            )
            return chunks

        except Exception as e:
            logger.error(
                f"Erro ao dividir o artigo ID {article.id} ({article.url}): {e}"
            )
            return []