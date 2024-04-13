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
        packet = server.reliability_receive()

    server.reliability_send()
    # server.shutdown()
    server.close()
