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

    def reliability_send(self, data: bytes) -> None:
        server_address = (self.server_address, self.server_port)
        while True:
            try:
                self.send_packet(self.seq_num, self.ack_num, PSH, server_address, data)
                print(
                    f"\n\nAfter Sent PSH: Seq Number: {self.seq_num}, Ack Number: {self.ack_num}\n\n"
                )
                packet, _ = self.receive_packet(ACK)

            except TimeoutError:
                print("Timeout occurred, leaving recvfrom")
                continue

            # check if I got a valid packet and not None
            if packet and packet.ack_num == self.seq_num:
                self.ack_num = packet.ack_num
                print(
                    f"\n\nAfter Receive ACK: Seq Number: {self.seq_num}, Ack Number: {self.ack_num}\n\n"
                )
                self.seq_num += 1
                break

    def reliability_receive(self) -> Packet:
        while True:
            try:
                #  maybe it received another packet, the packet and address are going None
                #  we need to save address it possible old / none packets come in. That the address might different
                packet, _ = self.receive_packet(PSH)
                address = (self.server_address, self.server_port)

            except TimeoutError:
                print("Timeout occurred, leaving recvfrom")
                continue

            if packet and address and self._check_packet_numbers(packet):
                self.server_seq_num = packet.seq_num
                print(
                    f"\n\nAfter Receive PSH: Seq Number: {self.server_seq_num}, Ack Number: {self.server_ack_num}\n\n"
                )
                self.server_ack_num += 1
                self.send_packet(self.server_seq_num, self.server_ack_num, ACK, address)
                print(
                    f"\n\nAfter Sent Ack: Seq Number: {self.server_seq_num}, Ack Number: {self.server_ack_num}\n\n"
                )
                return packet
            self.send_packet(self.server_seq_num, self.server_ack_num, ACK, address)
            return packet

    def shutdown(self) -> None:
        print("\n\nConnection Ended\n\n")
        return

    def _initialize_values(self):
        self.seq_num = 1
        self.ack_num = 0
        self.server_seq_num = 0
        self.server_ack_num = 0

    def _check_packet_numbers(self, packet: Packet) -> int:
        return (
            packet.seq_num == self.server_seq_num + 1
            and packet.ack_num == self.server_ack_num
        )
