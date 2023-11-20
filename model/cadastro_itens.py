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

class CadastroItens:
    def __init__(self):
        # Itens para avaliação
        self.arquivo_itens_avaliar = resource_path('database/itens_para_avaliar.csv')
        # itens avaliados
        self.arquivo_produtos = resource_path('database/produtos.csv')

        self.arquivo_categorias_itens = resource_path('database/categorias_itens.csv')

        # Verificar se o arquivo existe
        if not os.path.isfile(self.arquivo_itens_avaliar):
            # Criar o arquivo e adicionar os cabeçalhos das colunas
            df_cabecalho = pd.DataFrame(
                columns=["id", "foto_anexada", "tipo", "categoria", "nome_item", "descricao", "quantidade", "status", "condicao", "remetente_id", "rendimento"])
            df_cabecalho.to_csv(self.arquivo_itens_avaliar, index=False, sep=';')

        if not os.path.isfile(self.arquivo_produtos):
            # Criar o arquivo e adicionar os cabeçalhos das colunas
            df_cabecalho = pd.DataFrame(
                columns=["id", "foto_anexada", "tipo", "categoria", "nome_item", "descricao", "quantidade", "condicao", "valor", "remetente_id"])
            df_cabecalho.to_csv(self.arquivo_produtos, index=False, sep=';')
        
        if not os.path.isfile(self.arquivo_categorias_itens):
            # Criar o arquivo e adicionar os cabeçalhos das colunas
            df_cabecalho = pd.DataFrame(
                columns=["id", "nome"])
            df_cabecalho.to_csv(self.arquivo_categorias_itens, index=False, sep=';')

            # Adicione algumas categorias de itens
            self.cadastrar_categoria_item("Roupas")
            self.cadastrar_categoria_item("Eletrônicos")
            self.cadastrar_categoria_item("Livros")
            self.cadastrar_categoria_item("Brinquedos")
        
    
    def cadastrar_categoria_item(self, nome_categoria):
        # Lendo os dados da planilha de itens para avaliar
        categorias_itens_df = pd.read_csv(self.arquivo_categorias_itens, sep=';')

        # O id segue segue o padrão: 5 numeros aleatorios
        categoria_id = ''.join(random.choice(string.digits) for _ in range(5))

        # Criar o novo registro
        novo_registro = pd.DataFrame([[categoria_id, nome_categoria]], columns=["id", "nome"])

        # Adicionar o novo registro na planilha
        categorias_itens_df = pd.concat([categorias_itens_df, novo_registro], ignore_index=True)

        # Salvar a planilha
        categorias_itens_df.to_csv(self.arquivo_categorias_itens, index=False, sep=';')

        # Item cadastrado com sucesso
        return ["Sucesso:Categoria cadastrada com sucesso!", 201]
    
    @staticmethod
    def pegar_categorias_itens():
        arquivo_categorias_itens = resource_path('database/categorias_itens.csv')
        
        # Lendo os dados da planilha de itens para avaliar
        categorias_itens_df = pd.read_csv(arquivo_categorias_itens, sep=';')

        # Converter os dados para o formato de dicionario
        categorias_itens_json = categorias_itens_df.to_json(orient="records")
        json_categorias_itens = json.loads(categorias_itens_json)

        # Retornar os dados
        return json_categorias_itens

    # Metodo para listar todos os itens cadastrados de troca e doacao de um usuario
    def pegar_itens_cadastrados_troca_doacao(self, id_usuario: str):
        # Lendo os dados da planilha de itens para avaliar
        itens_para_avaliar_df = pd.read_csv(self.arquivo_itens_avaliar, sep=';')

        # Filtrar os itens do usuario
        itens_usuario_df = itens_para_avaliar_df[itens_para_avaliar_df["remetente_id"] == id_usuario]

        # Converter os dados para o formato json
        itens_json = itens_usuario_df.to_json(orient="records")
        json_itens = json.loads(itens_json)

        # Retornar os dados
        return json_itens

    # metodo para cadastrar itens para avaliação para troca e doacao
    def cadastrar_itens_para_avaliar(self, foto_anexada, tipo, nome_item, categoria_item, descricao, quantidade, condicao, remetente_id):
        # Lendo os dados da planilha de itens para avaliar
        itens_para_avaliar_df = pd.read_csv(self.arquivo_itens_avaliar, sep=';')

        # O id segue segue o padrão: I + 5 numeros aleatorios
        item_id = 'I'.join(random.choice(string.digits) for _ in range(5))

        # Criar o novo registro
        novo_registro = pd.DataFrame([[item_id, foto_anexada, tipo, categoria_item, nome_item, descricao, quantidade, 1, condicao, remetente_id, 0]], columns=[
                                        "id", "foto_anexada", "tipo", "categoria", "nome_item", "descricao", "quantidade", "status", "condicao", "remetente_id", "rendimento"])

        # Adicionar o novo registro na planilha
        itens_para_avaliar_df = pd.concat([itens_para_avaliar_df, novo_registro], ignore_index=True)

        # Salvar a planilha
        itens_para_avaliar_df.to_csv(self.arquivo_itens_avaliar, index=False, sep=';')

        # Item cadastrado com sucesso
        return ["Sucesso:Item cadastrado com sucesso!", 201]
    
    # metodo para cadastrar itens para venda
    def cadastrar_itens_para_venda(self, foto_anexada, tipo, nome_item, categoria_item, descricao, quantidade, condicao, valor, remetente_id):
        # Lendo os dados da planilha de itens para venda
        itens_para_venda_df = pd.read_csv(self.arquivo_produtos, sep=';')

        # O id segue segue o padrão: 5 numeros aleatorios
        item_id = ''.join(random.choice(string.digits) for _ in range(5))

        # Criar o novo registro
        novo_registro = pd.DataFrame([[item_id, foto_anexada, tipo, categoria_item, nome_item, descricao, quantidade, condicao, valor, remetente_id]], columns=[
                                        "id", "foto_anexada", "tipo", "categoria", "nome_item", "descricao", "quantidade", "condicao", "valor", "remetente_id"])

        # Adicionar o novo registro na planilha
        itens_para_venda_df = pd.concat([itens_para_venda_df, novo_registro], ignore_index=True)

        # Salvar a planilha
        itens_para_venda_df.to_csv(self.arquivo_produtos, index=False, sep=';')

        # Item cadastrado com sucesso
        return ["Sucesso:Item cadastrado com sucesso!", 201]
    
# cadastroitens = CadastroItens()
# cadastroitens.cadastrar_itens_para_avaliar("foto_anexada", "troca", "nome_item", "descricao", 1, "condicao", "remetente_id")