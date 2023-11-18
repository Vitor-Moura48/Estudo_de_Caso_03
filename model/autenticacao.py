from . import *
from core.util import resource_path

class Autenticacao:
    def __init__(self) -> None:
        self.arquivo_usuarios = resource_path('database/usuarios.csv')
        #Verifica se o csv usuarios.csv existe caso não exista vai criar o csv usuarios.csv

        # if not os.path.isdir('database'):
        #     os.mkdir('database')

        # Verificar se o arquivo existe
        if not os.path.isfile(self.arquivo_usuarios):
            # Criar o arquivo e adicionar os cabeçalhos das colunas
            df_cabecalho = pd.DataFrame(
                columns=["id", "usuario", "nome_completo", "senha", "creditos", "nivel_acesso"])
            df_cabecalho.to_csv(self.arquivo_usuarios, index=False, sep=';')
    
    def cadastrar(self, nome_completo: str, usuario: str, senha: str) -> list[str, int]:
        # Lendo os dados da planilha de médicos
        usuarios_df = pd.read_csv(self.arquivo_usuarios, sep=';')

        # Verificar se o login do médico existe na planilha
        usuario_existe = usuarios_df["usuario"].isin([usuario]).any()

        if usuario_existe:
            # Usuário já existe
            return ["Aviso:Usuário já existe", 409]
        else:
            # Obter o último id cadastrado
            ultimo_id = usuarios_df["id"].max()

            # Verificar se o id é nulo
            if pd.isna(ultimo_id):
                # Se for nulo, o id é 1
                ultimo_id = 1
            else:
                # Se não for nulo, incrementar o id
                ultimo_id += 1

            # Criar o novo registro
            novo_registro = pd.DataFrame([[ultimo_id, usuario, nome_completo, senha, 0, "cliente"]], columns=[
                                         "id", "usuario", "nome_completo", "senha", "creditos", "nivel_acesso"])

            # Adicionar o novo registro na planilha
            usuarios_df = pd.concat([usuarios_df, novo_registro], ignore_index=True)

            # Salvar a planilha
            usuarios_df.to_csv(self.arquivo_usuarios, index=False, sep=';')

            # Usuário cadastrado com sucesso
            return ["Sucesso:Usuário cadastrado com sucesso!", 201]
    
    def autenticar(self, usuario: str, senha: str) -> list[str, int]:
        # Lendo os dados da planilha de médicos
        usuarios_df = pd.read_csv(self.arquivo_usuarios, sep=';')

        # Verificar se o login do médico existe na planilha
        usuario_existe = usuarios_df["usuario"].isin([usuario]).any()

        if usuario_existe:
            # Obter a senha registrada para o médico
            senha_registrada = usuarios_df.loc[usuarios_df["usuario"]
                                               == usuario, "senha"].values[0]
            print(usuarios_df)
            print(usuarios_df.loc[usuarios_df["usuario"]
                                  == usuario, "senha"].values[0])

            if str(senha) == str(senha_registrada):
                # Usuário e senha corretos retorne o nome do usuario e o nivel de acesso
                nome_usuario = usuarios_df.loc[usuarios_df["usuario"]
                                               == usuario, "nome_completo"].values[0]
                creditos = usuarios_df.loc[usuarios_df["usuario"]
                                                  == usuario, "creditos"].values[0]
                nivel_acesso = usuarios_df.loc[usuarios_df["usuario"]
                                                  == usuario, "nivel_acesso"].values[0]
                
                return ["Sucesso:Usuário autenticado com sucesso!", 200, nome_usuario, creditos, nivel_acesso]
            else:
                # Senha incorreta
                return ["Aviso:Senha incorreta", 401]
        else:
            # Usuário não encontrado
            return ["Aviso:Usuário não encontrado", 404]