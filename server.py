import socket
from threading import Thread
from ast import literal_eval
from time import sleep
from uuid import uuid4
import secrets

class Server:
    def __init__(self, ip=None, port=5454):
        print("\033c", end="\r")
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = self.get_ip()
        self.port = port
        self.server.bind((self.ip, 5454))
        print(f"[ * ] Vinculado como: {self.ip}:{self.port}")
        self.clients = []
        self.game_data = {}
        self.generated_tokens = set()

    def gen_token(self):
        while True:
            token = secrets.token_bytes(4)

            if token not in self.generated_tokens:
                self.generated_tokens.add(token)
                return token.hex()

    def connect(self, data, addr):
        try:
            data = data.decode().split()
            if data[0] == "CONNECT":
                if len(self.clients) >= 4:
                    self.server.sendto(b"Error\nErro, o servidor esta cheio.", addr)
                    # print("[ ! ] Erro, o servidor está cheio")
                    return
                _id = len(self.clients)
                client = {"id": len(self.clients), "name": data[1], "addr": addr, "session_id": self.gen_token()}
                print(f"[ + ]\t\033[1;42m{data[1]}#{_id}\033[0m\t\033[1;44m{addr[0]}\033[0m\t\033[1;41m{client['session_id']}\033[0m")
                self.clients.append(client)
                self.server.sendto(f"CONNECTED\t{_id}\n{client['session_id']}\t{self.ip}\n".encode(), addr)
        except Exception as e:
            print(e)

    def sent_data(self, pkg_ps):
        def wrap0(f):
            def wrap():
                for client in self.clients:
                    try:
                        self.server.sendto(f().encode(), client["addr"])
                    except Exception as e:
                        print(f"Erro em sent_data: {e}")
                sleep(1 / pkg_ps)
            self.sent_function = wrap
        return wrap0

    def receive_data(self):
        def wrap0(f):
            def wrap():
                try:
                    data, addr = self.server.recvfrom(1024)
                    self.connect(data, addr)
                    f(data.decode())
                except Exception as e:
                    pass
            self.listen_function = wrap
        return wrap0

    def run(self):
        self.running = True
        self.server.settimeout(0.5)
        self.threads = {}
        self.threads["_run"] = Thread(target=self._run)
        self.threads["_run"].start()
        print("[ * ] Aguardando conexões")

    def _run(self):
        try:
            while self.running:
                self.listen_function()
                self.sent_function()
        finally:
            self.server.close()

    def stop(self):
        print("[ * ] Parando o serviço")
        self.running = False
        for thread in self.threads.values():
            thread.join()
        self.server.close()
        print("[ * ] Serviço parado")

    @staticmethod
    def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        except Exception as e:
            print(f"[ ! ] Erro ao obter o IP: {e}")
            ip = None
        finally:
            s.close()
        return ip

if __name__ == "__main__":
    s = Server()

    # Envia dados a todos os clientes 100 vezes por segundo
    @s.sent_data(100)
    def sent_data():
        return ""

    # Recebe dados dos clientes
    @s.receive_data()
    def receive_data(data):
        if data[0] == "{":
            pass
        print("Mensagem recebida:", data)

    s.run()
    # Aguarda um ENTER para fechar o programa
    input()
    s.stop()

    print(*s.clients, sep="\n")
