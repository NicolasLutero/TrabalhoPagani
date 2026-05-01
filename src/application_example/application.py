from src import Mensageria

Mensageria.start()

def hook_exemplo(ip, mensagem):
    print(f"{ip}: {mensagem}")

Mensageria.add_receive_hook(hook_exemplo)
