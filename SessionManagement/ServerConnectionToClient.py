import pickle
from .Session import Session
from Model.Packet import Packet


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
        print("Checking SYN packet")
        bytes_received, client_address = self.receive()
        packet: Packet = pickle.loads(bytes_received)
        print(f"Got SYN packet {self._check_syn(packet)}")
        if self._check_syn(packet):
            self._send_synack(client_address)
            print(f"Sent SYN/ACK packet")
            while True:
                bytes_received, _ = self.receive()
                packet: Packet = pickle.loads(bytes_received)
                if self._check_ack(packet):
                    print(f"Got SYN packet {self._check_ack(packet)}")
                    self.client_address, self.client_port = client_address
                    break

    def _send_synack(self, address: tuple):
        self.client_address, self.client_port = address
        packet = Packet(2, 1, None)
        packet.set_flag((2, 5))
        self.udp_socket.sendto(pickle.dumps(packet), address)

    def _check_syn(self, packet: Packet):
        return packet.flags == (2)

    def _check_ack(self, packet: Packet):
        return packet.flags == (5)

    # def receive(self, buffer_size) -> bytes:
    #     return self.server_socket.recvfrom(buffer_size)
