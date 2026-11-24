# models/repositorio.py — guarda os objetos em arquivos JSON (pasta data/)
import json
import os

from models.usuario import Usuario
from models.questao import Questao
from models.resultado import Resultado


class Repositorio:
    """Classe base: lê e grava uma lista de objetos em um arquivo JSON.
    As classes filhas dizem qual arquivo usar e como converter cada item."""

    arquivo = None

    def __init__(self, pasta='data'):
        self._caminho = os.path.join(pasta, self.arquivo)
        os.makedirs(pasta, exist_ok=True)
        self._itens = self._carregar()

    def _carregar(self):
        if not os.path.exists(self._caminho):
            itens = self.dados_iniciais()
            self._itens = itens
            self._salvar()
            return itens
        with open(self._caminho, encoding='utf-8') as f:
            return [self.converter(d) for d in json.load(f)]

    def _salvar(self):
        with open(self._caminho, 'w', encoding='utf-8') as f:
            json.dump([i.to_dict() for i in self._itens], f,
                      ensure_ascii=False, indent=2)

    def listar(self):
        return list(self._itens)

    # métodos que as filhas sobrescrevem (polimorfismo)
    def converter(self, dados):
        raise NotImplementedError

    def dados_iniciais(self):
        return []


class RepositorioUsuarios(Repositorio):

    arquivo = 'usuarios.json'

    def converter(self, dados):
        return Usuario.from_dict(dados)

    def buscar(self, email):
        email = (email or '').lower()
        return next((u for u in self._itens if u.email == email), None)

    def cadastrar(self, nome, email, senha):
        nome, email = nome.strip(), email.strip().lower()
        if len(nome) < 2:
            raise ValueError('Informe seu nome.')
        if '@' not in email or '.' not in email:
            raise ValueError('E-mail inválido.')
        if len(senha) < 4:
            raise ValueError('A senha precisa ter pelo menos 4 caracteres.')
        if self.buscar(email):
            raise ValueError('Já existe uma conta com esse e-mail.')
        usuario = Usuario.criar(nome, email, senha)
        self._itens.append(usuario)
        self._salvar()
        return usuario

    def autenticar(self, email, senha):
        usuario = self.buscar(email)
        if usuario and usuario.verificar_senha(senha):
            return usuario
        return None


