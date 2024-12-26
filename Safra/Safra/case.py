# Importar as bibliotecas necessárias para a análise de dados.

import subprocess
import sys
import pandas as pd
import numpy as np

dataframe = pd.read_excel("F:\Py\Safra\Dataset.xlsx")

print('Mostrar o dataframe' , dataframe)

# Apresentar as primeiras linhas do dataframe, informações sobre o dataframe, estatísticas descritivas e a forma do dataframe.

dataframe.head(10)

# Informações gerais do dataframe como quantidade de linhas e colunas, tipos de dados, quantidade de valores não nulos.
dataframe.info()

#Estatísticas descritivas para a verificação de possíveis outliers.
dataframe.describe()

#Estrutura do dataframe, mostrando quantidade de linhas e colunas.
dataframe.shape

# Sabendo que não há valores nulos no dataset não há necessidade de verifica-los por conta das informações apresentadas através da função
# 'dataframe.info()'.

# Supondo que um cliente pode realizar o financiamento de mais de um carro, não é necessário a verificação de duplicatas na
# coluna ID_Cliente, o mesmo para o restante das colunas, pois elas não contemplam um problema de duplicidade.

# Selecionar as colunas numéricas que podem apresentar outliers.

colunas_numericas = ['Idade','Valor_Financiado', 'Prazo_Financiamento (Meses)',
       'Taxa_de_Juros_ao_ano (%)', 'Valor_Parcela', 'Modelo_Ano_Veiculo',
       'Valor_Veiculo','Renda_Media_Regional',
       'Taxa_Inadimplencia_Regional']

dataframe[colunas_numericas].describe()

# Analisar os valores apresentados nas colunas selecionadas para verificar a presença de outliers.

# Aplicar um padrão de 2 casas decimais para uma melhor visualização dos dados.
dataframe['Valor_Parcela'] = dataframe['Valor_Parcela'].round(2)
dataframe['Valor_Veiculo'] = dataframe['Valor_Veiculo'].round(2)

# Transformar os valores da colunas que possuem '%' para seus valores originais.

dataframe['Taxa_Inadimplencia_Regional'] = dataframe['Taxa_Inadimplencia_Regional'] * 100
dataframe['Taxa_de_Juros_ao_ano (%)'] = dataframe['Taxa_de_Juros_ao_ano (%)'] * 100
dataframe['Taxa_de_Juros_ao_ano (%)'] = dataframe['Taxa_de_Juros_ao_ano (%)'].round(1)
dataframe['Taxa_Inadimplencia_Regional'] = dataframe['Taxa_Inadimplencia_Regional'].round(1)

print(dataframe)

# Criar uma função para categorizar a idade dos clientes em Jovem Adulto, Adulto e Idoso, afim de facilitar a visualização dos dados.

def categorizar_idade(idade):
    if idade < 35:
        return 'Jovem Adulto'
    elif idade < 55:
        return 'Adulto'
    else:
        return 'Idoso'    

# Aplicar a função 'categorizar_idade' na coluna 'Idade' e criar a coluna 'Faixa_Etaria'.
dataframe['Faixa_Etaria'] = dataframe['Idade'].apply(categorizar_idade)

# Criar um novo dataframe para armazenar a quantidade de clientes por gênero, faixa etária e faixa de renda.
df_metrica = dataframe.groupby(['Genero','Faixa_Etaria','Faixa_de_Renda'])['ID_Cliente'].count().reset_index()
df_metrica.rename(columns={'ID_Cliente':'Quantidade_Clientes'},inplace=True)
print(df_metrica)

import matplotlib.pyplot as plt

# Grafico em pizza para genero

df_metrica_genero = dataframe.groupby(['Genero'])['ID_Cliente'].count().reset_index()
df_metrica_genero.rename(columns={'ID_Cliente':'Quantidade_Clientes'},inplace=True)
df_metrica_genero

