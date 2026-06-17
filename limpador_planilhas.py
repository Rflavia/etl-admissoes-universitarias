import pandas as pd
from tkinter import Tk, filedialog, messagebox

from modelos.uniceplac import limpar_uniceplac
from modelos.unirv import limpar_unirv
from modelos.unb import limpar_unb


def ler_e_juntar_linhas(arquivo):
    df = pd.read_excel(
        arquivo,
        header=None,
        dtype=str,
        engine="openpyxl"
    )

    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    df["linha"] = df.apply(
        lambda x: " ".join(x.dropna().astype(str)),
        axis=1
    )

    df["linha"] = (
        df["linha"]
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    return df


def detectar_padrao_arquivo(arquivo):
    nome_arquivo = arquivo.lower()

    if "unirv" in nome_arquivo:
        return "unirv"

    if "unb" in nome_arquivo:
        return "unb"

    if "uniceplac" in nome_arquivo or "iniceplac" in nome_arquivo:
        return "uniceplac"

    df = pd.read_excel(
        arquivo,
        header=None,
        nrows=200,
        dtype=str,
        engine="openpyxl"
    )

    conteudo = " ".join(
        df.fillna("")
        .astype(str)
        .values
        .flatten()
    )

    if "Nome da pessoa candidata" in conteudo and "Curso/turno/Campus" in conteudo:
        return "unb"

    elif "Medicina (Aparecida)" in conteudo:
        return "unirv"

    elif "UNICEPLAC" in conteudo or "Nome Completo" in conteudo:
        return "uniceplac"

    else:
        return "generico"


def limpar_generico(df):
    return df[["linha"]].copy()


def limpar_textos(dados):
    for coluna in dados.columns:
        dados[coluna] = (
            dados[coluna]
            .astype(str)
            .str.replace(r"^\s*-+\s*", "", regex=True)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
            .replace("nan", "")
        )

    return dados


def processar_planilha(arquivo):
    padrao = detectar_padrao_arquivo(arquivo)

    if padrao == "unb":
        dados = limpar_unb(arquivo)

    elif padrao == "uniceplac":
        dados = limpar_uniceplac(arquivo)

    elif padrao == "unirv":
        df = ler_e_juntar_linhas(arquivo)
        dados = limpar_unirv(df)

    else:
        df = ler_e_juntar_linhas(arquivo)
        dados = limpar_generico(df)
        dados = limpar_textos(dados)

    dados = dados.dropna(how="all")

    saida = arquivo.replace(".xlsx", f"_LIMPO_{padrao}.xlsx")

    dados.to_excel(saida, index=False)

    return saida, padrao


janela = Tk()
janela.withdraw()

arquivo = filedialog.askopenfilename(
    title="Selecione a planilha",
    filetypes=[
        ("Planilhas Excel", "*.xlsx")
    ]
)

if arquivo:
    try:
        saida, padrao = processar_planilha(arquivo)

        messagebox.showinfo(
            "Concluído",
            f"Padrão detectado: {padrao}\n\nArquivo criado:\n{saida}"
        )

        print("Padrão detectado:", padrao)
        print("Arquivo criado:", saida)

    except Exception as erro:
        messagebox.showerror(
            "Erro",
            f"Ocorreu um erro:\n\n{erro}"
        )

        print("Erro:", erro)

else:
    print("Nenhum arquivo selecionado.")