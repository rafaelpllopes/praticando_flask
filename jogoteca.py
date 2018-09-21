from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from dao import JogoDao, UsuarioDao
from models import Jogo
import os
#import uuid

app = Flask(__name__)

app.secret_key = 'teste'
app.config['UPLOAD_PATH'] = \
    os.path.dirname(os.path.abspath(__file__)) + '/uploads'

jogo_dao = JogoDao()
usuario_dao = UsuarioDao()

@app.route('/')
def index():
    try:
        usuario = session['usuario_logado']
    except KeyError:
        usuario = None

    lista = jogo_dao.listar()

    return render_template('lista.html', titulo='Jogos', jogos=lista, usuario=usuario)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Usuario deve se logar')
        return  redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo', usuario=session['usuario_logado'])

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = jogo_dao.salvar(Jogo(nome, categoria, console))

    upload_path = app.config['UPLOAD_PATH']
    arquivo = request.files['arquivo']
    arquivo.save(f'{upload_path}/{jogo.id}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Usuario deve se logar')
        return  redirect(url_for('login', proxima=url_for('editar')))

    return render_template('editar.html', titulo='Editar Jogo', jogo =jogo_dao.busca_por_id(id), capa_jogo=f'{id}.jpg', usuario=session['usuario_logado'])

@app.route('/atualizar', methods=['POST'])
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    id = request.form['id']
    jogo = jogo_dao.salvar(Jogo(nome, categoria, console, id))
    upload_path = app.config['UPLOAD_PATH']
    arquivo = request.files['arquivo']
    arquivo.save(f'{upload_path}/{jogo.id}.jpg')

    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    jogo_dao.deletar(id)
    upload_path = app.config['UPLOAD_PATH']
    os.remove(f'{upload_path}/{id}.jpg')
    flash('O jogo foi removido com sucesso')
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'], request.form['senha'])

    if usuario:
        session['usuario_logado'] = usuario.id
        flash(usuario.nome + ' logou com sucesso!')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)
    else:
        flash('Usuario ou senha incorreto')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout realizado com sucesso')
    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagens(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

app.run(port=8000, debug=True)