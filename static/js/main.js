// static/js/main.js — carregado em todas as páginas

document.addEventListener('DOMContentLoaded', () => {

    console.log('[BMVC] main.js carregado com sucesso');

    // 1) Selo que mostra que o JS está ativo (página Guia)
    const status = document.getElementById('status-js');
    if (status) {
        status.textContent = 'JavaScript: ativo ✔';
        status.classList.add('ativo');
    }

    // 2) Alternar tema claro/escuro
    //    A escolha fica salva num cookie por 1 ano. Assim, ao atualizar a
    //    página ou trocar de página, o servidor já manda o tema escolhido.
    const btnTema = document.getElementById('btn-tema');
    const atualizarIcone = () => {
        btnTema.textContent = document.body.classList.contains('escuro') ? '☀️' : '🌙';
    };
    atualizarIcone();
    btnTema.addEventListener('click', () => {
        const escuro = document.body.classList.toggle('escuro');
        document.cookie = 'tema=' + (escuro ? 'escuro' : 'claro') + '; path=/; max-age=31536000; SameSite=Lax';
        atualizarIcone();
    });

    // 3) Mensagem (toast) que some sozinha
    const toast = document.getElementById('toast');
    if (toast) {
        setTimeout(() => toast.classList.add('saindo'), 3000);
        setTimeout(() => toast.remove(), 3600);
        // tira o ?msg=... da barra de endereço para não repetir no F5
        history.replaceState(null, '', location.pathname);
    }

    // 4) Cards da página Guia: clicar mostra/esconde o exemplo
    document.querySelectorAll('.card').forEach(card => {
        const alternar = () => {
            const aberto = card.classList.toggle('aberto');
            card.querySelector('.card__acao').textContent =
                aberto ? 'Esconder exemplo ▴' : 'Ver exemplo ▾';
        };
        card.addEventListener('click', alternar);
        card.addEventListener('keydown', e => {
            if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); alternar(); }
        });
    });
});
