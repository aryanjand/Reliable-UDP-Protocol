from SessionManagement.ClientConnectionToServer import ClientConnectionToServer
from Utils.argument_parser import client_parse_arguments
from Utils.file_operations import open_file, read_file_in_chunks


if __name__ == "__main__":

    print("TCP like Client Started!\n")
    server_ip_address, server_port, file_path = client_parse_arguments()

    file = open_file(file_path)

    client = ClientConnectionToServer()
    client.connect(server_ip_address, server_port)

    for chunk in read_file_in_chunks(file):
        client.reliability_send(chunk)
    # Sent EOF message
    client.reliability_send("**EOF**".encode())
    print("File Data Sent")

    # Receive message "File Data Received"
    packet = client.reliability_receive()

    file.close()
    client.close()
