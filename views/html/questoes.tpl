% rebase('views/html/layout.tpl', title='Questões · OOficina', usuario=usuario, mensagem=mensagem, scripts=['questoes.js'])

<main class="container">
    <div class="cabecalho-pagina">
        <div>
            <h1>Banco de questões</h1>
            <p class="dica">Área do administrador · {{len(questoes)}} questões cadastradas. As alterações aparecem no quiz de todos os estudantes.</p>
        </div>
        <div class="cabecalho-pagina__acoes">
            <a href="/quiz" class="btn btn--contorno-escuro">▶ Jogar quiz</a>
            <a href="/questoes/nova" class="btn">+ Nova questão</a>
        </div>
    </div>

    <div class="filtros">
        <input id="busca" type="search" placeholder="Buscar pelo enunciado...">
        <div class="filtros__pilares">
            <button type="button" class="chip ativo" data-pilar="">Todas</button>
            % for p in pilares:
            <button type="button" class="chip" data-pilar="{{p}}">{{p}}</button>
            % end
        </div>
    </div>

    % if not questoes:
    <p class="vazio">Nenhuma questão ainda. <a href="/questoes/nova">Crie a primeira!</a></p>
    % end

    <div class="lista-questoes">
        % for q in questoes:
        <article class="questao" data-pilar="{{q.pilar}}">
            <div class="questao__topo">
                <span class="tag">{{q.pilar}}</span>
                <span class="questao__autor">#{{q.id}} · por {{q.autor}}</span>
            </div>
            <h3>{{q.enunciado}}</h3>
            <ol class="questao__alts" type="A">
                % for i, alt in enumerate(q.alternativas):
                <li class="{{'correta' if i == q.correta else ''}}">{{alt}}</li>
                % end
            </ol>
            <div class="questao__acoes">
                <button type="button" class="link-btn mostrar-resposta">Mostrar resposta</button>
                <a href="/questoes/{{q.id}}/editar" class="btn btn--pequeno btn--contorno-escuro">Editar</a>
                <form method="post" action="/questoes/{{q.id}}/excluir" class="form-excluir">
                    <button type="submit" class="btn btn--pequeno btn--perigo" data-enunciado="{{q.enunciado}}">Excluir</button>
                </form>
            </div>
        </article>
        % end
    </div>
    <p id="sem-resultado" class="vazio oculto">Nenhuma questão encontrada com esse filtro.</p>
</main>

<div id="modal" class="modal oculto" role="dialog" aria-modal="true">
    <div class="modal__caixa">
        <h3>Excluir questão?</h3>
        <p id="modal-texto"></p>
        <div class="modal__acoes">
            <button type="button" id="modal-cancelar" class="btn btn--contorno-escuro">Cancelar</button>
            <button type="button" id="modal-confirmar" class="btn btn--perigo">Excluir</button>
        </div>
    </div>
</div>
