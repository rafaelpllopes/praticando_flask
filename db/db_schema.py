import sqlite3

conn = sqlite3.connect("jogoteca.db")
cursor = conn.cursor()


cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS jogo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(50) NOT NULL,
        categoria VARCHAR(40) NOT NULL,
        console VARCHAR(20) NOT NULL );
    """)

cursor.execute(
"""
    CREATE TABLE IF NOT EXISTS usuario (
        id VARCHAR(8) NOT NULL PRIMARY KEY,
        nome VARCHAR(20) NOT NULL,
        senha varchar(8) NOT NULL        
    );
""")

cursor.execute(
    """
    INSERT INTO usuario (id, nome, senha) VALUES ('admin', 'Administrador', 'admin');
    """
)
conn.commit()

cursor.executemany(
      'INSERT INTO jogo (nome, categoria, console) VALUES (?, ?, ?)',
      [
            ('God of War 4', 'Ação', 'PS4'),
            ('NBA 2k18', 'Esporte', 'Xbox One'),
            ('Rayman Legends', 'Indie', 'PS4'),
            ('Super Mario RPG', 'RPG', 'SNES'),
            ('Super Mario Kart', 'Corrida', 'SNES'),
            ('Fire Emblem Echoes', 'Estratégia', '3DS')
      ])

conn.commit()

conn.close()



