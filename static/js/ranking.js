// static/js/ranking.js — atualiza o ranking, a lista de online e o feed em tempo real

document.addEventListener('DOMContentLoaded', () => {
    const corpo = document.getElementById('corpo-ranking');
    const vazio = document.getElementById('ranking-vazio');
    const listaOnline = document.getElementById('lista-online');
    const feed = document.getElementById('feed');
    const medalhas = ['🥇', '🥈', '🥉'];

    function desenharRanking(linhas) {
        const anterior = {};
        corpo.querySelectorAll('tr').forEach(tr => { anterior[tr.dataset.nome] = tr.dataset.chave; });
        corpo.innerHTML = '';
        linhas.forEach(l => {
            const tr = document.createElement('tr');
            tr.dataset.nome = l.nome;
            tr.dataset.chave = `${l.posicao}|${l.acertos}|${l.respondidas}`;
            if (l.nome === window.EU) tr.classList.add('eu');
            const celulas = [
                l.posicao <= 3 ? medalhas[l.posicao - 1] : l.posicao,
                l.nome, l.quizzes, `${l.acertos}/${l.respondidas}`, `${l.indice}%`,
            ];
            celulas.forEach((valor, i) => {
                const td = document.createElement('td');
                if (i === 0) td.className = 'posicao';
                if (i === 4) { const b = document.createElement('strong'); b.textContent = valor; td.appendChild(b); }
                else td.textContent = valor;
                tr.appendChild(td);
            });
            corpo.appendChild(tr);
            // destaca quem mudou de posição ou de pontuação
            if (anterior[l.nome] !== tr.dataset.chave) TempoReal.piscar(tr);
        });
        vazio.classList.toggle('oculto', linhas.length > 0);
    }

    // marca as linhas que vieram do servidor para saber o que mudou depois
    corpo.querySelectorAll('tr').forEach(tr => {
        const tds = tr.querySelectorAll('td');
        tr.dataset.nome = tds[1].textContent;
        const [ac, resp] = tds[3].textContent.split('/');
        const pos = [...corpo.children].indexOf(tr) + 1;
        tr.dataset.chave = `${pos}|${ac}|${resp}`;
    });

    document.addEventListener('tempo-real', e => {
        const { tipo, dados } = e.detail;
        if (tipo === 'ranking') desenharRanking(dados);
        if (tipo === 'online') TempoReal.mostrarOnline(listaOnline, dados.nomes);
        if (tipo === 'atividade') TempoReal.adicionarAtividade(feed, dados);
    });
});
