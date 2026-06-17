def limpar_unirv(df):
    """
    Limpeza específica da UniRV.

    Resultado final:
    Nome | Curso | Banca | Situacao

    Faz:
    - remove Inscricao
    - remove Class_Geral
    - remove EXCEDENTES
    - deixa em Nome somente o nome do candidato
    - deixa Curso como Medicina
    - cria Banca como UniRV - Universidade de Rio Verde
    """

    # Pega só linhas que começam com inscrição + classificação
    df = df[df["linha"].str.match(r"^\d{6}\s+\d+\s+", na=False)]

    # Separa os campos usando regex
    dados = df["linha"].str.extract(
        r"^(?P<Inscricao>\d{6})\s+"
        r"(?P<Class_Geral>\d+)\s+"
        r"(?P<Curso>"
            r"Medicina \(Aparecida\) - "
            r"(?:Ampla concorrência \(Sistema Universal\)"
            r"|Cota - Estudantes Escola Pública"
            r"|Cota - Estudantes Negros"
            r"|Cota - Estudantes Índios e PCD)"
        r")\s+"
        r"(?P<Candidato>.*?)\s+"
        r"(?P<Situacao>APROVADO.*|EXCEDENTE.*)$"
    )

    # Remove linhas vazias
    dados = dados.dropna(how="all")

    # Limpa espaços em todas as colunas
    for coluna in dados.columns:
        dados[coluna] = (
            dados[coluna]
            .astype(str)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
            .replace("nan", "")
        )

    # Remove os excedentes
    dados = dados[
        ~dados["Situacao"].str.contains("EXCEDENTE", case=False, na=False)
    ].copy()

    # Remove inscrição e classificação
    dados = dados.drop(columns=["Inscricao", "Class_Geral"])

    # Deixa somente Medicina no curso
    dados["Curso"] = "Medicina"

    # Remove sujeiras que possam ter ficado antes do nome
    padroes_remover = [
        "concorrência (Sistema Universal)",
        "concorrencia (Sistema Universal)",
        "Estudantes Escola Pública",
        "Estudantes Escola Publica",
        "Estudantes Negros",
        "Estudantes Índios e PCD",
        "Estudantes Indios e PCD",
    ]

    for padrao in padroes_remover:
        dados["Candidato"] = dados["Candidato"].str.replace(
            padrao,
            "",
            regex=False
        )

    # Remove hífen no começo e espaços duplicados
    dados["Candidato"] = (
        dados["Candidato"]
        .str.replace(r"^\s*-+\s*", "", regex=True)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    # Cria a coluna Banca
    dados["Banca"] = "UniRV - Universidade de Rio Verde"

    # Renomeia Candidato para Nome
    dados = dados.rename(columns={
        "Candidato": "Nome"
    })

    # Ordem final das colunas
    dados = dados[
        [
            "Nome",
            "Curso",
            "Banca",
            "Situacao"
        ]
    ]

    return dados