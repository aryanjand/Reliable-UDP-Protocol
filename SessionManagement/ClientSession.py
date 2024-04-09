from Session import Session
from ..model.packet import Packet, generate_id


class ClientSession(Session):
    def __init__(self):
        super().__init__()
        self.syn_attempts = 0

    def three_way_handshake(self):
        if self.session:
            raise Exception("Connection Error: session is already established")
        # client's initial sequence number
        initial_seq_number = generate_id()
        self._send_initial_syn()
        attempts = 0
        while attempts < self.syn_attempts:
            try:
                attempts += 1
                packet, address = self._get_syn_ack()
                if packet.operation == SYN_ACK:
                    self._sent_ack()
                    self.session = ClientSession(self.address, initial_seq_number, packet.seq_number, self.socket)
                    print("Connection established")
                    break
            except socket.timeout as e:
                if attempts >= self.syn_attempts:
                    raise Exception("Connection failure: timeout error")
    
    

