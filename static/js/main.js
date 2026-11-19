// static/js/main.js — interatividade da página

document.addEventListener('DOMContentLoaded', () => {

    // 1) Indica que o JS foi carregado com sucesso
    const status = document.getElementById('status-js');
    if (status) {
        status.textContent = 'JavaScript: ativo ✔';
        status.classList.add('ativo');
    }
    console.log('[BMVC] main.js carregado com sucesso');

    // 2) Alternar tema claro/escuro
    const btnTema = document.getElementById('btn-tema');
    btnTema.addEventListener('click', () => {
        const escuro = document.body.classList.toggle('escuro');
        btnTema.textContent = escuro ? '☀️' : '🌙';
    });

    // 3) Cards: clicar mostra/esconde o exemplo de código
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

    // 4) Quiz
    const perguntas = [
        { p: 'Qual pilar permite que uma classe filha reaproveite código da classe mãe?',
          o: ['Encapsulamento', 'Herança', 'Abstração'], c: 1 },
        { p: 'Em Python, o que indica um atributo "privado" como self.__saldo?',
          o: ['Encapsulamento', 'Polimorfismo', 'Herança'], c: 0 },
        { p: 'Objetos diferentes respondendo ao mesmo método de formas diferentes é...',
          o: ['Abstração', 'Herança', 'Polimorfismo'], c: 2 },
        { p: 'Modelar só as características relevantes de algo do mundo real é...',
          o: ['Abstração', 'Encapsulamento', 'Polimorfismo'], c: 0 },
        { p: 'No padrão MVC, quem decide qual página (view) será exibida?',
          o: ['Model', 'Controller', 'View'], c: 1 },
    ];

    const elP = document.getElementById('quiz-pergunta');
    const elO = document.getElementById('quiz-opcoes');
    const elF = document.getElementById('quiz-feedback');
    const elPts = document.getElementById('quiz-pontos');
    const btnProx = document.getElementById('quiz-proxima');
    let atual = 0, pontos = 0;

    function mostrar() {
        const q = perguntas[atual];
        elP.textContent = `${atual + 1}/${perguntas.length} — ${q.p}`;
        elO.innerHTML = '';
        elF.textContent = '';
        btnProx.disabled = true;
        q.o.forEach((texto, i) => {
            const b = document.createElement('button');
            b.type = 'button';
            b.textContent = texto;
            b.addEventListener('click', () => responder(i, b));
            elO.appendChild(b);
        });
    }

    function responder(i, botao) {
        const q = perguntas[atual];
        const botoes = elO.querySelectorAll('button');
        botoes.forEach(b => b.disabled = true);
        botoes[q.c].classList.add('certa');
        if (i === q.c) {
            pontos++;
            elPts.textContent = pontos;
            elF.textContent = 'Acertou! 🎉';
            elF.style.color = 'var(--ok)';
        } else {
            botao.classList.add('errada');
            elF.textContent = `Não foi dessa vez. Resposta: ${q.o[q.c]}`;
            elF.style.color = 'var(--erro)';
        }
        btnProx.disabled = false;
        btnProx.textContent = atual === perguntas.length - 1 ? 'Ver resultado' : 'Próxima pergunta';
    }

    btnProx.addEventListener('click', () => {
        atual++;
        if (atual < perguntas.length) {
            mostrar();
        } else {
            elP.textContent = `Fim! Você acertou ${pontos} de ${perguntas.length}.`;
            elO.innerHTML = '';
            elF.textContent = '';
            btnProx.textContent = 'Recomeçar';
            btnProx.onclick = () => location.reload();
        }
    });

    mostrar();
});
