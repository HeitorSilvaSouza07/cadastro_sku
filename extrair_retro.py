import pandas as pd

ARQUIVO_ENTRADA = "produtos_classificados.xlsx"
ARQUIVO_SAIDA = "sku_retro.xlsx"

TERMOS_PRINCIPAIS = ["RETRO"]
TERMOS_VARIACAO = ["RETR", "RETR0"]


def normalizar(sku):
    partes = sku.split("-")
    for i, p in enumerate(partes):
        if p in TERMOS_VARIACAO:
            partes[i] = "RETRO"
    return "-".join(partes)


def gerar_nome(sku):
    return " ".join(p.capitalize() for p in sku.split("-"))


df = pd.read_excel(ARQUIVO_ENTRADA)

padrao_principal = "|".join(TERMOS_PRINCIPAIS)
padrao_variacao = "|".join(TERMOS_VARIACAO)

df_principal = df[df["SKU"].str.contains(rf"(?:^|-)(?:{padrao_principal})(?:-|$)", regex=True, na=False)].copy()
df_variacao = df[df["SKU"].str.contains(rf"(?:^|-)(?:{padrao_variacao})(?:-|$)", regex=True, na=False)].copy()

df_variacao["SKU"] = df_variacao["SKU"].apply(normalizar)
df_variacao["Nome"] = df_variacao["SKU"].apply(gerar_nome)

df_resultado = pd.concat([df_principal, df_variacao], ignore_index=True)
df_resultado = df_resultado.drop_duplicates(subset="SKU", keep="first")
df_resultado = df_resultado.sort_values("SKU").reset_index(drop=True)

df_resultado.to_excel(ARQUIVO_SAIDA, index=False)

print(f"Total RETRO extraidos: {len(df_resultado)}")
print(f"  - Principais: {len(df_principal)}")
print(f"  - Corrigidos: {len(df_variacao)}")
print("Finalizado!")
