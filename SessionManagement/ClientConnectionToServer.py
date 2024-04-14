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
        self.server_seq_num = None
        self.server_ack_num = None
        self.syn_attempts: int = 5

    def connect(self, address: str, port: int):
        #  data validation
        self.server_address = address
        self.server_port = port
        self.udp_socket.set_timeout_time(1)
        self._initialize_values()

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
                self._initialize_values()
                break

    def reliability_send(self, data: bytes) -> None:
        server_address = (self.server_address, self.server_port)
        while True:
            try:
                self.send_packet(PSH, server_address, data)
                print(
                    f"\n\nAfter Sent PSH: Seq Number: {self.seq_num}, Ack Number: {self.ack_num}\n\n"
                )
                packet, _ = self.receive_packet(ACK)

            except TimeoutError:
                print("Timeout occurred, leaving recvfrom")
                continue

            if packet.ack_num == self.seq_num:
                self.ack_num = packet.ack_num
                print(
                    f"\n\nAfter Receive ACK: Seq Number: {self.seq_num}, Ack Number: {self.ack_num}\n\n"
                )
                self.seq_num += 1
                break

    def reliability_receive(self) -> Packet:
        packet, address = self.receive_packet(PSH)
        print(
            f"\n\nAfter Receive PSH: Seq Number: {self.server_seq_num}, Ack Number: {self.server_ack_num}\n\n"
        )
        if self._check_packet_numbers(packet):
            self.server_seq_num = packet.seq_num
            self.server_ack_num += 1
            self.send_packet(ACK, address)
            print(
                f"\n\nAfter Sent Ack: Seq Number: {self.server_seq_num}, Ack Number: {self.server_ack_num}\n\n"
            )
            return packet
        self.send_packet(ACK, address)
        return packet

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

    def _initialize_values(self):
        self.seq_num = 1
        self.ack_num = 0
        self.server_seq_num = 0
        self.server_seq_num = 0

    def _check_packet_numbers(self, packet: Packet) -> int:
        return (
            packet.seq_num == self.server_seq_num + 1
            and packet.ack_num == self.server_ack_num
        )
