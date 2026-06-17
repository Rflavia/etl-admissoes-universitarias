# ETL de Admissões Universitárias

Sistema desenvolvido em Python para padronizar listas de aprovados de diferentes instituições de ensino superior.

O projeto realiza automaticamente:

- Leitura de planilhas Excel (.xlsx)
- Detecção do modelo da instituição
- Limpeza e padronização dos dados
- Remoção de excedentes
- Extração apenas dos candidatos aprovados
- Exportação para uma nova planilha limpa

Atualmente suporta:

✅ UniRV  
✅ UnB  
✅ UNICEPLAC  

---

## 🛠 Tecnologias utilizadas

- Python 3
- Pandas
- OpenPyXL
- Regex (Expressões Regulares)
- Tkinter

---

## Estrutura do projeto

```text
etl-admissoes-universitarias/

├── limpador_planilhas.py

├── modelos/
│   ├── __init__.py
│   ├── unb.py
│   ├── unirv.py
│   └── uniceplac.py

├── exemplos/
│   ├── unirv_original.png
│   ├── unirv_limpo.png
│   └── resumo_terminal.png

└── README.md
```

---

## Como funciona

O usuário seleciona uma planilha `.xlsx`.

O sistema:

1. Detecta automaticamente a instituição.
2. Extrai os dados relevantes.
3. Padroniza colunas 
4. Remove informações desnecessárias.
5. Mantém apenas os aprovados.
6. Gera uma nova planilha organizada.

---

# 📷 Exemplo 1 - Planilha original

Arquivo recebido da UniRV contendo:

- Inscrição
- Classificação
- Cotas
- Situação
- Dados misturados

![Original](exemplos/unirv_original.png)

---

# 📷 Exemplo 2 - Resultado gerado

Após o processamento, a planilha fica padronizada:

- Nome
- Curso
- Banca
- Situação

![Limpo](exemplos/unirv_limpo.png)

---

# 📷 Exemplo 3 - Resumo do processamento

O sistema exibe no terminal:

- Total de registros encontrados
- Quantidade de aprovados
- Quantidade de excedentes
- Quantidade removida

![Resumo](exemplos/resumo_terminal.png)

---

## 📈 Possíveis melhorias

- Exportação para CSV
- Interface gráfica mais completa
- Suporte a novas universidades
- Leitura de PDFs
- Geração de relatórios automáticos

---

## 👩‍💻 Autora

**Flávia Rosa**

Graduada em Análise e Desenvolvimento de Sistemas  
Pós-graduação em Data Science e Inteligência Artificial  

GitHub: @Rflavia
