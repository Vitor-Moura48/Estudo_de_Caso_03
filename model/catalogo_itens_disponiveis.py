import csv

class catalogo_itens_disponiveis:
    
    def mostrar_catalogo(self):
        with open('database/itens_avaliados.csv', 'r') as arquivo_itens:
            leitor_itens = csv.reader(arquivo_itens, delimiter=';')
            cabecalho = next(leitor_itens)
            for item in leitor_itens:
                print(f"Nome: {item[1]} || Quantidade: {item[2]} || Crédito: {item[5]}")

gereciamento = catalogo_itens_disponiveis()
gereciamento.mostrar_catalogo()