# BMVC - OOficina

OOficina - site destinado ao desenvolvimento de habilidades do usuário em relaçao ao conteúdo de POO

Conta de administrador criada automaticamente: `admin@bmvc.com` / senha `admin123`.

## Como executar

Precisa ter o Python 3 instalado.

```
pip install bottle
python route.py
```

Depois é só abrir http://localhost:8080 no navegador.

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
