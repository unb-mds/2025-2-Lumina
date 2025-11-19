import logging
from typing import Optional

from bs4 import BeautifulSoup

from app.models.article import Article
from app.models.pagescraper import PageScraper

# Configuração do logging
logger = logging.getLogger(__name__)


class MetroScraper(PageScraper):
    """
    Classe específica para raspar artigos do portal Metrópoles...
    """

    def __init__(self):
        super().__init__()

    def is_article_page(self, html_data: BeautifulSoup) -> bool:
        """
        Verifica (baseado na sua análise) se a página é um artigo real
        procurando pela meta tag 'article:section'.
        """
        try:
            # Procura pela "chave de ouro" que você encontrou
            meta_tag = html_data.find("meta", property="article:section")

            if meta_tag:
                logger.debug(
                    "Meta tag 'article:section' encontrada. Esta é uma página de artigo."
                )
                return True
            else:
                logger.debug(
                    "Meta tag 'article:section' NÃO encontrada. Esta é uma página de seção."
                )
                return False
        except Exception as e:
            logger.warning(
                f"Erro ao checar 'is_article_page': {e}. Assumindo que não é um artigo."
            )
            return False

    def _extract_title(self, html_data: BeautifulSoup) -> str:
        """Extrai o título e subtítulo, com fallbacks."""
        full_title = ""

        # --- TENTATIVA 1: Layout Original (HeaderNoticiaWrapper) ---
        try:
            # Procura a div que você identificou nas primeiras imagens
            title_container = html_data.find(
                "div", class_=lambda c: c and "HeaderNoticiaWrapper__Categoria" in c
            )
            if title_container:
                title_tag = title_container.find("h1")
                if title_tag:
                    full_title = title_tag.get_text(strip=True)

                subtitle_tag = title_container.find("h2")
                if subtitle_tag:
                    subtitle_text = subtitle_tag.get_text(strip=True)
                    if full_title and subtitle_text:
                        full_title = f"{full_title} - {subtitle_text}"
                    elif subtitle_text:
                        full_title = subtitle_text

                if full_title:
                    logger.debug("Título encontrado via HeaderNoticiaWrapper.")
                    return full_title

        except Exception as e:
            logger.warning(f"Erro ao tentar Tentativa 1 (HeaderNoticiaWrapper): {e}")

        logger.debug("Tentativa 1 falhou. Tentando fallbacks para o título.")

        # --- TENTATIVA 2: Meta Tag 'og:title' (Muito confiável) ---
        try:
            # Quase todas as páginas (mesmo as de gastronomia) terão isso
            meta_title = html_data.find("meta", property="og:title")
            if meta_title and meta_title.get("content"):
                full_title = meta_title["content"].strip()
                logger.debug("Título encontrado via meta 'og:title'.")
                return full_title
        except Exception as e:
            logger.warning(f"Erro ao tentar Tentativa 2 (og:title): {e}")

        # --- TENTATIVA 3: Tag <title> (Menos ideal, mas funciona) ---
        try:
            title_tag = html_data.find("title")
            if title_tag:
                full_title = title_tag.get_text(strip=True)
                # Otimização: remover o " | Metrópoles" no final
                if "|" in full_title:
                    full_title = full_title.split("|")[0].strip()

                logger.debug("Título encontrado via tag <title>.")
                return full_title
        except Exception as e:
            logger.warning(f"Erro ao tentar Tentativa 3 (<title>): {e}")

        logger.debug("Nenhuma tentativa de extração de título funcionou.")
        return ""  # Retorna vazio se tudo falhar

    def _extract_authors(self, html_data: BeautifulSoup) -> str:
        """Extrai um ou mais autores, com fallbacks."""

        # --- TENTATIVA 1: Layout Original (HeaderNoticiaWrapper) ---
        try:
            author_container = html_data.find(
                "div", class_=lambda c: c and "HeaderNoticiaWrapper__Autor" in c
            )
            if author_container:
                author_tags = author_container.find_all("a")
                if not author_tags:
                    author_text = author_container.get_text(strip=True)
                    if author_text:
                        logger.debug(
                            "Autor encontrado via HeaderNoticiaWrapper (sem <a>)."
                        )
                        return author_text

                authors = [a.get_text(strip=True) for a in author_tags]
                if authors:
                    logger.debug("Autor encontrado via HeaderNoticiaWrapper (com <a>).")
                    return ", ".join(authors)
        except Exception as e:
            logger.warning(f"Erro ao tentar Autor (Tentativa 1): {e}")

        # --- TENTATIVA 2: Meta Tag 'author' (Comum) ---
        try:
            meta_author = html_data.find("meta", attrs={"name": "author"})
            if meta_author and meta_author.get("content"):
                logger.debug("Autor encontrado via meta 'author'.")
                return meta_author["content"].strip()
        except Exception as e:
            logger.warning(f"Erro ao tentar Autor (Tentativa 2): {e}")

        # --- TENTATIVA 3: Classe "author" ou "autor" (Genérico) ---
        try:
            # Tenta encontrar algo com 'byline' ou 'author'
            author_tag = html_data.find(
                class_=lambda c: c
                and (
                    "author" in c.lower()
                    or "byline" in c.lower()
                    or "autor" in c.lower()
                )
            )
            if author_tag:
                author_text = author_tag.get_text(strip=True)
                # Limpeza comum (ex: "Por Redação")
                if author_text.lower().startswith("por "):
                    author_text = author_text[4:].strip()
                logger.debug("Autor encontrado via classe genérica 'author'/'byline'.")
                return author_text
        except Exception as e:
            logger.warning(f"Erro ao tentar Autor (Tentativa 3): {e}")

        logger.debug("Nenhum autor encontrado.")
        return ""  # Retorna "" se não achar

    def _extract_body(self, html_data: BeautifulSoup) -> str:
        """Extrai o corpo da notícia, com fallbacks."""

        body_container = None

        # --- TENTATIVA 1: Layout Original (ConteudoNoticiaWrapper) ---
        try:
            body_container = html_data.find(
                "div", class_=lambda c: c and "ConteudoNoticiaWrapper__Artigo-sc" in c
            )
            if body_container:
                logger.debug("Corpo encontrado via ConteudoNoticiaWrapper.")
            else:
                logger.debug("Tentativa 1 (ConteudoNoticiaWrapper) falhou.")
        except Exception as e:
            logger.warning(f"Erro ao tentar Corpo (Tentativa 1): {e}")

        # --- TENTATIVA 2: Tag <article> (Semântico) ---
        if not body_container:
            try:
                body_container = html_data.find("article")
                if body_container:
                    logger.debug("Corpo encontrado via tag <article>.")
                else:
                    logger.debug("Tentativa 2 (<article>) falhou.")
            except Exception as e:
                logger.warning(f"Erro ao tentar Corpo (Tentativa 2): {e}")

        # --- TENTATIVA 3: Classe "materia" ou "content" (Genérico) ---
        if not body_container:
            try:
                # Procura por classes comuns de conteúdo de artigo
                body_container = html_data.find(
                    "div",
                    class_=lambda c: c
                    and (
                        "materia" in c.lower()
                        or "article__body" in c.lower()
                        or "content" in c.lower()
                        or "conteudo" in c.lower()
                    ),
                )
                if body_container:
                    logger.debug(
                        "Corpo encontrado via classe genérica 'materia'/'content'."
                    )
                else:
                    logger.debug("Tentativa 3 (classe genérica) falhou.")
            except Exception as e:
                logger.warning(f"Erro ao tentar Corpo (Tentativa 3): {e}")

        # Se nenhuma tentativa encontrou um container, retorna ""
        if not body_container:
            logger.debug("Nenhum container de corpo encontrado.")
            return ""

        # --- Extração dos Parágrafos ---
        # Agora que temos um container, extraímos os <p>
        try:
            paragraphs = body_container.find_all("p")
            if not paragraphs:
                logger.debug("Container do corpo encontrado, mas sem tags <p>.")
                return body_container.get_text(strip=True)  # Fallback

            content_blocks = [
                p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)
            ]
            return "\n\n".join(content_blocks)

        except Exception as e:
            logger.warning(f"Erro ao extrair parágrafos do container: {e}")
            return ""

    def scrape_article(self, url: str, html_data: BeautifulSoup) -> Optional[Article]:
        """
        Implementação do método abstrato para raspar um artigo do Metrópoles.
        """

        # Extração dos componentes
        title = self._extract_title(html_data)
        author = self._extract_authors(html_data)
        content = self._extract_body(html_data)

        # Validação (elementos críticos)
        if not title:
            logger.error(f"Elemento crítico faltando: title (URL: {url})")
            return None

        if not content:
            logger.error(f"Elemento crítico faltando: body (URL: {url})")
            return None

        return Article(
            title=title,
            author=author,  # Pode ser "" se não encontrado
            url=url,
            content=content,
        )
