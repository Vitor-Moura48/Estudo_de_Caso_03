import os
import pandas

class Funcionario:
    def __init__(self):
        self.caminho_cadastro_produtos = "database/produtos.csv"

        if not os.path.exists(self.caminho_cadastro_produtos):
            arquivo = pandas.DataFrame()
            arquivo.to_csv(self.caminho_cadastro_produtos, index=False)

    def cadastrar_produtos_para_venda(self, nome, categoria, preco):
        try:
            arquivo_produto = pandas.read_csv(self.caminho_cadastro_produtos)
        except:
            arquivo_produto = pandas.DataFrame()

        if arquivo_produto.empty or not nome in arquivo_produto['nome'].astype(str).to_list():
            produto = pandas.DataFrame({'nome': [nome], 'categoria': [categoria], 'preco': [preco]})

            if arquivo_produto.empty:
                produto.to_csv(self.caminho_cadastro_produtos, index=False, mode='at')
            else:
                produto.to_csv(self.caminho_cadastro_produtos, index=False, mode='a', header=False)
            
            print("produto cadasatrado...")
        
        else:
            print("Produto já cadastrado!")

    def alterar_dados_produto(self, nome, categoria, preco):
        try:
            arquivo_produto = pandas.read_csv(self.caminho_cadastro_produtos)
        except:
            arquivo_produto = pandas.DataFrame()

        if not arquivo_produto.empty and nome in arquivo_produto['nome'].astype(str).to_list():
            indice = arquivo_produto[arquivo_produto['nome'] == nome].index
            arquivo_produto.loc[indice, 'nome'] = nome
            arquivo_produto.loc[indice, 'categoria'] = categoria
            arquivo_produto.loc[indice, 'preco'] = int(preco)

            arquivo_produto.to_csv(self.caminho_cadastro_produtos, index=False)

            print("produto alterado...")
            
        else:
            print("Produto não encontrado!")



# testando funções
funcionario = Funcionario()

funcionario.cadastrar_produtos_para_venda('garrafa', 'de vidro', '10')
funcionario.alterar_dados_produto('livro', 'das crônicas da quasinoite', '38')
funcionario.alterar_dados_produto('garrafa', 'de plástico', '6')
funcionario.cadastrar_produtos_para_venda('garrafa', 'de papel', '2')
