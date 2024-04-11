from Model.UDPSocket import UDPSocket


class Session:
    """
    It creates TCP like session, that provides reliability.
    """

    def __init__(self):
        self.udp_socket = UDPSocket()
        self.server_address = None
        self.server_port = None
        self.seq_number = None
        self.ack_number = None
        # implement timer

    def bind(self, address: tuple):
        self.server_address = address[0]
        self.server_port = address[1]
        self.udp_socket.udp_bind(address)

    def send(self, data):
        """
        This for the user, not for us. Handle
        """
        #  Need to use packet
        self.udp_socket.sendto(data, (self.server_address, self.server_port))
        # receive ACK
        self.seq_number += 1

    def receive(self) -> tuple:
        return self.udp_socket.recvfrom()

    def close(self):
        self._teardown()
        pass

    def _teardown(self):
        pass
