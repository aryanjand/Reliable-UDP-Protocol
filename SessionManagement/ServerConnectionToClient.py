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
        if packet.seq_num == 1:
            self._initialize_values(address)

        if self._check_packet_numbers(packet):
            self.client_seq_num = packet.seq_num
            print(
                f"\n\nAfter Receive PSH: Seq Number: {self.client_seq_num}, Ack Number: {self.client_ack_num}\n\n"
            )
            self.client_ack_num += 1

            self.send_packet(ACK, address)
            print(
                f"\n\nAfter Sent ACK: Seq Number: {self.client_seq_num}, Ack Number: {self.client_ack_num}\n\n"
            )
            return packet
        self.send_packet(ACK, address)
        return packet

    def reliability_send(self, data: bytes) -> None:
        client_address = (self.client_address, self.client_port)
        while True:
            try:
                self.send_packet(PSH, client_address, data)
                print(
                    f"\n\nAfter Sent PSH: Seq Number: {self.seq_num}, Ack Number: {self.ack_num}\n\n"
                )
                packet, _ = self.receive_packet(ACK)
                print(
                    f"\n\nAfter Receive ACK: Seq Number: {self.seq_num}, Ack Number: {self.ack_num}\n\n"
                )
                if packet.ack_num == self.seq_num:
                    self.seq_num += 1
                    break
            except ValueError as e:
                print(f"Error unpacking packet: {e}")
                continue

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
        self.seq_num = 1
        self.ack_num = 0
        self.client_seq_num = 0
        self.client_ack_num = 0

    def _check_packet_numbers(self, packet: Packet) -> int:
        return (
            packet.seq_num == self.client_seq_num + 1 and packet.ack_num == self.ack_num
        )
