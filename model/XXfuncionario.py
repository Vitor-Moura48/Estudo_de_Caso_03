import os
import pandas

class Funcionario:
    def __init__(self):
        self.caminho_produtos_cadastrados = "database/produtos_cadastrados.csv"
        self.caminho_produtos_avaliados = "database/produtos_avaliados.csv"

        if not os.path.exists(self.caminho_produtos_cadastrados):
            arquivo = pandas.DataFrame()
            arquivo.to_csv(self.caminho_produtos_cadastrados, index=False)

        if not os.path.exists(self.caminho_produtos_avaliados):
            arquivo = pandas.DataFrame()
            arquivo.to_csv(self.caminho_produtos_avaliados, index=False)

    def cadastrar_produtos_para_venda(self, nome, categoria, preco):
        try:
            arquivo_produtos_avaliados = pandas.read_csv(self.caminho_produtos_cadastrados)
        except:
            arquivo_produtos_avaliados = pandas.DataFrame()

        try:
            arquivo_produtos_cadastrados = pandas.read_csv(self.caminho_produtos_cadastrados)
        except:
            arquivo_produtos_cadastrados = pandas.DataFrame()

        if not arquivo_produtos_avaliados.empty and nome in arquivo_produtos_avaliados['nome'].astype(str).to_list():
            produto = pandas.DataFrame({'nome': [nome], 'categoria': [categoria], 'preco': [preco]})

            if arquivo_produtos_cadastrados.empty:
                produto.to_csv(self.caminho_produtos_cadastrados, index=False, mode='at')
            else:
                produto.to_csv(self.caminho_produtos_cadastrados, index=False, mode='a', header=False)
            
            print("produto cadasatrado...")
        
        else:
            print("Produto não foi avaliado!")

    def alterar_dados_produto(self, nome, categoria, preco):
        try:
            arquivo_produto = pandas.read_csv(self.caminho_produtos_cadastrados)
        except:
            arquivo_produto = pandas.DataFrame()

        if not arquivo_produto.empty and nome in arquivo_produto['nome'].astype(str).to_list():
            indice = arquivo_produto[arquivo_produto['nome'] == nome].index
            arquivo_produto.loc[indice, 'nome'] = nome
            arquivo_produto.loc[indice, 'categoria'] = categoria
            arquivo_produto.loc[indice, 'preco'] = int(preco)

            arquivo_produto.to_csv(self.caminho_produtos_cadastrados, index=False)

            print("produto alterado...")
            
        else:
            print("Produto não encontrado!")



# testando funções
funcionario = Funcionario()
