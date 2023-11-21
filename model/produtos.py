import csv
from . import *
import random
import string
import os

# Tipos de itens
# 1 - Troca
# 2 - Venda
# 3 - Doação

# Status do item
# 1 - Aguardando avaliação
# 2 - Aprovado
# 3 - Reprovado

class ProdutoItem:
    def __init__(self):
        # itens avaliados
        self.arquivo_produtos = resource_path('database/produtos.csv')
        self.arquivo_balanco_vendas = resource_path('database/balanco_vendas.csv')

        if not os.path.isfile(self.arquivo_produtos):
            # Criar o arquivo e adicionar os cabeçalhos das colunas
            df_cabecalho = pd.DataFrame(
                columns=["id", "foto_anexada", "tipo", "categoria", "nome_item", "descricao", "quantidade", "condicao", "valor", "remetente_id"])
            df_cabecalho.to_csv(self.arquivo_produtos, index=False, sep=';')

        if not os.path.isfile(self.arquivo_balanco_vendas):
            # Criar o arquivo e adicionar os cabeçalhos das colunas
            df_cabecalho = pd.DataFrame(
                columns=["id", "id_item", "id_comprador", "categoria", "tipo", "id_vendedor", "valor", "data_venda"])
            df_cabecalho.to_csv(self.arquivo_balanco_vendas, index=False, sep=';')

    def pegar_todos_produtos(self):
        produtos_df = pd.read_csv(self.arquivo_produtos, sep=';')
        itens_json = produtos_df.to_dict('records')

        # json_itens = json.loads(itens_json)

        return itens_json

    

