# models/questao.py — Model: questão de múltipla escolha sobre OO

PILARES = ['Abstração', 'Encapsulamento', 'Herança', 'Polimorfismo', 'Geral']


class Questao:

    def __init__(self, id, enunciado, alternativas, correta, pilar, autor):
        self.__id = id
        self.enunciado = enunciado
        self.alternativas = alternativas
        self.correta = correta
        self.pilar = pilar
        self.__autor = autor

    # ---- id e autor não mudam depois de criados ----
    @property
    def id(self):
        return self.__id

    @property
    def autor(self):
        return self.__autor

    # ---- atributos com validação (encapsulamento) ----
    @property
    def enunciado(self):
        return self.__enunciado

    @enunciado.setter
    def enunciado(self, valor):
        valor = (valor or '').strip()
        if len(valor) < 10:
            raise ValueError('O enunciado precisa ter pelo menos 10 caracteres.')
        self.__enunciado = valor

    @property
    def alternativas(self):
        return list(self.__alternativas)

    @alternativas.setter
    def alternativas(self, lista):
        lista = [a.strip() for a in lista if a and a.strip()]
        if len(lista) < 2:
            raise ValueError('Informe pelo menos 2 alternativas.')
        if len(set(a.lower() for a in lista)) != len(lista):
            raise ValueError('Existem alternativas repetidas.')
        self.__alternativas = lista

    @property
    def correta(self):
        return self.__correta

    @correta.setter
    def correta(self, indice):
        indice = int(indice)
        if not 0 <= indice < len(self.__alternativas):
            raise ValueError('Marque qual alternativa é a correta.')
        self.__correta = indice

    @property
    def pilar(self):
        return self.__pilar

    @pilar.setter
    def pilar(self, valor):
        if valor not in PILARES:
            raise ValueError('Escolha um pilar válido.')
        self.__pilar = valor

    @property
    def resposta(self):
        return self.__alternativas[self.__correta]

    def atualizar(self, enunciado, alternativas, correta, pilar):
        # valida tudo antes de alterar, para não deixar o objeto pela metade
        Questao(self.__id, enunciado, alternativas, correta, pilar, self.__autor)
        self.enunciado = enunciado
        self.alternativas = alternativas
        self.correta = correta
        self.pilar = pilar

    # ---- conversão para salvar em JSON ----
    def to_dict(self):
        return {'id': self.__id, 'enunciado': self.__enunciado,
                'alternativas': self.__alternativas, 'correta': self.__correta,
                'pilar': self.__pilar, 'autor': self.__autor}

    @classmethod
    def from_dict(cls, d):
        return cls(d['id'], d['enunciado'], d['alternativas'],
                   d['correta'], d['pilar'], d['autor'])
