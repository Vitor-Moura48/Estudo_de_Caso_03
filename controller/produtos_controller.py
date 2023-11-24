from model.avaliacao_itens import AvaliacaoItens
from model.produtos import ProdutoItem
from . import *

class ProdutosController:
    
    # Metodo todos os produtos
    @staticmethod
    def pegar_todos_produtos():
        produtos = ProdutoItem()

        itens = produtos.pegar_todos_produtos()
        return itens
    
    @staticmethod
    def cadastrar_produto(form, foto_item):
        produtos = ProdutoItem()

        categoria_item = form['categoria_item']
        nome_item = form['nome_item']
        descricao_item = form['descricao_item']
        condicao_item = form['condicao_item']
        tipo_item = form['tipo_item']
        quantidade_item = form['quantidade_item']
        id_usuario = form['id_usuario']
        valor = form['valor_produto']

        message, status = produtos.cadastrar_produto(nome_item=nome_item, categoria_item=categoria_item, descricao=descricao_item, condicao=condicao_item, tipo=tipo_item, quantidade=quantidade_item, foto_anexada=foto_item, remetente_id=id_usuario, valor=valor)

        response = make_response(jsonify({"message": message, "status": status}), status)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    
    # Metodo para adquirir item
    @staticmethod
    def adquirir_produto(token: str, id_produto: str):
        produtos = ProdutoItem()

        print(f"=================== ADQUIRIR PRODUTO ===================")
        print(f"Token: {token}")
        print(f"Id do produto: {id_produto}")
        print(f"=================== ADQUIRIR PRODUTO ===================")

        message, status = produtos.adquirir_produto(token, id_produto)
        
        response = make_response(jsonify({"message": message, "status": status}), 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
