import requests
from bs4 import BeautifulSoup

url = 'https://www.metropoles.com/esportes/rayssa-leal-e-vice-campea-da-etapa-de-las-vegas-da-sls'
# url = 'https://www.metropoles.com/sao-paulo/pm-em-moto-tem-cabeca-arrancada-apos-atropelar-e-matar-pedestre-em-sp'
# url = 'https://www.metropoles.com/mundo/o-que-trump-falou-sobre-bolsonaro-em-encontro-com-lula-na-malasia'

page = requests.get(url)

page_data = BeautifulSoup(page.text, 'html.parser')

news_date = page_data.find_all('time', class_='HeaderNoticiaWrapper__DataPublicacao-sc-4exe2y-3 dAMWSS')[1].text

news_author = page_data.find('a', rel='author').text

news_title = page_data.find('h1', class_='Text__TextBase-sc-1d75gww-0 TcJvw').text

news_content_data = page_data.find('div', class_='ConteudoNoticiaWrapper__Artigo-sc-19fsm27-1 dbCenN')
useless = news_content_data.find_all('div')
for div in useless:
    div.decompose()
news_content = news_content_data.text

print(f"Data de publicação: {news_date}")
print(f"Autor: {news_author}")
print(f"Título: {news_title}")
print(f"Conteúdo: {news_content}")