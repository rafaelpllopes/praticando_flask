from flask import Flask, render_template

app = Flask(__name__)

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

@app.route('/inicio')
def ola():
    lista = [Jogo('Super Mario', 'Ação', 'SNES'), Jogo('Pokemon Gold', 'RPG', 'GBA'), Jogo('Mortal Kombat', 'Luta', 'SNES')]
    return render_template('lista.html', titulo='Jogos', jogos=lista)

app.run(port=8000)