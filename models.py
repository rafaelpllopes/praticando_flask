class Jogo:
    def __init__(self, nome, categoria, console, capa=None, id=None):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.console = console
        self.capa = capa

class Usuario:
    def __init__(self, id, nome, senha=None):
        self.id = id
        self.nome = nome
        self.senha = senha