class RepositorioQuestoes(Repositorio):

    arquivo = 'questoes.json'

    def converter(self, dados):
        return Questao.from_dict(dados)

    def dados_iniciais(self):
        base = [
            # ---- Abstração ----
            ('Modelar só as características relevantes de algo do mundo real é...',
             ['Abstração', 'Encapsulamento', 'Polimorfismo'], 0, 'Abstração'),
            ('Em Python, qual módulo permite criar classes abstratas?',
             ['math', 'abc', 'typing', 'os'], 1, 'Abstração'),
            ('O que acontece ao instanciar uma classe que tem um @abstractmethod não implementado?',
             ['O objeto é criado normalmente', 'O método passa a retornar None',
              'Ocorre um TypeError', 'O Python ignora o decorator'], 2, 'Abstração'),
            ('Uma classe abstrata serve principalmente para...',
             ['Definir um modelo que as subclasses devem seguir', 'Guardar variáveis globais',
              'Substituir as funções do programa', 'Deixar o programa mais rápido'], 0, 'Abstração'),
            # ---- Encapsulamento ----
            ('Em Python, o que um atributo como self.__saldo representa?',
             ['Um atributo privado (encapsulamento)', 'Um método estático', 'Uma classe abstrata'], 0, 'Encapsulamento'),
            ('Qual decorator transforma um método em um atributo de leitura?',
             ['@staticmethod', '@classmethod', '@property', '@abstractmethod'], 2, 'Encapsulamento'),
            ('Por que usar um setter com validação em vez de deixar o atributo público?',
             ['Para deixar o código mais lento', 'Para impedir que o objeto receba valores inválidos',
              'Porque o Python não aceita atributos públicos', 'Para criar herança'], 1, 'Encapsulamento'),
            ('Em Python, um atributo com um único underline (self._nome) indica que...',
             ['É privado por convenção, mas ainda pode ser acessado', 'É uma constante',
              'Só existe dentro do construtor', 'É um atributo estático'], 0, 'Encapsulamento'),
            # ---- Herança ----
            ('Qual pilar permite que uma classe filha reaproveite código da classe mãe?',
             ['Encapsulamento', 'Herança', 'Abstração'], 1, 'Herança'),
            ('Qual função chama um método da classe mãe dentro da classe filha?',
             ['self()', 'parent()', 'super()', 'base()'], 2, 'Herança'),
            ('Como se declara que a classe Aluno herda de Pessoa em Python?',
             ['class Aluno extends Pessoa:', 'class Aluno(Pessoa):',
              'class Aluno inherits Pessoa:', 'class Pessoa(Aluno):'], 1, 'Herança'),
            ('Qual função verifica se um objeto é instância de uma classe (ou de uma filha dela)?',
             ['type()', 'isinstance()', 'issubclass()', 'id()'], 1, 'Herança'),
            ('Quando a classe filha redefine um método que já existe na mãe, isso se chama...',
             ['Sobrescrita (override)', 'Sobrecarga de construtor', 'Encapsulamento', 'Composição'], 0, 'Herança'),
            # ---- Polimorfismo ----
            ('Objetos diferentes respondendo ao mesmo método de formas diferentes é...',
             ['Abstração', 'Herança', 'Polimorfismo'], 2, 'Polimorfismo'),
            ('Duck typing, em Python, significa que...',
             ['Só classes com nome de animal viram objetos',
              'O que importa são os métodos que o objeto tem, não o tipo dele',
              'Toda classe precisa herdar de object', 'Uma variável nunca pode mudar de tipo'], 1, 'Polimorfismo'),
            ('Qual método especial define o que aparece ao fazer print(objeto)?',
             ['__init__', '__str__', '__len__', '__del__'], 1, 'Polimorfismo'),
            ('Usar + para somar números e também para juntar strings é um exemplo de...',
             ['Herança', 'Abstração', 'Polimorfismo (sobrecarga de operador)', 'Encapsulamento'], 2, 'Polimorfismo'),
            # ---- Geral ----
            ('No padrão MVC, quem decide qual página (view) será exibida?',
             ['Model', 'Controller', 'View'], 1, 'Geral'),
            ('No padrão MVC, onde ficam os dados e as regras da aplicação?',
             ['View', 'Controller', 'Model', 'Static'], 2, 'Geral'),
            ('O que é um objeto?',
             ['Um arquivo .py', 'Uma instância de uma classe', 'Um tipo de laço de repetição', 'Uma biblioteca'], 1, 'Geral'),
            ('Qual método é chamado automaticamente quando um objeto é criado em Python?',
             ['__init__', '__start__', '__create__', '__main__'], 0, 'Geral'),
            ('O que o parâmetro self representa dentro de um método?',
             ['A classe mãe', 'O próprio objeto que chamou o método', 'Uma variável global', 'O módulo atual'], 1, 'Geral'),
            ('Composição é quando...',
             ['Uma classe herda de duas outras', 'Um objeto é formado por outros objetos',
              'Um método chama a si mesmo', 'Duas classes têm o mesmo nome'], 1, 'Geral'),
            ('Qual a diferença entre @classmethod e @staticmethod?',
             ['Nenhuma, são iguais', '@classmethod recebe a classe (cls); @staticmethod não recebe nem a classe nem o objeto',
              '@staticmethod recebe o self', '@classmethod só funciona em classes abstratas'], 1, 'Geral'),
        ]
        return [Questao(i + 1, e, a, c, p, 'sistema') for i, (e, a, c, p) in enumerate(base)]

    def buscar(self, id):
        return next((q for q in self._itens if q.id == id), None)

    def criar(self, enunciado, alternativas, correta, pilar, autor):
        novo_id = max((q.id for q in self._itens), default=0) + 1
        questao = Questao(novo_id, enunciado, alternativas, correta, pilar, autor)
        self._itens.append(questao)
        self._salvar()
        return questao

    def atualizar(self, id, enunciado, alternativas, correta, pilar):
        questao = self.buscar(id)
        if questao is None:
            raise KeyError(id)
        questao.atualizar(enunciado, alternativas, correta, pilar)
        self._salvar()
        return questao

    def excluir(self, id):
        questao = self.buscar(id)
        if questao is None:
            raise KeyError(id)
        self._itens.remove(questao)
        self._salvar()


class RepositorioResultados(Repositorio):

    arquivo = 'resultados.json'

    def converter(self, dados):
        return Resultado.from_dict(dados)

    def registrar(self, email, respostas):
        resultado = Resultado(email, respostas)
        self._itens.append(resultado)
        self._salvar()
        return resultado

    def do_usuario(self, email):
        return [r for r in self._itens if r.email == email]
