from enum import IntEnum


class TCPFlag(IntEnum):
    FIN = 1
    SYN = 2
    RST = 3
    PSH = 4
    ACK = 5
    URG = 6
    ECE = 7
    CWR = 8
