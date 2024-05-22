from socket import socket
import threading
import logging  # Para melhor registro
from http_parser.http import HTTPParser


class MyRequestHandler(object):

    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.parser = HTTPParser()

    def handle(self):
        """Manipula a solicitação do cliente."""
        while True:
            data = self.client_socket.recv(1024)
            if not data:
                break

            self.parser.feed(data)

        # Processar os dados analisados ​​pelo parser
        if self.parser.is_done():
            # Extrair informações relevantes da solicitação HTTP
            method = self.parser.method
            path = self.parser.path
            headers = self.parser.headers

            # Gerar resposta apropriada com base na solicitação
            response = generate_response(method, path, headers)

            # Enviar a resposta de volta ao cliente
            self.client_socket.sendall(response)

def generate_response(method, path, headers):
    """Gera uma resposta HTTP com base na solicitação."""
    # Implementar lógica para gerar a resposta apropriada
    pass


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST_NAME, PORT_NUMBER))
        server_socket.listen(5)

        logging.info("Servidor iniciado na porta %d", PORT_NUMBER)

        while True:
            server_socket.settimeout(1)  # Definir um tempo limite para aceitar conexões
            try:
                client_connection, client_address = server_socket.accept()
                with client_connection:
                    logging.info("Conectado por %s:%d", client_address[0], client_address[1])
                    request_handler = MyRequestHandler(client_connection)
                    request_handler.handle()
            except socket.timeout:
                pass  # Lidar com tempos limite com elegância

if __name__ == "__main__":
    HOST_NAME = "localhost"
    PORT_NUMBER = 8000  # Ou qualquer número de porta desejado (evite portas privilegiadas < 1024)

    logging.basicConfig(level=logging.INFO)
    start_server()
