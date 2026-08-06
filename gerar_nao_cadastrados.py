import pandas as pd

ARQUIVO_ENTRADA = "produtos_classificados.xlsx"
ARQUIVO_SAIDA = "itens_nao_cadastrados_ordenado.xlsx"

df = pd.read_excel(ARQUIVO_ENTRADA)

nao_cadastrados = df[df["Cadastrado"].isna()].copy()

nao_cadastrados = nao_cadastrados[["SKU", "Nome", "Tipo", "Subtipo"]]

nao_cadastrados["chave_ordenacao"] = nao_cadastrados["SKU"].str.split("-").apply(
    lambda partes: partes[0] + "-" + partes[1] if len(partes) > 1 else partes[0]
)
nao_cadastrados = nao_cadastrados.sort_values(by=["chave_ordenacao", "SKU"]).drop(columns=["chave_ordenacao"])

nao_cadastrados.to_excel(ARQUIVO_SAIDA, index=False)
print(f"Gerado: {ARQUIVO_SAIDA} com {len(nao_cadastrados)} itens nao cadastrados.")
