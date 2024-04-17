from SessionManagement.ClientConnectionToServer import ClientConnectionToServer
from Utils.argument_parser import client_parse_arguments
from Utils.file_operations import open_file, read_file_in_chunks


if __name__ == "__main__":
    server_ip_address, server_port, file_path, file_mode = client_parse_arguments()
    print("TCP like Client Started!\n")

    file = open_file(file_path, file_mode)

    client = ClientConnectionToServer()
    client.connect(server_ip_address, server_port)

    for chunk in read_file_in_chunks(file, 512):
        # print("New Chunk")
        # print(f"\n\n{chunk}\n\n")
        client.reliability_send(chunk)

    # Sent EOF message
    client.reliability_send("**EOF**")
    print("File Data Sent")

    # Receive message "File Data Received"
    packet = client.reliability_receive()

    file.close()
    client.close()
