import sqlite3

class Database:
    def __init__(self, db_name='eventos.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS participantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
                data_nascimento TEXT NOT NULL,
                endereco TEXT NOT NULL,
                telefone TEXT NOT NULL,
                sexo TEXT NOT NULL,
                senha TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                data_inicio TEXT NOT NULL,
                hora_inicio TEXT NOT NULL,
                data_fim TEXT NOT NULL,
                hora_fim TEXT NOT NULL,
                local TEXT NOT NULL,
                preco REAL NOT NULL,
                lotacao_maxima INTEGER NOT NULL,
                num_participantes INTEGER DEFAULT 0,
                categoria TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS participantes_eventos (
                participante_id INTEGER,
                evento_id INTEGER,
                FOREIGN KEY(participante_id) REFERENCES participantes(id),
                FOREIGN KEY(evento_id) REFERENCES eventos(id),
                PRIMARY KEY (participante_id, evento_id)
            )
        ''')
        self.conn.commit()

    def add_participante(self, nome, cpf, data_nascimento, endereco, telefone, sexo, senha):
        self.cursor.execute('''
            INSERT INTO participantes (nome, cpf, data_nascimento, endereco, telefone, sexo, senha) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nome, cpf, data_nascimento, endereco, telefone, sexo, senha))
        self.conn.commit()

    def edit_participante(self, participante_id, nome, cpf, data_nascimento, endereco, telefone, sexo, senha):
        self.cursor.execute('''
            UPDATE participantes
            SET nome = ?, cpf = ?, data_nascimento = ?, endereco = ?, telefone = ?, sexo = ?, senha = ?
            WHERE id = ?
        ''', (nome, cpf, data_nascimento, endereco, telefone, sexo, senha, participante_id))
        self.conn.commit()

    def delete_participante(self, participante_id):
        self.cursor.execute('DELETE FROM participantes WHERE id = ?', (participante_id,))
        self.conn.commit()

    def get_participante(self, participante_id):
        self.cursor.execute('SELECT * FROM participantes WHERE id = ?', (participante_id,))
        return self.cursor.fetchone()

    def get_participantes(self):
        self.cursor.execute('SELECT * FROM participantes')
        return self.cursor.fetchall()

    def add_evento(self, nome, data_inicio, hora_inicio, data_fim, hora_fim, local, preco, lotacao_maxima,num_participantes, categoria):
        self.cursor.execute('''
            INSERT INTO eventos (nome, data_inicio, hora_inicio, data_fim, hora_fim, local, preco, lotacao_maxima, num_participantes,categoria) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?)
        ''', (nome, data_inicio, hora_inicio, data_fim, hora_fim, local, preco, lotacao_maxima, num_participantes,categoria))
        self.conn.commit()

    def edit_evento(self, evento_id, nome, data_inicio, hora_inicio, data_fim, hora_fim, local, preco, lotacao_maxima, num_participantes, categoria):
        self.cursor.execute('''
            UPDATE eventos
            SET nome = ?, data_inicio = ?, hora_inicio = ?, data_fim = ?, hora_fim = ?, local = ?, preco = ?, lotacao_maxima = ?, num_participantes = ?, categoria = ?
            WHERE id = ?
        ''', (nome, data_inicio, hora_inicio, data_fim, hora_fim, local, preco, lotacao_maxima, num_participantes, categoria, evento_id))
        self.conn.commit()


    def delete_evento(self, evento_id):
        self.cursor.execute('DELETE FROM eventos WHERE id = ?', (evento_id,))
        self.conn.commit()

    def get_evento(self, evento_id):
        self.cursor.execute('SELECT * FROM eventos WHERE id = ?', (evento_id,))
        return self.cursor.fetchone()

    def get_eventos(self):
        self.cursor.execute('SELECT * FROM eventos')
        return self.cursor.fetchall()

    def get_eventos_por_participante(self, participante_id):
        self.cursor.execute('''
            SELECT e.* FROM eventos e
            JOIN participantes_eventos pe ON e.id = pe.evento_id
            WHERE pe.participante_id = ?
        ''', (participante_id,))
        return self.cursor.fetchall()

    def get_eventos_paginados(self, pagina_atual, eventos_por_pagina):
        inicio = (pagina_atual - 1) * eventos_por_pagina
        self.cursor.execute('SELECT * FROM eventos LIMIT ? OFFSET ?', (eventos_por_pagina, inicio))
        return self.cursor.fetchall()
    
    def validate_user(self, nome,  senha):
        self.cursor.execute("SELECT * FROM participantes WHERE nome = ? and senha = ?", 
                            (nome, senha))
        return self.cursor.fetchone() 

    def buscar_eventos(self, nome=None, categoria=None, local=None):
        query = "SELECT * FROM eventos WHERE 1=1"
        params = []
        if nome:
            query += " AND nome LIKE ?"
            params.append(f"%{nome}%")
        if categoria:
            query += " AND categoria = ?"
            params.append(categoria)
        if local:
            query += " AND local LIKE ?"
            params.append(f"%{local}%")
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def relacionar_participante_evento(self, participante_id, evento_id):
        self.cursor.execute('''
            INSERT INTO participantes_eventos (participante_id, evento_id)
            VALUES (?, ?)
        ''', (participante_id, evento_id))
        self.conn.commit()

    def close(self):
        self.conn.close()