# Dados para o gráfico de pizza
labels = df_metrica_genero['Genero']
sizes = df_metrica_genero['Quantidade_Clientes']  # Quantidade de homens e mulheres
colors = ['pink', 'lightblue']
explode = (0.1, 0)  # Destacar a fatia dos homens

# Criar o gráfico de pizza
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)

# Garantir que o gráfico seja desenhado como um círculo
plt.axis('equal')

# Mostrar o gráfico
plt.show()

#grafico faixa de renda

df_metrica_renda = dataframe.groupby(['Faixa_de_Renda'])['ID_Cliente'].count().reset_index()
df_metrica_renda.rename(columns={'ID_Cliente':'Quantidade_Clientes'},inplace=True)
df_metrica_renda

import pandas as pd
import matplotlib.pyplot as plt

# Extrair os dados do DataFrame
labels = df_metrica_renda['Faixa_de_Renda']
sizes = df_metrica_renda['Quantidade_Clientes']

# Criar o gráfico de barras
plt.bar(labels, sizes, color=['green', 'red', 'orange'])

# Adicionar título e rótulos aos eixos
plt.title('Quantidade por Faixa de Renda')
plt.xlabel('Faixa de Renda')
plt.ylabel('Quantidade de Clientes')

# Mostrar o gráfico
plt.show()

#grafico faixa etaria

df_metrica_fetaria = dataframe.groupby(['Faixa_Etaria'])['ID_Cliente'].count().reset_index()
df_metrica_fetaria.rename(columns={'ID_Cliente':'Quantidade_Clientes'},inplace=True)
df_metrica_fetaria

import pandas as pd
import matplotlib.pyplot as plt

# Extrair os dados do DataFrame
labels = df_metrica_fetaria['Faixa_Etaria']
sizes = df_metrica_fetaria['Quantidade_Clientes']

# Criar o gráfico de barras
plt.bar(labels, sizes, color=['lightgreen', 'yellow', 'pink'])

# Adicionar título e rótulos aos eixos
plt.title('Quantidade por Faixa Etária')
plt.xlabel('Faixa Etária')
plt.ylabel('Quantidade de Clientes')

# Mostrar o gráfico
plt.show()


# Filtrar quais são os maiores empréstimos realizados.

# Primeiramente caluclar o valor do percentil 75 ou seja, o valor abaixo do qual 75% dos dados se encontram.
# Calcular o valor do percentil 75 da coluna 'Valor_Financiado'

percentil_75 = dataframe['Valor_Financiado'].quantile(0.75)

# Filtrar os 25% maiores valores da coluna 'Valor_Financiado'

maiores_25_porcento = dataframe[dataframe['Valor_Financiado'] >= percentil_75]

# Filtrar as características que queremos visualizar

maiores_25_porcento = maiores_25_porcento[['ID_Cliente', 'Faixa_Etaria', 'Genero', 'Regiao', 'Faixa_de_Renda', 'Valor_Financiado']]

# Agrupar pelas características e contar a frequência


frequencia = maiores_25_porcento.groupby(['Faixa_Etaria', 'Genero', 'Regiao', 'Faixa_de_Renda'])['ID_Cliente'].count().reset_index(name='Frequencia')

# Identificar qual o tipo de cliente mais frequente

tipo_mais_frequente = frequencia.sort_values(by='Frequencia', ascending=False).iloc[0]

print(tipo_mais_frequente)

# É possível realizar a mesma análise porém com parâmetros diferentes, o que pode gerar diferentes resultados.

percentil_90 = dataframe['Valor_Financiado'].quantile(0.90)

# Filtrar os 25% maiores valores da coluna 'Valor_Financiado'

maiores_10_porcento = dataframe[dataframe['Valor_Financiado'] >= percentil_90]

# Filtrar as características que queremos visualizar

maiores_10_porcento = maiores_10_porcento[['ID_Cliente', 'Faixa_Etaria', 'Genero', 'Regiao', 'Faixa_de_Renda', 'Valor_Financiado']]

