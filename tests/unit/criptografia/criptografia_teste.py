import src.criptografia as cr

rc1, rc2 = cr.gerar_par_chaves_rsa()
dc1, dc2 = cr.gerar_par_chaves_rsa()

tc = cr.gerar_chave_sessao_aes()

msm = "Salve seu noia!"
print(f"Mensagem Original: {msm}")

msm_enc = cr.encriptar_fim_a_fim(msm, rc1, dc2)

print(f"Mensagem Criptografada: {msm_enc}")

msm_des = cr.decriptar_fim_a_fim(msm_enc, dc1, rc2)

print(f"Mensagem Descriptografada: {msm_des}")
