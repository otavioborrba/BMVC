# BMVC - Guia de Orientação a Objetos

Projeto da disciplina de POO usando o BMVC

A página inicial é a tela de login. O sistema tem controle de acesso com dois perfis:

- **Estudante**: depois de entrar vai para o Guia dos pilares da OO, responde o quiz e acompanha o seu índice de acerto na página de Desempenho.
- **Administrador**: além disso, acessa as áreas restritas: o banco de questões (CRUD: criar, listar, editar e excluir) e o Painel do administrador, onde vê as estatísticas do sistema e gerencia os usuários (promover, rebaixar e excluir).

Se um estudante tentar abrir uma área restrita, ele vê a página **403 - Acesso restrito**. Quem não fez login é levado para a tela de login.

### Tempo real (WebSocket)

Junto com o Bottle (porta 8080) roda um servidor **WebSocket** (porta 8081), feito com a biblioteca padrão do Python (`controllers/tempo_real.py`). As páginas de quem está logado se conectam a ele e recebem atualizações na hora, sem recarregar:

- **Ranking ao vivo** (`/ranking`): o placar muda assim que alguém termina um quiz, com a lista de quem está online e um feed de atividades.
- **Indicador "● N online"** no menu de todas as páginas.
- **Painel do administrador**: números, usuários online e feed de atividades atualizados em tempo real.
- **Quiz**: aviso quando um administrador altera o banco de questões.

Conta de administrador criada automaticamente: `admin@bmvc.com` / senha `admin123`.

## Estrutura

```
BMVC/
├── route.py                    -> rotas e servidor
├── controllers/application.py  -> controller
├── controllers/tempo_real.py   -> servidor WebSocket (tempo real)
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

Depois é só abrir http://localhost:8080 no navegador. O WebSocket sobe sozinho na porta 8081.

Para ver o tempo real funcionando, abra o site em duas janelas (uma normal e uma anônima) com usuários diferentes.

## Rotas

| Rota | Quem acessa | O que faz |
|---|---|---|
| `/` ou `/login` | todos | login e criação de conta |
| `/guia` | logado | guia com os pilares da OO e resumo do desempenho |
| `/quiz` | logado | quiz de até 10 perguntas, por tema |
| `/quiz/resultado` | logado | recebe o resultado do quiz e salva |
| `/desempenho` | logado | índice de acerto geral, por pilar e histórico |
| `/ranking` | logado | ranking ao vivo, usuários online e feed de atividades (WebSocket) |
| `ws://localhost:8081` | logado | conexão WebSocket usada pelas páginas |
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
- Comunicação em tempo real via WebSocket: ranking, usuários online, feed de atividades e painel do admin
- Tema claro/escuro e página de erro 404
