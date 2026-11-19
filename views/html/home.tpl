% rebase('views/html/layout.tpl', title=pagina.titulo)

<section class="hero">
    <div class="container">
        <h1>{{pagina.titulo}}</h1>
        <p class="hero__sub">{{pagina.subtitulo}}</p>
        <a href="#pilares" class="btn">Começar a estudar</a>
    </div>
</section>

<main class="container">

    <section id="pilares">
        <h2>Os 4 pilares</h2>
        <p class="dica">Clique em um card para ver um exemplo em Python.</p>
        <div class="grade">
            % for i, p in enumerate(pagina.pilares, start=1):
            <article class="card" tabindex="0">
                <span class="card__num">{{i}}</span>
                <h3>{{p.nome}}</h3>
                <p>{{p.resumo}}</p>
                <pre class="card__codigo">{{p.exemplo}}</pre>
                <span class="card__acao">Ver exemplo ▾</span>
            </article>
            % end
        </div>
    </section>

    <section id="quiz">
        <h2>Quiz rápido</h2>
        <div class="quiz">
            <p id="quiz-pergunta" class="quiz__pergunta">Carregando...</p>
            <div id="quiz-opcoes" class="quiz__opcoes"></div>
            <p id="quiz-feedback" class="quiz__feedback" aria-live="polite"></p>
            <div class="quiz__rodape">
                <span>Pontuação: <strong id="quiz-pontos">0</strong></span>
                <button id="quiz-proxima" class="btn" type="button">Próxima pergunta</button>
            </div>
        </div>
    </section>

    <section id="sobre">
        <h2>Sobre este projeto</h2>
        <p>
            Esta página é servida por uma aplicação <strong>BMVC</strong>
            (Bottle + Model-View-Controller). O <em>Model</em>
            (<code>models/pagina.py</code>) guarda o conteúdo, o
            <em>Controller</em> (<code>controllers/application.py</code>)
            escolhe a view, e a <em>View</em> (<code>views/html/home.tpl</code>)
            monta o HTML. O CSS e o JS vêm da pasta <code>static/</code>.
        </p>
        <p id="status-js" class="status">JavaScript: inativo</p>
    </section>

</main>
