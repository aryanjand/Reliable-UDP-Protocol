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
        self.client_seq_num = None
        self.client_ack_num = None
        self.backlog = None
        self.max_retransmissions = 15
        self.tried_retransmissions = 0
        self.udp_socket.set_timeout_time(5)

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

        if packet.seq_num == 1 and packet.ack_num == 0:
            self._initialize_values(address)

        if self._check_packet_numbers(packet):
            self.client_seq_num = packet.seq_num
            print(
                f"\n\nAfter Receive PSH: Client Seq Number: {self.client_seq_num}, Client Ack Number: {self.client_ack_num}\n\n"
            )
            self.client_ack_num += 1

            self.send_packet(self.client_seq_num, self.client_ack_num, ACK, address)
            print(
                f"\n\nAfter Sent ACK: Client Seq Number: {self.client_seq_num}, Client Ack Number: {self.client_ack_num}\n\n"
            )
            return packet
        self.send_packet(self.client_seq_num, self.client_ack_num, ACK, address)
        return packet

    def reliability_send(self, data: bytes) -> None:
        client_address = (self.client_address, self.client_port)
        current_retransmissions = 0
        while current_retransmissions <= self.max_retransmissions:
            self.tried_retransmissions = current_retransmissions
            try:
                current_retransmissions += 1
                self.send_packet(self.seq_num, self.ack_num, PSH, client_address, data)
                print(
                    f"\n\nAfter Sent PSH: Seq Number: {self.seq_num}, Ack Number: {self.ack_num}\n\n"
                )
                packet, _ = self.receive_packet(ACK)
                if not packet:
                    self.send_packet(
                        self.client_seq_num, self.client_ack_num, ACK, client_address
                    )
            # HERE check for if I receive a ACK or PSH packet.
            # This is because if the last ACK was dropped that
            # Then the client didn't receive the ACK and we need to retransmit it again.
            # So what we can do it is simple retransmit the ACK and sent PSH with
            # acknowledgement that the data was received.
            except TimeoutError:
                print("Timeout occurred, leaving recvfrom")
                continue
            if packet:
                self.ack_num = packet.ack_num
                print(
                    f"\n\nAfter Receive ACK: Seq Number: {self.seq_num}, Ack Number: {self.ack_num}\n\n"
                )
                if packet.ack_num == self.seq_num:
                    self.seq_num += 1
                    break

    def shutdown(self) -> None:
        if self.tried_retransmissions >= self.max_retransmissions:
            print("Max Retransmissions Attempted!")
        print("\n\nConnection Ended\n\n")

    def _initialize_values(self, address: tuple) -> None:
        print("With first Packet. Connection Made!\n\n")
        self.client_address, self.client_port = address
        self.seq_num = 1
        self.ack_num = 0
        self.client_seq_num = 0
        self.client_ack_num = 0

    def _check_packet_numbers(self, packet: Packet) -> int:
        return (
            packet.seq_num == self.client_seq_num + 1
            and packet.ack_num == self.client_ack_num
        )
