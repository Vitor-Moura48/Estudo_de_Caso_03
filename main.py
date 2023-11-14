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
                            (f'1 - Módulo de Gestão de Leitos', '1'),
                            (f'2 - Módulo de Controle de Equipamento', '2'),
                            (f'3 - Módulo de Administração de Medicamentos', '3'),
                            (f'4 - Módulo de Agendamento e Controle de Visitas', '4'),
                            (f'5 - Módulo de Prontuário Eletrônico', '5'),
                            (f'6 - Módulo de Gestão de Equipes', '6'),
                            (f'7 - Módulo de Cadastro de Visitantes', '7'),
                            (f'8 - Módulo de Relátorios e Análises', '8'),
                            (f'9 - Encerrar a Sessão no Sistema', '9')
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
                #run()
                pass
            case '7':
                #run()
                pass
            case '8':
               #run()
               pass
            case '9':
                print(f'{cor_mensagem}👋 Obrigado por utilizar o Sistema{Style.RESET_ALL}\n')
                break
            case _:
                print(f'{cor_mensagem_erro}❌ Ocorreu um erro estranho{Style.RESET_ALL}\n')

except KeyboardInterrupt:
    print(f'{cor_mensagem_erro}❌ O Sistema foi interrompido forçadamente pelo usuário{Style.RESET_ALL}\n')
