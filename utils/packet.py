import struct

class Packet:
    def __init__(self, seq_num, ack_num, data):
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.data = data

    def pack(self):
        return struct.pack("ii128s", self.seq_num, self.ack_num, self.data.encode())

    @classmethod
    def unpack(cls, packed_data):
        seq_num, ack_num, data = struct.unpack("ii128s", packed_data)
        return cls(seq_num, ack_num, data.decode())

# Example usage
if __name__ == "__main__":
    packet = Packet(1, 2, "Hello, world!")
    packed_packet = packet.pack()
    unpacked_packet = Packet.unpack(packed_packet)
    print(unpacked_packet.seq_num, unpacked_packet.ack_num, unpacked_packet.data)
