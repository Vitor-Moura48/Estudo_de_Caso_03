from flask import Flask, request, jsonify, render_template, make_response, session
from app import app
from werkzeug.utils import secure_filename
import secrets
import os
from controller.avaliacao_controller import AvaliacaoItemsController
from core.util import resource_path
from model.cadastro_itens import CadastroItens

app.config['UPLOAD_FOLDER'] = resource_path('static/assets/img')

from controller.autenticacao_controller import AutenticacaoController
from controller.item_controller import ItemController

# pyinstaller -w -F --add-data "templates;templates" --add-data "static;static" --add-data "database;database" app.py

secret_key = secrets.token_hex(16)
app.secret_key = secret_key

@app.route('/')
def index():
    return render_template('index.html')

# Rota para a página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            data = request.get_json()
            session['username'] = data.get('username')
            return AutenticacaoController.autenticar_usuario(data)

        return render_template('auth/login.html')
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/userInfo')
def userInfo():
    try:
        token = request.args.get('token')
        return AutenticacaoController.getUserInfo(token)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/logout')
def logout():
    try:
        token = request.args.get('token')
        return AutenticacaoController.logout(token)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Rota para a página de cadastro
@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        # Verificar se o método é POST, ou seja, se o formulário foi submetido
        if request.method == 'POST':
            data = request.get_json()
            return AutenticacaoController.cadastrar_usuario(data)
        
        return render_template('auth/register.html')
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/menu')
def menu():
    return render_template('menu.html')

# -- inicio
@app.route('/itens_cadastrados')
def itens_cadastrados():
    return render_template('itens_cadastrados.html')

@app.route('/cadastrar_item', methods=['GET', 'POST'])
def cadastrar_item():
    try:
        categorias_itens = CadastroItens.pegar_categorias_itens()

        # Verificar se o método é POST, ou seja, se o formulário foi submetido
        if request.method == 'POST':
            imagem = request.files['foto_item']

            filename = secure_filename(imagem.filename)
            imagemName = secrets.token_hex(8)
            _, extensao = os.path.splitext(filename)
            imagemName = imagemName + extensao

            imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], imagemName))
            return ItemController.cadastrar_item_troca_doacao(request.form, imagemName)
    
        return render_template('cadastrar_item.html', categorias_itens=categorias_itens)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/itensCadastrados')
def api_itens_cadastrados():
    try:
        id_usuario = request.args.get('id_usuario')
        return ItemController.pegar_itens_cadastrados_tr_doa(id_usuario)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
# -- fim


# -- inicio Avaliação de itens + gestao de créditos
@app.route('/avaliacao_itens')
def avaliacao_itens():
    return render_template('avaliacao_itens.html')

@app.route('/api/avaliacaoItens')
def api_avaliacao_itens():
    try:
        return AvaliacaoItemsController.pegar_itens_avaliacao()
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/avaliar_item/<id>')
def avaliar_item(id):
    item = AvaliacaoItemsController.pegar_item_avaliacao_por_id(id)[0]
    print(item)
    return render_template('avaliar_item.html', item=item)

@app.route('/api/avaliarItem', methods=['POST'])
def api_avaliar_item():
    try:
        data = request.get_json()
        return AvaliacaoItemsController.avaliar_item(data)
    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': str(e)})
# -- fim

# -- inicio catalogo de itens
@app.route('/catalogo_itens')
def catalogo_itens():
    return render_template('catalogo_itens.html')


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/gestao_leitos')
def gestao_leitos():
    return render_template('modulo1/index.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

# Rota para a página de splash screen
@app.route('/splash')
def splash():
    return render_template('splash.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404