# BMVC - Guia de Orientação a Objetos

Projeto da disciplina de POO usando o BMVC

A página inicial é a tela de login. O sistema tem controle de acesso com dois perfis:

- **Estudante**: depois de entrar vai para o Guia dos pilares da OO, responde o quiz e acompanha o seu índice de acerto na página de Desempenho.
- **Administrador**: além disso, acessa as áreas restritas: o banco de questões (CRUD: criar, listar, editar e excluir) e o Painel do administrador, onde vê as estatísticas do sistema e gerencia os usuários (promover, rebaixar e excluir).

Se um estudante tentar abrir uma área restrita, ele vê a página **403 - Acesso restrito**. Quem não fez login é levado para a tela de login.

Conta de administrador criada automaticamente: `admin@bmvc.com` / senha `admin123`.

## Estrutura

```
BMVC/
├── route.py                    -> rotas e servidor
├── controllers/application.py  -> controller
├── models/
│   ├── pagina.py               -> conteúdo da página Guia
│   ├── usuario.py              -> classes Usuario e Administrador (herança)
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

| Rota | Quem acessa | O que faz |
|---|---|---|
| `/` ou `/login` | todos | login e criação de conta |
| `/guia` | logado | guia com os pilares da OO e resumo do desempenho |
| `/quiz` | logado | quiz de até 10 perguntas, por tema |
| `/quiz/resultado` | logado | recebe o resultado do quiz e salva |
| `/desempenho` | logado | índice de acerto geral, por pilar e histórico |
| `/questoes` | admin | lista de questões (Read) |
| `/questoes/nova` | admin | criar questão (Create) |
| `/questoes/<id>/editar` | admin | editar questão (Update) |
| `/questoes/<id>/excluir` | admin | excluir questão (Delete) |
| `/admin` | admin | painel com estatísticas e lista de usuários |
| `/admin/usuarios/<email>/perfil` | admin | promover ou rebaixar um usuário |
| `/admin/usuarios/<email>/excluir` | admin | excluir um usuário e os resultados dele |
| `/logout` | logado | sair da conta |

## Funcionalidades

- Login e cadastro de usuário (senha guardada com hash)
- Controle de acesso por perfil (estudante e administrador) com página 403 de acesso restrito
- CRUD completo de questões (só administrador), salvo em arquivo JSON
- Painel do administrador com estatísticas e gerenciamento de usuários
- 24 questões iniciais sobre os pilares da OO e MVC
- Quiz por tema, com perguntas e alternativas embaralhadas
- Resultado corrigido no servidor e salvo para cada usuário
- Página de desempenho com índice de acerto geral, por pilar e histórico
- Tema claro/escuro e página de erro 404
