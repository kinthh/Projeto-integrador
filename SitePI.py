'''
Este é o código para criar um site com Python utilizando a biblioteca Flask.
O objetivo é criar uma aplicação web, com um banco de dados e verificação de versão.
O banco de dados terá as atividades disponiveis no CEU e instituições que disponibilizem,
qualquer atividade gratuita.
'''

'Primeira etapa é instalar a bliblioteca e importar para utilizar no codigo.'

from flask import Flask, render_template
import sqlite3

'from flask import sqlalchemy VERIFICAR SE ESTÁ CORRETO!!!!'


app = Flask(__name__)

'criar a página inicial'
'é necessário o route para carregar a pagina e uma funcão que mostra o que vai aparecer na pagina'

from views import *


'O comando abaixo é necessário para colocar o site no ar'
if __name__ == '__main__':
    app.run(debug=True)



