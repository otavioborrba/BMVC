# models/pagina.py — Model: dados que a página exibe


class Pilar:
    """Um dos pilares da Orientação a Objetos."""

    def __init__(self, nome, resumo, exemplo):
        self.__nome = nome
        self.__resumo = resumo
        self.__exemplo = exemplo

    @property
    def nome(self):
        return self.__nome

    @property
    def resumo(self):
        return self.__resumo

    @property
    def exemplo(self):
        return self.__exemplo


class Pagina:
    """Conteúdo da página: título, subtítulo e lista de pilares."""

    def __init__(self, titulo, subtitulo, pilares):
        self.titulo = titulo
        self.subtitulo = subtitulo
        self.pilares = pilares

    @classmethod
    def home(cls):
        pilares = [
            Pilar('Abstração',
                  'Representar só o que importa de um objeto do mundo real, '
                  'escondendo detalhes desnecessários.',
                  'class Carro:\n    def acelerar(self): ...'),
            Pilar('Encapsulamento',
                  'Proteger os dados internos do objeto e expor apenas uma '
                  'interface controlada (getters, setters, @property).',
                  'self.__saldo = 0  # atributo privado'),
            Pilar('Herança',
                  'Uma classe filha reaproveita atributos e métodos da '
                  'classe mãe e pode especializá-los.',
                  'class Aluno(Pessoa):\n    ...'),
            Pilar('Polimorfismo',
                  'Objetos diferentes respondem à mesma mensagem cada um '
                  'do seu jeito.',
                  'for a in animais:\n    a.falar()'),
        ]
        return cls('Guia Rápido de Orientação a Objetos',
                   'Os 4 pilares da OO explicados de forma simples, '
                   'com exemplos em Python e um quiz para revisar.',
                   pilares)
