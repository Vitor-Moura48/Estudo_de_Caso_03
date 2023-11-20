from . import *
from model.cadastro_itens import CadastroItens

class ItemController:

    # Metodo para listar todos os itens cadastrados de troca e doacao de um usuario
    @staticmethod
    def pegar_itens_cadastrados_tr_doa(id_usuario):
        cadastroItens = CadastroItens()

        itens = cadastroItens.pegar_itens_cadastrados_troca_doacao(id_usuario)

        response = make_response(jsonify({"itens": itens}), 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    
    @staticmethod
    def get_item_by_id(id):
        pass
        # item = Item()

        # item = item.get_item_by_id(id)

        # response = make_response(jsonify({"item": item}), 200)
        # response.headers['Content-Type'] = 'application/json; charset=utf-8'
        # return response

    # Metodo para cadastrar item
    @staticmethod
    def cadastrar_item_troca_doacao(form, foto_item):
        cadastroItens = CadastroItens()

        nome_item = form['nome_item']
        descricao_item = form['descricao_item']
        condicao_item = form['condicao_item']
        tipo_item = form['tipo_item']
        quantidade_item = form['quantidade_item']
        id_usuario = form['id_usuario']

        print(nome_item)
        print(descricao_item)
        print(condicao_item)
        print(tipo_item)
        print(quantidade_item)
        print(id_usuario)
        print(foto_item)

        message, status = cadastroItens.cadastrar_itens_para_avaliar(nome_item=nome_item, descricao=descricao_item, condicao=condicao_item, tipo=tipo_item, quantidade=quantidade_item, foto_anexada=foto_item, remetente_id=id_usuario)

        response = make_response(jsonify({"message": message, "status": status}), status)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
