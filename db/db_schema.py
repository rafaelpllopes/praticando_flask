import sqlite3
import uuid
import os

os.remove('jogoteca.db')

conn = sqlite3.connect("jogoteca.db")
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS jogo (
        id BLOB UNIQUE PRIMARY KEY,
        nome VARCHAR(50) NOT NULL,
        categoria VARCHAR(40) NOT NULL,
        console VARCHAR(20) NOT NULL,
        capa VARCHAR(100)
    );
    """)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS usuario (
        id VARCHAR(8) UNIQUE NOT NULL PRIMARY KEY,
        nome VARCHAR(20) NOT NULL,
        senha varchar(8) NOT NULL        
    );
""")

cursor.execute(
    """
    INSERT INTO usuario (id, nome, senha) VALUES ('admin', 'Administrador', 'admin');
""")

conn.commit()

"""

def uuid():
    return "select substr(u,1,8)||'-'||substr(u,9,4)||'-4'||substr(u,13,3)||'-'||v||substr(u,17,3)||'-'||substr(u,21,12) from (select lower(hex(randomblob(16))) as u, substr('89ab',abs(random()) % 4 + 1, 1) as v);"
"""

cursor.executemany(
    'INSERT INTO jogo (id, nome, categoria, console) VALUES (?, ?, ?, ?)',
    [
        (str(uuid.uuid4()), 'God of War 4', 'Ação', 'PS4'),
        (str(uuid.uuid4()), 'NBA 2k18', 'Esporte', 'Xbox One'),
        (str(uuid.uuid4()), 'Rayman Legends', 'Indie', 'PS4'),
        (str(uuid.uuid4()), 'Super Mario RPG', 'RPG', 'SNES'),
        (str(uuid.uuid4()), 'Super Mario Kart', 'Corrida', 'SNES'),
        (str(uuid.uuid4()), 'Fire Emblem Echoes', 'Estratégia', '3DS')
    ])

conn.commit()

conn.close()
