from .Session import Session
from Model.Packet import Packet
from Model.TCPFlags import TCPFlag


class ServerConnectionToClient(Session):
    def __init__(self):
        super().__init__()
        self.client_address = None
        self.client_port = None
        self.backlog = None

    def bind(self, address: tuple):
        """
        Binds the server connection to the specified address and port.
        """
        self.server_address = address[0]
        self.server_port = address[1]
        self.udp_socket.bind(address)

    def listen(self, backlog: int):
        self.backlog = backlog
        pass

    def accept(self):
        # receive SYN
        packet: Packet
        packet, address = self.receive_packet((TCPFlag.SYN))
        self.client_address, self.client_port = address
        if (TCPFlag.SYN) == packet.flags:
            # sent SYN, ACK
            self.send_packet(
                (TCPFlag.SYN, TCPFlag.ACK), (self.client_address, self.client_port)
            )
            while True:
                # receive ACK
                packet, address = self.receive_packet((TCPFlag.ACK))
                if (TCPFlag.ACK) == packet.flags:
                    break