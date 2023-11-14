import csv
import random
import string
import os 

class CadastroItens:
    def __init__(self):
        arquivo_existe = os.path.isfile('database/itens.csv')
        
        try:
            with open('database/itens.csv','a',newline='') as arquivo_csv:
                escritor = csv.writer(arquivo_csv, delimiter=';')
                if not arquivo_existe:
                    escritor.writerow(['Codigo','Nome','Quantidade','Faixa de Valor','Descricao','Condicao'])
        except:
            pass
    
    def criar_codigo(self):
        caracteres = string.ascii_letters + string.digits
        
        codigo = ''.join(random.choice(caracteres) for _ in range(5))
        return codigo
    
    def codigo_existe(self, codigo, leitor):
        return any(item[0] == codigo for item in leitor)
    
    def cadastrar(self, nome,quantidade,faixa_valor,descricao,condicao):
        codigo = self.criar_codigo()
        
        with open('database/itens.csv','r',newline='') as arquivo:
            leitor = csv.reader(arquivo)

            while self.codigo_existe(codigo, leitor):
               
                codigo = self.criar_codigo()
               
                leitor.seek(0)

            dados = [codigo,nome,quantidade,faixa_valor,descricao,condicao] 

        with open('database/itens.csv','a',newline='') as arquivo_csv:
            escritor = csv.writer(arquivo_csv, delimiter=';')
            escritor.writerow(dados)
        

mai = CadastroItens()
mai.cadastrar('Nome',45,50.00,'balba','Bom')