import socket
from threading import Thread

class Client:
    def __init__(self, server_addr):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listen_function = None
        self.server_addr = server_addr

    def listen(self):
        def wrap0(f):
            def wrap():
                data, addr = self.client.recvfrom(1024)
                response = f(data.decode())
                self.client.sendto(response.encode(), addr)
            
            self.listen_function = wrap
            return None
        return wrap0
    def send_to_server(self, data):
        self.client.sendto(data.encode(), self.server_addr)

    def run(self):
        self.running = True
        self.run_thread = Thread(target=self.listen_function)
        self.run_thread.start()

    def _run(self):
        while self.running:
            self.listen_function()

    def close(self):
        self.running = False
        self.client.close()

c = Client(("172.18.1.32", 5454))
@c.listen()
def listen(data):
    print(data)
    return input("> ")

c.send_to_server("CONNECT LEO")
c.run()

input()
c.close()
