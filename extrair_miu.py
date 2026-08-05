import pandas as pd

ARQUIVO_ENTRADA = "produtos_classificados.xlsx"
ARQUIVO_SAIDA = "sku_miu.xlsx"


def trocar_mil_por_miu(sku):
    partes = sku.split("-")
    partes = ["MIU" if p == "MIL" else p for p in partes]
    return "-".join(partes)


df = pd.read_excel(ARQUIVO_ENTRADA)

df_miu = df[df["SKU"].str.contains(r"(?:^|-)MIU(?:-|$)", regex=True, na=False)].copy()
df_mil = df[df["SKU"].str.contains(r"(?:^|-)MIL(?:-|$)", regex=True, na=False)].copy()

df_mil["SKU"] = df_mil["SKU"].apply(trocar_mil_por_miu)
df_mil["Nome"] = df_mil["SKU"].apply(lambda x: " ".join(p.capitalize() for p in x.split("-")))

df_resultado = pd.concat([df_miu, df_mil], ignore_index=True)
df_resultado = df_resultado.drop_duplicates(subset="SKU", keep="first")

df_resultado.to_excel(ARQUIVO_SAIDA, index=False)
print(f"Total MIU extraídos: {len(df_resultado)}")
print("Finalizado!")
