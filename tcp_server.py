from SessionManagement.ServerConnectionToClient import ServerConnectionToClient
from Utils.argument_parser import server_parse_arguments

if __name__ == "__main__":
    print("TCP like Server Started!\n")
    server = ServerConnectionToClient()
    server_ip, server_port = server_parse_arguments()
    server.bind((server_ip, server_port))
    server.listen(5)
    # server.accept()

    while True:
        try:
            packet = server.reliability_receive()
        except TimeoutError:
            print("Timeout occurred, leaving recvfrom")
            continue
        # print(f"Packet data received on server {packet.data}")
        if packet.data == "**EOF**".encode():
            break

    server.reliability_send("File Received".encode())

    server.shutdown()
    server.close()
