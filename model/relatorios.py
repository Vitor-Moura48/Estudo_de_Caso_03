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

class Relatorios:
    def __init__(self):
        self.arquivo_produtos = resource_path('database/produtos.csv')
        self.arquivo_balanco_vendas = resource_path('database/balanco_vendas.csv')
        self.arquivo_usuarios = resource_path('database/usuarios.csv')
        self.arquivo_itens_avaliar = resource_path('database/itens_para_avaliar.csv')
        self.arquivo_historico_doacao = resource_path('database/historico_doacao.csv')
        self.arquivo_historico_troca = resource_path('database/historico_troca.csv')

    # Metodo para pegar a quantidade de itens cadastrados, avaliados, trocados, doados
    def pegar_relatorio(self):
        produtos_df = pd.read_csv(self.arquivo_produtos, sep=';')
        itens_avaliar_df = pd.read_csv(self.arquivo_itens_avaliar, sep=';')
        historico_doacao_df = pd.read_csv(self.arquivo_historico_doacao, sep=';')
        historico_troca_df = pd.read_csv(self.arquivo_historico_troca, sep=';')

        # Pegando a quantidade de itens cadastrados
        quantidade_itens_cadastrados = len(produtos_df)

        # Pegando a quantidade de itens avaliados quando o status é 2 (aprovado) e 3 (reprovado)
        quantidade_itens_avaliados = len(itens_avaliar_df.loc[itens_avaliar_df['status'] == 2] + itens_avaliar_df.loc[itens_avaliar_df['status'] == 3])


        # Pegando a quantidade de itens trocados
        quantidade_itens_trocados = len(historico_troca_df)

        # Pegando a quantidade de itens doados
        quantidade_itens_doacao = len(historico_doacao_df)

        print(f"Quantidade de itens doados: {quantidade_itens_doacao}")

        return {
            'itens_cadastrados': quantidade_itens_cadastrados,
            'itens_avaliados': quantidade_itens_avaliados,
            'itens_trocados': quantidade_itens_trocados,
            'itens_doacao': quantidade_itens_doacao
        }
    
    # Metodo para gerar e retornar relatorio estatisticos com base nos itens cadastrados e total de vendas
    def gerar_relatorio_estatistico(self):
        try:
            # CSV balanço de venda=> id;id_item;id_comprador;categoria;tipo;id_vendedor;valor;data_venda
            produtos_df = pd.read_csv(self.arquivo_produtos, sep=';')
            balanco_vendas_df = pd.read_csv(self.arquivo_balanco_vendas, sep=';')

            # Pegando a quantidade de itens cadastrados
            quantidade_itens_cadastrados = len(produtos_df)


            # Pegando a quantidade de itens vendidos
            quantidade_itens_vendidos = len(balanco_vendas_df)


            data = {
                'itens_cadastrados': quantidade_itens_cadastrados,
                'itens_vendidos': quantidade_itens_vendidos,
            }

            return data
        
        except Exception as e:
            print(f"Erro ao gerar relatório estatístico: {str(e)}")
            return None

