import socket
import ipaddress
import os
import sys

sys.path.append(os.path.abspath("../utils"))
from argument_parser import parse_arguments
from file_operations import open_file, read_file_in_chunks


class ReliableUDPClient:
    def __init__(self, server_address=None, server_port=None):
        self._server_address = server_address
        self._server_port = server_port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    @property
    def server_address(self):
        return self._server_address

    @server_address.setter
    def server_address(self, value):
        try:
            ipaddress.ip_address(value)  # Check if the IP address is valid
            self._server_address = value
        except ValueError:
            raise ValueError(
                "Invalid IP address format. Please provide a valid IP address."
            )

    @property
    def server_port(self):
        return self._server_port

    @server_port.setter
    def server_port(self, value):
        try:
            value = int(value)
            if not (0 <= value <= 65535):
                raise ValueError("Port number must be between 0 and 65535.")
            self._server_port = value
        except ValueError:
            raise ValueError(
                "Invalid port number format. Please provide a valid port number."
            )

    def send(self, data):
        self._socket.sendto(
            str(data).encode(), (self._server_address, self._server_port)
        )

    def receive(self):
        return self._socket.recvfrom(1024)

    def close_socket(self):
        self._socket.close()


# Example usage
if __name__ == "__main__":
    args = parse_arguments()
    server_ip_address = args.ip_address
    server_port = args.port
    file_path = args.file_path

    file = open_file(file_path)
    file_size = os.path.getsize(file_path)
    client = ReliableUDPClient(server_ip_address, server_port)

    client.send(file_size)
    print("File size Send")

    for chunk in read_file_in_chunks(file):
        client.send(chunk)
    print("File Data Send")

    response = client.receive()
    print("Server response:", response)

    file.close()
    client.close_socket()
