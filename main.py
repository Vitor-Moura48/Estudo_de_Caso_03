import inquirer
from colorama import init, Fore, Style

init()

# Função para colorir o texto
def color_text(hex_color):
    hex_color = hex_color.lstrip('#')

    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    return '\033[38;2;{};{};{}m'.format(*rgb_color)

cor_titulo = color_text('D90479')
cor_pergunta = Fore.WHITE
cor_resposta = Fore.MAGENTA
cor_mensagem = Fore.YELLOW
cor_mensagem_erro = Fore.RED

try:
    while True:
        print(f'{cor_titulo}╔══════════════════════════════════════════════════════════╗')
        print(f'║                                                          ║')
        print(f'║ 🏥 Sistema ')
        print(f'║                                            v1.0.0        ║')
        print(f'║                                                          ║')
        print(f'╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n')

        pergunta = [
            inquirer.List('opcao',
                        message=f'Selecione o módulo que deseja acessar',
                        choices=[
                            (f'1 - Módulo de Cadastro de Itens', '1'),
                            (f'2 - Módulo de avaliação de Itens', '2'),
                            (f'3 - Módulo de Gestão de Créditos', '3'),
                            (f'4 - Módulo de Catálogo de Itens Disponíveis', '4'),
                            (f'5 - Módulo de Troca de Itens', '5'),
                            (f'6 - Módulo de Doação de Itens', '6'),
                            (f'7 - Módulo de Relatórios e Estatísticas', '7'),                       
                            (f'8 - Módulo de Gestão de Estoque de Produtos à Venda', '8'),
                            (f'9 - Módulo de Balanço de Vendas', '9'),
                            (f'10 - Módulo de Relatórios Estatíticos ', '10'),
                            (f'11 - Encerrar a Sessão no Sistema', '11')
                        ])
        ]

        respostas = inquirer.prompt(pergunta)

        # Verifique se as respostas são nulas
        if respostas is None:
            raise KeyboardInterrupt
        
        opcao = respostas['opcao']

        print(f'{cor_titulo}=>{Style.RESET_ALL} Você selecionou a opção: {cor_titulo}{opcao}{Style.RESET_ALL}\n')

        match opcao:
            case '1':
                #run()
                pass

            case '2':
                #run()
                pass

            case '3':
                #run()
                pass

            case '4':
                #run()
                pass

            case '5':
                #run()
                pass

            case '6':
                from model.cliente import Cliente
                cliente = Cliente()
                cliente.doar_item(input("Nome: "), input("Descrição: "), input("Condição: "))

            case '7':
                #run()
                pass

            case '8':
                from model.funcionario import Funcionario
                funcionario = Funcionario()

                pergunta = [
                        inquirer.List('opcao',
                        message = f'Selecione a opção deseja acessar',
                        choices = [
                                (f'1 - Cadastrar produtos', '1'),
                                (f'2 - Alterar dados do produto', '2'),
                                (f'3 - Encerrar a Sessão no Sistema', '3')
                                ])
                        ]
                respostas = inquirer.prompt(pergunta)
                opcao = respostas['opcao']

                match opcao:
                    case '1':
                        funcionario.cadastrar_produtos_para_venda(input("Nome: "), input("Categoria: "), input("Preço: "))
                    
                    case '2':
                        funcionario.alterar_dados_produto(input("Nome: "), input("Categoria: "), input("Preço: "))

                    case '3':
                        break
               
            case '9':
                print(f'{cor_mensagem}👋 Obrigado por utilizar o Sistema{Style.RESET_ALL}\n')
                break
            
            case _:
                print(f'{cor_mensagem_erro}❌ Ocorreu um erro estranho{Style.RESET_ALL}\n')

except KeyboardInterrupt:
    print(f'{cor_mensagem_erro}❌ O Sistema foi interrompido forçadamente pelo usuário{Style.RESET_ALL}\n')
