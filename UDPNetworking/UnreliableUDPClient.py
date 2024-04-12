from socket import socket, AF_INET, SOCK_DGRAM

BUFF_SIZE = 1024


class ReliableUDPClient:
    def __init__(self, server_address=None, server_port=None):
        self._server_address = server_address
        self._server_port = server_port
        self._socket = socket(AF_INET, SOCK_DGRAM)

    def send(self, data: bytes) -> None:
        self._socket.sendto(data, (self._server_address, self._server_port))

    def receive(self) -> str:
        msg_from_server, _ = self._socket.recvfrom(BUFF_SIZE)
        print(f"Message from Server: {msg_from_server.decode()}")
        return msg_from_server.decode()

    def close_socket(self) -> None:
        try:
            self._socket.close()
        except OSError as e:
            print(f"Error closing socket: {e}")
