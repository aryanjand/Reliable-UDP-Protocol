def generate_id():
    """
    When we add multiple client connections, make it a random id.
    """
    return 1


class Packet:
    def __init__(self, seq_num: int, ack_num: int, flags: tuple, data: str):
        self.seq_num: int = seq_num
        self.ack_num: int = ack_num
        self.flags: tuple = flags
        self.data: str = data
