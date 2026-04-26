from src import persistencia as pers, criptografia as crip


class Mensageria:
    _instancia = None

    def __init__(self):
        self.config = None

    def __new__(cls, *args, **kwargs):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def start(self):
        pers.registrar_evento("Iniciando Mensageria", "aviso")
        self._load_config()
        print("Implementa Connect da Rede")

    def _load_config(self):
        pers.registrar_evento("Carregando Config", "aviso")
        self.config = pers.carregar_config()
        if self.config is None:
            pers.registrar_evento("Config não encontrado", "aviso")
            self._create_config()

    def _create_config(self):
        pers.registrar_evento("Criando Config", "aviso")
        chave_publica, chave_privada = crip.gerar_par_chaves_rsa()
        self.config = {
            "chave publica": chave_publica,
            "chave privada": chave_privada
        }
        pers.registrar_evento("Salvando Config", "aviso")
        pers.salvar_config(self.config)


def start():
    mensageria = Mensageria()
    mensageria.start()
