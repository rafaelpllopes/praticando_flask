from flask import Flask, render_template,  request

app = Flask(__name__)

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
    return render_template('lista.html', titulo='Jogos', jogos=lista)


app.run(port=8000, debug=True)