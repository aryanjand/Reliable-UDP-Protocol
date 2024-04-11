from socket import socket, AF_INET, SOCK_DGRAM
from Model.Packet import Packet
import pickle

BUFF_SIZE = 1024


class ReliableUDPServer:
    def __init__(self, server_address: str, server_port: int) -> None:
        self.server_address: str = server_address
        self.server_port: int = server_port
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind((self.server_address, self.server_port))
        print(f"Server created bound to port: ${server_port}")

    def receive(self) -> str:
        try:
            bytes_received, address = self.socket.recvfrom(BUFF_SIZE)
            packet = pickle.loads(bytes_received)
            print(f"Client IP Address: {address}")
            print(
                f"Packet from Server: {packet} {packet.seq_num} {packet.ack_num} {packet.flags} {packet.data}"
            )
            return packet
        except Exception as e:
            print(f"Error receiving message: {e}")
            return ""

    def send(self, data: str, client_address: tuple) -> None:
        self.socket.sendto(data.encode(), client_address)
        return None
