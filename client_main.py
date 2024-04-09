import os
import struct
from UDPNetworking.ReliableUDPClient import ReliableUDPClient
from Model.packet import Packet
from Utils.argument_parser import parse_arguments
from Utils.file_operations import open_file, read_file_in_chunks


if __name__ == "__main__":
    args = parse_arguments()
    server_ip_address = args.ip_address
    server_port = args.port
    file_path = args.file_path

    file = open_file(file_path)
    file_size = os.path.getsize(file_path)
    client = ReliableUDPClient(server_ip_address, server_port)

    client.send(str(struct.pack("i", file_size)))
    print("File size Sent")

    seq_num = 0  # Initial sequence number
    for chunk in read_file_in_chunks(file):
        packet = Packet(seq_num, 0, chunk)
        client.send(str(packet.pack()))
        seq_num += 1  # Increment sequence number for each chunk
    print("File Data Sent")

    response = client.receive()
    print("Server response:", response)

    file.close()
    client.close_socket()
