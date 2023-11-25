from model.balanco_vendas import BalancoVendas
from . import *

class BalancoController:

    @staticmethod
    def pegar_todos_itens_vendidos():
        balanco = BalancoVendas()

        itens = balanco.pegar_todos_itens_vendidos()
      
        response = make_response(jsonify({"itens": itens, 'status': 200}), 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response