from .TCPSession import TCPSession
from Model.Packet import Packet, generate_id
from Model.TCPFlags import TCPFlag

SYN = (TCPFlag.SYN,)
SYN_ACK = (TCPFlag.SYN, TCPFlag.ACK)
ACK = (TCPFlag.ACK,)
PSH = (TCPFlag.PSH,)
FIN = (TCPFlag.FIN,)


class ClientConnectionToServer(TCPSession):
    def __init__(self):
        super().__init__()
        self.initial_seq_number: int = None
        self.syn_attempts: int = 5

    def connect(self, address: str, port: int):
        #  data validation
        self.server_address = address
        self.server_port = port
        self.udp_socket.set_timeout_time(1)
        self._set_sequence_and_ack_numbers()  # TESTING
        # self._three_way_handshake() # TESTING

    def _three_way_handshake(self):
        attempts = 0
        server_address = (self.server_address, self.server_port)
        self.send_packet(SYN, server_address)

        while attempts < self.syn_attempts:
            attempts += 1
            packet, _ = self.receive_packet(SYN_ACK)
            if packet.flags == SYN_ACK:
                self.send_packet(ACK, server_address)
                print("\n\nConnection established\n\n")
                self._set_sequence_and_ack_numbers()
                break

    def reliability_send(self, data: bytes) -> None:
        server_address = (self.server_address, self.server_port)
        while True:
            try:
                self.send_packet(PSH, server_address, data)
                packet, _ = self.receive_packet(ACK)

            except TimeoutError:
                print("Timeout occurred, leaving recvfrom")
                continue

            if packet.ack_num == self.seq_num:
                self.seq_num += 1
                break

    def reliability_receive(self) -> tuple:
        pass

    def shutdown(self) -> None:
        self._teardown()
        print("\n\nConnection Ended\n\n")
        return

    def _teardown(self) -> None:
        """
        Perform the teardown process for the TCP session for the server.

        Args:
        None
        """
        server_address = (self.server_address, self.server_port)
        self.send_packet(FIN, server_address)
        self.receive_packet(ACK)  # returns server address
        self.receive_packet(FIN)  # returns server address
        self.send_packet(ACK, server_address)
        return

    def _set_sequence_and_ack_numbers(self):
        self.seq_num = 1
        self.ack_num = 0
