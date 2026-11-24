% rebase('views/html/layout.tpl', title=pagina.titulo, usuario=usuario, mensagem=mensagem)

<section class="hero">
    <div class="container">
        <h1>{{pagina.titulo}}</h1>
        <p class="hero__sub">{{pagina.subtitulo}}</p>
        <a href="#pilares" class="btn">Começar a estudar</a>
        <a href="/quiz" class="btn btn--contorno">Ir para o quiz</a>
    </div>
</section>

<main class="container">

    <section class="resumo">
        % if desempenho.quizzes:
        <div class="resumo__numero">{{desempenho.indice_geral}}%</div>
        <div class="resumo__texto">
            <strong>Seu índice de acerto</strong>
            <span>{{desempenho.acertos}} de {{desempenho.respondidas}} respostas certas em {{desempenho.quizzes}} quiz(zes).
            % fraco = desempenho.pilar_mais_fraco()
            % if fraco:
            Vale revisar <strong>{{fraco}}</strong>.
            % end
            </span>
        </div>
        <a href="/desempenho" class="btn btn--contorno-escuro">Ver desempenho</a>
        % else:
        <div class="resumo__numero">—</div>
        <div class="resumo__texto">
            <strong>Olá, {{usuario.primeiro_nome}}!</strong>
            <span>Leia os pilares abaixo e depois faça o quiz para ver seu índice de acerto.</span>
        </div>
        <a href="/quiz" class="btn">Fazer o quiz</a>
        % end
    </section>

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

    <section id="sobre">
        <h2>Sobre este projeto</h2>
        <p>
            Esta página é servida por uma aplicação <strong>BMVC</strong>
            (Bottle + Model-View-Controller). O <em>Model</em>
            (<code>models/</code>) guarda os dados, o
            <em>Controller</em> (<code>controllers/application.py</code>)
            escolhe a view, e a <em>View</em> (<code>views/html/</code>)
            monta o HTML. O CSS e o JS vêm da pasta <code>static/</code>.
        </p>
        <p id="status-js" class="status">JavaScript: inativo</p>
    </section>

</main>
