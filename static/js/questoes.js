// static/js/questoes.js — busca/filtro, modal de exclusão e validação do formulário

document.addEventListener('DOMContentLoaded', () => {

    // ---------- LISTA: busca + filtro por pilar ----------
    const busca = document.getElementById('busca');
    const chips = document.querySelectorAll('.chip');
    const questoes = document.querySelectorAll('.questao');
    let pilarAtivo = '';

    function filtrar() {
        const termo = busca.value.trim().toLowerCase();
        let visiveis = 0;
        questoes.forEach(q => {
            const texto = q.querySelector('h3').textContent.toLowerCase();
            const ok = (!pilarAtivo || q.dataset.pilar === pilarAtivo) && texto.includes(termo);
            q.classList.toggle('oculto', !ok);
            if (ok) visiveis++;
        });
        document.getElementById('sem-resultado')
            .classList.toggle('oculto', visiveis > 0 || questoes.length === 0);
    }

    if (busca) {
        busca.addEventListener('input', filtrar);
        chips.forEach(chip => chip.addEventListener('click', () => {
            chips.forEach(c => c.classList.toggle('ativo', c === chip));
            pilarAtivo = chip.dataset.pilar;
            filtrar();
        }));
    }

    // ---------- LISTA: mostrar/esconder resposta ----------
    document.querySelectorAll('.mostrar-resposta').forEach(btn => {
        btn.addEventListener('click', () => {
            const card = btn.closest('.questao');
            const aberta = card.classList.toggle('revelada');
            btn.textContent = aberta ? 'Esconder resposta' : 'Mostrar resposta';
        });
    });

    // ---------- LISTA: modal de confirmação antes de excluir ----------
    const modal = document.getElementById('modal');
    let formPendente = null;

    document.querySelectorAll('.form-excluir').forEach(form => {
        form.addEventListener('submit', e => {
            e.preventDefault();
            formPendente = form;
            document.getElementById('modal-texto').textContent =
                '"' + form.querySelector('button').dataset.enunciado + '"';
            modal.classList.remove('oculto');
        });
    });

    if (modal) {
        const fechar = () => { modal.classList.add('oculto'); formPendente = null; };
        document.getElementById('modal-cancelar').addEventListener('click', fechar);
        modal.addEventListener('click', e => { if (e.target === modal) fechar(); });
        document.addEventListener('keydown', e => { if (e.key === 'Escape') fechar(); });
        document.getElementById('modal-confirmar').addEventListener('click', () => {
            if (formPendente) formPendente.submit();
        });
    }

    // ---------- FORMULÁRIO: contador e validação antes de enviar ----------
    const form = document.getElementById('form-questao');
    if (form) {
        const enunciado = form.querySelector('textarea[name=enunciado]');
        const contador = document.getElementById('contador');
        const erro = document.getElementById('erro-js');
        const atualizarContador = () => { contador.textContent = enunciado.value.length; };
        enunciado.addEventListener('input', atualizarContador);
        atualizarContador();

        // destaca a alternativa marcada como correta
        const destacar = () => {
            form.querySelectorAll('.alternativa').forEach(div => {
                div.classList.toggle('marcada', div.querySelector('input[type=radio]').checked);
            });
        };
        form.querySelectorAll('input[type=radio]').forEach(r => r.addEventListener('change', destacar));
        destacar();

        form.addEventListener('submit', e => {
            const alts = [...form.querySelectorAll('input[name^=alt]')].map(i => i.value.trim());
            const correta = form.querySelector('input[name=correta]:checked');
            let msg = '';
            if (alts.filter(a => a).length < 2) msg = 'Preencha pelo menos 2 alternativas.';
            else if (!correta || !alts[correta.value]) msg = 'A alternativa marcada como correta está vazia.';
            if (msg) {
                e.preventDefault();
                erro.textContent = msg;
                erro.classList.remove('oculto');
            }
        });
    }
});
