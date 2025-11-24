import pytest
import json
from unittest.mock import MagicMock, call, mock_open
from app.webcrawler.Metropoles.metrowebcrawler import MetropolesCrawler
from app.models.article import Article

@pytest.fixture
def mock_dependencies(mocker):
    """
    Mocka todas as dependências externas da classe.
    """
    mocker.patch("app.webcrawler.Metropoles.metrowebcrawler.Downloader")
    mocker.patch("app.webcrawler.Metropoles.metrowebcrawler.MetroScraper")
    mocker.patch("app.webcrawler.Metropoles.metrowebcrawler.MetroLinkExtractor")
    mocker.patch("app.webcrawler.Metropoles.metrowebcrawler.ArticleDB")
    
    mocker.patch("builtins.open", mock_open())
    mocker.patch("os.path.exists", return_value=False)
    mocker.patch("os.remove")

@pytest.fixture
def crawler(mock_dependencies):
    return MetropolesCrawler()

class TestMetropolesCrawler:

    # --- Testes de Inicialização e Estado ---

    def test_initialization_seeds(self, crawler):
        assert not crawler.Urls_to_visit.empty()
        urls_in_queue = list(crawler.Urls_to_visit.queue)
        assert any("politica" in url for url in urls_in_queue)

    def test_save_state(self, crawler, mocker):
        crawler.visited_urls.add("http://visited.com")
        crawler.Urls_to_visit.queue.clear()
        crawler.Urls_to_visit.put("http://next.com")

        mock_file = mocker.patch("builtins.open", mock_open())
        crawler.save_state()

        handle = mock_file()
        written_content = "".join(call.args[0] for call in handle.write.mock_calls)
        assert "http://visited.com" in written_content
        assert "http://next.com" in written_content

    def test_load_state_success(self, crawler, mocker):
        fake_state = json.dumps({
            "visited_urls": ["http://old-visited.com"],
            "urls_to_visit": ["http://pending.com"]
        })
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("builtins.open", mock_open(read_data=fake_state))

        crawler.load_state()

        assert "http://old-visited.com" in crawler.visited_urls
        queue_list = list(crawler.Urls_to_visit.queue)
        assert "http://pending.com" in queue_list

    def test_load_state_exception(self, crawler, mocker):
        """
        NOVO: Simula erro ao carregar o estado (ex: JSON inválido ou erro de disco).
        Cobre as linhas 89-90.
        """
        mocker.patch("os.path.exists", return_value=True)
        # Força erro no json.load ou open
        mocker.patch("builtins.open", side_effect=Exception("Arquivo corrompido"))
        
        crawler.load_state() # Não deve quebrar, deve apenas logar o erro

    def test_save_state_exception(self, crawler, mocker):
        mocker.patch("builtins.open", side_effect=Exception("Disk full"))
        crawler.save_state() # Não deve quebrar

    # --- Testes do Loop Principal (Crawl) ---

    def test_crawl_skip_visited(self, crawler):
        url = "http://metropoles.com/politica/artigo-velho"
        crawler.visited_urls.add(url)
        crawler.Urls_to_visit.queue.clear()
        crawler.Urls_to_visit.put(url)

        crawler.crawl(max_pages=1)
        crawler.downloader.fetch.assert_not_called()

    def test_crawl_download_fail(self, crawler):
        url = "http://metropoles.com/politica/artigo-quebrado"
        crawler.Urls_to_visit.queue.clear()
        crawler.Urls_to_visit.put(url)
        crawler.downloader.fetch.return_value = None # Simula falha

        crawler.crawl(max_pages=1)

        crawler.scraper.is_article_page.assert_not_called()
        assert url not in crawler.visited_urls

    def test_crawl_scrape_fail(self, crawler):
        """
        NOVO: Simula falha no scraper (retorna None mesmo sendo página de artigo).
        Cobre a linha 132 (else do if article).
        """
        url = "http://metropoles.com/politica/artigo-bugado"
        crawler.Urls_to_visit.queue.clear()
        crawler.Urls_to_visit.put(url)

        crawler.downloader.fetch.return_value = "<html></html>"
        crawler.scraper.is_article_page.return_value = True
        
        # O Scraper falha em extrair os dados
        crawler.scraper.scrape_article.return_value = None

        crawler.crawl(max_pages=1)

        # Não salva nada
        crawler.database.save_article.assert_not_called()
        # Mas deve ter visitado
        assert url in crawler.visited_urls

    def test_crawl_not_article_page(self, crawler):
        url = "http://metropoles.com/politica/"
        crawler.Urls_to_visit.queue.clear()
        crawler.Urls_to_visit.put(url)

        crawler.downloader.fetch.return_value = "<html></html>"
        crawler.scraper.is_article_page.return_value = False
        crawler.link_extractor.extract.return_value = {"http://metropoles.com/politica/novo"}

        crawler.crawl(max_pages=1)

        crawler.database.save_article.assert_not_called()
        crawler.link_extractor.extract.assert_called()
        assert "http://metropoles.com/politica/novo" in crawler.visited_urls

    def test_crawl_article_wrong_category(self, crawler):
        url = "http://metropoles.com/entretenimento/bbb/fofoca"
        crawler.Urls_to_visit.queue.clear()
        crawler.Urls_to_visit.put(url)

        crawler.downloader.fetch.return_value = "<html></html>"
        crawler.scraper.is_article_page.return_value = True

        crawler.crawl(max_pages=1)
        crawler.database.save_article.assert_not_called()

    def test_crawl_success_save_article(self, crawler):
        url = "http://metropoles.com/politica/noticia-boa"
        crawler.Urls_to_visit.queue.clear()
        crawler.Urls_to_visit.put(url)

        crawler.downloader.fetch.return_value = "<html>Conteúdo</html>"
        crawler.scraper.is_article_page.return_value = True
        
        fake_article = Article(title="Título", author="Autor", url=url, content="Texto")
        crawler.scraper.scrape_article.return_value = fake_article
        crawler.link_extractor.extract.return_value = set()

        crawler.crawl(max_pages=1)

        crawler.scraper.scrape_article.assert_called_with(url, "<html>Conteúdo</html>")
        crawler.database.save_article.assert_called_with(fake_article)
        assert url in crawler.visited_urls

    def test_crawl_state_saving_interval(self, crawler, mocker):
        mock_save = mocker.patch.object(crawler, 'save_state')
        
        crawler.Urls_to_visit.queue.clear()
        for i in range(25):
            crawler.Urls_to_visit.put(f"http://metropoles.com/politica/{i}")

        crawler.downloader.fetch.return_value = "<html></html>"
        crawler.scraper.is_article_page.return_value = False
        crawler.link_extractor.extract.return_value = set()

        crawler.crawl(max_pages=25)

        assert mock_save.call_count >= 2