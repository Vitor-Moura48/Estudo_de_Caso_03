from model.avaliacao_itens import AvaliacaoItens
from . import *
from model.cadastro_itens import CadastroItens

class AvaliacaoItemsController:
    
    # Metodo para pegar os itens para avaliação
    @staticmethod
    def pegar_itens_avaliacao():
        avaliacaoItens = AvaliacaoItens()

        itens = avaliacaoItens.pegar_itens_avaliacao_troca_doacao()

        response = make_response(jsonify({"itens": itens}), 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    @staticmethod
    def avaliar_item(data):
        avaliacaoItens = AvaliacaoItens()

        # {
        # "conclusao_item": "2",
        # "creditos_atribuir": "1",
        # "id_item": "I66864",
        # "id_usuario": "1e"
        # }

        conclusao_item = data['conclusao_item']
        creditos_atribuir = data['creditos_atribuir']
        id_item = data['id_item']
        id_usuario = data['id_usuario']

        message, status = avaliacaoItens.avaliar_item(id_item=id_item, id_usuario=id_usuario, conclusao_item=conclusao_item, creditos_atribuir=creditos_atribuir)

        response = make_response(jsonify({"message": 'ok', "status": 200}), 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    
    # Metodo para pegar um item para avaliação de acordo com o id do item
    @staticmethod
    def pegar_item_avaliacao_por_id(id_item):
        avaliacaoItens = AvaliacaoItens()

        return avaliacaoItens.pegar_item_avaliacao_por_id(id_item)
