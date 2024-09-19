# -*- coding: utf-8 -*-
"""automacao-mkt-chat-1de2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ntH0UcxJLgm3dovfZ2YjoSwSGPjcqM8g
"""

import pandas as pd
import numpy as np
import datetime

# O código desse notebook esta no github: https://github.com/Russel-Servicos/automacao-mkt-chat

caminho_do_arquivo = "/content/Tabela_SalesIQ_18_09.csv"
data = "18/09/2024"

df = pd.read_csv(caminho_do_arquivo)

## Remove linhas duplicadas
df = df.drop_duplicates(subset = ["Name"])

## Remove colunas
df = df.drop(columns = ['Visitor ID', 'Initiated Time', 'IP', 'Mode'], axis = 1)

## Muda os tipos de dados das colunas
columns_to_type_conversions={
    'Page': 'str',
    'Question':'str',
    'Source': 'str',
    'Campaign Name': 'str',
  }
df = df.astype(columns_to_type_conversions)

clear_column_nan_value = lambda column_name: np.where(df[column_name] == 'nan', '', df[column_name])

df['Page'] = clear_column_nan_value('Page')
df['Question'] = clear_column_nan_value('Question')
df['Source'] = clear_column_nan_value('Source')
df['Campaign Name'] = clear_column_nan_value('Campaign Name')

## Filtra as linhas a coluna Page (Página de Aterrissagem)
query_is_russelvagas = "not (Page.str.contains('russelvagas.com'))"
df = df.query(query_is_russelvagas)

## Renomeia colunas
columns = {
    "Name": "ID do Visitante",
    "Page": "Página de Aterrissagem",
    "Campaign Medium": "Meio",
    "Campaign Name": "Campanha",
    "Campaign Source": "Origem",
    "State": "Estado",
    "Source": "Canal"
}
df = df.rename(columns=columns)

# Cria novas colunas
df['Data'] = data
df['Qualificação'] = ''
df['Contagem'] = ''
df['Taxa de Conversão'] = ''

## Reorganiza colunas
df = df.reindex(['Data','ID do Visitante','Canal','Página de Aterrissagem','Question','Origem','Meio','Campanha','Estado','Keyword','Qualificação','Contagem','Taxa de Conversão'], axis = 1)

## Atribui as linhas, o valor "Emprego"
query_is_emprego = "(Question.str.contains('Emprego', case=False))"
df_is_emprego = df.query(query_is_emprego)
df_is_emprego.loc[:, "Qualificação"] = "Emprego"

query_is_not_emprego = f"not {query_is_emprego}"
df_not_is_emprego = df.query(query_is_not_emprego)

df = pd.concat([df_is_emprego, df_not_is_emprego])

## Deletar linhas da coluna 'Página de Aterrissagem' que conter 'russelvagas'
df = df.drop(columns = ['Question'], axis = 1)

# Exportar como CSV
now = datetime.datetime.now()
now = now.strftime("%Y_%m_%d_%H_%M")
df.to_csv(f'./planilha_chat_estagio_1de2_{now}.csv', index=False)