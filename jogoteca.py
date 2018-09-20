from flask import Flask, render_template, request, redirect, session, flash, url_for
from dao import JogoDao, UsuarioDao
from models import Jogo, Usuario

app = Flask(__name__)

app.secret_key = 'teste'

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
    jogo_dao.salvar(Jogo(nome, categoria, console))
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



app.run(port=8000, debug=True)