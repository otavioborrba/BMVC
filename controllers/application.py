# controllers/application.py — Controller: recebe as requisições e escolhe a view
import json

from bottle import template, request, response, redirect

from models.pagina import Pagina
from models.questao import PILARES
from models.repositorio import RepositorioUsuarios, RepositorioQuestoes, RepositorioResultados
from models.resultado import Desempenho

SEGREDO_COOKIE = 'troque-este-segredo-bmvc'

MENSAGENS = {
    'criada': 'Questão criada com sucesso!',
    'editada': 'Questão atualizada!',
    'excluida': 'Questão excluída.',
    'bemvindo': 'Login feito. Bons estudos!',
    'conta': 'Conta criada. Bem-vindo(a)!',
    'saiu': 'Você saiu da sua conta.',
}


class Application:

    def __init__(self):
        self.usuarios = RepositorioUsuarios()
        self.questoes = RepositorioQuestoes()
        self.resultados = RepositorioResultados()

    # ------------------------------------------------------------------
    # Sessão (cookie assinado com o e-mail do usuário logado)
    # ------------------------------------------------------------------
    def usuario_logado(self):
        email = request.get_cookie('usuario', secret=SEGREDO_COOKIE)
        return self.usuarios.buscar(email) if email else None

    def exigir_login(self):
        usuario = self.usuario_logado()
        if usuario is None:
            redirect('/')
        return usuario

    def _entrar(self, usuario):
        response.set_cookie('usuario', usuario.email, secret=SEGREDO_COOKIE,
                            path='/', httponly=True)

    def _mensagem(self):
        return MENSAGENS.get(request.query.msg, '')

    # ------------------------------------------------------------------
    # Páginas gerais
    # ------------------------------------------------------------------
    def guia(self):
        usuario = self.exigir_login()
        desempenho = Desempenho(self.resultados.do_usuario(usuario.email))
        return template('views/html/guia', pagina=Pagina.home(), usuario=usuario,
                        desempenho=desempenho, mensagem=self._mensagem())

    def erro404(self):
        return template('views/html/erro404', usuario=self.usuario_logado())

    # ------------------------------------------------------------------
    # Login / cadastro / logout
    # ------------------------------------------------------------------
    def login_get(self, erro='', aba='entrar', dados=None):
        if self.usuario_logado():
            redirect('/guia')
        return template('views/html/login', erro=erro, aba=aba,
                        dados=dados or {}, usuario=None,
                        mensagem=self._mensagem(),
                        total=len(self.questoes.listar()))

    def login_post(self):
        email = request.forms.getunicode('email', '')
        senha = request.forms.getunicode('senha', '')
        usuario = self.usuarios.autenticar(email, senha)
        if usuario is None:
            return self.login_get(erro='E-mail ou senha incorretos.',
                                  dados={'email': email})
        self._entrar(usuario)
        redirect('/guia?msg=bemvindo')

    def cadastro_post(self):
        nome = request.forms.getunicode('nome', '')
        email = request.forms.getunicode('email', '')
        senha = request.forms.getunicode('senha', '')
        try:
            usuario = self.usuarios.cadastrar(nome, email, senha)
        except ValueError as e:
            return self.login_get(erro=str(e), aba='cadastro',
                                  dados={'nome': nome, 'email': email})
        self._entrar(usuario)
        redirect('/guia?msg=conta')

    def logout(self):
        response.delete_cookie('usuario', path='/')
        redirect('/?msg=saiu')

    # ------------------------------------------------------------------
    # CRUD de questões (qualquer usuário logado)
    # ------------------------------------------------------------------
    def questoes_listar(self):
        usuario = self.exigir_login()
        questoes = sorted(self.questoes.listar(), key=lambda q: q.id)
        return template('views/html/questoes', usuario=usuario,
                        questoes=questoes, pilares=PILARES,
                        mensagem=self._mensagem())

    def _form(self, usuario, questao=None, erro='', dados=None):
        if dados is None and questao is not None:
            dados = {'enunciado': questao.enunciado,
                     'alternativas': questao.alternativas,
                     'correta': questao.correta, 'pilar': questao.pilar}
        dados = dados or {'enunciado': '', 'alternativas': [],
                          'correta': 0, 'pilar': PILARES[0]}
        return template('views/html/questao_form', usuario=usuario,
                        questao=questao, dados=dados, erro=erro,
                        pilares=PILARES)

    def _dados_do_formulario(self):
        alternativas = [request.forms.getunicode('alt%d' % i, '') for i in range(4)]
        try:
            correta = int(request.forms.get('correta', '0'))
        except ValueError:
            correta = 0
        # a posição da correta tem que contar só as alternativas preenchidas
        preenchidas = [i for i, a in enumerate(alternativas) if a.strip()]
        correta_ajustada = preenchidas.index(correta) if correta in preenchidas else -1
        return {
            'enunciado': request.forms.getunicode('enunciado', ''),
            'alternativas': alternativas,
            'correta': correta,
            'correta_ajustada': correta_ajustada,
            'pilar': request.forms.getunicode('pilar', ''),
        }

    def questao_nova_get(self):
        return self._form(self.exigir_login())

    def questao_nova_post(self):
        usuario = self.exigir_login()
        d = self._dados_do_formulario()
        try:
            self.questoes.criar(d['enunciado'], d['alternativas'],
                                d['correta_ajustada'], d['pilar'], usuario.primeiro_nome)
        except ValueError as e:
            return self._form(usuario, erro=str(e), dados=d)
        redirect('/questoes?msg=criada')

    def questao_editar_get(self, id):
        usuario = self.exigir_login()
        questao = self.questoes.buscar(id)
        if questao is None:
            return self.erro404()
        return self._form(usuario, questao)

    def questao_editar_post(self, id):
        usuario = self.exigir_login()
        questao = self.questoes.buscar(id)
        if questao is None:
            return self.erro404()
        d = self._dados_do_formulario()
        try:
            self.questoes.atualizar(id, d['enunciado'], d['alternativas'],
                                    d['correta_ajustada'], d['pilar'])
        except ValueError as e:
            return self._form(usuario, questao, erro=str(e), dados=d)
        redirect('/questoes?msg=editada')

    def questao_excluir(self, id):
        self.exigir_login()
        try:
            self.questoes.excluir(id)
        except KeyError:
            return self.erro404()
        redirect('/questoes?msg=excluida')

    # ------------------------------------------------------------------
    # Quiz e desempenho (qualquer usuário logado)
    # ------------------------------------------------------------------
    def quiz(self):
        usuario = self.exigir_login()
        lista = [{'id': q.id, 'enunciado': q.enunciado, 'alternativas': q.alternativas,
                  'correta': q.correta, 'pilar': q.pilar}
                 for q in self.questoes.listar()]
        # evita que um "</script>" digitado numa questão quebre a página
        dados_json = json.dumps(lista, ensure_ascii=False).replace('</', '<\\/')
        return template('views/html/quiz', usuario=usuario, dados_json=dados_json,
                        total=len(lista), pilares=PILARES)

    def quiz_resultado(self):
        """Recebe as respostas do quiz (JSON), corrige no servidor e salva."""
        usuario = self.usuario_logado()
        if usuario is None:
            response.status = 401
            return {'erro': 'login necessário'}
        dados = request.json or {}
        respostas = []
        for r in dados.get('respostas', []):
            questao = self.questoes.buscar(int(r.get('id', 0)))
            if questao is not None:
                respostas.append({'pilar': questao.pilar,
                                  'acertou': int(r.get('escolha', -1)) == questao.correta})
        if not respostas:
            response.status = 400
            return {'erro': 'nenhuma resposta válida'}
        resultado = self.resultados.registrar(usuario.email, respostas)
        geral = Desempenho(self.resultados.do_usuario(usuario.email))
        return {'acertos': resultado.acertos, 'total': resultado.total,
                'percentual': resultado.percentual, 'indice_geral': geral.indice_geral}

    def desempenho(self):
        usuario = self.exigir_login()
        desempenho = Desempenho(self.resultados.do_usuario(usuario.email))
        return template('views/html/desempenho', usuario=usuario, desempenho=desempenho)
