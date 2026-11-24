# BMVC - Guia de Orientação a Objetos

Projeto da disciplina de POO usando o BMVC

A página inicial é a tela de login. Depois de entrar, o usuário vai para o Guia dos pilares da OO (abstração, encapsulamento, herança e polimorfismo), pode gerenciar o banco de questões (CRUD: criar, listar, editar e excluir), responder o quiz e acompanhar o seu índice de acerto na página de Desempenho.

## Estrutura

```
BMVC/
├── route.py                    -> rotas e servidor
├── controllers/application.py  -> controller
├── models/
│   ├── pagina.py               -> conteúdo da página Guia
│   ├── usuario.py              -> classe Usuario (login)
│   ├── questao.py              -> classe Questao (com validações)
│   ├── resultado.py            -> classes Resultado e Desempenho (índice de acerto)
│   └── repositorio.py          -> salva usuários, questões e resultados em JSON
├── views/html/                 -> templates (.tpl)
├── static/                     -> css e js
└── data/                       -> criado ao rodar (usuarios, questoes e resultados .json)
```

## Como executar

Precisa ter o Python 3 instalado.

```
pip install bottle
python route.py
```

Depois é só abrir http://localhost:8080 no navegador.

## Rotas

| Rota | O que faz |
|---|---|
| `/` ou `/login` | login e criação de conta |
| `/guia` | guia com os pilares da OO e resumo do desempenho |
| `/questoes` | lista de questões (Read) |
| `/questoes/nova` | criar questão (Create) |
| `/questoes/<id>/editar` | editar questão (Update) |
| `/questoes/<id>/excluir` | excluir questão (Delete) |
| `/quiz` | quiz de até 10 perguntas, por tema |
| `/quiz/resultado` | recebe o resultado do quiz e salva |
| `/desempenho` | índice de acerto geral, por pilar e histórico |
| `/logout` | sair da conta |

Com exceção do login, todas as páginas só podem ser acessadas por quem fez login.

## Funcionalidades

- Login e cadastro de usuário (senha guardada com hash)
- CRUD completo de questões, salvo em arquivo JSON
- 24 questões iniciais sobre os pilares da OO e MVC
- Quiz por tema, com perguntas e alternativas embaralhadas
- Resultado corrigido no servidor e salvo para cada usuário
- Página de desempenho com índice de acerto geral, por pilar e histórico
- Tema claro/escuro e página de erro 404
