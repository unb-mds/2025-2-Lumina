import pytest
import json
import os
from unittest.mock import MagicMock, call, mock_open
from app.webcrawler.G1.g1webcrawler import WebCrawler
from app.models.article import Article

@pytest.fixture
def mock_dependencies(mocker):
    """
    Mocka todas as dependências externas da classe.
    """
    mocker.patch("app.webcrawler.G1.g1webcrawler.Downloader")
    mocker.patch("app.webcrawler.G1.g1webcrawler.G1Scraper")
    mocker.patch("app.webcrawler.G1.g1webcrawler.G1LinkExtractor")
    mocker.patch("app.webcrawler.G1.g1webcrawler.ArticleDB")
    
    # Mock de sistema de arquivos
    mocker.patch("builtins.open", mock_open())
    mocker.patch("os.path.exists", return_value=False)
    mocker.patch("os.remove")

@pytest.fixture
def crawler(mock_dependencies):
    return WebCrawler()

class TestG1WebCrawler:

    # --- Testes de Inicialização e Estado ---

    def test_initialization_seeds(self, crawler):
        assert not crawler.Urls_to_visit.empty()
        urls = list(crawler.Urls_to_visit.queue)
        assert "https://g1.globo.com/politica" in urls

    def test_save_state(self, crawler, mocker):
        crawler.visited_urls.add("http://g1.com/visitado")
        mock_file = mocker.patch("builtins.open", mock_open())
        crawler.save_state()
        handle = mock_file()
        content = "".join(call.args[0] for call in handle.write.mock_calls)
        assert "http://g1.com/visitado" in content

    def test_save_state_exception(self, crawler, mocker):
        mocker.patch("builtins.open", side_effect=Exception("Erro de disco"))
        crawler.save_state()

    def test_load_state_success(self, crawler, mocker):
        data = json.dumps({
            "visited_urls": ["http://old.com"],
            "urls_to_visit": ["http://new.com"]
        })
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("builtins.open", mock_open(read_data=data))
        crawler.load_state()
        assert "http://old.com" in crawler.visited_urls
        assert "http://new.com" in list(crawler.Urls_to_visit.queue)

    def test_load_state_create_new(self, crawler, mocker):
        mocker.patch("os.path.exists", return_value=False)
        mock_file = mocker.patch("builtins.open", mock_open())
        crawler.load_state()
        mock_file.assert_called_with("crawler_state.json", "w", encoding="utf-8")

    def test_load_state_exception(self, crawler, mocker):
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("builtins.open", side_effect=Exception("Corrompido"))
        crawler.load_state()

    def test_reset_state(self, crawler, mocker):
        mocker.patch("os.path.exists", return_value=True)
        mock_remove = mocker.patch("os.remove")
        crawler.reset_state()
        mock_remove.assert_called_with("crawler_state.json")

    # --- Testes do Loop Principal (Crawl) ---

    def test_crawl_skip_visited(self, crawler):
        url = "http://g1.com/ja-fui"
        crawler.visited_urls.add(url)
        crawler.Urls_to_visit.queue.clear()
        crawler.Urls_to_visit.put(url)
        crawler.crawl(max_pages=1)
        crawler.downloader.fetch.assert_not_called()

    def test_crawl_log_skipped_visited(self, crawler, capsys):
        crawler.Urls_to_visit.queue.clear()
        for i in range(50):
            url = f"http://g1.com/visited/{i}"
            crawler.visited_urls.add(url)
            crawler.Urls_to_visit.put(url)
        crawler.crawl(max_pages=50)
        captured = capsys.readouterr()
        assert "50 URLs já visitados pulados até agora" in captured.out

    def test_crawl_download_fail(self, crawler):
        url = "http://g1.com/fail"
        crawler.Urls_to_visit.queue.clear()
        crawler.Urls_to_visit.put(url)
        crawler.downloader.fetch.return_value = None
        crawler.crawl(max_pages=1)
        crawler.scraper.scrape_article.assert_not_called()

    def test_crawl_success_article(self, crawler):
        url = "https://g1.globo.com/politica/noticia/2023/fake.ghtml"
        crawler.Urls_to_visit.queue.clear()
        crawler.Urls_to_visit.put(url)
        crawler.downloader.fetch.return_value = "<html>OK</html>"
        fake_article = Article(title="Manchete", author="Repórter", url=url, content="Texto")
        crawler.scraper.scrape_article.return_value = fake_article
        crawler.link_extractor.extract.return_value = set()
        crawler.crawl(max_pages=1)
        crawler.database.save_article.assert_called_with(fake_article)
        assert url in crawler.visited_urls

    def test_crawl_scrape_fail_returns_none(self, crawler):
        url = "https://g1.globo.com/politica/noticia/2023/vazio.ghtml"
        crawler.Urls_to_visit.queue.clear()
        crawler.Urls_to_visit.put(url)
        crawler.downloader.fetch.return_value = "<html>Vazio</html>"
        crawler.scraper.scrape_article.return_value = None
        crawler.crawl(max_pages=1)
        crawler.database.save_article.assert_not_called()
        assert url in crawler.visited_urls

    # --- Testes Específicos da Lógica de Filtragem G1 ---

    def test_crawl_skip_wrong_category(self, crawler, capsys):
        url = "https://g1.globo.com/pop-arte/noticia/filme.ghtml"
        crawler.Urls_to_visit.queue.clear()
        crawler.Urls_to_visit.put(url)
        crawler.downloader.fetch.return_value = "<html></html>"
        crawler.link_extractor.extract.return_value = set()
        crawler.crawl(max_pages=1)
        crawler.database.save_article.assert_not_called()
        captured = capsys.readouterr()
        assert "Artigo de outra categoria pulado" in captured.out

    def test_crawl_skip_not_article_structure(self, crawler):
        url = "https://g1.globo.com/politica/video-explicativo.ghtml"
        crawler.Urls_to_visit.queue.clear()
        crawler.Urls_to_visit.put(url)
        crawler.downloader.fetch.return_value = "<html></html>"
        crawler.link_extractor.extract.return_value = set()
        crawler.crawl(max_pages=1)
        crawler.database.save_article.assert_not_called()
    
    def test_crawl_skip_generic_page(self, crawler):
        url = "https://g1.globo.com/politica/"
        crawler.Urls_to_visit.queue.clear()
        crawler.Urls_to_visit.put(url)
        crawler.downloader.fetch.return_value = "<html></html>"
        crawler.link_extractor.extract.return_value = set()
        crawler.crawl(max_pages=1)
        crawler.database.save_article.assert_not_called()
        crawler.link_extractor.extract.assert_called()

    def test_crawl_checkpoint_logs(self, crawler, capsys):
        """Simula 101 URLs processadas (não-artigos) para log de checkpoint."""
        crawler.Urls_to_visit.queue.clear()
        for i in range(101):
            crawler.Urls_to_visit.put(f"https://g1.globo.com/politica/secao/{i}")
        crawler.downloader.fetch.return_value = "<html></html>"
        crawler.link_extractor.extract.return_value = set()
        crawler.crawl(max_pages=200)
        captured = capsys.readouterr()
        assert "[CHECKPOINT] Total URLs processados: 100" in captured.out

    def test_crawl_log_ten_articles(self, crawler, capsys):
        """
        NOVO: Simula 10 artigos extraídos com sucesso para disparar o log de progresso.
        Cobre o bloco 'if pages_crawled % 10 == 0'.
        """
        crawler.Urls_to_visit.queue.clear()
        for i in range(10):
            crawler.Urls_to_visit.put(f"https://g1.globo.com/politica/noticia/2023/artigo{i}.ghtml")

        crawler.downloader.fetch.return_value = "<html>OK</html>"
        crawler.link_extractor.extract.return_value = set()
        crawler.scraper.scrape_article.return_value = MagicMock(title="Artigo Teste")

        crawler.crawl(max_pages=10)

        captured = capsys.readouterr()
        # Verifica se o log específico apareceu
        assert "10/10 artigos" in captured.out

    def test_crawl_adds_links_to_queue(self, crawler):
        url = "https://g1.globo.com/politica/"
        crawler.Urls_to_visit.queue.clear()
        crawler.Urls_to_visit.put(url)
        crawler.downloader.fetch.return_value = "<html></html>"
        valid_link = "https://g1.globo.com/politica/noticia/nova.ghtml"
        invalid_link = "https://g1.globo.com/esporte/"
        
        crawler.link_extractor.extract.side_effect = [{valid_link, invalid_link}, set()]
        crawler.scraper.scrape_article.return_value = MagicMock(title="Novo")
        
        crawler.crawl(max_pages=1)
        assert valid_link in crawler.visited_urls
        assert invalid_link not in crawler.visited_urls

    def test_crawl_state_saving_interval(self, crawler, mocker):
        """
        Verifica salvamento periódico.
        IMPORTANTE: fetch retorna HTML para não cair no 'continue' e pular o save.
        """
        mock_save = mocker.patch.object(crawler, 'save_state')
        crawler.Urls_to_visit.queue.clear()
        for i in range(55):
            crawler.Urls_to_visit.put(f"https://g1.globo.com/politica/{i}")

        # Deve retornar HTML (mesmo que vazio) para chegar ao final do loop
        crawler.downloader.fetch.return_value = "<html></html>"
        crawler.link_extractor.extract.return_value = set()

        crawler.crawl(max_pages=55)
        # Pelo menos 1 save intermediário + 1 final
        assert mock_save.call_count >= 2