# Agrupar pelas características e contar a frequência


frequencia2 = maiores_10_porcento.groupby(['Faixa_Etaria', 'Genero', 'Regiao', 'Faixa_de_Renda'])['ID_Cliente'].count().reset_index(name='Frequencia')

# Identificar qual o tipo de cliente mais frequente

tipo_mais_frequente2 = frequencia2.sort_values(by='Frequencia', ascending=False).iloc[0]

print(tipo_mais_frequente2)

#Sabendo quem são os clientes que realizam os maiores empréstimos, podemos analisar quais são as características predominantes 
# desses clientes, como faixa etária, gênero, região e faixa de renda.

# Criar um novo dataframe para armazenar a quantidade de clientes por faixa etária entre os maiores empréstimos.

df_etaria_25 = maiores_25_porcento.groupby(['Faixa_Etaria'])['ID_Cliente'].count().reset_index()
df_etaria_25.rename(columns={'ID_Cliente':'Quantidade_Clientes'},inplace=True)
print(df_etaria_25)

# Criar um novo dataframe para armazenar a quantidade de clientes por Genero entre os maiores empréstimos.

df_genero_25 = maiores_25_porcento.groupby(['Genero'])['ID_Cliente'].count().reset_index()
df_genero_25.rename(columns={'ID_Cliente':'Quantidade_Clientes'},inplace=True)
print(df_genero_25)

# Criar um novo dataframe para armazenar a quantidade de clientes por Região entre os maiores empréstimos.

df_regiao_25 = maiores_25_porcento.groupby(['Regiao'])['ID_Cliente'].count().reset_index()
df_regiao_25.rename(columns={'ID_Cliente':'Quantidade_Clientes'},inplace=True)
print(df_regiao_25)

# Criar um novo dataframe para armazenar a quantidade de clientes por Faixa de Renda entre os maiores empréstimos.

df_renda_25 = maiores_25_porcento.groupby(['Faixa_de_Renda'])['ID_Cliente'].count().reset_index()
df_renda_25.rename(columns={'ID_Cliente':'Quantidade_Clientes'},inplace=True)
print(df_renda_25)

# Criar um novo dataframe para armazenar a quantidade de financiamentos por região

df_regiao = dataframe.groupby(['Regiao'])['Valor_Financiado'].sum().reset_index()
df_regiao.rename(columns={'Valor_Financiado':'Volume_Regiao'},inplace=True)
df_regiao.sort_values(by='Volume_Regiao', ascending=False)

# Podemos evidenciar que a região com maior volume de financiamentos é a região C.

df_regiao_renda = dataframe.groupby(['Regiao', 'Taxa_Inadimplencia_Regional', 'Renda_Media_Regional'])['ID_Cliente'].count().reset_index()
df_regiao_renda.rename(columns={'ID_Cliente':'Quantidade_Clientes'},inplace=True)
print(df_regiao_renda)

# Existe uma correlação entre a Renda Média Regional e a Taxa de Inadimplência Regional, ou seja, quanto maior a renda média regional, menor
# a taxa de inadimplência regional, isso é evidenciado pelas respecitvas taxas de inadimplência regional e renda média regional, das regiões
# A, B, C e D

# Utilizar a função 'mean' no dataframe principal na coluna 'Valor_Veiculo' para calcular a média do valor dos veículos financiados.

media_valor_veiculo = dataframe['Valor_Veiculo'].mean()
print(media_valor_veiculo.round(2))

# O valor médio dos veículos financiados é de R$ 84.813,67.

# Utilizar a função 'groupby()' e 'count' para verificar qual a quantidade de financiamentos por modelo de veículo.

df_modelo_ano = dataframe.groupby(['Modelo_Ano_Veiculo'])['ID_Cliente'].count().reset_index()
df_modelo_ano.rename(columns={'ID_Cliente':'Quantidade_Clientes'},inplace=True)
df_modelo_ano.sort_values(by='Quantidade_Clientes', ascending=False)

