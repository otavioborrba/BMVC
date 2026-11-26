# route.py — ponto de entrada da aplicação BMVC (Bottle + MVC)
import os
from bottle import Bottle, run, static_file

# Garante que os caminhos relativos (views/, static/, data/) funcionem de qualquer pasta
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from controllers.application import Application

app = Bottle()
ctl = Application()


# ---------- Arquivos estáticos (CSS, JS, imagens) ----------
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./static')


# ---------- Login / cadastro (página inicial) ----------
@app.get('/')
@app.get('/login')
def login_get():
    return ctl.login_get()


@app.post('/login')
def login_post():
    return ctl.login_post()


@app.post('/cadastro')
def cadastro_post():
    return ctl.cadastro_post()


@app.get('/logout')
def logout():
    return ctl.logout()


# ---------- CRUD de questões (área restrita: administrador) ----------
@app.get('/questoes')                       # Read (lista)
def questoes_listar():
    return ctl.questoes_listar()


@app.get('/questoes/nova')                  # Create (formulário)
def questao_nova_get():
    return ctl.questao_nova_get()


@app.post('/questoes/nova')                 # Create (salvar)
def questao_nova_post():
    return ctl.questao_nova_post()


@app.get('/questoes/<id:int>/editar')       # Update (formulário)
def questao_editar_get(id):
    return ctl.questao_editar_get(id)


@app.post('/questoes/<id:int>/editar')      # Update (salvar)
def questao_editar_post(id):
    return ctl.questao_editar_post(id)


@app.post('/questoes/<id:int>/excluir')     # Delete
def questao_excluir(id):
    return ctl.questao_excluir(id)


# ---------- Páginas só para quem fez login ----------
@app.get('/guia')
def guia():
    return ctl.guia()


@app.get('/quiz')
def quiz():
    return ctl.quiz()


@app.post('/quiz/resultado')                # recebe o resultado do quiz (JSON)
def quiz_resultado():
    return ctl.quiz_resultado()


@app.get('/desempenho')
def desempenho():
    return ctl.desempenho()


# ---------- Painel do administrador (área restrita) ----------
@app.get('/admin')
def admin():
    return ctl.admin()


@app.post('/admin/usuarios/<email>/perfil')
def admin_alterar_perfil(email):
    return ctl.admin_alterar_perfil(email)


@app.post('/admin/usuarios/<email>/excluir')
def admin_excluir_usuario(email):
    return ctl.admin_excluir_usuario(email)


@app.error(404)
def nao_encontrado(error):
    return ctl.erro404()


if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True, reloader=True)
