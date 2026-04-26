import json
import os

CAMINHO_ARQUIVO = "config.json"

def carregar_config():
    """
    Tenta ler o arquivo de configuração local.
    Retorna um dicionário com os dados ou None se for a primeira vez.
    """
    if not os.path.exists(CAMINHO_ARQUIVO):
        return None

    with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)

def salvar_config(dados_config):
    """
    Salva e atualiza o arquivo de configuração no disco.
    """
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(dados_config, arquivo, indent=4)