# Os modelos de veículos mais financiados são os modelos 2012, 2014, 2015 e 2021 igualmente com 44 financiamentos.

# Criar um filtro para obter a quantidade de clientes inadimplentes.

clientes_inadimplentes = dataframe[dataframe['Status_Pagamento'] == "Inadimplente"]

# Calcular a taxa de clientes inadimplentes

qntd_clientes_inadimplentes = clientes_inadimplentes['ID_Cliente'].count()
qntd_clientes_totais = dataframe['ID_Cliente'].count()

taxa_inadimplencia_geral = qntd_clientes_inadimplentes / qntd_clientes_totais 
print(' A taxa de Inadimplencia Geral é : ', taxa_inadimplencia_geral * 100, '%', sep='')

# Criar novos dataframes para armezenar a taxa de clientes inadimplentes por faixa de renda, faixa etária, gênero, região e faixa de renda.

df_inadimplentes_renda = clientes_inadimplentes.groupby(['Faixa_de_Renda'])['ID_Cliente'].count().reset_index()

df_total_renda = dataframe.groupby(['Faixa_de_Renda'])['ID_Cliente'].count().reset_index()

df_taxa_renda = pd.merge(df_inadimplentes_renda, df_total_renda, on='Faixa_de_Renda', how='inner') 


df_taxa_renda['Taxa_Faixa_de_Renda'] = round((df_taxa_renda['ID_Cliente_x'] / df_taxa_renda['ID_Cliente_y']) * 100, 2)
df_taxa_renda.drop(columns=['ID_Cliente_x', 'ID_Cliente_y'], inplace=True )

print(df_taxa_renda)

# Criar novos dataframes para armezenar a taxa de clientes inadimplentes por faixa etária, gênero, região e faixa de renda.

df_inadimplentes_renda_regiao = clientes_inadimplentes.groupby(['Renda_Media_Regional'])['ID_Cliente'].count().reset_index()

df_total_renda_regiao = dataframe.groupby(['Renda_Media_Regional'])['ID_Cliente'].count().reset_index()

df_taxa_renda_regiao = pd.merge(df_inadimplentes_renda_regiao, df_total_renda_regiao, on='Renda_Media_Regional', how='inner') 


df_taxa_renda_regiao['Taxa_Inadimplencia_Renda_Regional'] = round((df_taxa_renda_regiao['ID_Cliente_x'] / df_taxa_renda_regiao['ID_Cliente_y']) * 100, 2)
df_taxa_renda_regiao.drop(columns=['ID_Cliente_x', 'ID_Cliente_y'], inplace=True )

print(df_taxa_renda_regiao)

df_inadimplentes_regiao = clientes_inadimplentes.groupby(['Regiao'])['ID_Cliente'].count().reset_index()

df_total_regiao = dataframe.groupby(['Regiao'])['ID_Cliente'].count().reset_index()

df_taxa_regiao = pd.merge(df_inadimplentes_regiao, df_total_regiao, on='Regiao', how='inner') 


df_taxa_regiao['Taxa_Inadimplencia_Regiao'] = round((df_taxa_regiao['ID_Cliente_x'] / df_taxa_regiao['ID_Cliente_y']) * 100, 2)
df_taxa_regiao.drop(columns=['ID_Cliente_x', 'ID_Cliente_y'], inplace=True )

print(df_taxa_regiao)

df_inadimplentes_etaria = clientes_inadimplentes.groupby(['Faixa_Etaria'])['ID_Cliente'].count().reset_index()

df_total_etaria = dataframe.groupby(['Faixa_Etaria'])['ID_Cliente'].count().reset_index()

df_taxa_etaria = pd.merge(df_inadimplentes_etaria, df_total_etaria, on='Faixa_Etaria', how='inner') 


