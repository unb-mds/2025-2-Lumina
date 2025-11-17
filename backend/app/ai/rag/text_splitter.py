import logging
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


from app.models.article import Article

logger = logging.getLogger(__name__)


class TextSplitter:
    """
    Responsável por dividir o conteúdo de um Article em chunks (pedaços)
    menores e mais gerenciáveis para o processo de embedding e RAG.
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Inicializa o TextSplitter com as configurações de divisão.

        Args:
            chunk_size (int): O tamanho máximo de cada chunk (em caracteres).
            chunk_overlap (int): O número de caracteres de sobreposição
                                 entre chunks consecutivos.
        """
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
            separators=[
                "\n\n",  # Prioriza quebra entre parágrafos
                "\n",  # Quebra por linha
                ".",  # Quebra por sentença
                " ",  # Quebra por palavra
                "",  # Força a quebra
            ],
        )
        logger.info(
            f"TextSplitter inicializado com chunk_size={chunk_size} "
            f"e chunk_overlap={chunk_overlap}"
        )

    def split_article(self, article: Article) -> List[Document]:
        """
        Divide o conteúdo de um artigo em uma lista de `Document`s (chunks).

        Cada `Document` contém um pedaço do texto e metadados relevantes.

        Args:
            article (Article): O objeto Article a ser dividido.

        Returns:
            List[Document]: Uma lista de chunks. Retorna lista vazia se o
                            artigo não tiver conteúdo ou se ocorrer um erro.

        Raises:
            ValueError: Se o artigo não tiver um ID, que é essencial para
                        vincular os chunks ao artigo original.
        """
        if not article.id:
            raise ValueError("O artigo a ser dividido não possui um ID.")

        if not article.content:
            logger.warning(
                f"Artigo ID {article.id} não possui conteúdo para ser dividido."
            )
            return []

        # Metadados que serão replicados em todos os chunks
        metadata = {
            "article_id": article.id,
            "url": article.url,
            "title": article.title,
        }

        try:
            # O método `create_documents` do LangChain faz a mágica:
            # 1. Pega uma lista de textos (no nosso caso, só o `article.content`)
            # 2. Pega uma lista de metadados (só o nosso `metadata`)
            # 3. Divide o texto e anexa os metadados correspondentes a cada chunk
            chunks = self.splitter.create_documents([article.content], [metadata])
            logger.info(f"Artigo ID {article.id} dividido em {len(chunks)} chunks.")
            return chunks
        except Exception as e:
            logger.error(
                f"Erro ao dividir o artigo ID {article.id} com o LangChain: {e}"
            )
            # Em caso de falha, retorna uma lista vazia para não quebrar o fluxo
            return []
