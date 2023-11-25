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
                columns=["id", "usuario", "nome_completo", "senha", "creditos", "nivel_acesso", "token"])
            df_cabecalho.to_csv(self.arquivo_usuarios, index=False, sep=';')
    
    def cadastrar(self, nome_completo: str, usuario: str, senha: str) -> list[str, int]:
        # Lendo os dados da planilha de usuários
        usuarios_df = pd.read_csv(self.arquivo_usuarios, sep=';')

        # Verificar se o login do usuário existe na planilha
        usuario_existe = usuarios_df["usuario"].isin([usuario]).any()

        if usuario_existe:
            # Usuário já existe
            return ["Aviso:Usuário já existe", 409]
        else:
            # Gerar o id seguindo o formato: 4 numeros aleatorios
            id_usuario = secrets.token_hex(6)

            # Criar o novo registro
            novo_registro = pd.DataFrame([[id_usuario, usuario, nome_completo, senha, 0, "cliente", ""]], columns=[
                                         "id", "usuario", "nome_completo", "senha", "creditos", "nivel_acesso", "token"])

            # Adicionar o novo registro na planilha
            usuarios_df = pd.concat([usuarios_df, novo_registro], ignore_index=True)

            # Salvar a planilha
            usuarios_df.to_csv(self.arquivo_usuarios, index=False, sep=';')

            # Usuário cadastrado com sucesso
            return ["Sucesso:Usuário cadastrado com sucesso!", 201]
    
    def autenticar(self, usuario: str, senha: str) -> list[str, int]:
        # Lendo os dados da planilha de usuários
        usuarios_df = pd.read_csv(self.arquivo_usuarios, sep=';')

        # Verificar se o login do usuário existe na planilha
        usuario_existe = usuarios_df["usuario"].isin([usuario]).any()

        if usuario_existe:
            # Obter a senha registrada para o usuário
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
                
                token = self.setToken(usuario)
                return ["Sucesso:Usuário autenticado com sucesso!", 200, token]
            else:
                # Senha incorreta
                return ["Aviso:Senha incorreta", 401]
        else:
            # Usuário não encontrado
            return ["Aviso:Usuário não encontrado", 404]
    
    # Função para pegar o usuario pelo token
    def getUserInfo(self, token: str):
        # Lendo os dados da planilha de usuários
        usuarios_df = pd.read_csv(self.arquivo_usuarios, sep=';')

        # Verificar se o token do usuário existe na planilha
        usuario_existe = usuarios_df["token"].isin([token]).any()

        if usuario_existe:
            # Obter o nome do usuario
            id_usuario = usuarios_df.loc[usuarios_df["token"]
                                               == token, "id"].values[0]
            
            # o id_usuario é string
            id_usuario = str(id_usuario)
                                         
            nome_usuario = usuarios_df.loc[usuarios_df["token"]
                                               == token, "nome_completo"].values[0]
            creditos = usuarios_df.loc[usuarios_df["token"]
                                                  == token, "creditos"].values[0]
            nivel_acesso = usuarios_df.loc[usuarios_df["token"]
                                                  == token, "nivel_acesso"].values[0]
            
            if isinstance(creditos, np.int64):
                creditos = int(creditos)

            return [200, "Sucesso:Usuário autenticado com sucesso!", {"nome": nome_usuario, "creditos": creditos, "nivel_acesso": nivel_acesso, "id_usuario": id_usuario}]
        else:
            # Usuário não encontrado
            return [404, "Aviso:Usuário não encontrado", {}]

    # Função para gerar o token e salvar no csv e gerar um arquivo de token.txt
    def setToken(self, usuario: str):
        # Lendo os dados da planilha de usuários
        usuarios_df = pd.read_csv(self.arquivo_usuarios, sep=';')

        # Verificar se o login do usuário existe na planilha
        usuario_existe = usuarios_df["usuario"].isin([usuario]).any()

        if usuario_existe:
            # Obter o token
            token = secrets.token_urlsafe(16)

            # Adicionar o token na planilha
            usuarios_df["token"] = usuarios_df["token"].astype(str)
            usuarios_df.loc[usuarios_df["usuario"] == usuario, "token"] = token

            # Salvar a planilha
            usuarios_df.to_csv(self.arquivo_usuarios, index=False, sep=';')

            # Salvar o token em um arquivo
            arquivo_token = open(resource_path('database/token.txt'), 'w')
            arquivo_token.write(token)
            arquivo_token.close()

            return token
    
    # Metodo que pega o token do arquivo token.txt e verifica se ele existe no csv e retorna o token
    def getToken(self):
        # Lendo os dados da planilha de usuários
        usuarios_df = pd.read_csv(self.arquivo_usuarios, sep=';')

        # Verificar se o arquivo existe
        if os.path.isfile(resource_path('database/token.txt')):
            # Abrir o arquivo de token
            arquivo_token = open(resource_path('database/token.txt'), 'r')
            token = arquivo_token.read()
            arquivo_token.close()

            # Verificar se o token existe na planilha
            token_existe = usuarios_df["token"].isin([token]).any()

            if token_existe:
                return token
            else:
                return ""
        else:
            return ""

    # Metodo para logout do usuario, ele apaga o token do usuario no csv e no arquivo token.txt
    def logout(self, token: str):
        # Lendo os dados da planilha de usuários
        usuarios_df = pd.read_csv(self.arquivo_usuarios, sep=';')

        # Verificar se o token do usuário existe na planilha
        usuario_existe = usuarios_df["token"].isin([token]).any()

        if usuario_existe:
            # Apagar o token na planilha
            usuarios_df.loc[usuarios_df["token"] == token, "token"] = ""

            # Salvar a planilha
            usuarios_df.to_csv(self.arquivo_usuarios, index=False, sep=';')

            # Apagar o token no arquivo
            arquivo_token = open(resource_path('database/token.txt'), 'w')
            arquivo_token.write("")
            arquivo_token.close()

            return [200, "Sucesso:Usuário deslogado com sucesso!"]
        else:
            # Usuário não encontrado
            return [404, "Aviso:Usuário não encontrado"]