import pandas as pd


def limpar_unb(arquivo):
    df = pd.read_excel(
        arquivo,
        header=0,
        dtype=str,
        engine="openpyxl"
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    dados = df[
        [
            "Nome do candidato",
            "Curso/turno/Campus"
        ]
    ].copy()

    dados = dados.rename(columns={
        "Nome do candidato": "NOME",
        "Curso/turno/Campus": "CURSO"
    })

    dados["NOME"] = (
        dados["NOME"]
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    dados["CURSO"] = (
        dados["CURSO"]
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
        .str.split("/")
        .str[0]
        .str.strip()
    )

    dados = dados[
        (dados["NOME"] != "")
        & (dados["NOME"] != "nan")
        & (dados["CURSO"] != "")
        & (dados["CURSO"] != "nan")
    ].copy()

    dados["INSTITUIÇÃO"] = "UnB"

    dados = dados[
        [
            "NOME",
            "CURSO",
            "INSTITUIÇÃO"
        ]
    ]

    return dados