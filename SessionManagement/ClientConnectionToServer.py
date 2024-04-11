from .Session import Session
from Model.Packet import Packet, generate_id
import pickle


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

        # Sent SYN packet
        self.initial_seq_number = self.seq_number = generate_id()
        self.ack_number = 0
        packet = Packet(self.seq_number, self.ack_number, (2), None)
        self.udp_socket.sendto(
            # Note this takes in bytes
            pickle.dumps(packet),
            (self.server_address, self.server_port),
        )
        print("Sent SYN Packet")

        attempts = 0
        while attempts < self.syn_attempts:
            attempts += 1

            # receive ACK
            bytes_received, _ = self.udp_socket.recvfrom()
            packet: Packet = pickle.loads(bytes_received)
            print(
                f"Packet from Server: {packet} {packet.seq_num} {packet.ack_num} {packet.flags} {packet.data}"
            )

            if packet.flags == (2, 5):
                packet = Packet(self.seq_number, self.ack_number, None)
                packet.set_flag((5))
                self.udp_socket.sendto(
                    pickle.dumps(packet), (self.server_address, self.server_port)
                )
                print("Connection established")
                break
