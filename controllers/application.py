# controllers/application.py — Controller: recebe as requisições e escolhe a view
import json

from bottle import template, request, response, redirect, HTTPResponse

from models.pagina import Pagina
from models.questao import PILARES
from models.repositorio import RepositorioUsuarios, RepositorioQuestoes, RepositorioResultados
from models.resultado import Desempenho
from controllers.tempo_real import CentralTempoReal

SEGREDO_COOKIE = 'troque-este-segredo-bmvc'

MENSAGENS = {
    'criada': 'Questão criada com sucesso!',
    'editada': 'Questão atualizada!',
    'excluida': 'Questão excluída.',
    'bemvindo': 'Login feito. Bons estudos!',
    'conta': 'Conta criada. Bem-vindo(a)!',
    'saiu': 'Você saiu da sua conta.',
    'promovido': 'Usuário promovido a administrador.',
    'rebaixado': 'Usuário voltou a ser estudante.',
    'usuario_excluido': 'Usuário excluído.',
    'proprio': 'Você não pode alterar ou excluir a sua própria conta pelo painel.',
    'ultimo_admin': 'O sistema precisa ter pelo menos um administrador.',
}


class Application:

    def __init__(self, tempo_real=None):
        self.usuarios = RepositorioUsuarios()
        self.questoes = RepositorioQuestoes()
        self.resultados = RepositorioResultados()
        # central do WebSocket: avisa as páginas abertas quando algo muda
        self.tempo_real = tempo_real or CentralTempoReal()

    # ------------------------------------------------------------------
    # Renderização: páginas de quem está logado recebem um token para o WebSocket
    # ------------------------------------------------------------------
    def _render(self, nome, **dados):
        usuario = dados.get('usuario')
        if usuario is not None:
            dados['ws_token'] = self.tempo_real.token_para(usuario)
            dados['ws_porta'] = self.tempo_real.porta
        return template(nome, **dados)

    # ------------------------------------------------------------------
    # Dados que são enviados em tempo real
    # ------------------------------------------------------------------
    def _ranking(self):
        linhas = []
        for u in self.usuarios.listar():
            d = Desempenho(self.resultados.do_usuario(u.email))
            if d.quizzes:
                linhas.append({'nome': u.nome, 'quizzes': d.quizzes, 'acertos': d.acertos,
                               'respondidas': d.respondidas, 'indice': d.indice_geral})
        linhas.sort(key=lambda l: (-l['indice'], -l['respondidas'], l['nome'].lower()))
        for posicao, linha in enumerate(linhas, start=1):
            linha['posicao'] = posicao
        return linhas

    def _estatisticas(self):
        geral = Desempenho(self.resultados.listar())
        return {'usuarios': len(self.usuarios.listar()),
                'admins': self.usuarios.total_admins(),
                'questoes': len(self.questoes.listar()),
                'quizzes': geral.quizzes,
                'indice': '%d%%' % geral.indice_geral if geral.respondidas else '—'}

    def _avisar(self, icone, texto, autor='', ranking=False, questoes=False):
        """Publica uma atividade e os dados que mudaram para as páginas abertas."""
        self.tempo_real.registrar_atividade(icone, texto, autor)
        if ranking:
            self.tempo_real.publicar('ranking', self._ranking())
        if questoes:
            self.tempo_real.publicar('questoes', {'total': len(self.questoes.listar())})
        self.tempo_real.publicar('estatisticas', self._estatisticas(), so_admin=True)

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

    def exigir_acesso(self, area):
        """Controle de acesso: sem login vai para o login;
        logado sem permissão recebe a página de acesso restrito (403)."""
        usuario = self.exigir_login()
        if not usuario.pode_acessar(area):
            pagina = self._render('views/html/restrito', usuario=usuario)
            raise HTTPResponse(body=pagina, status=403)
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
        usuario = self.exigir_acesso('guia')
        desempenho = Desempenho(self.resultados.do_usuario(usuario.email))
        return self._render('views/html/guia', pagina=Pagina.home(), usuario=usuario,
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
        self._avisar('👋', f'{usuario.nome} criou uma conta na OOficina', usuario.email)
        redirect('/guia?msg=conta')

    def logout(self):
        response.delete_cookie('usuario', path='/')
        redirect('/?msg=saiu')

    # ------------------------------------------------------------------
    # CRUD de questões (área restrita: somente administrador)
    # ------------------------------------------------------------------
    def questoes_listar(self):
        usuario = self.exigir_acesso('questoes')
        questoes = sorted(self.questoes.listar(), key=lambda q: q.id)
        return self._render('views/html/questoes', usuario=usuario,
                        questoes=questoes, pilares=PILARES,
                        mensagem=self._mensagem())

    def _form(self, usuario, questao=None, erro='', dados=None):
        if dados is None and questao is not None:
            dados = {'enunciado': questao.enunciado,
                     'alternativas': questao.alternativas,
                     'correta': questao.correta, 'pilar': questao.pilar}
        dados = dados or {'enunciado': '', 'alternativas': [],
                          'correta': 0, 'pilar': PILARES[0]}
        return self._render('views/html/questao_form', usuario=usuario,
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
        return self._form(self.exigir_acesso('questoes'))

    def questao_nova_post(self):
        usuario = self.exigir_acesso('questoes')
        d = self._dados_do_formulario()
        try:
            nova = self.questoes.criar(d['enunciado'], d['alternativas'],
                                       d['correta_ajustada'], d['pilar'], usuario.primeiro_nome)
        except ValueError as e:
            return self._form(usuario, erro=str(e), dados=d)
        self._avisar('📝', f'{usuario.primeiro_nome} criou a questão #{nova.id} ({nova.pilar})',
                     usuario.email, questoes=True)
        redirect('/questoes?msg=criada')

    def questao_editar_get(self, id):
        usuario = self.exigir_acesso('questoes')
        questao = self.questoes.buscar(id)
        if questao is None:
            return self.erro404()
        return self._form(usuario, questao)

    def questao_editar_post(self, id):
        usuario = self.exigir_acesso('questoes')
        questao = self.questoes.buscar(id)
        if questao is None:
            return self.erro404()
        d = self._dados_do_formulario()
        try:
            self.questoes.atualizar(id, d['enunciado'], d['alternativas'],
                                    d['correta_ajustada'], d['pilar'])
        except ValueError as e:
            return self._form(usuario, questao, erro=str(e), dados=d)
        self._avisar('✏️', f'{usuario.primeiro_nome} editou a questão #{id}', usuario.email, questoes=True)
        redirect('/questoes?msg=editada')

    def questao_excluir(self, id):
        usuario = self.exigir_acesso('questoes')
        try:
            self.questoes.excluir(id)
        except KeyError:
            return self.erro404()
        self._avisar('🗑️', f'{usuario.primeiro_nome} excluiu a questão #{id}', usuario.email, questoes=True)
        redirect('/questoes?msg=excluida')

    # ------------------------------------------------------------------
    # Quiz e desempenho (qualquer usuário logado)
    # ------------------------------------------------------------------
    def quiz(self):
        usuario = self.exigir_acesso('quiz')
        lista = [{'id': q.id, 'enunciado': q.enunciado, 'alternativas': q.alternativas,
                  'correta': q.correta, 'pilar': q.pilar}
                 for q in self.questoes.listar()]
        # evita que um "</script>" digitado numa questão quebre a página
        dados_json = json.dumps(lista, ensure_ascii=False).replace('</', '<\\/')
        return self._render('views/html/quiz', usuario=usuario, dados_json=dados_json,
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
        self._avisar('🎯', f'{usuario.primeiro_nome} acertou {resultado.acertos} de {resultado.total} '
                           f'({resultado.percentual}%) no quiz', usuario.email, ranking=True)
        return {'acertos': resultado.acertos, 'total': resultado.total,
                'percentual': resultado.percentual, 'indice_geral': geral.indice_geral}

    def desempenho(self):
        usuario = self.exigir_acesso('desempenho')
        desempenho = Desempenho(self.resultados.do_usuario(usuario.email))
        return self._render('views/html/desempenho', usuario=usuario, desempenho=desempenho)

    # ------------------------------------------------------------------
    # Painel do administrador (área restrita)
    # ------------------------------------------------------------------
    def admin(self):
        admin = self.exigir_acesso('admin')
        linhas = []
        for u in sorted(self.usuarios.listar(), key=lambda u: (not u.eh_admin, u.nome.lower())):
            d = Desempenho(self.resultados.do_usuario(u.email))
            linhas.append({'usuario': u, 'quizzes': d.quizzes, 'indice': d.indice_geral})
        todos = Desempenho(self.resultados.listar())
        questoes = self.questoes.listar()
        por_pilar = [(p, sum(1 for q in questoes if q.pilar == p)) for p in PILARES]
        return self._render('views/html/admin', usuario=admin, linhas=linhas,
                        total_usuarios=len(linhas),
                        total_admins=self.usuarios.total_admins(),
                        total_questoes=len(questoes), por_pilar=por_pilar,
                        geral=todos, mensagem=self._mensagem(),
                        atividades=self.tempo_real.atividades())

    def admin_alterar_perfil(self, email):
        admin = self.exigir_acesso('admin')
        if email.lower() == admin.email:
            redirect('/admin?msg=proprio')
        para_admin = request.forms.get('perfil') == 'admin'
        try:
            alterado = self.usuarios.alterar_perfil(email, para_admin)
        except KeyError:
            return self.erro404()
        except ValueError:
            redirect('/admin?msg=ultimo_admin')
        self._avisar('🛡️', f'{alterado.nome} agora é {alterado.perfil.lower()}', admin.email)
        redirect('/admin?msg=' + ('promovido' if para_admin else 'rebaixado'))

    def admin_excluir_usuario(self, email):
        admin = self.exigir_acesso('admin')
        if email.lower() == admin.email:
            redirect('/admin?msg=proprio')
        try:
            self.usuarios.excluir(email)
        except KeyError:
            return self.erro404()
        except ValueError:
            redirect('/admin?msg=ultimo_admin')
        self.resultados.excluir_do_usuario(email.lower())
        self._avisar('❌', 'Um usuário foi removido pelo administrador', admin.email, ranking=True)
        redirect('/admin?msg=usuario_excluido')

    # ------------------------------------------------------------------
    # Ranking ao vivo (atualizado pelo WebSocket)
    # ------------------------------------------------------------------
    def ranking(self):
        usuario = self.exigir_acesso('ranking')
        return self._render('views/html/ranking', usuario=usuario, ranking=self._ranking(),
                            atividades=self.tempo_real.atividades())
