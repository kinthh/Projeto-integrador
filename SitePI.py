from flask import Flask

app = Flask(__name__)

# Importar rotas DEPOIS de criar o app
from views import *

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)