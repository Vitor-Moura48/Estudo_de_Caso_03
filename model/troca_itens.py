import csv

class Cliente:
    def __init__(self, nome, creditos):
        self.nome = nome
        self.creditos = creditos
        self.itens_selecionados = []
        self.estoque_atualizado = []

    def selecionar_item(self):
        try:
            escolha = input("Escolha o item desejado acima: ")
            quantidade = int(input("Quantos você quer: "))
        except ValueError:
            print("Entrada inválida. Certifique-se de inserir um valor numérico para a quantidade.")
            return

        with open("database/avaliacao.csv", "r") as arquivo_item:
            leitor_itens = csv.reader(arquivo_item, delimiter=';')
            cabecalho = next(leitor_itens)
            for linha in leitor_itens:
                nome_item, preco_item, quantidade_item, *_ = linha
                quantidade_item = int(quantidade_item)
                if nome_item == escolha:
                    if quantidade <= quantidade_item:
                        quantia = quantidade_item - quantidade
                        if quantia == 0:
                            print("Você pegou o último item!")
                        else:
                            self.itens_selecionados.append([nome_item, preco_item, quantia])
                            self.estoque_atualizado.append([nome_item, preco_item, quantia])
                    else:
                        print("Quantidade superior ao que tem no estoque")
                        return

        with open("database/avaliacao.csv", "w", newline='') as arquivo_item:
            escritor = csv.writer(arquivo_item, delimiter=';')
            escritor.writerow(cabecalho)
            escritor.writerows(self.estoque_atualizado)

    def concluir_troca(self):
        total_creditos_gastos = sum(int(item[1]) * int(item[2]) for item in self.itens_selecionados)
        if total_creditos_gastos <= self.creditos:
            self.creditos -= total_creditos_gastos
            return True
        else:
            print("Créditos insuficientes para concluir a troca.")
            return False

# Exemplo de uso
cliente1 = Cliente("João", 100)
cliente1.selecionar_item()

if cliente1.concluir_troca():
    print(f"Troca concluída! Novo saldo de créditos: {cliente1.creditos}")
else:
    print("Troca não concluída.")
