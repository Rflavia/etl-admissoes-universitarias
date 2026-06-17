import re
import pandas as pd
import unicodedata


def remover_acentos(texto):
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ASCII", "ignore").decode("ASCII")
    return texto


def limpar_nome(nome):
    nome = str(nome)

    nome = nome.replace("\n", " ")

    nome = re.sub(r"\s+", " ", nome).strip()

    nome = remover_acentos(nome)

    nome = re.sub(r"[^A-Za-z\s]", "", nome)

    nome = re.sub(r"\s+", " ", nome).strip()

    return nome.upper()


def limpar_uniceplac(arquivo):
    df = pd.read_excel(
        arquivo,
        header=None,
        dtype=str,
        engine="openpyxl"
    )

    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    nomes = []

    for _, linha in df.iterrows():
        valores = [
            str(valor).replace("\n", " ").strip()
            for valor in linha
            if pd.notna(valor)
        ]

        for i, valor in enumerate(valores):
            valor_limpo = str(valor).strip()

            # procura classificação: 1º, 2º, 31º etc.
            eh_classificacao = re.fullmatch(
                r"\d{1,3}[º°o]?",
                valor_limpo
            )

            if not eh_classificacao:
                continue

            # depois da classificação, procura inscrição
            for j in range(i + 1, len(valores)):
                inscricao = str(valores[j]).strip()

                eh_inscricao = re.fullmatch(
                    r"0?\d{8,12}",
                    inscricao
                )

                if not eh_inscricao:
                    continue

                # depois da inscrição, pega o primeiro texto que parece nome
                for possivel_nome in valores[j + 1:]:
                    possivel_nome = str(possivel_nome).strip()

                    if re.search(
                        r"Nome Completo|Classificacao|Classificação|Inscrição|Data|Horário|UNICEPLAC|Página",
                        possivel_nome,
                        re.I
                    ):
                        continue

                    if re.search(
                        r"\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2}|\d{1,2}h",
                        possivel_nome
                    ):
                        continue

                    nome = limpar_nome(possivel_nome)

                    if len(nome.split()) >= 2:
                        nomes.append(nome)
                        break

                break

    dados = pd.DataFrame({
        "NOME": nomes
    })

    dados = dados[dados["NOME"] != ""]
    dados = dados.drop_duplicates()

    dados["CURSO"] = "Medicina"
    dados["INSTITUIÇÃO"] = "UNICEPLAC"

    dados = dados[["NOME", "CURSO", "INSTITUIÇÃO"]]

    return dados