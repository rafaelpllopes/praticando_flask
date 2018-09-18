from flask import Flask, render_template, request, redirect, session, flash

app = Flask(__name__)

app.secret_key = 'teste'

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


lista = []
lista.append(Jogo('Super Mario', 'Ação', 'SNES'))
lista.append(Jogo('Pokemon Gold', 'RPG', 'GBA'))
lista.append(Jogo('Mortal Kombat', 'Luta', 'SNES'))

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    lista.append(Jogo(nome, categoria, console))
    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    if request.form['senha'] == 'mestra' and request.form['usuario'] == 'teste':
        session['usuario_logado'] = request.form['usuario']
        flash(request.form['usuario'] + ' logou com sucesso')
        return redirect('/')
    else:
        flash('Usuario ou senha incorreto')
        return redirect('/login')

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout realizado com sucesso')
    return redirect('/login')



app.run(port=8000, debug=True)