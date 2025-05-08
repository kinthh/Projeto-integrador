import sqlite3

Source_base = 'C:/Users/Rodrigo/Downloads/Projeto Integrado 1 TESTE DE FUNCIONALIDADES/pythonProject'

Source1 = Source_base + '/BD_PI1.sql'
Source2 = Source_base + '/Insert.sql'

# 1. Conecta ao banco de dados (cria se não existir)
banco_final = Source_base + '/Banco_Dados_PI1.db'
conn = sqlite3.connect(banco_final)
cursor = conn.cursor()

# 2. Lê e executa o arquivo principal (BD_PI1.sql)
with open(Source1, 'r', encoding='utf-8') as f:
    cursor.executescript(f.read())

with open(Source2, 'r', encoding='utf-8') as f:
    cursor.executescript(f.read())


# 4. Salva e fecha
conn.commit()
conn.close()

print("Banco criado e dados inseridos com sucesso!")