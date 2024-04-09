from UDPNetworking.ReliableUDPServer import ReliableUDPServer

if __name__ == "__main__":
    server = ReliableUDPServer("localhost", 8080)
    server.receive()
    server.receive()
