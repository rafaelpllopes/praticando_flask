from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from dao import JogoDao, UsuarioDao
from models import Jogo, Usuario
import os

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
    try:
        nome = request.form['nome']
        categoria = request.form['categoria']
        console = request.form['console']
        jogo = jogo_dao.salvar(Jogo(nome, categoria, console))
        try:
            upload_path = app.config['UPLOAD_PATH']
            arquivo = request.files['arquivo']
            arquivo.save(f'{upload_path}/{jogo.id}.jpg')
        except:
            pass

        flash('Jogo salvo com sucesso')

    except:
        flash('Ocorreu um erro ao salvar')

    return redirect(url_for('index'))

@app.route('/editar/<id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Usuario deve se logar')
        return  redirect(url_for('login', proxima=url_for('editar')))

    return render_template('editar.html', titulo='Editar Jogo', jogo =jogo_dao.busca_por_id(id), capa_jogo=f'{id}.jpg', usuario=session['usuario_logado'])

@app.route('/atualizar', methods=['POST'])
def atualizar():
    try:

        nome = request.form['nome']
        categoria = request.form['categoria']
        console = request.form['console']
        id = request.form['id']
        jogo = jogo_dao.salvar(Jogo(nome, categoria, console, id))

        try:
            arquivo = request.files['arquivo']
            upload_path = app.config['UPLOAD_PATH']
            arquivo.save(f'{upload_path}/{jogo.id}.jpg')
        except:
            pass

        flash('Jogo atualizado com sucesso')
    except:
        flash('Ocorreu um erro ao salvar')



    return redirect(url_for('index'))


@app.route('/deletar/<id>')
def deletar(id):
    try:
        jogo_dao.deletar(id)
        try:
            upload_path = app.config['UPLOAD_PATH']
            os.remove(f'{upload_path}/{id}.jpg')
        except:
            pass
        flash('O jogo foi removido com sucesso')
    except:
        flash('Ocorreu um erro ao deletar')
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = usuario_dao.autenticar(request.form['usuario'], request.form['senha'])

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

@app.route('/usuario')
def usuario():
    try:
        usuario = session['usuario_logado']
    except KeyError:
        usuario = None

    lista = usuario_dao.listar()
    return render_template('usuario_lista.html', titulo='Usuarios', usuarios=lista, usuario=usuario)

@app.route('/novo_usuario')
def novo_usuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Usuario deve se logar')
        return  redirect(url_for('login', proxima=url_for('novo_usuario')))
    return render_template('novo_usuario.html', titulo='Novo Usuario', usuario=session['usuario_logado'])

@app.route('/criar_usuario', methods=['POST'])
def criar_usuario():
    id = request.form['id']
    nome = request.form['nome']
    senha = request.form['senha']
    usuario_dao.salvar(Usuario(id, nome, senha))

    return redirect(url_for('usuario'))

@app.route('/editar_usuario/<id>')
def editar_usuario(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Usuario deve se logar')
        return  redirect(url_for('login', proxima=url_for('editar_usuario')))

    return render_template('editar_usuario.html', titulo='Editar Usuario', user =usuario_dao.busca_por_id(id), usuario=session['usuario_logado'])

@app.route('/atualizar_usuario', methods=['POST'])
def atualizar_usuario():
    try:
        id = request.form['id']
        nome = request.form['nome']
        senha = request.form['senha']
        usuario_dao.editar(Usuario(id, nome, senha))
        flash('Usuario atualizado com sucesso')
    except:
        flash('Ocorreu um erro ao salvar')

    return redirect(url_for('usuario'))


@app.route('/deletar_usuario/<id>')
def deletar_usuario(id):
    usuario_dao.deletar(id)
    flash('O usuario foi removido com sucesso')
    return redirect(url_for('usuario'))

app.run(port=8000, debug=True)