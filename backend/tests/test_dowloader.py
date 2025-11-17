import time
from unittest.mock import Mock

import pytest
import requests
from app.webcrawler.dowloader import Downloader
from bs4 import BeautifulSoup
from pytest_mock import MockerFixture

# --- Fixture de Teste (Ambiente Controlado) ---


@pytest.fixture
def downloader():
    """Retorna uma instância do Downloader com 3 retries para os testes."""
    # Usamos max_tries=3 para garantir que os testes de retry funcionem
    return Downloader(max_tries=3)


@pytest.fixture
def mock_requests_get(mocker: MockerFixture):
    """
    Fixture principal que intercepta (mocka) o 'requests.get'.
    Isso nos dá controle total sobre o que a rede "responde".
    """
    # 'mocker.patch' substitui o 'requests.get' real por um simulacro
    return mocker.patch("requests.get")


@pytest.fixture
def mock_time_sleep(mocker: MockerFixture):
    """
    Mocka o 'time.sleep' para que os testes de retry
    executem instantaneamente, sem pausas reais.
    """
    return mocker.patch("time.sleep")


# --- Testes ---


def test_fetch_success_caminho_feliz(
    downloader: Downloader, mock_requests_get: MockerFixture
):
    """
    Testa o "caminho feliz" (Happy Path).
    Simula uma resposta 200 OK da internet na primeira tentativa.
    """
    # 1. Configuração do Mock
    # Simula uma resposta de sucesso
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.text = "<html><h1>Título</h1></html>"
    # Configura o raise_for_status() para não fazer nada (sucesso)
    mock_response.raise_for_status.return_value = None

    # 2. Execução
    result = downloader.fetch("http://sucesso.com")

    # 3. Verificação
    assert isinstance(result, BeautifulSoup)
    assert result.find("h1").text == "Título"
    # Garante que foi chamado apenas 1 vez (não tentou retries)
    mock_requests_get.assert_called_once_with(
        "http://sucesso.com", headers=downloader.headers, timeout=10
    )


def test_fetch_timeout_com_retry_e_sucesso(
    downloader: Downloader,
    mock_requests_get: MockerFixture,
    mock_time_sleep: MockerFixture,
):
    """
    Testa o 'except requests.Timeout'.
    Simula um Timeout na primeira tentativa, e um sucesso na segunda.
    """
    # 1. Configuração do Mock
    # Simula falha de Timeout na primeira chamada, e sucesso na segunda
    mock_requests_get.side_effect = [
        requests.Timeout("Simulação de Timeout"),  # 1ª chamada (falha)
        Mock(  # 2ª chamada (sucesso)
            status_code=200,
            text="<html><h1>Sucesso</h1></html>",
            raise_for_status=Mock(return_value=None),
        ),
    ]

    # 2. Execução
    result = downloader.fetch("http://timeout.com")

    # 3. Verificação
    assert result is not None
    assert result.find("h1").text == "Sucesso"
    # Garante que o requests.get foi chamado 2 vezes
    assert mock_requests_get.call_count == 2
    # Garante que ele esperou (chamou o time.sleep)
    mock_time_sleep.assert_called_once_with(1)  # 2**0 = 1 segundo


def test_fetch_http_error_404_sem_retry(
    downloader: Downloader,
    mock_requests_get: MockerFixture,
    mock_time_sleep: MockerFixture,
):
    """
    Testa o 'except requests.HTTPError' para erros 4xx (ex: 404 Not Found).
    O código deve parar (break) e NÃO tentar retries.
    """
    # 1. Configuração do Mock
    # Cria uma resposta de erro 404
    mock_response_404 = Mock(status_code=404)
    # Cria a exceção HTTPError
    http_error = requests.HTTPError(response=mock_response_404)
    # Diz ao mock para levantar essa exceção
    mock_requests_get.side_effect = http_error

    # 2. Execução
    result = downloader.fetch("http://notfound404.com")

    # 3. Verificação
    assert result is None  # Deve falhar e retornar None
    # Garante que foi chamado apenas 1 vez (desistiu no 'break')
    mock_requests_get.assert_called_once()
    # Garante que NÃO esperou (não chamou time.sleep)
    mock_time_sleep.assert_not_called()


def test_fetch_http_error_503_com_retry_e_falha(
    downloader: Downloader,
    mock_requests_get: MockerFixture,
    mock_time_sleep: MockerFixture,
    mocker: MockerFixture,
):
    """
    Testa o 'except requests.HTTPError' para erros 5xx (ex: 503 Server Error).
    O código deve tentar retries (pois não é um erro 4xx) e falhar no final.
    """
    # 1. Configuração do Mock
    mock_response_503 = Mock(status_code=503)
    http_error = requests.HTTPError(response=mock_response_503)
    # Simula o erro 503 em TODAS as 3 tentativas
    mock_requests_get.side_effect = http_error

    # 2. Execução
    result = downloader.fetch("http://servererror503.com")

    # 3. Verificação
    assert result is None  # Deve falhar e retornar None
    # Garante que tentou 3 vezes (max_tries)
    assert mock_requests_get.call_count == 3
    # Garante que tentou 2 retries (chamou sleep 2 vezes)
    assert mock_time_sleep.call_count == 2
    # Verifica as pausas com backoff exponencial (2**0=1s, 2**1=2s)
    mock_time_sleep.assert_has_calls([mocker.call(1), mocker.call(2)])


def test_fetch_general_exception_com_retry_e_falha(
    downloader: Downloader,
    mock_requests_get: MockerFixture,
    mock_time_sleep: MockerFixture,
):
    """
    Testa o 'except requests.RequestException' genérico.
    Deve tentar retries e falhar após 3 tentativas.
    """
    # 1. Configuração do Mock
    # Simula uma exceção genérica em TODAS as 3 tentativas
    mock_requests_get.side_effect = requests.RequestException("Erro genérico")

    # 2. Execução
    result = downloader.fetch("http://genericerror.com")

    # 3. Verificação
    assert result is None  # Deve falhar e retornar None
    # Garante que tentou 3 vezes (max_tries)
    assert mock_requests_get.call_count == 3
    # Garante que tentou 2 retries (chamou sleep 2 vezes)
    assert mock_time_sleep.call_count == 2
