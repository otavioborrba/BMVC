<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <header class="topo">
        <div class="container topo__conteudo">
            <a class="logo" href="/">&lt;OO/&gt; Guia</a>
            <nav>
                <a href="#pilares">Pilares</a>
                <a href="#quiz">Quiz</a>
                <a href="#sobre">Sobre</a>
                <button id="btn-tema" class="btn-tema" type="button" aria-label="Alternar tema">🌙</button>
            </nav>
        </div>
    </header>

    {{!base}}

    <footer class="rodape">
        <div class="container">
            Projeto BMVC I — Orientação a Objetos · UnB · Servido com Python + Bottle
        </div>
    </footer>

    <script src="/static/js/main.js"></script>
</body>
</html>
