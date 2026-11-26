# controllers/tempo_real.py — comunicação em tempo real via WebSocket
#
# O servidor WebSocket roda numa thread separada (porta 8081), ao lado do Bottle
# (porta 8080). Quando algo acontece no sistema (um quiz terminado, uma questão
# criada, alguém entrando), o controller chama publicar() e todas as páginas
# abertas recebem o aviso na hora, sem precisar recarregar.
#
# Foi feito só com a biblioteca padrão do Python, seguindo o protocolo
# WebSocket (RFC 6455): handshake HTTP + troca de "frames".
import base64
import hashlib
import json
import secrets
import socket
import struct
import threading
from datetime import datetime
from urllib.parse import urlparse, parse_qs

GUID_WEBSOCKET = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'


class ConexaoWebSocket:
    """Uma aba de navegador conectada ao servidor."""

    def __init__(self, sock, usuario):
        self.__sock = sock
        self.__lock = threading.Lock()
        self.usuario = usuario          # {'nome', 'email', 'admin'}
        self.aberta = True

    # ---------- leitura ----------
    def _receber_exato(self, n):
        dados = b''
        while len(dados) < n:
            parte = self.__sock.recv(n - len(dados))
            if not parte:
                raise ConnectionError('conexão fechada')
            dados += parte
        return dados

    def receber(self):
        """Lê um frame do navegador. Retorna (opcode, conteudo)."""
        b1, b2 = self._receber_exato(2)
        opcode = b1 & 0x0F
        tamanho = b2 & 0x7F
        if tamanho == 126:
            tamanho = struct.unpack('>H', self._receber_exato(2))[0]
        elif tamanho == 127:
            tamanho = struct.unpack('>Q', self._receber_exato(8))[0]
        mascara = self._receber_exato(4) if b2 & 0x80 else b'\x00' * 4
        conteudo = bytearray(self._receber_exato(tamanho))
        for i in range(len(conteudo)):           # o navegador sempre "mascara" os dados
            conteudo[i] ^= mascara[i % 4]
        return opcode, bytes(conteudo)

    # ---------- escrita ----------
    def _enviar_frame(self, opcode, conteudo):
        cabecalho = bytes([0x80 | opcode])
        n = len(conteudo)
        if n < 126:
            cabecalho += bytes([n])
        elif n < 65536:
            cabecalho += bytes([126]) + struct.pack('>H', n)
        else:
            cabecalho += bytes([127]) + struct.pack('>Q', n)
        with self.__lock:
            self.__sock.sendall(cabecalho + conteudo)

    def enviar(self, mensagem):
        """Envia um dicionário como JSON (frame de texto)."""
        try:
            self._enviar_frame(0x1, json.dumps(mensagem, ensure_ascii=False).encode('utf-8'))
        except OSError:
            self.aberta = False

    def pong(self, conteudo):
        self._enviar_frame(0xA, conteudo)

    def fechar(self):
        self.aberta = False
        try:
            self._enviar_frame(0x8, b'')
        except OSError:
            pass
        try:
            self.__sock.close()
        except OSError:
            pass


