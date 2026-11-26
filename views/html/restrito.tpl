% rebase('views/html/layout.tpl', title='Acesso restrito · OOficina', usuario=usuario, ws_token=get('ws_token', ''), ws_porta=get('ws_porta', ''))
<main class="container erro restrito">
    <div class="restrito__icone">🔒</div>
    <h1>403</h1>
    <h2>Acesso restrito</h2>
    <p>
        Esta área é exclusiva para <strong>administradores</strong>.<br>
        Você entrou como <strong>{{usuario.nome}}</strong> ({{usuario.perfil}}).
    </p>
    <a href="/guia" class="btn">Voltar para o Guia</a>
</main>
