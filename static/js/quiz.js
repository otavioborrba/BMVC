// static/js/quiz.js — quiz com as questões do banco; envia o resultado para o servidor

const POR_RODADA = 10;

const embaralhar = lista => {
    const copia = [...lista];
    for (let i = copia.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [copia[i], copia[j]] = [copia[j], copia[i]];
    }
    return copia;
};

document.addEventListener('DOMContentLoaded', () => {
    const todas = window.QUESTOES || [];
    const telaInicio = document.getElementById('quiz-inicio');
    const telaJogo = document.getElementById('quiz-jogo');
    const telaFim = document.getElementById('quiz-fim');
    const chips = document.querySelectorAll('#escolha-pilar .chip');
    const info = document.getElementById('qtd-info');
    const btnComecar = document.getElementById('btn-comecar');

    const elP = document.getElementById('quiz-pergunta');
    const elO = document.getElementById('quiz-opcoes');
    const elF = document.getElementById('quiz-feedback');
    const elPts = document.getElementById('quiz-pontos');
    const elPilar = document.getElementById('q-pilar');
    const barra = document.getElementById('barra');
    const btnProx = document.getElementById('quiz-proxima');

    let pilarEscolhido = '';
    let perguntas = [], atual = 0, pontos = 0, respostas = [];

    // ---------- tela inicial: escolher o tema ----------
    const disponiveis = () => todas.filter(q => !pilarEscolhido || q.pilar === pilarEscolhido);
    function atualizarInfo() {
        const n = Math.min(disponiveis().length, POR_RODADA);
        info.textContent = n ? `Você vai responder ${n} pergunta(s).` : 'Não há questões desse tema ainda.';
        btnComecar.disabled = n === 0;
    }
    chips.forEach(chip => chip.addEventListener('click', () => {
        chips.forEach(c => c.classList.toggle('ativo', c === chip));
        pilarEscolhido = chip.dataset.pilar;
        atualizarInfo();
    }));
    atualizarInfo();

    btnComecar.addEventListener('click', () => {
        perguntas = embaralhar(disponiveis()).slice(0, POR_RODADA);
        telaInicio.classList.add('oculto');
        telaJogo.classList.remove('oculto');
        mostrar();
    });

    // ---------- perguntas ----------
    function mostrar() {
        const q = perguntas[atual];
        elPilar.textContent = q.pilar;
        elP.textContent = `${atual + 1}/${perguntas.length} — ${q.enunciado}`;
        barra.style.width = (atual / perguntas.length * 100) + '%';
        elO.innerHTML = '';
        elF.textContent = '';
        btnProx.disabled = true;
        // embaralha as alternativas, mas guarda a posição original de cada uma
        embaralhar(q.alternativas.map((texto, i) => ({ texto, i }))).forEach(alt => {
            const b = document.createElement('button');
            b.type = 'button';
            b.textContent = alt.texto;
            b.dataset.original = alt.i;
            b.addEventListener('click', () => responder(alt.i, b));
            elO.appendChild(b);
        });
    }

    function responder(escolha, botao) {
        const q = perguntas[atual];
        respostas.push({ id: q.id, escolha });
        elO.querySelectorAll('button').forEach(b => {
            b.disabled = true;
            if (Number(b.dataset.original) === q.correta) b.classList.add('certa');
        });
        if (escolha === q.correta) {
            pontos++;
            elPts.textContent = pontos;
            elF.textContent = 'Acertou! 🎉';
            elF.style.color = 'var(--ok)';
        } else {
            botao.classList.add('errada');
            elF.textContent = `Não foi dessa vez. Resposta: ${q.alternativas[q.correta]}`;
            elF.style.color = 'var(--erro)';
        }
        btnProx.disabled = false;
        btnProx.textContent = atual === perguntas.length - 1 ? 'Ver resultado' : 'Próxima';
    }

    btnProx.addEventListener('click', () => {
        atual++;
        if (atual < perguntas.length) return mostrar();
        finalizar();
    });

    // ---------- resultado: mostra na tela e salva no servidor ----------
    async function finalizar() {
        barra.style.width = '100%';
        telaJogo.classList.add('oculto');
        telaFim.classList.remove('oculto');
        const pct = Math.round(pontos / perguntas.length * 100);
        document.getElementById('fim-percentual').textContent = pct + '%';
        document.getElementById('fim-texto').textContent =
            `Você acertou ${pontos} de ${perguntas.length}. ` +
            (pct >= 70 ? 'Mandou bem!' : 'Vale revisar os pilares no Guia e tentar de novo.');
        const geral = document.getElementById('fim-geral');
        geral.textContent = 'Salvando resultado...';
        try {
            const resp = await fetch('/quiz/resultado', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ respostas }),
            });
            if (!resp.ok) throw new Error(resp.status);
            const dados = await resp.json();
            geral.textContent = `Resultado salvo. Seu índice geral de acerto agora é ${dados.indice_geral}%.`;
        } catch (e) {
            geral.textContent = 'Não foi possível salvar o resultado.';
        }
    }
});
