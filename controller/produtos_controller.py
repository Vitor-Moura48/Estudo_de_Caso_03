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
    
    # Metodo para adiquirir um produto
    # @staticmethod
    # def adquirir_produto(id_item, id_comprador):
    #     produtos = ProdutoItem()
    #     avaliacao = AvaliacaoItens()

    #     item = produtos.pegar_item_por_id(id_item)
    #     item['status'] = 2
    #     produtos.atualizar_item(item)

    #     avaliacao.adicionar_avaliacao_item(id_item, id_comprador)

    #     return True
