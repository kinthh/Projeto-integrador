import sqlite3
# esse arquivo foi criado apenas para realizar um teste com um bd

# Conectar ao banco de dados (ou criar um novo)
conn = sqlite3.connect('teste.db')

# Criar um cursor
cursor = conn.cursor()

# Criar a tabela 'usuarios'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
''')

# Inserir alguns dados de exemplo
cursor.execute('INSERT INTO usuarios (nome, email) VALUES (?, ?)', ('Alice', 'alice@example.com'))
cursor.execute('INSERT INTO usuarios (nome, email) VALUES (?, ?)', ('Bob', 'bob@example.com'))
cursor.execute('INSERT INTO usuarios (nome, email) VALUES (?, ?)', ('Carol', 'carol@example.com'))

# Salvar (commit) as alterações
conn.commit()

# Fechar a conexão
conn.close()

print("Banco de dados e tabela criados com sucesso!")