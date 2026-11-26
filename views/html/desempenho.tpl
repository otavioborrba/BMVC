% rebase('views/html/layout.tpl', title='Desempenho · OOficina', usuario=usuario, scripts=['desempenho.js'])

<main class="container">
    <div class="cabecalho-pagina">
        <div>
            <h1>Meu desempenho</h1>
            <p class="dica">Seu índice de acerto em todos os quizzes que você fez.</p>
        </div>
        <a href="/quiz" class="btn">Fazer um quiz</a>
    </div>

    % if not desempenho.quizzes:
    <div class="vazio">
        <p>Você ainda não respondeu nenhum quiz.</p>
        <a href="/quiz" class="btn">Começar agora</a>
    </div>
    % else:
    <div class="estatisticas">
        <div class="estat estat--destaque">
            <span class="estat__valor contar" data-valor="{{desempenho.indice_geral}}" data-sufixo="%">{{desempenho.indice_geral}}%</span>
            <span class="estat__rotulo">Índice geral de acerto</span>
        </div>
        <div class="estat">
            <span class="estat__valor contar" data-valor="{{desempenho.quizzes}}">{{desempenho.quizzes}}</span>
            <span class="estat__rotulo">Quizzes feitos</span>
        </div>
        <div class="estat">
            <span class="estat__valor"><span class="contar" data-valor="{{desempenho.acertos}}">{{desempenho.acertos}}</span>/{{desempenho.respondidas}}</span>
            <span class="estat__rotulo">Respostas certas</span>
        </div>
        <div class="estat">
            <span class="estat__valor contar" data-valor="{{desempenho.melhor.percentual}}" data-sufixo="%">{{desempenho.melhor.percentual}}%</span>
            <span class="estat__rotulo">Melhor quiz ({{desempenho.melhor.data}})</span>
        </div>
    </div>

    <h2>Acerto por pilar</h2>
    % fraco = desempenho.pilar_mais_fraco()
    % if fraco:
    <p class="dica">O pilar em que você mais erra é <strong>{{fraco}}</strong>. Que tal revisar no <a href="/guia#pilares">Guia</a>?</p>
    % end
    <div class="barras">
        % for pilar, acertos, total, pct in desempenho.por_pilar():
        <div class="barra-pilar">
            <span class="barra-pilar__nome">{{pilar}}</span>
            <div class="barra-pilar__trilho">
                % if total:
                <div class="barra-pilar__valor {{'baixo' if pct < 50 else 'medio' if pct < 70 else 'alto'}}" data-largura="{{pct}}"></div>
                % end
            </div>
            <span class="barra-pilar__pct">{{'%d%%' % pct if total else '—'}}</span>
            <span class="barra-pilar__info">{{'%d/%d' % (acertos, total) if total else 'sem respostas'}}</span>
        </div>
        % end
    </div>

    <h2>Últimos quizzes</h2>
    <table class="tabela">
        <thead>
            <tr><th>Data</th><th>Acertos</th><th>Aproveitamento</th></tr>
        </thead>
        <tbody>
            % for r in desempenho.historico():
            <tr>
                <td>{{r.data}}</td>
                <td>{{r.acertos}} de {{r.total}}</td>
                <td><span class="tag {{'tag--ok' if r.percentual >= 70 else 'tag--erro' if r.percentual < 50 else ''}}">{{r.percentual}}%</span></td>
            </tr>
            % end
        </tbody>
    </table>
    % end
</main>
