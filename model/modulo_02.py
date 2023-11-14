import csv
import os

class AvaliacaoItens:
    def __init__(self):
        arquivo_existe = os.path.isfile('database/avaliacao.csv')
        
        try:
            with open('database/avaliacao.csv','a',newline='') as arquivo_csv_avaliacao:
                escritor = csv.writer(arquivo_csv, delimiter=';')
                if not arquivo_existe:
                    escritor.writerow(['Codigo','Nome','Quantidade','Faixa de Valor','Condicao','Creditos','Aprovacao'])
        except:
            pass
        
        novas_linhas_itens = []

        with open('database/itens.csv','r') as arquivo_csv:
            leitor = csv.reader(arquivo_csv,delimiter=';')
            cabecalho = next(leitor)

            for item in leitor:
                if len(item) >= 6:
                    print(f'Código: {item[0]} - Nome: {item[1]}\nQuantidade: {item[2]} - Faixa de valor: {item[3]}\nDescrição: {item[4]} - Condição: {item[5]}\n')
                    
                    pontuacao = int(input('-Digite a pontuação de créditos-\nCritérios:\nFaixa de valor | Condição\n0R$-50R$ = 2 pontos | Ruim = Não aprovado\n50R$-100R$ = 4 pontos | Mediano = 5\n100R$-500R$ = 6 pontos | Bom = 10 pontos\n500R$-1000+ = 8 pontos | Excelente = 15 pontos\nR:'))
                    
                    aprovacao = input("Aprovado ou não, com justificativa:\n")
                    
                    dados = [item[0],item[1],item[2],item[3],item[5],pontuacao,aprovacao]
                    
                    if aprovacao == 'Aprovado':
                        with open('database/avaliacao.csv','a',newline='') as arquivo_csv_avaliacao:
                            escritor_csv = csv.writer(arquivo_csv_avaliacao, delimiter=';')
                            escritor_csv.writerow(dados)
                    
                    else:
                        continue

                    novas_linhas_itens.append(item)

        with open('database/itens.csv', 'w', newline='') as arquivo_csv_itens:
            escritor_itens = csv.writer(arquivo_csv_itens, delimiter=';')
            escritor_itens.writerow(cabecalho) 
            escritor_itens.writerows(novas_linhas_itens)  


mai = AvaliacaoItens()
