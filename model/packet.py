import struct


def generate_id():
    """
    When we add multiple client connections, make it a random id.
    """
    return 1


class Packet:
    def __init__(self, seq_num, ack_num, data):
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.data = data

    def pack(self):
        # Assuming seq_num and ack_num are integers
        packed_data = struct.pack(
            "<ii{}s".format(len(self.data)),
            self.seq_num,
            self.ack_num,
            self.data.encode(),
        )
        print("ii{}s".format(len(self.data)))
        return packed_data

    @staticmethod
    def unpack(packed_data):
        seq_num, ack_num, data = struct.unpack(
            "<ii{}s".format(len(packed_data) - 8), packed_data
        )
        return Packet(seq_num, ack_num, data.decode())
