// static/js/login.js — abas Entrar/Criar conta e botão de ver senha

document.addEventListener('DOMContentLoaded', () => {
    const abas = document.querySelectorAll('.aba');
    const forms = {
        entrar: document.getElementById('form-entrar'),
        cadastro: document.getElementById('form-cadastro'),
    };

    abas.forEach(aba => {
        aba.addEventListener('click', () => {
            abas.forEach(a => a.classList.toggle('ativa', a === aba));
            Object.entries(forms).forEach(([nome, form]) => {
                form.classList.toggle('oculto', nome !== aba.dataset.aba);
            });
            const erro = document.querySelector('.painel-login .alerta');
            if (erro) erro.remove();
            forms[aba.dataset.aba].querySelector('input').focus();
        });
    });

    document.querySelectorAll('.ver-senha').forEach(btn => {
        btn.addEventListener('click', () => {
            const input = btn.previousElementSibling;
            const mostrando = input.type === 'text';
            input.type = mostrando ? 'password' : 'text';
            btn.textContent = mostrando ? '👁' : '🙈';
        });
    });
});
