import csv
import datetime
from . import *
import random
import string
import os
from core.util import resource_path

# Tipos de itens
# 1 - Troca
# 2 - Venda
# 3 - Doação

# Status do item
# 1 - Aguardando avaliação
# 2 - Aprovado
# 3 - Reprovado

class BalancoVendas:
    def __init__(self):
        self.arquivo_balanco_vendas = resource_path('database/balanco_vendas.csv')

    # Metodo que pega todos os itens vendidos
    def pegar_todos_itens_vendidos(self):
        try:
            # Lendo os dados da planilha de itens para avaliar
            balanco_vendas_df = pd.read_csv(self.arquivo_balanco_vendas, sep=';')

            # Transformar o dataframe em um dicionario
            balanco_vendas = balanco_vendas_df.to_dict('records')

            return balanco_vendas
        except Exception as e:
            print(e)
            return []

