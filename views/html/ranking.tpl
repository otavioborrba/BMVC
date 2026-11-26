% rebase('views/html/layout.tpl', title='Ranking ao vivo · OOficina', usuario=usuario, ws_token=get('ws_token', ''), ws_porta=get('ws_porta', ''), scripts=['ranking.js'])

<main class="container">
    <div class="cabecalho-pagina">
        <div>
            <span class="tag tag--vivo"><span class="pulso"></span> Ao vivo</span>
            <h1>Ranking da OOficina</h1>
            <p class="dica">Atualizado em tempo real: quando alguém termina um quiz, o placar muda na hora.</p>
        </div>
        <a href="/quiz" class="btn">Fazer um quiz</a>
    </div>

    <div class="ranking-grade">
        <section>
            <table class="tabela tabela-ranking">
                <thead>
                    <tr><th>#</th><th>Nome</th><th>Quizzes</th><th>Acertos</th><th>Índice</th></tr>
                </thead>
                <tbody id="corpo-ranking">
                    % for l in ranking:
                    <tr class="{{'eu' if l['nome'] == usuario.nome else ''}}">
                        <td class="posicao">{{['🥇', '🥈', '🥉'][l['posicao'] - 1] if l['posicao'] <= 3 else l['posicao']}}</td>
                        <td>{{l['nome']}}</td>
                        <td>{{l['quizzes']}}</td>
                        <td>{{l['acertos']}}/{{l['respondidas']}}</td>
                        <td><strong>{{l['indice']}}%</strong></td>
                    </tr>
                    % end
                </tbody>
            </table>
            <p id="ranking-vazio" class="vazio {{'' if not ranking else 'oculto'}}">Ninguém fez um quiz ainda. Seja o primeiro!</p>
        </section>

        <aside class="lateral">
            <section class="painel-vivo">
                <h3><span class="pulso"></span> Online agora</h3>
                <ul id="lista-online" class="lista-online"><li class="dica">Conectando...</li></ul>
            </section>
            <section class="painel-vivo">
                <h3><span class="pulso"></span> Atividade</h3>
                <ul id="feed" class="feed">
                    % for a in atividades:
                    <li><span class="feed__icone">{{a['icone']}}</span><span class="feed__texto">{{a['texto']}}</span><span class="feed__hora">{{a['hora']}}</span></li>
                    % end
                    % if not atividades:
                    <li class="feed__vazio dica">Nada ainda. As ações aparecem aqui na hora.</li>
                    % end
                </ul>
            </section>
        </aside>
    </div>
</main>

% import json
<script>window.EU = {{!json.dumps(usuario.nome).replace('</', '<\\/')}};</script>
