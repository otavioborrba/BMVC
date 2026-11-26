% rebase('views/html/layout.tpl', title='Quiz · OOficina', usuario=usuario, scripts=['quiz.js'])

<main class="container estreito">
    <div class="cabecalho-pagina">
        <div>
            <h1>Quiz de OO</h1>
            <p class="dica">Rodadas de até 10 perguntas sorteadas entre {{total}} questões.</p>
        </div>
        <a href="/desempenho" class="btn btn--contorno-escuro">Meu desempenho</a>
    </div>

    <!-- tela inicial: escolha do tema -->
    <div id="quiz-inicio" class="quiz">
        <p class="quiz__pergunta">Sobre qual tema você quer responder?</p>
        <div class="filtros__pilares" id="escolha-pilar">
            <button type="button" class="chip ativo" data-pilar="">Todos</button>
            % for p in pilares:
            <button type="button" class="chip" data-pilar="{{p}}">{{p}}</button>
            % end
        </div>
        <p class="dica" id="qtd-info"></p>
        <button id="btn-comecar" class="btn" type="button">Começar</button>
    </div>

    <!-- tela das perguntas -->
    <div id="quiz-jogo" class="quiz oculto">
        <div class="progresso"><div id="barra" class="progresso__barra"></div></div>
        <span id="q-pilar" class="tag"></span>
        <p id="quiz-pergunta" class="quiz__pergunta"></p>
        <div id="quiz-opcoes" class="quiz__opcoes"></div>
        <p id="quiz-feedback" class="quiz__feedback" aria-live="polite"></p>
        <div class="quiz__rodape">
            <span>Acertos: <strong id="quiz-pontos">0</strong></span>
            <button id="quiz-proxima" class="btn" type="button" disabled>Próxima</button>
        </div>
    </div>

    <!-- tela de resultado -->
    <div id="quiz-fim" class="quiz resultado-quiz oculto">
        <div id="fim-percentual" class="resultado-quiz__numero"></div>
        <p id="fim-texto" class="quiz__pergunta"></p>
        <p id="fim-geral" class="dica"></p>
        <div class="form__acoes">
            <a href="/desempenho" class="btn btn--contorno-escuro">Ver desempenho</a>
            <button type="button" class="btn" onclick="location.reload()">Jogar de novo</button>
        </div>
    </div>
</main>

<script>window.QUESTOES = {{!dados_json}};</script>
