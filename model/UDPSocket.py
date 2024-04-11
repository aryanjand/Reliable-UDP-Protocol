from socket import socket, AF_INET, SOCK_DGRAM
import pickle
from .Packet import Packet


BUFF_SIZE = 1024


class UDPSocket:
    """
    Udp Socket
    """

    def __init__(self) -> None:
        self._socket = socket(AF_INET, SOCK_DGRAM)

    def sendto(self, data: bytes, address: tuple) -> None:
        self._socket.sendto(data, address)

    def recvfrom(self) -> tuple:
        bytes_received, address = self._socket.recvfrom(BUFF_SIZE)
        packet: Packet = pickle.loads(bytes_received)
        # print(
        #     f"Packet from Server: {packet}\n"
        #     f"Seq: {packet.seq_num}\n"
        #     f"Ack: {packet.ack_num}\n"
        #     f"Flags: {packet.flags}\n"
        #     f"Data: {packet.data}"
        # )
        return (bytes_received, address)

    def bind(self, address: tuple):
        self._socket.bind(address)

    def read(self) -> None:
        pass

    def write(self) -> None:
        pass

    def close_socket(self) -> None:
        try:
            self._socket.close()
        except OSError as e:
            print(f"Error closing socket: {e}")
