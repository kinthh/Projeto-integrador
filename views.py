from SitePI import app
from flask import render_template, request, render_template_string
import sqlite3

def buscar_atividades(filtro=None, valor=None):
    conn = sqlite3.connect('Banco_Dados_PI1.db')
    cursor = conn.cursor()
    
    query = """
    SELECT 
        a.id,
        m.nome as modalidade,
        a.turno,
        a.idade,
        n.nome as nivel,
        a.horario,
        a.dias_semana,
        a.analista,
        a.local,
        a.disponivel_em
    FROM atividades a
    JOIN modalidades m ON a.modalidade_id = m.id
    LEFT JOIN niveis n ON a.nivel_id = n.id
    """
    
    if filtro and valor:
        if filtro == 'modalidade':
            query += " WHERE m.nome LIKE ?"
        elif filtro == 'nivel':
            query += " WHERE n.nome LIKE ?"
        else:
            query += f" WHERE a.{filtro} LIKE ?"
        
        cursor.execute(query, ('%' + valor + '%',))
    else:
        cursor.execute(query)
    
    resultados = cursor.fetchall()
    conn.close()
    return resultados

@app.route('/')
@app.route('/')
def homepage():
    conn = sqlite3.connect('Banco_Dados_PI1.db')
    cursor = conn.cursor()

    modalidades = [row[0] for row in cursor.execute("""
        SELECT DISTINCT m.nome 
        FROM atividades a
        JOIN modalidades m ON a.modalidade_id = m.id
        ORDER BY m.nome ASC
    """)]

    niveis = [row[0] for row in cursor.execute("""
        SELECT DISTINCT n.nome 
        FROM atividades a
        JOIN niveis n ON a.nivel_id = n.id
        ORDER BY n.nome ASC
    """)]

    faixas = [row[0] for row in cursor.execute("""
        SELECT DISTINCT idade 
        FROM atividades
        WHERE idade IS NOT NULL
        ORDER BY 
        CASE 
            WHEN idade GLOB '[0-9]*' THEN CAST(idade AS INTEGER)
            ELSE 999  -- Para valores não numéricos
        END ASC
    """)]


    conn.close()
    return render_template('homepage.html', modalidades=modalidades, niveis=niveis, faixas=faixas)



@app.route('/contatos')
def contatos():
    return render_template('contatos.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/buscar', methods=['GET'])
@app.route('/buscar')
@app.route('/buscar')
@app.route('/buscar', methods=['GET'])

def buscar():
    modalidade = request.args.get('modalidade', '')
    nivel = request.args.get('nivel', '')
    idade = request.args.get('idade', '')
    busca = request.args.get('busca', '')

    conn = sqlite3.connect('Banco_Dados_PI1.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    SELECT 
        a.id,
        m.nome as modalidade,
        a.turno,
        a.idade,
        n.nome as nivel,
        a.horario,
        a.dias_semana,
        a.analista,
        a.local,
        a.disponivel_em
    FROM atividades a
    JOIN modalidades m ON a.modalidade_id = m.id
    LEFT JOIN niveis n ON a.nivel_id = n.id
    WHERE 1=1
    """
    params = []

    if modalidade:
        query += " AND m.nome = ?"
        params.append(modalidade)
    if nivel:
        query += " AND n.nome = ?"
        params.append(nivel)
    if idade:
        query += " AND a.idade = ?"
        params.append(idade)
    if busca:
        query += " AND (m.nome LIKE ? OR n.nome LIKE ? OR a.idade LIKE ? OR a.horario LIKE ? OR a.dias_semana LIKE ? OR a.analista LIKE ? OR a.local LIKE ? OR a.disponivel_em LIKE ?)"
        search_term = f"%{busca}%"
        params.extend([search_term]*8)

    resultados = cursor.execute(query, params).fetchall()
    conn.close()

    return render_template_string('''
        {% if resultados %}
            <div class="resultados-container">
                {% for atividade in resultados %}
                    <div class="atividade-card">
                        <h3>{{ atividade['modalidade'] }}</h3>
                        <p><strong>Turno:</strong> {{ atividade['turno'] }}</p>
                        <p><strong>Idade:</strong> {{ atividade['idade'] if atividade['idade'] else 'Não especificado' }}</p>
                        <p><strong>Nível:</strong> {{ atividade['nivel'] if atividade['nivel'] else 'Não especificado' }}</p>
                        <p><strong>Horário:</strong> {{ atividade['horario'] }}</p>
                        <p><strong>Dias:</strong> {{ atividade['dias_semana'] }}</p>
                        <p><strong>Analista:</strong> {{ atividade['analista'] if atividade['analista'] else 'Não especificado' }}</p>
                        <p><strong>Local:</strong> {{ atividade['local'] if atividade['local'] else 'Não especificado' }}</p>
                        <p><strong>Disponível em:</strong> {{ atividade['disponivel_em'] if atividade['disponivel_em'] else 'CEU Rosa da China' }}</p>
                    </div>
                {% endfor %}
            </div>
        {% else %}
            <p class="no-results">Nenhuma atividade encontrada.</p>
        {% endif %}
    ''', resultados=resultados)
