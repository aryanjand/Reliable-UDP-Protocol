from .Session import Session
from Model.Packet import Packet, generate_id
from Model.TCPFlags import TCPFlag


class ClientConnectionToServer(Session):
    def __init__(self):
        super().__init__()
        self.initial_seq_number: int = None
        self.syn_attempts: int = 5

    def connect(self, address: str, port: int):
        #  data validation
        self.server_address = address
        self.server_port = port
        # self.socket.bind()
        self._three_way_handshake()

    def _three_way_handshake(self):
        self.initial_seq_number = self.seq_number = generate_id()
        self.ack_number = 0
        attempts = 0
        self.send_packet((TCPFlag.SYN), (self.server_address, self.server_port))

        while attempts < self.syn_attempts:
            attempts += 1
            packet: Packet
            packet, _ = self.receive_packet((TCPFlag.SYN, TCPFlag.ACK))
            if packet.flags == (TCPFlag.SYN, TCPFlag.ACK):
                self.send_packet((TCPFlag.ACK), (self.server_address, self.server_port))
                print("Connection established")
                break
