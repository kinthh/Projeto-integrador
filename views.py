from SitePI import app
from flask import render_template
@app.route('/')
def homepage():
    return render_template('homepage.html')
'Possivel segunda pagina'
@app.route('/contatos')
def contatos():
    return render_template('contatos.html')
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

