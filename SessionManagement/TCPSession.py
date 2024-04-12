from Model.UDPSocket import UDPSocket
from Model.Packet import Packet
from Model.TCPFlags import TCPFlag
from Utils.serializer import serialize, deserialize
from abc import ABC, abstractmethod


class TCPSession(ABC):
    """
    A class that creates a TCP-like session using UDP, providing reliability features.

    Attributes:
    - udp_socket: An instance of UDPSocket for communication.
    - server_address: The address of the server.
    - server_port: The port number of the server.
    - seq_number: The sequence number for the session.
    - ack_number: The acknowledgment number for the session.

    Methods:
    - __init__: Initialize the Session object.
    - bind: Bind the session to a specified address.
    - send: Send data over the session with reliability features.
    - receive: Receive data from the session with reliability features.
    - close: Close the session.
    - _teardown: Perform the teardown process for the session.
    """

    def __init__(self):
        """
        Initialize the Session object.
        """
        self.udp_socket: UDPSocket = UDPSocket()
        self.server_address: str = None
        self.server_port: int = None
        self.seq_number: int = None
        self.ack_number: int = None
        # implement timer

    def bind(self, address: tuple):
        """
        Bind the session to a specified address.

        Args:
        - address: The address (ip, port) to bind the session to.
        """
        self.server_address: str = address[0]
        self.server_port: int = address[1]
        self.udp_socket.bind(address)

    def reliability_send(self, data: bytes):
        """
        Need to reliability features in here. Receive ACK and timeout.
        Send data over the session with reliability features.

        Args:
        - data: The data to be sent, in bytes.
        """
        self.udp_socket.sendto(data, (self.server_address, self.server_port))
        # Receive ACK
        self.seq_number += 1

    def reliability_receive(self) -> tuple:
        """
        Need to reliability features in here.
        Receive data from the session with reliability features.

        Returns:
        - bytes_received: The received bytes of data.
        - address: The address (ip, port) from which the data was received.
        """
        return self.udp_socket.recvfrom()

    def send_packet(self, flags: tuple, address: tuple, data: bytes = None) -> None:
        """
        Send a packet over the session with reliability features.

        Args:
        - flags: The flags for the packet.
        - data: The data to be sent, in bytes.
        """
        packet = Packet(self.seq_number, self.ack_number, flags, data)
        packet_serialize = serialize(packet)
        self.udp_socket.sendto(packet_serialize, address)
        print(f"Sent {flags} Packet")

    def receive_packet(self, flags: tuple) -> tuple:
        """
        Receive a packet from the session with reliability features.

        Args:
        - flags: The expected flags for the received packet.

        Returns:
        - packet: The received packet.
        - client_address: The address (ip, port) from which the data was received.
        """
        bytes_received, client_address = self.udp_socket.recvfrom()
        print(
            f"Check Server for Client Address {client_address}"
        )  # Debugging: Missing Client Address
        packet: Packet = deserialize(bytes_received)
        print(f"Received: {packet.flags} Packet. Data: {packet.data}")
        if packet.flags == flags:
            return (packet, client_address)
        else:
            raise ValueError(f"Received packet with unexpected flags {packet.flags}")

    @abstractmethod
    def shutdown(self) -> None:
        """
        Shutdown the TCP session.
        """
        pass

    def close(self) -> None:
        """
        Close the TCP session.
        """
        pass

    @abstractmethod
    def _teardown(self) -> None:
        """
        Perform the teardown process for the TCP session.
        """
        pass
