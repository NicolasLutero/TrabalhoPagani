from src.rede import Peer

class MensageriaMock:
    def receive_message(self, message):
        print(f'{message}\n Mensagem Recebida')

peer = Peer(MensageriaMock())
peer.iniciar()

pacote = {
    "mensagem_cifrada": b"mensagem_cifrada",
    "chave_aes_cifrada": b"chave_aes",
    "iv": b"iv",
    "assinatura": b"assinatura"
}

peer.enviar_para(('localhost', 6767), pacote)