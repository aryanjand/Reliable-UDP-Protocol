from SessionManagement.ClientConnectionToServer import ClientConnectionToServer
from Utils.argument_parser import parse_arguments
from Utils.file_operations import open_file, read_file_in_chunks


if __name__ == "__main__":

    print("TCP like Client Started!\n")
    args = parse_arguments()
    server_ip_address = args.ip_address
    server_port = args.port
    file_path = args.file_path

    file = open_file(file_path)
    # file_size = os.path.getsize(file_path)
    client = ClientConnectionToServer()
    client.connect(server_ip_address, server_port)

    # seq_num = 0  # Initial sequence number
    # for chunk in read_file_in_chunks(file):
    #     packet = Packet(seq_num, 0, (4) chunk)
    #     client.send(pickle.dumps(packet))
    #     seq_num += 1  # Increment sequence number for each chunk
    # print("File Data Sent")

    file.close()
    client.shutdown()
    client.close()
