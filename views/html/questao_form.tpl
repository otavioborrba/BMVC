% editando = questao is not None
% titulo = 'Editar questão #%d' % questao.id if editando else 'Nova questão'
% rebase('views/html/layout.tpl', title=titulo + ' · Guia de OO', usuario=usuario, scripts=['questoes.js'])

<main class="container estreito">
    <a href="/questoes" class="voltar">← Voltar para a lista</a>
    <h1>{{titulo}}</h1>

    % if erro:
    <p class="alerta alerta--erro">{{erro}}</p>
    % end

    % acao = '/questoes/%d/editar' % questao.id if editando else '/questoes/nova'
    <form id="form-questao" class="form form--card" method="post" action="{{acao}}">
        <label>Enunciado
            <textarea name="enunciado" rows="3" required minlength="10" maxlength="300">{{dados['enunciado']}}</textarea>
            <small class="contador"><span id="contador">0</span>/300</small>
        </label>

        <label>Pilar
            <select name="pilar">
                % for p in pilares:
                <option value="{{p}}" {{'selected' if p == dados['pilar'] else ''}}>{{p}}</option>
                % end
            </select>
        </label>

        <fieldset>
            <legend>Alternativas <small>(preencha de 2 a 4 e marque a correta)</small></legend>
            % alts = list(dados['alternativas']) + [''] * 4
            % for i in range(4):
            <div class="alternativa">
                <input type="radio" name="correta" value="{{i}}" id="c{{i}}" {{'checked' if i == int(dados['correta']) else ''}}>
                <label for="c{{i}}" class="letra">{{'ABCD'[i]}}</label>
                <input type="text" name="alt{{i}}" value="{{alts[i]}}" placeholder="Alternativa {{'ABCD'[i]}}{{' (opcional)' if i >= 2 else ''}}" maxlength="120">
            </div>
            % end
        </fieldset>

        <p id="erro-js" class="alerta alerta--erro oculto"></p>

        <div class="form__acoes">
            <a href="/questoes" class="btn btn--contorno-escuro">Cancelar</a>
            <button type="submit" class="btn">{{'Salvar alterações' if editando else 'Criar questão'}}</button>
        </div>
    </form>
</main>
