import socket
from utils.packet import Packet


class ReliableUDPServer:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.server_address, self.server_port))
        print("Bind Done")

    def receive(self):
        bytesReceived = self.socket.recvfrom(1024)
        message = bytesReceived[0]
        address = bytesReceived[1]
        clientMsg = "Message from Client:{}".format(Packet.unpack(message).data)
        clientIP = "Client IP Address:{}".format(address)
        print(clientIP)
        print(clientMsg)

    def send(self, data: str, client_address):
        self.socket.sendto(data.encode(), client_address)


# Example usage
if __name__ == "__main__":
    server = ReliableUDPServer("localhost", 8080)
    server.receive()
    server.receive()
    # print(f"Received data from {client_address}: {data}")
    # server.send("Hello, client!", client_address)
