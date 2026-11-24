% rebase('views/html/layout.tpl', title='Entrar · Guia de OO', usuario=None, mensagem=mensagem, scripts=['login.js'])

<section class="hero hero--login">
    <div class="container hero-login">

        <div class="hero-login__texto">
            <span class="selo">Banco de questões de OO</span>
            <h1>Estude Orientação a Objetos e acompanhe sua evolução</h1>
        </div>

        <div class="painel-login">
            <div class="abas" role="tablist">
                <button type="button" class="aba {{'ativa' if aba == 'entrar' else ''}}" data-aba="entrar">Entrar</button>
                <button type="button" class="aba {{'ativa' if aba == 'cadastro' else ''}}" data-aba="cadastro">Criar conta</button>
            </div>

            % if erro:
            <p class="alerta alerta--erro">{{erro}}</p>
            % end

            <form id="form-entrar" class="form {{'' if aba == 'entrar' else 'oculto'}}" method="post" action="/login">
                <label>E-mail
                    <input type="email" name="email" value="{{dados.get('email', '')}}" required>
                </label>
                <label>Senha
                    <span class="campo-senha">
                        <input type="password" name="senha" required>
                        <button type="button" class="ver-senha" aria-label="Mostrar senha">👁</button>
                    </span>
                </label>
                <button class="btn btn--cheio" type="submit">Entrar</button>
            </form>

            <form id="form-cadastro" class="form {{'' if aba == 'cadastro' else 'oculto'}}" method="post" action="/cadastro">
                <label>Nome
                    <input type="text" name="nome" value="{{dados.get('nome', '')}}" required minlength="2">
                </label>
                <label>E-mail
                    <input type="email" name="email" value="{{dados.get('email', '')}}" required>
                </label>
                <label>Senha <small>(mínimo 4 caracteres)</small>
                    <span class="campo-senha">
                        <input type="password" name="senha" required minlength="4">
                        <button type="button" class="ver-senha" aria-label="Mostrar senha">👁</button>
                    </span>
                </label>
                <button class="btn btn--cheio" type="submit">Criar conta</button>
            </form>
        </div>

    </div>
</section>
