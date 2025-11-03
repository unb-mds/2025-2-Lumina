import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, Any
import json

# URL 
URL_ALVO = "https://g1.globo.com/rj/rio-de-janeiro/noticia/2025/10/27/tiroteio-em-costa-barros.ghtml"
NOME_ARQUIVO_JSON = "g1-dados.json"


def scrapear_noticia_g1(url: str):
    # Removendo type hints para evitar o NameError
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a URL {url}: {e}")
        return {}

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # === ETAPA DE LIMPEZA: REMOÇÃO DE BLOCOS INDESEJADOS (Newsletter/Propaganda) ===
    # 1. Remove o contêiner da Newsletter (classe que você identificou)
    newsletter_elem = soup.find('div', class_='newsletter-g1_container')
    if newsletter_elem:
        newsletter_elem.extract()
        
    # 2. Remove o bloco "MAIS LIDAS" ou outros widgets similares (geralmente abaixo do corpo)
    mais_lidas_elem = soup.find('div', class_='mc-column entities')
    if mais_lidas_elem:
         mais_lidas_elem.extract()

    # (1) Título
    titulo_elem = soup.select_one('.content-head__title[itemprop="headline"]')
    titulo = titulo_elem.text.strip() if titulo_elem else "Título não encontrado"

    # (2) Subtítulo, Autor e Data
    subtitulo_elem = soup.select_one('.content-head__subtitle[itemprop="alternativeHeadline"]')
    subtitulo = subtitulo_elem.text.strip() if subtitulo_elem else ""
    
    # Lógica de Autor
    autor = "Autor não encontrado"
    autor_signature_elem = soup.select_one('.top_signature_text_author-name')
    if autor_signature_elem:
        autor_texto = autor_signature_elem.text.replace('Por ', '').strip()
        if autor_texto:
            autor = autor_texto
    
    if autor == "Autor não encontrado":
        autor_elem = soup.select_one('.content-publication-data__from')
        if autor_elem:
            autor = autor_elem.get('title', '').strip()
            
    if not autor or autor == "{}":
        autor = "Autor não encontrado"

    # Data de Publicação (Limpeza DD/MM/AAAA)
    data_elem = soup.select_one('.content-publication-data__updated')
    data_completa = data_elem.text.strip() if data_elem else ""
    
    data_limpa = data_completa
    match = re.search(r'(\d{2}\/\d{2}\/\d{4})', data_completa)
    if match:
        data_limpa = match.group(1)
    
    # (3) Artigo Completo
    paragrafos = []
    
    # Lógica de busca de container (Notícia padrão vs. Blog)
    corpo_container = soup.find('div', class_='mc-article-body')
    if not corpo_container:
        corpo_container = soup.find('div', class_='post-body')
    if not corpo_container:
         corpo_container = soup.find('div', class_='content-text')


    if corpo_container:
        # Busca tags p, blockquote, ul e li para capturar listas (como o WhatsApp CTA)
        elementos_texto = corpo_container.find_all(['p', 'blockquote', 'ul', 'li'])
        
        for elem in elementos_texto:
            texto_limpo = elem.text.strip()
            
            # Filtro de exclusão por Palavra-Chave
            excluir = False
            
            if any(keyword in texto_limpo for keyword in [
                'Leia também:', 
                'O blog', 
                'Clique aqui para seguir o canal', 
                'WhatsApp', 
                'Telegram', 
                'crie uma conta Globo gratuita', 
                'Para se inscrever',
                'De segunda a sábado, as notícias que você não pode perder diretamente no seu e-mail.'
            ]):
                excluir = True

            if texto_limpo and not excluir: 
                paragrafos.append(texto_limpo)

    artigo_completo = "\n\n".join(paragrafos)

    # Estruturação (Output)
    dados_noticia = {
        "url_fonte": url,
        "titulo": titulo,
        "subtitulo": subtitulo,
        "autor": autor,
        "data_publicacao": data_limpa,
        "artigo_completo": artigo_completo
    }
    
    return dados_noticia


def salvar_json(dados: Dict[str, Any], nome_arquivo: str):
    
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        # Salva o dicionário, formatado (indent=4), preservando acentos
        json.dump(dados, f, indent=4, ensure_ascii=False)
    
    print(f"\n[SUCESSO] Dados salvos em '{nome_arquivo}'.")

if __name__ == "__main__":
    
    print(f"--- Iniciando Scraping da URL: {URL_ALVO} ---")
    
    dados_coletados = scrapear_noticia_g1(URL_ALVO)
    
    if dados_coletados:
        
        print("\n--- Resultados Extraídos ---")
        print(f"Título: {dados_coletados.get('titulo')}")
        print(f"Autor: {dados_coletados.get('autor')}")
        print(f"Data: {dados_coletados.get('data_publicacao')}")
        # Imprime uma amostra do início do artigo
        corpo_amostra = dados_coletados.get('artigo_completo')
        if corpo_amostra:
            print(f"Artigo (primeiros 100 caracteres): {corpo_amostra[:100].replace('\n', ' ')}...")
            # Atualmente ele impreme os primeiros 100 caracteres do artigo completo, porém as informações completas estão no arquivo JSON.
        
        salvar_json(dados_coletados, NOME_ARQUIVO_JSON)
        
    else:
        print("\nFalha ao extrair dados. O arquivo JSON não foi criado.")