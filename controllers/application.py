# controllers/application.py — Controller: decide qual view mostrar
from bottle import template
from models.pagina import Pagina


class Application:

    def __init__(self):
        # Mapa: nome da página -> método que a renderiza
        self.pages = {
            'home': self.home,
            'erro404': self.erro404,
        }

    def render(self, page):
        content = self.pages.get(page, self.erro404)
        return content()

    def home(self):
        pagina = Pagina.home()
        return template('views/html/home', pagina=pagina)

    def erro404(self):
        return template('views/html/erro404')
