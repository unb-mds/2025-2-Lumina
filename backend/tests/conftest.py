import os
import sys

# 1. Define uma chave falsa ANTES de importar o main
# Isso engana a verificação do main.py e permite que o teste inicie
os.environ["GOOGLE_API_KEY"] = "fake_key_para_testes_automatizados"

# 2. Adiciona o diretório raiz ao path (ajuda a evitar erros de importação)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))