# models/usuario.py — Model: usuários do sistema (estudante e administrador)
import hashlib
import os


class Usuario:
    """Estudante: estuda pelo guia, joga o quiz e acompanha o próprio desempenho."""

    tipo = 'estudante'

    def __init__(self, nome, email, senha_hash, sal):
        self.__nome = nome
        self.__email = email.lower()
        self.__senha_hash = senha_hash
        self.__sal = sal

    @classmethod
    def criar(cls, nome, email, senha):
        """Cria um usuário novo a partir da senha em texto (que não é guardada)."""
        sal = os.urandom(8).hex()
        return cls(nome, email, cls._gerar_hash(senha, sal), sal)

    @staticmethod
    def _gerar_hash(senha, sal):
        return hashlib.sha256((sal + senha).encode('utf-8')).hexdigest()

    def verificar_senha(self, senha):
        return self._gerar_hash(senha, self.__sal) == self.__senha_hash

    @property
    def nome(self):
        return self.__nome

    @property
    def email(self):
        return self.__email

    @property
    def primeiro_nome(self):
        return self.__nome.split()[0]

    # ---- controle de acesso: cada classe responde do seu jeito (polimorfismo) ----
    @property
    def eh_admin(self):
        return False

    @property
    def perfil(self):
        return 'Estudante'

    def pode_acessar(self, area):
        """Diz se o usuário pode entrar em uma área do site."""
        return area in ('guia', 'quiz', 'desempenho')

    def como(self, classe):
        """Cria uma cópia deste usuário como outra classe (usado para promover/rebaixar)."""
        return classe(self.__nome, self.__email, self.__senha_hash, self.__sal)

    # ---- conversão para salvar em JSON ----
    def to_dict(self):
        return {'nome': self.__nome, 'email': self.__email, 'tipo': self.tipo,
                'senha_hash': self.__senha_hash, 'sal': self.__sal}

    @staticmethod
    def from_dict(d):
        # escolhe a classe certa de acordo com o tipo salvo no JSON
        classe = Administrador if d.get('tipo') == 'admin' else Usuario
        return classe(d['nome'], d['email'], d['senha_hash'], d['sal'])


class Administrador(Usuario):
    """Administrador: herda tudo do estudante e ainda gerencia questões e usuários."""

    tipo = 'admin'

    @property
    def eh_admin(self):
        return True

    @property
    def perfil(self):
        return 'Administrador'

    def pode_acessar(self, area):
        return area in ('questoes', 'admin') or super().pode_acessar(area)
