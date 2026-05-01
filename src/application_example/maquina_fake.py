# maquina_fake.py
from src import criptografia as crip
from src import rede


puk_string = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2c5hSxD7Pp5HgFo+UV2C\ncWxKPCOQa54RQULG9cpDpPJRxwjdJ8ZWTzo3YW6/hcJSz7n6sliyZXX2r6KNz/wU\n0gNarFXH84DtFRx6My5io6JMNzSjKq88yttAvoNk2yrYgzRXwLI9VftelppxjJer\nT9Io4e/G37mMgMcLGGRoa2Uiy76C3ibdy/9aQZTWELax48jaCEgdIAiin19KcUpS\nPvwxUM42F0VSSJX3//AmyTypCxWrKUIIdpQ0Mt5DTl1izcIsY4d516Ytf6y3Nvks\nzb69PsRc4a8BAV6PH53lg4ZA9z2AaqcLIvbNigfrB3/2H4KJAvoZp81e7EAlS3xx\nqQIDAQAB\n-----END PUBLIC KEY-----"
prk_string = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDZzmFLEPs+nkeA\nWj5RXYJxbEo8I5BrnhFBQsb1ykOk8lHHCN0nxlZPOjdhbr+FwlLPufqyWLJldfav\noo3P/BTSA1qsVcfzgO0VHHozLmKjokw3NKMqrzzK20C+g2TbKtiDNFfAsj1V+16W\nmnGMl6tP0ijh78bfuYyAxwsYZGhrZSLLvoLeJt3L/1pBlNYQtrHjyNoISB0gCKKf\nX0pxSlI+/DFQzjYXRVJIlff/8CbJPKkLFaspQgh2lDQy3kNOXWLNwixjh3nXpi1/\nrLc2+SzNvr0+xFzhrwEBXo8fneWDhkD3PYBqpwsi9s2KB+sHf/YfgokC+hmnzV7s\nQCVLfHGpAgMBAAECggEABNvF/AYvcvVvgK0pEBvG+2yGeJjBS0OpFkZJwnui2z/6\nhtDFGiXu9yQRAZZJi5xkYegMoxDRpFJa0KhbUHhKwJqJjPTG5o28/CHfMFtIoQAC\ntWwlRAaWE3i+yEeNc7Dp4bD3tvLJTBM04dglHOIMB+/j48WIL3Jn1qTAZxvKRoCR\nZIq6EG5HVnvl2annZj7sxaelTRyAf/5+gHtgWJqK9xHjk5KP2nBK0ZbFXDHzXaNq\nQkDYTBQO4RwTLl+OlrvibOqev77LqsN16wVx/9Lh1IlesXW8e/Sx58x/FarqtdWD\nWZGrNHXycqCsWMNOyix/8BI5+FVf9MRYl1G/1ZFtOQKBgQD3jGCUgZtfwlKvEh2p\niWDhk7pjmLS5ewe70WoepmZnVE4+78JKflSDBt71CPjMUDwrheBgf4DDMv/DrIH6\ndk8AhvkyLxkKrIhvjIgHmXFGn8fGkOhWTuHVqRanvtiXF1qLyig1Kog+eq397MSV\nZoomsqYGV8vjiwxyzIgz8o68vQKBgQDhPgzVoA/DChskefwcIRTgy2dyMCYQL4Uq\nk/snssdqGac7VqxNoGADy1tUm+wZsyA0PYz2cklXjTS9tPgkpj2jDRyiuT973xOb\nKF32XfeuzhbmNpD2vpVv5z58TT7FCUeJRywHRA0g/zmiD4iDVj2a7lRwbcKNgTLt\n5gvUrZX1XQKBgQCyzYFhIvCATVL9w18LewAwT00c7Ur0gkoGvm8hLl3fGsTdrr4u\nomsWrRrT8KQMp5OeeDemW9I8rBSTWIIVz+imX9eVCPHUhOSTdfU3T/zC31wkL7yx\nwo5ajqSfizjUgXjUabN7G3qHboNIWwFvTD5TT0yeXkIV2/Sk4tkqdHPnHQKBgG0s\nGyJr61fYjSFX8sdbjXgLfr9M8RYFQmFJyoEKWTdm6bSMJQWXBxKvvTu8O2qVdLV9\nY9aLvFqwOXD9xwxUeymNkGSar1eF30XkAe8IyqUyhMzeg9Lkux+7EIFFG3h7L+4s\nzf1TkZ19t1yCdONbqI5wmALKYHMfvSSrzO4vmLCNAoGBAIqoeh0DJ+ECraJ+gL/N\nAEo1Da5ji2OhtYWdQlClnnC0BlLopIHRcPpAvMYAX+Ah6FVBblFGexgbdk++joz+\ngei262HW3Y19VgyHnjRtKf6AVCmSrhXnzFqYvgMKxxubPaG72rSfCY50BCeUsL8E\nKWiq0PkQxKr8fJEjDubbVSvn\n-----END PRIVATE KEY-----"
puk_fake = crip.desserializar_chave_publica_rsa(puk_string)
prk_fake = crip.desserializar_chave_privada_rsa(prk_string)


puk_mensageria_string = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwFnyvZiSeUQFcA0fIEoS\nzYc1MhuY4JQqZoyifSjpEdiWZnjYit+snOejD/N58nYZv4LkZKJF0PoPG1ZGwEUq\n5Rkk92We5rqSen7G7rG8mv7TjCTAu58kshg91TU0AEto3VwhstRchZJ4DguXfCUT\n9RykFcAqGwdslHYvWL49jLYlM97QZxIGuwF3LL+Il+otKLRHRD0l8H+c0xkuU5Qp\nnr9oN1DyVlwrH+MI+KbAZhmT3yVnD+SNN/qsStHcmb04Uj+3W6ZYRLqx6q7zET2z\ndL7cSfutTbVbghgZ3x0K4l2S37CAqdEDlXyNTorHnxU9LR2cNSinqMvJcupi1mbd\nMQIDAQAB\n-----END PUBLIC KEY-----"
puk_mensageria = crip.desserializar_chave_publica_rsa(puk_mensageria_string)


ip = "('127.0.0.1', 6769)"
ip = eval(ip)
peer_fake = rede.Peer(None)


while True:
    mensagem = input("Mensagem (-1 para sair): ")
    if mensagem == "-1":
        break

    pacote = crip.encriptar_fim_a_fim(
        mensagem,
        prk_fake,          # fake assina
        puk_mensageria     # destino real
    )

    peer_fake.enviar_para(ip, pacote)
