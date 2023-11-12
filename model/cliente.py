import os
import pandas

class Cliente():
    def __init__(self):
        self.caminho_registro_doacoes = "database/doacoes.csv"

        if not os.path.exists(self.caminho_registro_doacoes):
            arquivo = pandas.DataFrame()
            arquivo.to_csv(self.caminho_registro_doacoes, index=False)


    def doar_item(self, nome, descricao, condicao):
        try:
            arquivo_doacao = pandas.read_csv(self.caminho_registro_doacoes)
        except:
            arquivo_doacao = pandas.DataFrame()
        
        doacao = pandas.DataFrame({'nome': [nome], 'descricao': [descricao], 'condicao': [condicao]})

        if arquivo_doacao.empty:
            doacao.to_csv(self.caminho_registro_doacoes, index=False, mode='at')
        else:
            doacao.to_csv(self.caminho_registro_doacoes, index=False, mode='a', header=False)
    

# testando funções
cliente = Cliente()

cliente.doar_item('garrafa', 'de vidro', 'quase nova')
cliente.doar_item('livro', 'das crônicas da quasinoite', 'conservado')
