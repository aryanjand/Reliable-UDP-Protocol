from .TCPSession import TCPSession
from Model.Packet import Packet
from Model.TCPFlags import TCPFlag

SYN = (TCPFlag.SYN,)
SYN_ACK = (TCPFlag.SYN, TCPFlag.ACK)
ACK = (TCPFlag.ACK,)
PSH = (TCPFlag.PSH,)
FIN = (TCPFlag.FIN,)


class ServerConnectionToClient(TCPSession):
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
        packet, address = self.receive_packet(SYN)
        if SYN == packet.flags:
            # sent SYN, ACK
            self.send_packet(SYN_ACK, address)
            while True:
                # receive ACK
                packet, address = self.receive_packet(ACK)
                if ACK == packet.flags:
                    print("\n\nConnection established\n\n")
                    self._initialize_values(address)
                    break

    def reliability_receive(self) -> Packet | None:
        packet, address = self.receive_packet(PSH)
        self._initialize_values(address)  # TESTING ONLY

        if self._check_packet_numbers(packet):
            self.ack_num += 1
            self.send_packet(ACK, address)
            return packet
        self.send_packet(ACK, address)
        return

    def reliability_send(self, data: bytes) -> None:
        pass

    def shutdown(self) -> None:
        self._teardown()
        print("\n\nConnection Ended\n\n")

    def _teardown(self) -> None:
        """
        Perform the teardown process for the TCP session.

        Args:
        - is_client_initiator: True if the client is initiating the teardown, False otherwise.
        """
        client_address = (self.client_address, self.client_port)
        self.receive_packet(FIN)  # returns server address
        self.send_packet(ACK, client_address)
        self.send_packet(FIN, client_address)
        self.receive_packet(ACK)  # returns server address

    def _initialize_values(self, address: tuple) -> None:
        self.client_address, self.client_port = address
        self.seq_num = 0
        self.ack_num = 0

    def _check_packet_numbers(self, packet: Packet) -> int:
        return packet.seq_num == self.seq_num + 1 and packet.ack_num == self.ack_num
