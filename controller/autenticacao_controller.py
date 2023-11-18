from model.autenticacao import Autenticacao
from flask import jsonify, make_response
import numpy as np

class AutenticacaoController:

    # Curiosidade: Metodos estatisticos não precisam de uma instancia da classe para serem executados!
    @staticmethod
    def autenticar_usuario(data):
        autenticacao = Autenticacao()

        username = data.get('username')
        password = data.get('password')

        message, status, username, credits, access_level = autenticacao.autenticar(username, password)

        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"Message: {message}")
        print(f"Status: {status}")
        print(f"Credito: {credits}")
        print(f"Access: {access_level}")

        if isinstance(credits, np.int64):
            credits = int(credits)

        response = make_response(jsonify({"message": message, "status": status, "user": { "username": username, "credits": credits, "access_level": access_level }}), status)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        
        return response
    
    @staticmethod
    def cadastrar_usuario(data):
        autenticacao = Autenticacao()

        nome_completo = data.get('fullName')
        username = data.get('username')
        password = data.get('password')

        print(f"Nome Completo: {nome_completo}")
        print(f"Username: {username}")
        print(f"Password: {password}")

        message, status = autenticacao.cadastrar(nome_completo, username, password)

        response = make_response(jsonify({"message": message, "status": status}), status)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response