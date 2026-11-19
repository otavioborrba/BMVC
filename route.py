# route.py — ponto de entrada da aplicação BMVC (Bottle + MVC)
import os
from bottle import Bottle, run, static_file

# Garante que os caminhos relativos (views/, static/) funcionem de qualquer pasta
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from controllers.application import Application

app = Bottle()
ctl = Application()


# ---------- Arquivos estáticos (CSS, JS, imagens) ----------
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./static')


# ---------- Páginas ----------
@app.route('/')
@app.route('/home')
def home():
    return ctl.render('home')


@app.error(404)
def nao_encontrado(error):
    return ctl.render('erro404')


if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True, reloader=True)
