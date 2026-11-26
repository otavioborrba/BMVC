% rebase('views/html/layout.tpl', title='Painel do administrador · OOficina', usuario=usuario, mensagem=mensagem, scripts=['admin.js'])

<main class="container">
    <div class="cabecalho-pagina">
        <div>
            <span class="tag tag--admin">Área restrita</span>
            <h1>Painel do administrador</h1>
            <p class="dica">Visão geral do sistema e gerenciamento dos usuários.</p>
        </div>
        <a href="/questoes" class="btn">Gerenciar questões</a>
    </div>

    <div class="estatisticas">
        <div class="estat estat--destaque">
            <span class="estat__valor">{{total_usuarios}}</span>
            <span class="estat__rotulo">Usuários cadastrados ({{total_admins}} admin)</span>
        </div>
        <div class="estat">
            <span class="estat__valor">{{total_questoes}}</span>
            <span class="estat__rotulo">Questões no banco</span>
        </div>
        <div class="estat">
            <span class="estat__valor">{{geral.quizzes}}</span>
            <span class="estat__rotulo">Quizzes respondidos</span>
        </div>
        <div class="estat">
            <span class="estat__valor">{{'%d%%' % geral.indice_geral if geral.respondidas else '—'}}</span>
            <span class="estat__rotulo">Índice médio de acerto</span>
        </div>
    </div>

    <h2>Usuários</h2>
    <input id="busca-usuario" class="busca" type="search" placeholder="Buscar por nome ou e-mail...">
    <table class="tabela tabela-usuarios">
        <thead>
            <tr><th>Nome</th><th>E-mail</th><th>Perfil</th><th>Quizzes</th><th>Índice</th><th>Ações</th></tr>
        </thead>
        <tbody>
            % for l in linhas:
            % u = l['usuario']
            % eu = u.email == usuario.email
            <tr data-busca="{{u.nome.lower()}} {{u.email}}">
                <td>{{u.nome}}{{' (você)' if eu else ''}}</td>
                <td>{{u.email}}</td>
                <td><span class="tag {{'tag--admin' if u.eh_admin else ''}}">{{u.perfil}}</span></td>
                <td>{{l['quizzes']}}</td>
                <td>{{'%d%%' % l['indice'] if l['quizzes'] else '—'}}</td>
                <td class="acoes">
                    % if eu:
                    <span class="dica">—</span>
                    % else:
                    <form method="post" action="/admin/usuarios/{{u.email}}/perfil" class="form-confirmar"
                          data-titulo="{{'Rebaixar para estudante?' if u.eh_admin else 'Promover a administrador?'}}"
                          data-texto="{{u.nome}} ({{u.email}})">
                        <input type="hidden" name="perfil" value="{{'estudante' if u.eh_admin else 'admin'}}">
                        <button type="submit" class="btn btn--pequeno btn--contorno-escuro">{{'Rebaixar' if u.eh_admin else 'Promover'}}</button>
                    </form>
                    <form method="post" action="/admin/usuarios/{{u.email}}/excluir" class="form-confirmar"
                          data-titulo="Excluir usuário?" data-texto="{{u.nome}} ({{u.email}}) e todos os resultados dele serão apagados.">
                        <button type="submit" class="btn btn--pequeno btn--perigo">Excluir</button>
                    </form>
                    % end
                </td>
            </tr>
            % end
        </tbody>
    </table>
    <p id="sem-usuario" class="vazio oculto">Nenhum usuário encontrado.</p>

    <h2>Questões por pilar</h2>
    % maior = max([n for _, n in por_pilar] + [1])
    <div class="barras">
        % for pilar, n in por_pilar:
        <div class="barra-pilar">
            <span class="barra-pilar__nome">{{pilar}}</span>
            <div class="barra-pilar__trilho"><div class="barra-pilar__valor alto" data-largura="{{round(n / maior * 100)}}"></div></div>
            <span class="barra-pilar__pct">{{n}}</span>
            <span class="barra-pilar__info">questões</span>
        </div>
        % end
    </div>
</main>

<div id="modal" class="modal oculto" role="dialog" aria-modal="true">
    <div class="modal__caixa">
        <h3 id="modal-titulo"></h3>
        <p id="modal-texto"></p>
        <div class="modal__acoes">
            <button type="button" id="modal-cancelar" class="btn btn--contorno-escuro">Cancelar</button>
            <button type="button" id="modal-confirmar" class="btn">Confirmar</button>
        </div>
    </div>
</div>
