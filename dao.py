import sqlite3
import uuid
from models import Jogo, Usuario

SQL_DELETA_JOGO = 'DELETE FROM jogo where id = ?'
SQL_JOGO_POR_ID = 'SELECT id, nome, categoria, console FROM jogo WHERE id = ?'
SQL_USUARIO_POR_ID = 'SELECT id, nome FROM usuario WHERE id = ?'
SQL_USUARIO_AUTENTICAR = 'SELECT id, nome FROM usuario WHERE id = ? and senha = ?'
SQL_ATUALIZA_JOGO = 'UPDATE jogo SET nome = ?, categoria = ?, console = ? WHERE id = ?'
SQL_BUSCA_JOGOS = 'SELECT id, nome, categoria, console FROM jogo'
SQL_BUSCA_USUARIOS = 'SELECT id, nome FROM usuario'
SQL_CRIA_JOGO = 'INSERT INTO jogo (id, nome, categoria, console) VALUES (?, ?, ?, ?)'
SQL_CRIA_USUARIO = 'INSERT INTO usuario (id, nome, senha) VALUES (?, ?, ?)'
SQL_ATUALIZA_USUARIO = 'UPDATE usuario SET nome = ?, senha = ? WHERE id = ?'
SQL_DELETA_USUARIO = 'DELETE FROM usuario where id = ?'


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
            id = str(uuid.uuid4())
            cursor.execute(SQL_CRIA_JOGO, (id, jogo.nome, jogo.categoria, jogo.console))
            jogo.id = id

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

    def autenticar(self, id, senha):
        conn = self.__db.connect(self.__db_name)
        cursor = conn.cursor()
        cursor.execute(SQL_USUARIO_AUTENTICAR, (id, senha))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        conn.close()
        return usuario

    def busca_por_id(self, id):
        conn = self.__db.connect(self.__db_name)
        cursor = conn.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        tupla = cursor.fetchone()
        conn.close()
        return Usuario(tupla[0], tupla[1])

    def listar(self):
        conn = self.__db.connect(self.__db_name)
        cursor = conn.cursor()
        cursor.execute(SQL_BUSCA_USUARIOS)
        usuarios = traduz_usuarios(cursor.fetchall())
        conn.close()
        return usuarios

    def salvar(self, usuario):
        conn = self.__db.connect(self.__db_name)
        cursor = conn.cursor()
        cursor.execute(SQL_CRIA_USUARIO, (usuario.id, usuario.nome, usuario.senha))
        conn.commit()
        conn.close()

    def editar(self, usuario):
        conn = self.__db.connect(self.__db_name)
        cursor = conn.cursor()
        cursor.execute(SQL_ATUALIZA_USUARIO, (usuario.nome, usuario.senha, usuario.id))
        conn.commit()
        conn.close()

    def deletar(self, id):
        conn = self.__db.connect(self.__db_name)
        cursor = conn.cursor()
        cursor.execute(SQL_DELETA_USUARIO, (id, ))
        conn.commit()
        conn.close()


def traduz_jogos(jogos):
    def cria_jogo_com_tupla(tupla):
        return Jogo(tupla[1], tupla[2], tupla[3], id=str(tupla[0]))
    return list(map(cria_jogo_com_tupla, jogos))


def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1])

def traduz_usuarios(usuarios):
    return list(map(traduz_usuario, usuarios))