import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature


def gerar_par_chaves_rsa():
    """
    Gera um par de chaves RSA (Privada e Pública) para a identidade do usuário.
    Tamanho: 2048 bits.
    """
    chave_privada = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    chave_publica = chave_privada.public_key()

    return chave_privada, chave_publica


def gerar_chave_sessao_aes():
    """
    Gera uma chave simétrica temporária (AES-256) e um Vetor de Inicialização (IV).
    """
    chave_aes = os.urandom(32)  # 256 bits
    iv = os.urandom(16)  # 128 bits para o modo CBC

    return chave_aes, iv


def encriptar_fim_a_fim(mensagem_texto, prk_remetente, puk_destinatario):
    """
    Recebe um texto claro e as chaves necessárias.
    Retorna um dicionário com o pacote PGP pronto para a camada de Rede.
    """
    mensagem_bytes = mensagem_texto.encode('utf-8')

    # 1. ASSINATURA DIGITAL
    # Quem envia, assina usando sua própria Chave Privada.
    assinatura = prk_remetente.sign(
        mensagem_bytes,
        asym_padding.PSS(
            mgf=asym_padding.MGF1(hashes.SHA256()),
            salt_length=asym_padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # 2. GERAR CHAVE DE SESSÃO
    chave_aes, iv = gerar_chave_sessao_aes()

    # 3. CIFRAR A MENSAGEM
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    mensagem_padded = padder.update(mensagem_bytes) + padder.finalize()

    cipher_aes = Cipher(algorithms.AES(chave_aes), modes.CBC(iv), backend=default_backend())
    encryptor = cipher_aes.encryptor()
    mensagem_cifrada = encryptor.update(mensagem_padded) + encryptor.finalize()

    # 4. CIFRAR A CHAVE DE SESSÃO
    # A chave AES é cifrada com a Chave Pública do Destinatário.
    chave_aes_cifrada = puk_destinatario.encrypt(
        chave_aes,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # O Módulo de Rede do Gustavo vai receber isso num formato de dicionário
    return {
        "mensagem_cifrada": mensagem_cifrada,
        "chave_aes_cifrada": chave_aes_cifrada,
        "iv": iv,
        "assinatura": assinatura
    }


def decriptar_fim_a_fim(pacote_rede, prk_destinatario, puk_remetente):
    """
    Faz o processo inverso: abre o envelope digital recebido pela rede.
    Retorna a mensagem em texto claro ou dispara um erro se houver adulteração.
    """
    # Extraindo as partes do pacote
    mensagem_cifrada = pacote_rede["mensagem_cifrada"]
    chave_aes_cifrada = pacote_rede["chave_aes_cifrada"]
    iv = pacote_rede["iv"]
    assinatura = pacote_rede["assinatura"]

    # 1. RECUPERAR A CHAVE DE SESSÃO
    # O destinatário usa sua própria Chave Privada para destrancar a chave AES
    chave_aes = prk_destinatario.decrypt(
        chave_aes_cifrada,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 2. DECIFRAR A MENSAGEM
    # Com a chave AES em mãos, deciframos o corpo da mensagem
    cipher_aes = Cipher(algorithms.AES(chave_aes), modes.CBC(iv), backend=default_backend())
    decryptor = cipher_aes.decryptor()
    mensagem_decifrada_padded = decryptor.update(mensagem_cifrada) + decryptor.finalize()

    # Removendo o (padding) que o AES exige
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    mensagem_bytes = unpadder.update(mensagem_decifrada_padded) + unpadder.finalize()

    # 3. VERIFICAR A ASSINATURA
    # Verifica se quem enviou foi mesmo o remetente e se ninguém alterou os bytes no caminho
    try:
        puk_remetente.verify(
            assinatura,
            mensagem_bytes,
            asym_padding.PSS(
                mgf=asym_padding.MGF1(hashes.SHA256()),
                salt_length=asym_padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    except InvalidSignature:
        raise ValueError("A assinatura é inválida ou a mensagem foi adulterada")

    return mensagem_bytes.decode('utf-8')
