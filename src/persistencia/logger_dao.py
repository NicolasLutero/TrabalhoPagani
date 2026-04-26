import logging
import os
from datetime import datetime

ARQUIVO_LOG = "mensageria.log"

def configurar_logger():
    """
    Se o arquivo não existir, ele cria. Se existir, ele anexa no final.
    """
    logging.basicConfig(
         filename=ARQUIVO_LOG,
         level=logging.INFO,
         format="%(asctime)s - [%(levelname)s] - %(message)s",
         datefmt='%Y-%m-%d %H:%M:%S',
         encoding="utf-8"
    )

#Chama a configuração assim que este arquivo for importado
configurar_logger()

def registrar_evento(mensagem, tipo="info"):
    """
    Função que a mensageria vai chamar para anotar o que aconteceu
    """

    if tipo.lower() == "info":
        logging.info(mensagem)
    elif tipo.lower() == "aviso":
        logging.warning(mensagem)
    elif tipo.lower() == "erro":
        logging.error(mensagem)
    else:
        logging.info(mensagem)

