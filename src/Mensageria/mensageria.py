from cryptography.hazmat.primitives import serialization
import sys

from src import persistencia as pers, criptografia as crip, rede
from time import sleep


class Mensageria:
    _instancia = None

    def __new__(cls, *args, **kwargs):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._config = None
            cls._instancia._peer = rede.Peer(cls._instancia)
            cls._instancia._receive_hooks = []
        return cls._instancia

    def start(self):
        pers.registrar_evento("Iniciando Mensageria", "info")
        self._load_config()
        self._peer.iniciar()

    def _load_config(self):
        pers.registrar_evento("Carregando Config", "info")
        self._config = pers.carregar_config()
        if self._config is None:
            pers.registrar_evento("Config não encontrado", "info")
            self._create_config()
        else:
            puk, prk = self._config["chave publica"], self._config["chave privada"]
            puk = crip.desserializar_chave_publica_rsa(puk)
            prk = crip.desserializar_chave_privada_rsa(prk)
            self._config["chave publica"], self._config["chave privada"] = puk, prk

    def _create_config(self):
        pers.registrar_evento("Criando Config", "info")
        chave_privada, chave_publica = crip.gerar_par_chaves_rsa()
        self._config = {
            "chave publica": chave_publica,
            "chave privada": chave_privada
        }
        self._save_config()

    def _save_config(self):
        pers.registrar_evento("Salvando Config", "info")
        config = self._config
        puk, prk = config["chave publica"], config["chave privada"]
        puk, prk = crip.serializar_chave_rsa(puk, prk)
        config["chave publica"], config["chave privada"] = puk, prk
        pers.salvar_config(self._config)

    def send_message(self, message, ip):
        puk = rede.get_puk(ip)
        prk = self._config["chave privada"]
        msm_crip = crip.encriptar_fim_a_fim(message, prk, puk)
        self._peer.enviar_para(ip, msm_crip)

    def receive_message(self, ip, pacote):
        puk_string = self._config["peers conhecidos"][str(ip[0])]
        puk = crip.desserializar_chave_publica_rsa(puk_string)

        mensagem = crip.decriptar_fim_a_fim(
            pacote,
            self._config["chave privada"],
            puk
        )

        for hook in self._receive_hooks:
            hook(ip, mensagem)

    def add_receive_hook(self, hook):
        self._receive_hooks.append(hook)


def start():
    mensageria = Mensageria()
    mensageria.start()

def add_receive_hook(hook):
    mensageria = Mensageria()
    mensageria.add_receive_hook(hook)
