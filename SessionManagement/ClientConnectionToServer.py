from .TCPSession import TCPSession
from Model.Packet import Packet, generate_id
from Model.TCPFlags import TCPFlag


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
        # self._three_way_handshake() : TESTING

    def _three_way_handshake(self):
        attempts = 0
        self.send_packet((TCPFlag.SYN), (self.server_address, self.server_port))

        while attempts < self.syn_attempts:
            attempts += 1
            packet: Packet
            packet, _ = self.receive_packet((TCPFlag.SYN, TCPFlag.ACK))
            if packet.flags == (TCPFlag.SYN, TCPFlag.ACK):
                self.send_packet((TCPFlag.ACK), (self.server_address, self.server_port))
                print("\n\nConnection established\n\n")
                self.initial_seq_number = self.seq_num = generate_id()
                self.ack_num = 0
                break

    def reliability_send(self, data: bytes) -> None:
        while True:
            try:
                self.send_packet(
                    (TCPFlag.PSH), (self.server_address, self.server_port), data
                )
                packet, _ = self.receive_packet((TCPFlag.ACK))

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

    def _teardown(self) -> None:
        """
        Perform the teardown process for the TCP session.

        Args:
        - is_client_initiator: True if the client is initiating the teardown, False otherwise.
        """
        self.send_packet((TCPFlag.FIN), (self.server_address, self.server_port))
        self.receive_packet((TCPFlag.ACK))  # returns server address
        self.receive_packet((TCPFlag.FIN))  # returns server address
        self.send_packet((TCPFlag.ACK), (self.server_address, self.server_port))
