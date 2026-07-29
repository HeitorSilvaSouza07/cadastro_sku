import pandas as pd

ARQUIVO_ENTRADA = "skus_extraidos2.xlsx"
ARQUIVO_SAIDA = "produtos_classificados.xlsx"

# Palavras que aparecem como prefixo genérico (ex: "KIT-2-POTE-PRETO") e que
# NUNCA devem "vencer" um produto mais específico contido no mesmo SKU.
GENERICOS = {"KIT"}

CATEGORIAS = {
    # --- Acessórios ---
    "OCULOS":     {"tipo": "Acessório", "subtipo": "Óculos"},
    "BOLSA":      {"tipo": "Acessório", "subtipo": "Bolsa"},
    "RELOGIO":    {"tipo": "Acessório", "subtipo": "Relógio"},
    "MASCULINO":  {"tipo": "Acessório", "subtipo": "Relógio"},  # SKU truncado, sem prefixo RELOGIO
    "PULSEIRA":   {"tipo": "Acessório", "subtipo": "Pulseira"},
    "COLAR":      {"tipo": "Acessório", "subtipo": "Colar"},
    "BRACELETE":  {"tipo": "Acessório", "subtipo": "Bracelete"},

    # --- Produtos de beleza ---
    "RIMEL":      {"tipo": "Produto de beleza", "subtipo": "Rímel"},
    "RIMAL":      {"tipo": "Produto de beleza", "subtipo": "Rímel"},  # variação/typo de RIMEL
    "BATOM":      {"tipo": "Produto de beleza", "subtipo": "Batom"},
    "PERFUME":    {"tipo": "Produto de beleza", "subtipo": "Perfume"},
    "PO":         {"tipo": "Produto de beleza", "subtipo": "Pó facial"},
    "GLOSS":      {"tipo": "Produto de beleza", "subtipo": "Gloss labial"},

    # --- Utensílios domésticos ---
    "POTE":       {"tipo": "Utensílio doméstico", "subtipo": "Pote"},
    "POTES":      {"tipo": "Utensílio doméstico", "subtipo": "Pote"},
    "TACA":       {"tipo": "Utensílio doméstico", "subtipo": "Taça"},
    "TABUA":      {"tipo": "Utensílio doméstico", "subtipo": "Tábua de corte"},
    "ESPREMEDOR": {"tipo": "Utensílio doméstico", "subtipo": "Espremedor de alho"},
    "JOGO":       {"tipo": "Utensílio doméstico", "subtipo": "Jogo de talheres"},
    "CONJUNTO":   {"tipo": "Utensílio doméstico", "subtipo": "Conjunto de churrasco"},
    "ESCOVA":     {"tipo": "Utensílio doméstico", "subtipo": "Escova"},
    "FORMA":      {"tipo": "Utensílio doméstico", "subtipo": "Forma descartável"},

    # --- Eletroportáteis ---
    "PROCESSADOR": {"tipo": "Eletroportátil", "subtipo": "Processador de alimentos"},
    "MIXER":       {"tipo": "Eletroportátil", "subtipo": "Mixer"},
    "BALANCA":     {"tipo": "Eletroportátil", "subtipo": "Balança de cozinha"},

    # --- Genérico (só usado se nada mais específico for encontrado) ---
    "KIT":        {"tipo": "Kit", "subtipo": "Kit genérico"},
}


def gerar_nome(sku):
    palavras = sku.split("-")
    nome = " ".join(palavra.capitalize() for palavra in palavras)
    return nome


def classificar(sku):
    palavras = sku.split("-")
    encontrados = [p for p in palavras if p in CATEGORIAS]

    if not encontrados:
        return ("Não classificado", "Não classificado")

    especificos = [p for p in encontrados if p not in GENERICOS]
    escolhido = especificos[0] if especificos else encontrados[0]

    return (
        CATEGORIAS[escolhido]["tipo"],
        CATEGORIAS[escolhido]["subtipo"],
    )


df = pd.read_excel(ARQUIVO_ENTRADA)
df["Nome"] = df["SKU"].apply(gerar_nome)
df[["Tipo", "Subtipo"]] = df["SKU"].apply(lambda x: pd.Series(classificar(x)))
df.to_excel(ARQUIVO_SAIDA, index=False)
print("Finalizado!")