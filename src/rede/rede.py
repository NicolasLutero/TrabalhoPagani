import base64
import json
import socket
from typing import Tuple
import threading

def formatar_para_json(res_cripto):
    pacote_json = {
        "mensagem_cifrada": base64.b64encode(res_cripto["mensagem_cifrada"]).decode('utf-8'),
        "chave_aes_cifrada": base64.b64encode(res_cripto["chave_aes_cifrada"]).decode('utf-8'),
        "iv": base64.b64encode(res_cripto["iv"]).decode('utf-8'),
        "assinatura": base64.b64encode(res_cripto["assinatura"]).decode('utf-8')
    }
    
    return json.dumps(pacote_json, indent=4)

def reconstruir_pacote_original(dados_brutos):
    pacote_json = json.loads(dados_brutos.decode('utf-8'))

    pacote_original = {
        "mensagem_cifrada": base64.b64decode(pacote_json["mensagem_cifrada"]),
        "chave_aes_cifrada": base64.b64decode(pacote_json["chave_aes_cifrada"]),
        "iv": base64.b64decode(pacote_json["iv"]),
        "assinatura": base64.b64decode(pacote_json["assinatura"])
    }

    return pacote_original


class Peer:
    def __init__(self, mensageria):
        self._socket_escuta = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._rodando = False
        self._mensageria = mensageria

    def iniciar(self):
        self._rodando = True
        self._thread_servidor = threading.Thread(target=self._loop_escuta)
        self._thread_servidor.start()

    def _loop_escuta(self):
        self._socket_escuta.bind(('0.0.0.0', 6767))
        self._socket_escuta.listen(5)

        while self._rodando:
            try:
                conn, addr = self._socket_escuta.accept()
                threading.Thread(target=self._lidar_com_conexao, args=(conn, addr)).start()
            except Exception as e:
                print(f"Erro no accept: {e}")

    def desligar(self):
        self._rodando = False

    def _lidar_com_conexao(self, conn, addr):
        with conn:
            try:
                dados_brutos = conn.recv(8192)
                if not dados_brutos: return

                pacote_original = reconstruir_pacote_original(dados_brutos)
                self._mensageria.receive_message(pacote_original)
                    
            except Exception as e:
                print(f"Erro ao processar mensagem de {addr}: {e}")            

    def enviar_para(self, endereco_destinatario, pacote_criptografado):
        pacote_envio_json = formatar_para_json(pacote_criptografado)

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(endereco_destinatario)
                s.sendall(pacote_envio_json.encode('utf-8'))

        except ConnectionRefusedError:
            print("Erro: O destinatário não está aceitando conexões.")

        except Exception as e:
            print(f"Ocorreu um erro no envio: {e}")

