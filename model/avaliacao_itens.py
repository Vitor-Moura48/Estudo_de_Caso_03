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

class AvaliacaoItens:
    def __init__(self):
        # Itens para avaliação
        self.arquivo_itens_avaliar = resource_path('database/itens_para_avaliar.csv')
        # itens avaliados
        self.arquivo_produtos = resource_path('database/produtos.csv')

        # usuarios
        self.arquivo_usuarios = resource_path('database/usuarios.csv')

        #historico doacao
        self.arquivo_historico_doacao = resource_path('database/historico_doacao.csv')

        #historico troca
        self.arquivo_historico_troca = resource_path('database/historico_troca.csv')


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
        
        if not os.path.isfile(self.arquivo_historico_doacao):
            # Criar o arquivo e adicionar os cabeçalhos das colunas
            df_cabecalho = pd.DataFrame(
                columns=["id", "foto_anexada", "tipo", "categoria", "nome_item", "descricao", "quantidade", "condicao", "remetente_id"])
            df_cabecalho.to_csv(self.arquivo_historico_doacao, index=False, sep=';')

        if not os.path.isfile(self.arquivo_historico_troca):
            # Criar o arquivo e adicionar os cabeçalhos das colunas
            df_cabecalho = pd.DataFrame(
                columns=["id", "foto_anexada", "tipo", "categoria", "nome_item", "descricao", "quantidade", "condicao", "valor", "remetente_id"])
            df_cabecalho.to_csv(self.arquivo_historico_troca, index=False, sep=';')
    

    # Metodo para listar todos os itens cadastrados com o status 1 de troca e doacao
    def pegar_itens_avaliacao_troca_doacao(self):
        # Lendo os dados da planilha de itens para avaliar
        itens_para_avaliar_df = pd.read_csv(self.arquivo_itens_avaliar, sep=';')

        # Filtrar os itens do usuario
        itens_usuario_df = itens_para_avaliar_df[itens_para_avaliar_df["status"] == 1]

        # Converter os dados para o formato json
        itens_json = itens_usuario_df.to_json(orient="records")
        json_itens = json.loads(itens_json)

        # Retornar os dados
        return json_itens
    
    # Metodo para pegar um item para avaliação de acordo com o id do item
    def pegar_item_avaliacao_por_id(self, id_item: str):
        # Lendo os dados da planilha de itens para avaliar
        itens_para_avaliar_df = pd.read_csv(self.arquivo_itens_avaliar, sep=';')

        # Filtrar os itens do usuario
        item_df = itens_para_avaliar_df[itens_para_avaliar_df["id"] == id_item]

        # Converter os dados para o formato json
        item_json = item_df.to_json(orient="records")
        json_item = json.loads(item_json)

        # Retornar os dados
        return json_item
    
    # Metodo para avaliar um item e atribuir ao usuário o credito quando aprovado e atualizar o status do item no arquivo de itens para avaliar e adiciona o item aprovado no arquivo de produtos
    def avaliar_item(self, id_item: str, id_usuario: str, conclusao_item: str, creditos_atribuir: str):
        # Lendo os dados da planilha de itens para avaliar
        itens_para_avaliar_df = pd.read_csv(self.arquivo_itens_avaliar, sep=';')

        # Filtrar os itens do usuario
        item_df = itens_para_avaliar_df[itens_para_avaliar_df["id"] == id_item]

        # Verificar se o item existe
        if item_df.empty:
            return ["Erro:Item não encontrado!", 404]

        # Pegar o item
        item = item_df.iloc[0]

        # Pegar o status do item
        status_item = item["status"]

        # Verificar se o item já foi avaliado
        if status_item != 1:
            return ["Erro:Item já foi avaliado!", 400]

        # Pegar o id do remetente
        remetente_id = item["remetente_id"]

        # Verificar se o item foi aprovado se foi aprovado atualizar o status do item para 2 e adicionar o item no arquivo de produtos e atribuir o credito ao usuario
        if conclusao_item == "2":
            # Atualizar o status do item para 2
            itens_para_avaliar_df.loc[itens_para_avaliar_df["id"] == id_item, "status"] = int(2)

            # Atirbui o credito ao usuario
            self.atribuir_credito_usuario(id_usuario, creditos_atribuir)

            # Atribui o credito a atribuir no rendimento do item
            itens_para_avaliar_df.loc[itens_para_avaliar_df["id"] == id_item, "rendimento"] = int(creditos_atribuir)

            # Salvar o arquivo
            itens_para_avaliar_df.to_csv(self.arquivo_itens_avaliar, index=False, sep=';')

            # Pegar os dados do item e adicionar no arquivo de produtos
            self.adicionar_item_arquivo_produtos(item)
            
        elif conclusao_item == "3":
            # Atualizar o status do item para 3
            itens_para_avaliar_df.loc[itens_para_avaliar_df["id"] == id_item, "status"] = int(3)

            # Salvar o arquivo
            itens_para_avaliar_df.to_csv(self.arquivo_itens_avaliar, index=False, sep=';')

        return ["Sucesso:Item avaliado com sucesso!", 200]
    
    # Metodo para atribuir o credito ao usuario
    def atribuir_credito_usuario(self, id_usuario: str, creditos_atribuir: str):
        # Lendo os dados da planilha de usuarios
        usuarios_df = pd.read_csv(self.arquivo_usuarios, sep=';')

        # Filtrar os usuarios
        usuario_df = usuarios_df[usuarios_df["id"] == id_usuario]

        # Pegar o usuario
        usuario = usuario_df.iloc[0]

        # Pegar o saldo do usuario
        saldo_usuario = usuario["creditos"]

        # Atribuir os creditos ao usuario
        saldo_usuario = saldo_usuario + int(creditos_atribuir)

        # Atualizar o saldo do usuario
        usuarios_df.loc[usuarios_df["id"] == id_usuario, "creditos"] = saldo_usuario

        # Salvar o arquivo
        usuarios_df.to_csv(self.arquivo_usuarios, index=False, sep=';')

    # Metodo para adicionar o item no arquivo de produtos
    def adicionar_item_arquivo_produtos(self, item):
        # Lendo os dados da planilha de produtos
        produtos_df = pd.read_csv(self.arquivo_produtos, sep=';')

        # Pegar o id do item
        id_item = item["id"]

        # Pegar a foto do item
        foto_anexada = item["foto_anexada"]

        # Pegar o tipo do item
        tipo = item["tipo"]

        # Pegar a categoria do item
        categoria = item["categoria"]

        # Pegar o nome do item
        nome_item = item["nome_item"]

        # Pegar a descricao do item
        descricao = item["descricao"]

        # Pegar a quantidade do item
        quantidade = item["quantidade"]

        # Pegar a condicao do item
        condicao = item["condicao"]

        # Pegar o remetente do item
        remetente_id = item["remetente_id"]

        # Pegar o rendimento do item
        rendimento = item["rendimento"]

        # Pegar o valor do item
        valor = rendimento * quantidade

        # Verificar se o tipo do item é troca ou doacao
        if tipo == 1 or tipo == 3:
            # Pegar os dados do item e adicionar no arquivo de produtos
            
            novo_produto = pd.DataFrame([[id_item, foto_anexada, tipo, categoria, nome_item, descricao, quantidade, condicao, valor, remetente_id]], columns=[
                                            "id", "foto_anexada", "tipo", "categoria", "nome_item", "descricao", "quantidade", "condicao", "valor", "remetente_id"])
            
            # Adicionar o novo registro na planilha
            produtos_df = pd.concat([produtos_df, novo_produto], ignore_index=True)

            # Salvar a planilha
            produtos_df.to_csv(self.arquivo_produtos, index=False, sep=';')

            # Verificar se o tipo do item é doacao
            if tipo == 3:
                # Pegar os dados do item e adicionar no arquivo de historico doacao
                novo_historico_doacao = pd.DataFrame([[id_item, foto_anexada, tipo, categoria, nome_item, descricao, quantidade, condicao, remetente_id]], columns=[
                                            "id", "foto_anexada", "tipo", "categoria", "nome_item", "descricao", "quantidade", "condicao", "remetente_id"])
                
                # Adicionar o novo registro na planilha
                historico_doacao_df = pd.read_csv(self.arquivo_historico_doacao, sep=';')
                historico_doacao_df = pd.concat([historico_doacao_df, novo_historico_doacao], ignore_index=True)

                # Salvar a planilha
                historico_doacao_df.to_csv(self.arquivo_historico_doacao, index=False, sep=';')

            elif tipo == 1:
                # Pegar os dados do item e adicionar no arquivo de historico troca
                novo_historico_troca = pd.DataFrame([[id_item, foto_anexada, tipo, categoria, nome_item, descricao, quantidade, condicao, valor, remetente_id]], columns=[
                                            "id", "foto_anexada", "tipo", "categoria", "nome_item", "descricao", "quantidade", "condicao", "valor", "remetente_id"])
                
                # Adicionar o novo registro na planilha
                historico_troca_df = pd.read_csv(self.arquivo_historico_troca, sep=';')
                historico_troca_df = pd.concat([historico_troca_df, novo_historico_troca], ignore_index=True)

                # Salvar a planilha
                historico_troca_df.to_csv(self.arquivo_historico_troca, index=False, sep=';')