// static/js/desempenho.js — anima os números e as barras da página de desempenho

document.addEventListener('DOMContentLoaded', () => {
    // números contando do zero até o valor final
    document.querySelectorAll('.contar').forEach(el => {
        const final = Number(el.dataset.valor);
        const sufixo = el.dataset.sufixo || '';
        const inicio = performance.now(), duracao = 800;
        function passo(agora) {
            const t = Math.min((agora - inicio) / duracao, 1);
            el.textContent = Math.round(final * t) + sufixo;
            if (t < 1) requestAnimationFrame(passo);
        }
        requestAnimationFrame(passo);
    });

    // barras crescendo até o percentual de cada pilar
    requestAnimationFrame(() => {
        document.querySelectorAll('.barra-pilar__valor').forEach(barra => {
            barra.style.width = barra.dataset.largura + '%';
        });
    });
});
