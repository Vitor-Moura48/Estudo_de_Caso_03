import csv
import datetime
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
        self.arquivo_usuarios = resource_path('database/usuarios.csv')

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

    # Metodo para pegar todos os produtos quando a quantidade for maior que 0
    def pegar_todos_produtos(self):
        try:
            # Lendo os dados da planilha de itens para avaliar
            produtos_df = pd.read_csv(self.arquivo_produtos, sep=';')

            # Pegar os itens que a quantidade é maior que 0
            produtos_df = produtos_df.loc[produtos_df['quantidade'] > 0]

            # Transformar o dataframe em um dicionario
            produtos = produtos_df.to_dict('records')

            return produtos
        except Exception as e:
            print(e)
            return []
    
    # metodo para cadastrar produto
    def cadastrar_produto(self, foto_anexada, tipo, categoria_item, nome_item, descricao, quantidade, condicao, valor, remetente_id):
        # Lendo os dados da planilha de itens para avaliar
        produtos_df = pd.read_csv(self.arquivo_produtos, sep=';')

        # O id segue segue o padrão: 5 numeros aleatorios
        produto_id = 'I' + ''.join(random.choice(string.digits) for _ in range(5))

        # Criar o novo registro
        novo_registro = pd.DataFrame([[produto_id, foto_anexada, tipo, categoria_item, nome_item, descricao, quantidade, condicao, valor, remetente_id]], columns=["id", "foto_anexada", "tipo", "categoria", "nome_item", "descricao", "quantidade", "condicao", "valor", "remetente_id"])

        # Adicionar o novo registro ao final do arquivo
        produtos_df = pd.concat([produtos_df, novo_registro], ignore_index=True)

        # Salvar o arquivo
        produtos_df.to_csv(self.arquivo_produtos, index=False, sep=';')


        return ["Produto cadastrado com sucesso!", 201]
    
    # Metodo para produto
    def adquirir_produto(self, token, id_produto):
        try:
            # Lendo os dados da planilha de produtos
            produtos_df = pd.read_csv(self.arquivo_produtos, sep=';')

            # Lendo os dados da planilha de usuarios
            usuarios_df = pd.read_csv(self.arquivo_usuarios, sep=';')

            # Lendo os dados da planilha de balanco de vendas
            balanco_vendas_df = pd.read_csv(self.arquivo_balanco_vendas, sep=';')

            # Pegar o id do comprador
            id_comprador = usuarios_df.loc[usuarios_df['token'] == token]['id'].values[0]

            # Pegar o id do vendedor
            id_vendedor = produtos_df.loc[produtos_df['id'] == id_produto]['remetente_id'].values[0]

            # Pega quanto de credito o comprador tem
            credito_comprador = usuarios_df.loc[usuarios_df['id'] == id_comprador]['creditos'].values[0]
            credito_comprador = int(credito_comprador)

            # Pegar o valor do produto
            valor = produtos_df.loc[produtos_df['id'] == id_produto]['valor'].values[0]
            valor = int(valor)

            print(f"=> O usuario tem {credito_comprador} de credito e o produto custa {valor}")

            # Pegar a quantidade do produto
            quantidade = produtos_df.loc[produtos_df['id'] == id_produto]['quantidade'].values[0]

            # C

            # Verificar se o comprador tem credito suficiente para comprar o produto e se o produto tem quantidade suficiente
            if credito_comprador >= valor and quantidade > 0:
                # Diminuir a quantidade do produto
                produtos_df.loc[produtos_df['id'] == id_produto, 'quantidade'] = quantidade - 1

                # Diminuir o credito do comprador
                usuarios_df.loc[usuarios_df['id'] == id_comprador, 'creditos'] = credito_comprador - valor

                # Adicionar o registro de venda
                # O id segue segue o padrão: 5 numeros aleatorios
                venda_id = 'V' + ''.join(random.choice(string.digits) for _ in range(5))

                # Criar o novo registro
                novo_registro = pd.DataFrame([[venda_id, id_produto, id_comprador, 'categoria', 'tipo', id_vendedor, valor, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")]], columns=["id", "id_item", "id_comprador", "categoria", "tipo", "id_vendedor", "valor", "data_venda"])

                # Adicionar o novo registro ao final do arquivo
                balanco_vendas_df = pd.concat([balanco_vendas_df, novo_registro], ignore_index=True)

                # Salvar o arquivo
                balanco_vendas_df.to_csv(self.arquivo_balanco_vendas, index=False, sep=';')

                # Salvar o arquivo
                produtos_df.to_csv(self.arquivo_produtos, index=False, sep=';')

                # Salvar o arquivo
                usuarios_df.to_csv(self.arquivo_usuarios, index=False, sep=';')

                return ["Sucesso:Produto adquirido com sucesso!", 200]
            else:
                return ["Aviso:Você não tem creditos suficiente para comprar o produto!", 400] 
        except Exception as e:
            print(e)
            return ["Erro: Ocorreu um erro ao adquirir o produto.", 500]

    

