from Model.UDPSocket import UDPSocket


class Session:
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

    def send(self, data: bytes):
        """
        Need to reliability features in here. Receive ACK and timeout.
        Send data over the session with reliability features.

        Args:
        - data: The data to be sent, in bytes.
        """
        self.udp_socket.sendto(data, (self.server_address, self.server_port))
        # Receive ACK
        self.seq_number += 1

    def receive(self) -> tuple:
        """
        Need to reliability features in here.
        Receive data from the session with reliability features.

        Returns:
        - bytes_received: The received bytes of data.
        - address: The address (ip, port) from which the data was received.
        """
        return self.udp_socket.recvfrom()

    def close(self):
        self._teardown()

    def _teardown(self):
        pass
