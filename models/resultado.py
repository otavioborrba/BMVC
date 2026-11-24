# models/resultado.py — Model: resultado de um quiz e desempenho do usuário
from datetime import datetime

from models.questao import PILARES


class Resultado:
    """Um quiz respondido: guarda cada resposta (pilar e se acertou)."""

    def __init__(self, email, respostas, data=None):
        self.__email = email
        self.__respostas = respostas          # [{'pilar': ..., 'acertou': True/False}]
        self.__data = data or datetime.now().strftime('%d/%m/%Y %H:%M')

    @property
    def email(self):
        return self.__email

    @property
    def data(self):
        return self.__data

    @property
    def respostas(self):
        return list(self.__respostas)

    @property
    def total(self):
        return len(self.__respostas)

    @property
    def acertos(self):
        return sum(1 for r in self.__respostas if r['acertou'])

    @property
    def percentual(self):
        return round(self.acertos / self.total * 100) if self.total else 0

    def to_dict(self):
        return {'email': self.__email, 'data': self.__data, 'respostas': self.__respostas}

    @classmethod
    def from_dict(cls, d):
        return cls(d['email'], d['respostas'], d['data'])


class Desempenho:
    """Junta todos os resultados de um usuário e calcula os índices de acerto."""

    def __init__(self, resultados):
        self.__resultados = list(resultados)

    def __respostas(self):
        return [r for res in self.__resultados for r in res.respostas]

    @property
    def quizzes(self):
        return len(self.__resultados)

    @property
    def respondidas(self):
        return len(self.__respostas())

    @property
    def acertos(self):
        return sum(1 for r in self.__respostas() if r['acertou'])

    @property
    def indice_geral(self):
        return round(self.acertos / self.respondidas * 100) if self.respondidas else 0

    @property
    def melhor(self):
        return max(self.__resultados, key=lambda r: (r.percentual, r.acertos), default=None)

    def por_pilar(self):
        """Lista de (pilar, acertos, total, percentual) para cada pilar."""
        tabela = []
        for pilar in PILARES:
            do_pilar = [r for r in self.__respostas() if r['pilar'] == pilar]
            acertos = sum(1 for r in do_pilar if r['acertou'])
            total = len(do_pilar)
            pct = round(acertos / total * 100) if total else None
            tabela.append((pilar, acertos, total, pct))
        return tabela

    def pilar_mais_fraco(self):
        com_dados = [p for p in self.por_pilar() if p[2] > 0]
        return min(com_dados, key=lambda p: p[3])[0] if com_dados else None

    def historico(self, limite=10):
        return list(reversed(self.__resultados))[:limite]
