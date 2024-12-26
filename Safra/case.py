import pandas as pd
import numpy as np
from scipy.stats import zscore

dataframe = pd.read_excel("F:\Py\Safra\Dataset.xlsx")
data_teste = pd.read_excel("F:\Py\Safra\Data_teste.xlsx")

#verificar valores duplicados na coluna ID_Cliente

# dup_id = dataframe['ID_Cliente'].duplicated().sum()
# ids_duplicados = dataframe[dup_id]
# print("Valores duplicados na coluna ID_Cliente: ", ids_duplicados)

#print(dataframe)
#print(data_teste)

ids_duplicados_teste = data_teste[data_teste.duplicated(subset="ID_Cliente", keep=False)]
print("Quantidade de Valores duplicados na coluna ID_Cliente: ", ids_duplicados_teste)

idades_negativas = data_teste[data_teste['Idade'] < 0]
if not idades_negativas.empty:
    print("Idades negativas: ", idades_negativas)
else:
    print("Não há idades negativas")

    