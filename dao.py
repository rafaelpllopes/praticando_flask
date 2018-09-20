import sqlite3
from models import Jogo, Usuario

SQL_DELETA_JOGO = 'DELETE FROM jogo where id = %s'
SQL_JOGO_POR_ID = 'SELECT id, nome, categoria, console FROM jogo WHERE id = ?'
SQL_USUARIO_POR_ID = 'SELECT id, nome, senha FROM usuario WHERE id = ? and senha = ?'
SQL_ATUALIZA_JOGO = 'UPDATE jogo SET nome = ?, categoria = ?, console = ? WHERE id = ?'
SQL_BUSCA_JOGOS = 'SELECT id, nome, categoria, console FROM jogo'
SQL_CRIA_JOGO = 'INSERT INTO jogo (nome, categoria, console) VALUES (?, ?, ?)'


class JogoDao:
    def __init__(self):
        self.__db = sqlite3
        self.__db_name = 'db/jogoteca.db'

    def salvar(self, jogo):
        conn = self.__db.connect(self.__db_name)
        cursor = conn.cursor()

        if (jogo.id):
            cursor.execute(SQL_ATUALIZA_JOGO, (jogo.nome, jogo.categoria, jogo.console, jogo.id))
        else:
            cursor.execute(SQL_CRIA_JOGO, (jogo.nome, jogo.categoria, jogo.console))
            jogo.id = cursor.lastrowid

        conn.commit()
        conn.close()
        return jogo

    def listar(self):
        conn = self.__db.connect(self.__db_name)
        cursor = conn.cursor()
        cursor.execute(SQL_BUSCA_JOGOS)
        jogos = traduz_jogos(cursor.fetchall())
        conn.close()
        return jogos

    def busca_por_id(self, id):
        conn = self.__db.connect(self.__db_name)
        cursor = conn.cursor()
        cursor.execute(SQL_JOGO_POR_ID, (id,))
        tupla = cursor.fetchone()
        conn.close()
        return Jogo(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def deletar(self, id):
        conn = self.__db.connect(self.__db_name)
        cursor = conn.cursor()
        cursor.execute(SQL_DELETA_JOGO, (id, ))
        conn.commit()
        conn.close()


class UsuarioDao:
    def __init__(self):
        self.__db = sqlite3
        self.__db_name = 'db/jogoteca.db'

    def buscar_por_id(self, id, senha):
        conn = self.__db.connect(self.__db_name)
        cursor = conn.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id, senha))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        conn.close()
        return usuario


def traduz_jogos(jogos):
    def cria_jogo_com_tupla(tupla):
        return Jogo(tupla[1], tupla[2], tupla[3], id=tupla[0])
    return list(map(cria_jogo_com_tupla, jogos))


def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2])