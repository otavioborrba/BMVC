# BMVC - Guia de Orientação a Objetos

Projeto da disciplina de POO usando o BMVC

A aplicação serve uma página com um resumo dos 4 pilares da OO (abstração, encapsulamento, herança e polimorfismo), exemplos de código em Python e um quiz pra revisar o conteúdo.

## Estrutura

```
BMVC/
├── route.py                    -> rotas e servidor
├── controllers/application.py  -> controller
├── models/pagina.py            -> model (conteúdo da página)
├── views/html/                 -> templates (.tpl)
└── static/                     -> css e js
```

## Como executar

Precisa ter o Python 3 instalado.

```
pip install bottle
python route.py
```

Depois é só abrir http://localhost:8080 no navegador.

## Funcionalidades

- Página principal renderizada a partir de template .tpl
- CSS e JS carregados pela rota /static
- Tema claro/escuro
- Cards que mostram exemplos de código ao clicar
- Quiz com pontuação
- Página de erro 404
