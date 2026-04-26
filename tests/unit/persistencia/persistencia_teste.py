from src.persistencia import carregar_config, salvar_config, registrar_evento

config = carregar_config()
registrar_evento("Carregando Config!")
print(config)
if config is None:
    registrar_evento("Config Não Foi Encontrado!")
    registrar_evento("Criando Config!")
    config = {
        "Teste": 1
    }
    salvar_config(config)
    registrar_evento("Config Salvo!")
else:
    registrar_evento("Config Carregado com Sucesso!")
print(config)
