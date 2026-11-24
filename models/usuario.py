# models/usuario.py — Model: usuário que acessa o sistema
import hashlib
import os


class Usuario:
    """Usuário: estuda pelo guia, gerencia o banco de questões, joga o quiz e vê o desempenho."""

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

    # ---- conversão para salvar em JSON ----
    def to_dict(self):
        return {'nome': self.__nome, 'email': self.__email,
                'senha_hash': self.__senha_hash, 'sal': self.__sal}

    @classmethod
    def from_dict(cls, d):
        return cls(d['nome'], d['email'], d['senha_hash'], d['sal'])
