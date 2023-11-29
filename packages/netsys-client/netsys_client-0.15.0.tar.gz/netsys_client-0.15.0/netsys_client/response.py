import socket
import json

class Response:

    _host = 'localhost'
    _port = 12345

    def send_message(self, message):

        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.connect((self._host, self._port))
        self._client.sendall(str.encode(message))
        data = self._client.recv(4096)
        print('Recebido:', data.decode())
        self._client.close()

    