df_taxa_etaria['Taxa_Inadimplencia_Faixa_Etaria'] = round((df_taxa_etaria['ID_Cliente_x'] / df_taxa_etaria['ID_Cliente_y']) * 100, 2)
df_taxa_etaria.drop(columns=['ID_Cliente_x', 'ID_Cliente_y'], inplace=True )

print(df_taxa_etaria)


df_taxa_genero = clientes_inadimplentes.groupby(['Genero'])['ID_Cliente'].count().reset_index()
df_taxa_genero.rename(columns={'ID_Cliente':'Quantidade_Clientes'},inplace=True)
df_taxa_genero

# Genero não afeta a taxa de inadimplência, pois a quantidade de clientes inadimplentes é igual para ambos os gêneros.

# Criar uma função para categorizar o Valor Financiado em Faixas, afim de facilitar a visualização dos dados.

def categorizar_valor(valor):
    if valor <= 20000:
        return '0 a 20000'
    elif valor <= 30000:
        return '20000 a 30000'
    elif valor <= 40000:
        return '30000 a 40000'
    elif valor <= 50000:
        return '40000 a 50000'
    elif valor <= 60000:
        return '50000 a 60000'
    elif valor <= 70000:
        return '60000 a 70000'
    elif valor <= 80000:
        return '70000 a 80000'
    else:
        return '80000 ou mais'    

# Aplicar a função 'categorizar_valor' na coluna 'Valor_Financiado' e criar a coluna 'Faixa_Valor'.
dataframe['Faixa_Valor'] = dataframe['Valor_Financiado'].apply(categorizar_valor)
clientes_inadimplentes['Faixa_Valor'] = clientes_inadimplentes['Valor_Financiado'].apply(categorizar_valor)

# -------------------

df_inadimplentes_valor_financiado = clientes_inadimplentes.groupby(['Faixa_Valor'])['ID_Cliente'].count().reset_index()

df_total_valor_financiado = dataframe.groupby(['Faixa_Valor'])['ID_Cliente'].count().reset_index()

df_taxa_valor_financiado = pd.merge(df_inadimplentes_valor_financiado, df_total_valor_financiado, on='Faixa_Valor', how='inner') 


df_taxa_valor_financiado['Taxa_Inadimplencia_Valor'] = round((df_taxa_valor_financiado['ID_Cliente_x'] / df_taxa_valor_financiado['ID_Cliente_y']) * 100, 2)
df_taxa_valor_financiado.drop(columns=['ID_Cliente_x', 'ID_Cliente_y'], inplace=True )

print(df_taxa_valor_financiado)

# A taxa de inadimplência geral tende a aumentar de acordo quanto mais próximo os valores das Faixa de Valores Financiados e Renda da Região
# estão de seus valores médios. Isso é evidenciado pelos valores das taxas de inadimplência por Renda Regional e Faixa de Valor Financiado 
# aumentarem ao aproximarem dos seus respectivos valores médios, já em relação a faixa etária, a taxa de inadimplência tende a diminuir 
# quanto menor a idade do cliente.

df_qnt_inadimplente_etaria = clientes_inadimplentes.groupby(['Faixa_Etaria'])['ID_Cliente'].count().reset_index()
df_qnt_inadimplente_etaria.rename(columns={'ID_Cliente':'Quantidade_Clientes'},inplace=True)
print(df_qnt_inadimplente_etaria)

df_inadimplente_modelo = clientes_inadimplentes.groupby(['Modelo_Ano_Veiculo'])['ID_Cliente'].count().reset_index()
df_inadimplente_modelo.rename(columns={'ID_Cliente':'Quantidade_Clientes'},inplace=True)
print(df_inadimplente_modelo)

clientes_inadimplentes.groupby(['Faixa_Valor'])['ID_Cliente'].count()

clientes_inadimplentes.groupby(['Faixa_de_Renda'])['ID_Cliente'].count()














