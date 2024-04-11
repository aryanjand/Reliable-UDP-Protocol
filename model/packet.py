import struct


def generate_id():
    """
    When we add multiple client connections, make it a random id.
    """
    return 1


class Packet:
    def __init__(self, seq_num: int, ack_num: int, data: str):
        self.seq_num: int = seq_num
        self.ack_num: int = ack_num
        self.flags: tuple = None  # Error: We can't pack and unpack a tuple.
        self.data = data

    def set_flag(self, flags: tuple):
        self.flags = flags

    # def pack(self):
    #     # Assuming seq_num and ack_num are integers
    #     packed_data = struct.pack(
    #         "<ii{}p{}s".format(len(bytes(self.flags)) + 1, len(self.data)),
    #         self.seq_num,
    #         self.ack_num,
    #         bytes(self.flags),
    #         self.data.encode(),
    #     )
    #     print("ii{}p{}s".format(len(bytes(self.flags)) + 1, len(self.data)))
    #     return packed_data

    # @staticmethod
    # def unpack(packed_data):
    #     seq_num, ack_num, flags, data = struct.unpack_from(
    #         "<ii{}p{}s".format(len(packed_data) - 8), packed_data
    #     )
    #     print(seq_num, ack_num, flags, data)
    #     packet = Packet(seq_num, ack_num, data.decode())
    #     packet.set_flag(flags)
    #     return packet
