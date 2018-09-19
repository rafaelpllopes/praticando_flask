from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)

app.secret_key = 'teste'

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha

usuario1 = Usuario('teste1', 'Usuario teste 1', '1234')
usuario2 = Usuario('teste2', 'Usuario teste 2', '5678')

usuarios = {usuario1.id: usuario1,
            usuario2.id: usuario2}

lista = []
lista.append(Jogo('Super Mario', 'Ação', 'SNES'))
lista.append(Jogo('Pokemon Gold', 'RPG', 'GBA'))
lista.append(Jogo('Mortal Kombat', 'Luta', 'SNES'))

@app.route('/')
def index():
    try:
        usuario = session['usuario_logado']
    except KeyError:
        usuario = None

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
    lista.append(Jogo(nome, categoria, console))
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = request.form['usuario']
    senha = request.form['senha']
    print(usuario in usuarios)
    print(usuarios['teste1'].id)
    if usuario in usuarios:
        user = usuarios[usuario]
        if user.senha == senha:
            session['usuario_logado'] = user.id
            flash(user.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Usuario ou senha incorreto')
            return redirect(url_for('login'))
    else:
        flash('Usuario ou senha incorreto')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout realizado com sucesso')
    return redirect(url_for('index'))



app.run(port=8000, debug=True)