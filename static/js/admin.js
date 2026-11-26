// static/js/admin.js — busca de usuários, confirmação das ações e barras do painel

document.addEventListener('DOMContentLoaded', () => {

    // busca por nome ou e-mail na tabela de usuários
    const busca = document.getElementById('busca-usuario');
    const linhas = document.querySelectorAll('.tabela-usuarios tbody tr');
    busca.addEventListener('input', () => {
        const termo = busca.value.trim().toLowerCase();
        let visiveis = 0;
        linhas.forEach(tr => {
            const ok = tr.dataset.busca.includes(termo);
            tr.classList.toggle('oculto', !ok);
            if (ok) visiveis++;
        });
        document.getElementById('sem-usuario').classList.toggle('oculto', visiveis > 0);
    });

    // janela de confirmação antes de promover, rebaixar ou excluir
    const modal = document.getElementById('modal');
    const confirmar = document.getElementById('modal-confirmar');
    let pendente = null;

    document.querySelectorAll('.form-confirmar').forEach(form => {
        form.addEventListener('submit', e => {
            e.preventDefault();
            pendente = form;
            document.getElementById('modal-titulo').textContent = form.dataset.titulo;
            document.getElementById('modal-texto').textContent = form.dataset.texto;
            confirmar.classList.toggle('btn--perigo', form.action.endsWith('/excluir'));
            modal.classList.remove('oculto');
        });
    });

    const fechar = () => { modal.classList.add('oculto'); pendente = null; };
    document.getElementById('modal-cancelar').addEventListener('click', fechar);
    modal.addEventListener('click', e => { if (e.target === modal) fechar(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') fechar(); });
    confirmar.addEventListener('click', () => { if (pendente) pendente.submit(); });

    // barras de questões por pilar crescendo
    requestAnimationFrame(() => {
        document.querySelectorAll('.barra-pilar__valor').forEach(b => {
            b.style.width = b.dataset.largura + '%';
        });
    });
});

// ---------- tempo real: números, online e feed do painel ----------
document.addEventListener('tempo-real', e => {
    const { tipo, dados } = e.detail;
    if (tipo === 'estatisticas') {
        [['est-usuarios', dados.usuarios], ['est-admins', dados.admins], ['est-questoes', dados.questoes],
         ['est-quizzes', dados.quizzes], ['est-indice', dados.indice]].forEach(([id, valor]) => {
            const el = document.getElementById(id);
            if (el.textContent !== String(valor)) {
                el.textContent = valor;
                TempoReal.piscar(el.closest('.estat'));
            }
        });
    }
    if (tipo === 'online') TempoReal.mostrarOnline(document.getElementById('lista-online'), dados.nomes);
    if (tipo === 'atividade') TempoReal.adicionarAtividade(document.getElementById('feed'), dados);
});
