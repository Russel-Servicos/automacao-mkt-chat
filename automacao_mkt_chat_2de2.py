# -*- coding: utf-8 -*-
"""automacao-mkt-chat-2de2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1L_GF99OGbUKRpZVU6XPgwa0EBV4Z41Ke
"""

import pandas as pd
import datetime
import numpy as np

caminho_do_arquivo = "/content/planilha_chat_estagio_2de2_2024_09_18_23_36.csv"
data = "11/09/2024"

df = pd.read_csv(caminho_do_arquivo)

## Conta quantidade de qualificado, não qualificado e emprego
qty_ids = len(df.index)

qty_qualified = df.query("Qualificação == 'Qualificado'")
qty_qualified = len(qty_qualified.index)
percentage_qualified = qty_qualified / qty_ids
percentage_qualified = "{:.0%}".format(percentage_qualified)

## Muda os tipos de dados das colunas
columns_to_type_conversions = {
    'Canal': 'str',
    'Origem':'str',
    'Meio': 'str',
    'Campanha': 'str',
  }
df = df.astype(columns_to_type_conversions)

clear_column_nan_value = lambda column_name: np.where(df[column_name] == 'nan', '', df[column_name])

df['Canal'] = clear_column_nan_value('Canal')
df['Origem'] = clear_column_nan_value('Origem')
df['Meio'] = clear_column_nan_value('Meio')
df['Campanha'] = clear_column_nan_value('Campanha')

## Busca os valores únicos dos canais
canais = pd.unique(df["Canal"])
origens = pd.unique(df["Origem"])
meios = pd.unique(df["Meio"])
campanhas = pd.unique(df["Campanha"])
qualificacoes = pd.unique(df["Qualificação"])

## Contagem e Taxa de Conversão das colunas: Canal, Origem, Meio e Campanha
def generate_data_column_contagem(values, column):
  result_list = []

  for value in values:
    df_filtered = df.query(f"{column} == '{value}'")
    total_rows = len(df_filtered.index)

    df_qualified = df_filtered.query("Qualificação == 'Qualificado'")
    qty_qualified_category = len(df_qualified.index)

    calculation = f"{value}: {total_rows} - {qty_qualified_category}"

    if total_rows > 0:
      percentage = qty_qualified_category / total_rows
      percentage = "{:.0%}".format(percentage)
    else:
      percentage = 0

    result_list.append({
        "TaxaConversão": percentage,
        "Calculo": calculation
    })
  return result_list

def generate_data_column_contagem_from_qualificacao(values, column):
  result_list = []

  for value in values:
    df_filtered = df.query(f"{column} == '{value}'")
    total_rows = len(df_filtered.index)

    calculation = f"{value}: {total_rows}"

    if total_rows > 0:
      percentage = total_rows / qty_ids
      percentage = "{:.0%}".format(percentage)
    else:
      percentage = 0

    result_list.append({
        "TaxaConversão": percentage,
        "Calculo": calculation
    })
  return result_list

contagem_canais_dict = generate_data_column_contagem(values=canais, column="Canal")
contagem_origens_dict = generate_data_column_contagem(values=origens, column="Origem")
contagem_meios_dict = generate_data_column_contagem(values=meios, column="Meio")
contagem_campanhas_dict = generate_data_column_contagem(values=campanhas, column="Campanha")

contagem_qualificacao_dict = generate_data_column_contagem_from_qualificacao(values=qualificacoes, column="Qualificação")

## Insere valores na coluna Contagem e Taxa de Conversão
all_contagem_rows_dict = contagem_qualificacao_dict + [ {} ] + contagem_canais_dict + [ {} ] + contagem_origens_dict + [ {} ] + contagem_meios_dict + [ {} ] + contagem_campanhas_dict

total_rows = df.shape[0]
total_rows_contagem = len(all_contagem_rows_dict)
total_rows_that_must_be_blank = total_rows - total_rows_contagem

for _ in range(total_rows_that_must_be_blank):
  all_contagem_rows_dict.append({})

list_taxa_conversao = []
list_contagem = []

for value in all_contagem_rows_dict:
  dict_is_empty = len(value.keys()) == 0

  if dict_is_empty:
    list_taxa_conversao.append("")
    list_contagem.append("")
  else:
    list_taxa_conversao.append(value["TaxaConversão"])
    list_contagem.append(value["Calculo"])

df.loc[:, "Taxa de Conversão"] = list_taxa_conversao
df.loc[:, "Contagem"] = list_contagem

## Adiciona o valor Chat SalesIQ na coluna Canal
# df_salesiq = df.query("Canal in ['Adwords', 'Direct', 'Referrals', 'Search Engine']")
# df_salesiq.loc[:, "Canal"] = "Chat SalesIQ"

# df_not_salesiq = df.query("Canal not in ['Adwords', 'Direct', 'Referrals', 'Search Engine']")

# df_final = pd.concat([df_salesiq, df_not_salesiq])

## Adiciona valores totais na primeira linha, embaixo da linha das colunas
df.loc[-1] = [data, qty_ids, qty_qualified, percentage_qualified, "", "", "", "", "", "", "", ""]
df.index = df.index + 1
df = df.sort_index()

# Exportar como CSV
now = datetime.datetime.now()
now = now.strftime("%Y_%m_%d_%H_%M")
df.to_csv(f'./planilha_chat_estagio_2de2_{now}.csv', index=False)