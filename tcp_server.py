from SessionManagement.ServerConnectionToClient import ServerConnectionToClient
from Utils.argument_parser import server_parse_arguments
from Utils.file_operations import write_file

if __name__ == "__main__":
    print("TCP like Server Started!\n")
    server = ServerConnectionToClient()
    server_ip, server_port = server_parse_arguments()
    server.bind((server_ip, server_port))
    server.listen(5)

    while True:
        try:
            packet = server.reliability_receive()
        except TimeoutError:
            print("Timeout occurred, leaving recvfrom")
            continue
        if packet:
            if packet.data == "**EOF**":
                break
            write_file(
                "Client-Data.txt",
                packet.data,
            )

    server.reliability_send("File Received".encode())

    server.shutdown()
    server.close()
