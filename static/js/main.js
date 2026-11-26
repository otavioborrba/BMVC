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

// ================================================================
// Tempo real (WebSocket)
// A página se conecta ao servidor WebSocket (porta 8081) usando o token
// que o controller colocou no <body>. Cada mensagem chega como
// {tipo, dados} e é repassada para a página como o evento 'tempo-real'.
// ================================================================
(function () {
    const token = document.body.dataset.wsToken;
    const porta = document.body.dataset.wsPorta;
    if (!token || !porta || !('WebSocket' in window)) return;

    const indicador = document.getElementById('online');
    let tentativas = 0;

    function conectar() {
        // "localhost" pode virar o endereço IPv6 (::1); o servidor escuta em IPv4
        const host = location.hostname === 'localhost' ? '127.0.0.1' : location.hostname;
        const ws = new WebSocket(`ws://${host}:${porta}/?token=${token}`);

        ws.addEventListener('open', () => {
            tentativas = 0;
            indicador.classList.remove('desconectado');
            indicador.title = 'Conectado em tempo real';
            console.log('[BMVC] WebSocket conectado');
        });

        ws.addEventListener('message', evento => {
            const msg = JSON.parse(evento.data);
            if (msg.tipo === 'online') {
                indicador.querySelector('b').textContent = msg.dados.total;
                indicador.title = 'Online: ' + msg.dados.nomes.join(', ');
            }
            // avisa os scripts da página (ranking.js, admin.js, quiz.js...)
            document.dispatchEvent(new CustomEvent('tempo-real', { detail: msg }));
        });

        ws.addEventListener('close', () => {
            indicador.classList.add('desconectado');
            indicador.querySelector('b').textContent = '–';
            indicador.title = 'Reconectando...';
            // tenta de novo: 1s, 2s, 4s... até 10s
            const espera = Math.min(1000 * 2 ** tentativas++, 10000);
            setTimeout(conectar, espera);
        });
    }

    conectar();
})();

// Funções usadas pelas páginas com partes "ao vivo"
window.TempoReal = {
    mostrarOnline(lista, nomes) {
        lista.innerHTML = '';
        nomes.forEach(nome => {
            const li = document.createElement('li');
            li.textContent = nome;
            lista.appendChild(li);
        });
    },
    adicionarAtividade(feed, a) {
        const vazio = feed.querySelector('.feed__vazio');
        if (vazio) vazio.remove();
        const li = document.createElement('li');
        li.className = 'novo';
        [['feed__icone', a.icone], ['feed__texto', a.texto], ['feed__hora', a.hora]].forEach(([classe, texto]) => {
            const span = document.createElement('span');
            span.className = classe;
            span.textContent = texto;
            li.appendChild(span);
        });
        feed.prepend(li);
        while (feed.children.length > 20) feed.lastElementChild.remove();
    },
    piscar(el) {
        el.classList.remove('piscar');
        void el.offsetWidth;          // reinicia a animação
        el.classList.add('piscar');
    },
};
