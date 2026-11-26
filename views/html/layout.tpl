<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
    % # versão dos arquivos estáticos: mudar o número obriga o navegador a baixar de novo
    % v = '9'
    % # o tema escolhido fica num cookie, então a página já vem no tema certo
    % from bottle import request
    % tema = request.get_cookie('tema', '')
    <link rel="stylesheet" href="/static/css/style.css?v={{v}}">
</head>
<body class="{{'escuro' if tema == 'escuro' else ''}}" data-ws-porta="{{get('ws_porta', '')}}" data-ws-token="{{get('ws_token', '')}}">
    % usuario = get('usuario', None)
    <header class="topo">
        <div class="container topo__conteudo">
            <a class="logo" href="/">
                <span class="logo__icone">{ }</span>
                <span class="logo__texto">
                    <span class="logo__nome"><span class="logo__oo">OO</span>ficina</span>
                    <span class="logo__sub">Laboratório de Orientação a Objetos</span>
                </span>
            </a>
            <nav>
                % if usuario:
                <a href="/guia">Guia</a>
                <a href="/quiz">Quiz</a>
                <a href="/desempenho">Desempenho</a>
                <a href="/ranking">Ranking</a>
                % if usuario.eh_admin:
                <a href="/questoes">Questões</a>
                <a href="/admin" class="nav__admin">Painel</a>
                <span class="nav__usuario">Administrador</span>
                % else:
                <span class="nav__usuario">Olá, {{usuario.primeiro_nome}}</span>
                % end
                <span id="online" class="online desconectado" title="Conectando ao tempo real..."><i></i><b>–</b> online</span>
                <a href="/logout" class="nav__sair">Sair</a>
                % end
                <button id="btn-tema" class="btn-tema" type="button" aria-label="Alternar tema">{{'☀️' if tema == 'escuro' else '🌙'}}</button>
            </nav>
        </div>
    </header>

    % mensagem = get('mensagem', '')
    % if mensagem:
    <div id="toast" class="toast">{{mensagem}}</div>
    % end

    {{!base}}

    <footer class="rodape">
        <div class="container">
            Projeto BMVC — Orientação a Objetos · UnB · Servido com Python + Bottle
        </div>
    </footer>

    <script src="/static/js/main.js?v={{v}}"></script>
    % for s in get('scripts', []):
    <script src="/static/js/{{s}}?v={{v}}"></script>
    % end
</body>
</html>
