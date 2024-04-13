from socket import socket, AF_INET, SOCK_DGRAM

# import pickle
# from .Packet import Packet

BUFF_SIZE = 1024


class UDPSocket:
    """
    A simple wrapper class for a UDP socket.

    Attributes:
    - _socket: The underlying UDP socket object.

    Methods:
    - __init__: Initialize the UDPSocket object.
    - sendto: Send data over the UDP socket to a specified address.
    - recvfrom: Receive data from the UDP socket.
    - bind: Bind the UDP socket to a specified address.
    - close_socket: Close the UDP socket.
    """

    def __init__(self) -> None:
        """
        Initialize the UDPSocket object.
        """
        self._socket = socket(AF_INET, SOCK_DGRAM)

    def sendto(self, data: bytes, address: tuple) -> None:
        """
        Send data over the UDP socket to a specified address.

        Args:
        - data: The data to be sent, in bytes.
        - address: The address (ip, port) to send the data to.
        """
        self._socket.sendto(data, address)
        return

    def recvfrom(self) -> tuple:
        """
        Receive data from the UDP socket.

        Returns:
        - bytes_received: The received bytes of data.
        - address: The address (ip, port) from which the data was received.
        """
        bytes_received, address = self._socket.recvfrom(BUFF_SIZE)
        return (bytes_received, address)

    def timeout(self):
        return self._socket.timeout

    def set_timeout_time(self, time: float) -> None:
        self._socket.settimeout(time)
        return

    def bind(self, address: tuple) -> None:
        """
        Bind the UDP socket to a specified address.

        Args:
        - address: The address (ip, port) to bind the socket to.
        """
        self._socket.bind(address)
        return

    def read(self) -> None:
        pass

    def write(self) -> None:
        pass

    def close_udp_socket(self) -> None:
        """
        Close the UDP socket.
        """
        try:
            self._socket.close()
            return
        except OSError as e:
            print(f"Error closing socket: {e}")