class CentralTempoReal:
    """Guarda as conexões abertas e distribui os eventos para todas elas."""

    def __init__(self, host='127.0.0.1', porta=8081):
        self.host = host
        self.porta = porta
        self.__conexoes = set()
        self.__tokens = {}              # token -> dados do usuário
        self.__atividades = []          # últimas atividades (para quem abrir a página depois)
        self.__lock = threading.Lock()

    # ---------- autenticação ----------
    def token_para(self, usuario):
        """Gera um token para a página do usuário logado se conectar ao WebSocket."""
        token = secrets.token_urlsafe(16)
        with self.__lock:
            if len(self.__tokens) > 5000:      # evita crescer para sempre
                self.__tokens.clear()
            self.__tokens[token] = {'nome': usuario.nome, 'email': usuario.email,
                                    'admin': usuario.eh_admin}
        return token

    # ---------- servidor ----------
    def iniciar(self):
        """Abre a porta do WebSocket numa thread separada do Bottle."""
        try:
            servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            servidor.bind((self.host, self.porta))
            servidor.listen(50)
        except OSError as erro:
            print(f'[WebSocket] não foi possível usar a porta {self.porta}: {erro}')
            return False
        threading.Thread(target=self._aceitar, args=(servidor,), daemon=True).start()
        print(f'[WebSocket] ouvindo em ws://{self.host}:{self.porta}')
        return True

    def _aceitar(self, servidor):
        while True:
            sock, _ = servidor.accept()
            threading.Thread(target=self._atender, args=(sock,), daemon=True).start()

    def _handshake(self, sock):
        """Lê o pedido HTTP do navegador e responde 101 (troca para WebSocket)."""
        pedido = b''
        while b'\r\n\r\n' not in pedido:
            parte = sock.recv(1024)
            if not parte or len(pedido) > 8192:
                return None
            pedido += parte
        linhas = pedido.decode('latin-1').split('\r\n')
        caminho = linhas[0].split(' ')[1] if len(linhas[0].split(' ')) > 1 else '/'
        cabecalhos = {}
        for linha in linhas[1:]:
            if ':' in linha:
                nome, valor = linha.split(':', 1)
                cabecalhos[nome.strip().lower()] = valor.strip()

        token = parse_qs(urlparse(caminho).query).get('token', [''])[0]
        with self.__lock:
            usuario = self.__tokens.get(token)
        chave = cabecalhos.get('sec-websocket-key')
        if usuario is None or not chave or cabecalhos.get('upgrade', '').lower() != 'websocket':
            sock.sendall(b'HTTP/1.1 403 Forbidden\r\nContent-Length: 0\r\n\r\n')
            return None

        aceite = base64.b64encode(hashlib.sha1((chave + GUID_WEBSOCKET).encode()).digest()).decode()
        sock.sendall(('HTTP/1.1 101 Switching Protocols\r\n'
                      'Upgrade: websocket\r\nConnection: Upgrade\r\n'
                      f'Sec-WebSocket-Accept: {aceite}\r\n\r\n').encode())
        return dict(usuario)

    def _atender(self, sock):
        conexao = None
        try:
            usuario = self._handshake(sock)
            if usuario is None:
                sock.close()
                return
            conexao = ConexaoWebSocket(sock, usuario)
            with self.__lock:
                self.__conexoes.add(conexao)
            self._avisar_online()
            while conexao.aberta:
                opcode, conteudo = conexao.receber()
                if opcode == 0x8:                 # o navegador fechou a aba
                    break
                if opcode == 0x9:                 # ping -> responde pong
                    conexao.pong(conteudo)
        except (OSError, ConnectionError, ValueError):
            pass
        finally:
            if conexao is not None:
                conexao.fechar()
                with self.__lock:
                    self.__conexoes.discard(conexao)
                self._avisar_online()

    # ---------- envio de eventos ----------
    def publicar(self, tipo, dados, so_admin=False):
        """Envia um evento {tipo, dados} para todas as páginas conectadas."""
        mensagem = {'tipo': tipo, 'dados': dados}
        with self.__lock:
            destinos = [c for c in self.__conexoes if c.usuario['admin'] or not so_admin]
        for conexao in destinos:
            conexao.enviar(mensagem)

    def online(self):
        with self.__lock:
            nomes = {c.usuario['email']: c.usuario['nome'] for c in self.__conexoes}
        return sorted(nomes.values(), key=str.lower)

    def _avisar_online(self):
        nomes = self.online()
        self.publicar('online', {'total': len(nomes), 'nomes': nomes})

    def registrar_atividade(self, icone, texto, autor=''):
        """Guarda uma atividade e avisa todo mundo na hora."""
        atividade = {'icone': icone, 'texto': texto, 'autor': autor,
                     'hora': datetime.now().strftime('%H:%M:%S')}
        with self.__lock:
            self.__atividades.insert(0, atividade)
            del self.__atividades[20:]
        self.publicar('atividade', atividade)

    def atividades(self):
        with self.__lock:
            return list(self.__atividades)
